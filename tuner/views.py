from django.shortcuts import get_object_or_404, redirect, render
from users.models import MyUser
import json
from django.conf import settings
import os


def tuner(request, pk):
    notes_file = open(os.path.join(settings.BASE_DIR, 'tuner/static/tuner/notes.json'))
    notes_dict = json.load(notes_file)
    notes_list = notes_dict.keys()

    return render(request, 'tuner/base_tuner.html', {'notes_list':notes_list})
