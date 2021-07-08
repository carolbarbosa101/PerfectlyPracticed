from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def login_page(request):
    return render(request, 'users/login.html',{})

def success(request):
    return render(request, 'users/success.html',{})

def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account sucessfully created for {email}')
            return redirect('login_page')
    else:
        form = UserRegisterForm()
    return render(request, 'users/sign_up.html',{'form':form})