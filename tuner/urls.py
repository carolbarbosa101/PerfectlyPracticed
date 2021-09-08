from django.urls import path
from . import views

urlpatterns = [
    path('tuner/<int:user_pk>/', views.tuner, name='tuner'),
]