# Generated by Django 2.2.4 on 2019-10-18 17:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scenario', '0017_auto_20191018_0549'),
        ('users', '0010_like'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='Liked_Story',
        ),
    ]
