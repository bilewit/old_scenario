# Generated by Django 2.2.4 on 2019-12-19 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0059_auto_20191219_1858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='time',
            new_name='time_sent',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='reciever',
        ),
        migrations.AddField(
            model_name='messages',
            name='thread',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread', to='users.Thread'),
        ),
        migrations.AddField(
            model_name='profile',
            name='inbox',
            field=models.ManyToManyField(blank=True, related_name='inbox', to='users.Thread'),
        ),
        migrations.AddField(
            model_name='thread',
            name='created',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='thread created'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='ZTNMElfnrc', max_length=10),
        ),
        migrations.AlterField(
            model_name='thread',
            name='room',
            field=models.ManyToManyField(blank=True, related_name='chat_room', to=settings.AUTH_USER_MODEL),
        ),
    ]
