from django.db import models
from users.models import MyUser


class Timer(models.Model):
    total_time = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(
        MyUser,
        related_name='timer',
        on_delete=models.CASCADE,
    )

class Task(models.Model):
    text = models.TextField(default='')
    time = models.PositiveIntegerField()
    editing = models.BooleanField(default=False)

    timer = models.ForeignKey(
        Timer,
        related_name='tasks',
        on_delete=models.CASCADE,
    )
