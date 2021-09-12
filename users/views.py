from dashboard.views import dashboard
from django.shortcuts import redirect, render
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import messages
from .forms import UserRegisterForm
from musicsite.middleware import login_exempt

# This tutorial used was used as rough guide for creating the forms, views and templates in login/sign up:
# https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog

@login_exempt
def login_success(request):
    pk = request.user.id
    return redirect(f'dashboard/{pk}/')


@login_exempt
def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account sucessfully created for {email}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/base_auth_signup.html',{'form':form})