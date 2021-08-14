from django.db import models
from users.models import MyUser

class Metronome(models.Model):
    bpm = models.IntegerField(default=0)

    user = models.ForeignKey(
        MyUser,
        related_name='metronome',
        on_delete=models.CASCADE,
    )