# Generated by Django 2.2.4 on 2019-12-12 06:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scenario', '0030_remove_story_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='story_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
