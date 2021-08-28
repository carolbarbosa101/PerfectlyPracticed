from dashboard.views import dashboard
from django.shortcuts import redirect, render
from django.contrib.auth.models import AbstractBaseUser
from django.contrib import messages
from .forms import UserRegisterForm
from musicsite.middleware import login_exempt

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
    return render(request, 'users/sign_up.html',{'form':form})