from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('song_book/<int:user_pk>/', views.song_book, name='song_book'),
    path('song_book/<int:user_pk>/song_post/<str:status>/', views.song_post, name='song_post'),
    path('song_book/<int:user_pk>/song_delete/<int:song_pk>/', views.song_delete, name='song_delete'),
    path('song_book/song_move/', views.song_move, name='song_move'),
    path('song_book/song_note/', views.song_note, name='song_note'),
    path('song_book/<int:user_pk>/song_video/<int:song_pk>/', views.song_video, name='song_video'),
    path('song_book/<int:user_pk>/song_recording/<int:song_pk>/', views.song_recording, name='song_recording'),
    path('song_book/song_recording/sign_s3/<str:file_name>/', views.sign_s3, name='sign_s3'),
    path('song_book/<int:user_pk>/song_recording_delete/<int:song_pk>/<int:recording_pk>/', views.song_recording_delete, name='song_recording_delete'),
]