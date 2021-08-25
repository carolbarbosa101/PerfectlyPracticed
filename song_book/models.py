from django.db import models
from users.models import MyUser

class Song(models.Model):
    text = models.TextField(default='')
    status = models.TextField(default='to_learn')
    list_index = models.IntegerField(default=0)
    note = models.TextField(default='Click here to add notes...')
    video = models.TextField(default='https://www.youtube.com/embed/NpEaa2P7qZI')

    user = models.ForeignKey(
        MyUser,
        related_name='songs',
        on_delete=models.CASCADE,
    )
