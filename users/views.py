from dashboard.views import dashboard
from django.shortcuts import redirect, render
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request, 'users/login.html',{})

@login_required
def login_success(request):
    pk = request.user.id
    return redirect(f'dashboard/{pk}/')

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
    return render(request, 'users/sign_up.html',{'form':form})