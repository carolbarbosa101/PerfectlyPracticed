from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
import dashboard.views

urlpatterns = [
    path('dashboard/<int:pk>/', dashboard.views.dashboard, name='dashboard'),
    path('goal_tick/<int:pk>/', dashboard.views.goal_tick, name='goal_tick'),
    path('goal_edit/<int:pk>/', dashboard.views.goal_edit, name='goal_edit'),
]