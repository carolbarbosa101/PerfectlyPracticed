from django.db import models
from django.db.models.base import Model
from users.models import MyUser

class Goal(models.Model):
    text = models.TextField(default='')
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    editing = models.BooleanField(default=False)

    user = models.ForeignKey(
        MyUser,
        related_name='goals',
        on_delete=models.CASCADE,
    )
