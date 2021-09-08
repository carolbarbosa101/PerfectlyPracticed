from django.urls import path
from . import views

urlpatterns = [
    path('metronome/<int:user_pk>/', views.metronome, name='metronome'),
]