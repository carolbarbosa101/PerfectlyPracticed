from django.urls import path
from . import views

urlpatterns = [
    path('metronome/<int:pk>/', views.metronome, name='metronome'),
]