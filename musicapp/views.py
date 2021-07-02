from django.shortcuts import render

# Create your views here.
def login_page(request):
    return render(request, 'musicapp/login_page.html',{})

def sign_up(request):
    return render(request, 'musicapp/sign_up.html',{})