from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exercise/', views.exercise_view, name='exercise'),
    path('weight/', views.weight_view, name='weight'),
    path('admin-page/', views.admin_view, name='admin_page'),
    path('exercise/edit/<int:pk>/', views.edit_exercise, name='edit_exercise'),
    path('exercise/delete/<int:pk>/', views.delete_exercise, name='delete_exercise'),
    path('weight/edit/<int:pk>/', views.edit_weight, name='edit_weight'),
    path('weight/delete/<int:pk>/', views.delete_weight, name='delete_weight'),

    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='gym_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    
    path('toggle-public/', views.toggle_public, name='toggle_public'),
    path('user/<str:username>/', views.public_profile, name='public_profile'),
    path('admin-page/toggle-block/<int:user_id>/', views.toggle_block, name='toggle_block'),
    path('admin-page/toggle-admin/<int:user_id>/', views.toggle_admin, name='toggle_admin'),
]