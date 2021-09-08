from django.urls import path
from . import views

urlpatterns = [
    path('timer/<int:user_pk>/', views.timer, name='timer'),
    path('timer/<int:user_pk>/task_delete/<int:task_pk>/', views.task_delete, name='task_delete'),
]