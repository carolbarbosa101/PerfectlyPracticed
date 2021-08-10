from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),
    path('dashboard/goal_tick/<int:pk>/', views.goal_tick, name='goal_tick'),
    path('dashboard/goal_edit/<int:pk>/', views.goal_edit, name='goal_edit'),
]