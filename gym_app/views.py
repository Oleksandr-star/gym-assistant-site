from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Exercise, WeightRecord, UserProfile
from .forms import RegisterForm, ExerciseForm, WeightForm, UserUpdateForm, ExerciseUpdateForm, WeightUpdateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Avg
from django.db.models.functions import TruncWeek

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'gym_app/register.html', {'form': form})

@login_required
def index(request):
    user = request.user
    exercises_all = Exercise.objects.filter(user=user)
    total_workouts = exercises_all.count()
    if exercises_all:
        avg_weight = sum(ex.weight for ex in exercises_all) / total_workouts
    else:
        avg_weight = 0
    last_exercises = exercises_all.order_by('-date')[:5]
    last_weight = WeightRecord.objects.filter(user=user).order_by('-date').first()
    return render(request, 'gym_app/index.html', {
        'last_exercises': last_exercises,
        'last_weight': last_weight,
        'total_workouts': total_workouts,
        'avg_weight': round(avg_weight, 1),  # округлюємо для читабельності
    })

@login_required
@login_required
def exercise_view(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, 'Вправу додано!')
            return redirect('exercise')
    else:
        form = ExerciseForm()

    history_list = Exercise.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(history_list, 10)
    page = request.GET.get('page')
    history = paginator.get_page(page)

    weekly_avg = Exercise.objects.filter(user=request.user) \
        .annotate(week=TruncWeek('date')) \
        .values('week') \
        .annotate(avg_weight=Avg('weight')) \
        .order_by('week')
    chart_labels = [entry['week'].strftime('%d.%m') for entry in weekly_avg]
    chart_values = [float(entry['avg_weight']) for entry in weekly_avg]

    return render(request, 'gym_app/exercise.html', {
        'form': form,
        'history': history,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    })

@login_required
def weight_view(request):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Вага збережена!')
            return redirect('weight')
    else:
        form = WeightForm()
    records_list = WeightRecord.objects.filter(user=request.user).order_by('date')
    labels = [r.date.strftime('%d.%m') for r in records_list]
    values = [float(r.weight) for r in records_list]
    paginator = Paginator(records_list, 10)
    page = request.GET.get('page')
    records = paginator.get_page(page)

    return render(request, 'gym_app/weight.html', {
        'form': form,
        'records': records,
        'labels': labels,
        'values': values,
    })

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    users = User.objects.all()
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    return render(request, 'gym_app/admin_page.html', {
        'users': users,
        'query': query,
    })
    
@login_required
@user_passes_test(is_admin)
def toggle_block(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'розблоковано' if user.is_active else 'заблоковано'
    messages.success(request, f'Користувача {user.username} {status}.')
    return redirect('admin_page')

@login_required
@user_passes_test(is_admin)
def toggle_admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, 'Не можна змінити роль собі.')
        return redirect('admin_page')
    user.is_superuser = not user.is_superuser
    user.is_staff = not user.is_staff
    user.save()
    role = 'адміністратора' if user.is_superuser else 'звичайного користувача'
    messages.success(request, f'Роль {user.username} змінено на {role}.')
    return redirect('admin_page')

@login_required
def edit_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExerciseUpdateForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вправу оновлено!')
            return redirect('exercise')
    else:
        form = ExerciseUpdateForm(instance=exercise)
    return render(request, 'gym_app/edit_exercise.html', {'form': form})

@login_required
def delete_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk, user=request.user)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Вправу видалено!')
        return redirect('exercise')
    return render(request, 'gym_app/confirm_delete.html', {'object': exercise, 'type': 'вправу'})

@login_required
def edit_weight(request, pk):
    record = get_object_or_404(WeightRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WeightUpdateForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запис ваги оновлено!')
            return redirect('weight')
    else:
        form = WeightUpdateForm(instance=record)
    return render(request, 'gym_app/edit_weight.html', {'form': form})

@login_required
def delete_weight(request, pk):
    record = get_object_or_404(WeightRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Запис ваги видалено!')
        return redirect('weight')
    return render(request, 'gym_app/confirm_delete.html', {'object': record, 'type': 'запис ваги'})

@login_required
def profile(request):
    return render(request, 'gym_app/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'gym_app/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль змінено успішно!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'gym_app/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Акаунт видалено.')
        return redirect('login')
    return render(request, 'gym_app/confirm_delete_account.html')

@login_required
def toggle_public(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.is_public = not profile.is_public
    profile.save()
    return redirect('profile')

def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = UserProfile.objects.filter(user=user, is_public=True).first()
    if not profile:
        messages.error(request, 'Профіль приватний.')
        return redirect('index')

    exercises = Exercise.objects.filter(user=user)
    total_workouts = exercises.count()
    avg_weight = sum(ex.weight for ex in exercises) / total_workouts if total_workouts else 0
    weights = WeightRecord.objects.filter(user=user).order_by('-date')[:10]
    return render(request, 'gym_app/public_profile.html', {
        'profile_user': user,
        'total_workouts': total_workouts,
        'avg_weight': round(avg_weight, 1),
        'weights': weights,
    })