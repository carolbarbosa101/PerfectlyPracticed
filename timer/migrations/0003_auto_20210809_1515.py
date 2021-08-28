# Generated by Django 3.2.5 on 2021-08-09 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timer', '0002_auto_20210808_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='timer',
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='users.myuser'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Timer',
        ),
    ]