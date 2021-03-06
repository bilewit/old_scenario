# Generated by Django 2.2.4 on 2019-12-14 00:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scenario', '0032_auto_20191212_0645'),
        ('users', '0030_auto_20191213_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=1100)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.StoryComment')),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scenario.Story')),
            ],
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user_from',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='user_to',
        ),
        migrations.DeleteModel(
            name='Comment_Story',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
