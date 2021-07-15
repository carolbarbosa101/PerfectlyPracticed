from django.db import models
from django.db.models.base import Model

class Goal(models.Model):
    text = models.TextField(default='')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
