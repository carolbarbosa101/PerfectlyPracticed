from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
import json
from django.contrib.staticfiles.storage import staticfiles_storage


def tuner(request, pk):
    the_user = MyUser.objects.get(pk=pk)
    notes_file = open('tuner/static/tuner/notes.json')
    notes_dict = json.load(notes_file)
    notes_list = notes_dict.keys()

    return render(request, 'tuner/base_tuner.html', {'notes_list':notes_list})
