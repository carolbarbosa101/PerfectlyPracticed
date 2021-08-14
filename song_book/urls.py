from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('song_book/<int:pk>/', views.song_book, name='song_book'),
    path('song_book/<int:pk>/song_post/<str:status>/', views.song_post, name='song_post'),
    path('song_book/<int:user_pk>/song_delete/<int:song_pk>/', views.song_delete, name='song_delete'),
    path('song_book/song_move/', views.song_move, name='song_move'),
]