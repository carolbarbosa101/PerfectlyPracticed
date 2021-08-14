from django.db import models
from users.models import MyUser

class Song(models.Model):
    text = models.TextField(default='')
    status = models.TextField(default='to_learn')
    list_index = models.IntegerField(default=0)

    user = models.ForeignKey(
        MyUser,
        related_name='songs',
        on_delete=models.CASCADE,
    )
