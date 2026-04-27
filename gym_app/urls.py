from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercise/', views.exercise_view, name='exercise'),
    path('weight/', views.weight_view, name='weight'),
    path('admin-page/', views.admin_view, name='admin_page'),

    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gym_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]