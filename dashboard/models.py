from django.db import models
from django.db.models.base import Model
from users.models import MyUser
from datetime import datetime as dt

class Goal(models.Model):
    text = models.TextField(default='Placeholder')
    due_date = models.DateField(blank=True, null=True)
    date_str = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    editing = models.BooleanField(default=False)

    user = models.ForeignKey(
        MyUser,
        related_name='goals',
        on_delete=models.CASCADE,
    )
