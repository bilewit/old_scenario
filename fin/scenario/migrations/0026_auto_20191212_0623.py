# Generated by Django 2.2.4 on 2019-12-12 06:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0025_auto_20191212_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(default=None, null=True, related_name='story_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
