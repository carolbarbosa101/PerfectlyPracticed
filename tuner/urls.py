from django.urls import path
from . import views

urlpatterns = [
    path('tuner/<int:pk>/', views.tuner, name='tuner'),
]