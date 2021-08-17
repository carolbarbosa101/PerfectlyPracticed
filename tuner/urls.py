from django.urls import path
from . import views

urlpatterns = [
    path('tuner/<int:pk>/', views.metronome, name='tuner'),
]