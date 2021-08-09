from django.db import models
from users.models import MyUser

class Task(models.Model):
    text = models.TextField(default='')
    time = models.PositiveIntegerField()
    colour = models.TextField(default='')

    user = models.ForeignKey(
        MyUser,
        related_name='tasks',
        on_delete=models.CASCADE,
    )
