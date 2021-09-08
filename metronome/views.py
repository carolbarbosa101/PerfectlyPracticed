from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
from .models import Metronome
from django.http import HttpResponseForbidden

def metronome(request, user_pk):
    the_user = MyUser.objects.get(pk=user_pk)
    if request.user != the_user:
        return HttpResponseForbidden('You do not have permission to view this page.')
    return render(request, 'metronome/base_metronome.html')
