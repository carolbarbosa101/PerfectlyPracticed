from django.db import models
from django.db.models.base import Model

class Goal(models.Model):
    text = models.TextField(default='')
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    editing = models.BooleanField(default=False)
