from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('success', views.success, name='success'),
]