from django.db import models
from django.db.models.base import Model

class Goals(models.Model):
    text = models.TextField(default='')
    due_date = models.DateField()
