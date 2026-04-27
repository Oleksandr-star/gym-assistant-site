from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Exercise, WeightRecord
from .forms import RegisterForm, ExerciseForm, WeightForm
from django.db.models import Q

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
    exercises = Exercise.objects.filter(user=user).order_by('-date')[:5]
    weights = WeightRecord.objects.filter(user=user).order_by('-date')[:1]
    return render(request, 'gym_app/index.html', {
        'exercises': exercises,
        'weights': weights,
    })

@login_required
def exercise_view(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('exercise')
    else:
        form = ExerciseForm()
    history = Exercise.objects.filter(user=request.user).order_by('-date')
    return render(request, 'gym_app/exercise.html', {'form': form, 'history': history})

@login_required
def weight_view(request):
    if request.method == 'POST':
        form = WeightForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('weight')
    else:
        form = WeightForm()
    records = WeightRecord.objects.filter(user=request.user).order_by('date')

    labels = [r.date.strftime('%d.%m') for r in records]
    values = [float(r.weight) for r in records]
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
    return render(request, 'gym_app/admin_page.html', {'users': users, 'query': query})