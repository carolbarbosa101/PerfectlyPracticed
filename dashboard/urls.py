from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/<int:user_pk>/', views.dashboard, name='dashboard'),
    path('dashboard/<int:user_pk>/goal_tick/<int:goal_pk>/', views.goal_tick, name='goal_tick'),
    path('dashboard/<int:user_pk>/goal_edit/<int:goal_pk>/', views.goal_edit, name='goal_edit'),
]