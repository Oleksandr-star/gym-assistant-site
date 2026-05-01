from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Exercise, WeightRecord

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'weight', 'reps', 'notes', 'rpe']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rpe': forms.Select(choices=[(i, i) for i in range(1, 11)],
                                attrs={'class': 'form-control'}),
        }

class WeightForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ExerciseUpdateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'weight', 'reps', 'notes', 'rpe']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rpe': forms.Select(choices=[(i, i) for i in range(1, 11)],
                                attrs={'class': 'form-control'}),
        }

class WeightUpdateForm(forms.ModelForm):
    class Meta:
        model = WeightRecord
        fields = ['weight']
        widgets = {
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }