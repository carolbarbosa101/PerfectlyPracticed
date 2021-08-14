from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
from .models import Metronome

def metronome(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    return render(request, 'metronome/base_metronome.html')
