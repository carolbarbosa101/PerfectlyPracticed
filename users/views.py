from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def login(request):
    return render(request, 'users/login.html',{})

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