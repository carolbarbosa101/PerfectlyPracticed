from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('song_book/<int:pk>/', views.song_book, name='song_book'),
]