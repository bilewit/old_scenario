# Generated by Django 2.2.4 on 2019-12-12 06:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0031_story_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
