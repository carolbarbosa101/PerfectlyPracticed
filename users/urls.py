from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from musicsite.middleware import login_exempt

urlpatterns = [
    path('', login_exempt(auth_views.LoginView.as_view(template_name='users/base_auth_login.html')), name='login'),
    path('login_success', views.login_success, name='login_success'),
    path('logout', login_exempt(auth_views.LogoutView.as_view(template_name='base_auth_login.html')), name='logout'),
    path('sign_up', views.sign_up, name='sign_up'),
]