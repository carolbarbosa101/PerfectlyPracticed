from django.urls import path
from . import views

urlpatterns = [
    path('timer/<int:pk>/', views.timer, name='timer'),
]