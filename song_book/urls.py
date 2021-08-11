from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('song_book/<int:pk>/', views.song_book, name='song_book'),
    path('song_book/<int:pk>/song_post/<int:status_num>/', views.song_post, name='song_post'),
    path('song_book/<int:user_pk>/song_delete/<int:song_pk>/', views.song_delete, name='song_delete'),
]