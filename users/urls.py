from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
]