# Generated by Django 2.2.4 on 2019-12-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0036_auto_20191226_2144'),
        ('users', '0066_auto_20191226_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='pByFZFQEG9', max_length=10),
        ),
        migrations.RemoveField(
            model_name='stats',
            name='stories_finished',
        ),
        migrations.AddField(
            model_name='stats',
            name='stories_finished',
            field=models.ManyToManyField(blank=True, related_name='stories_finished', to='scenario.Story'),
        ),
        migrations.RemoveField(
            model_name='stats',
            name='stories_played',
        ),
        migrations.AddField(
            model_name='stats',
            name='stories_played',
            field=models.ManyToManyField(blank=True, related_name='stories_played', to='scenario.Story'),
        ),
        migrations.RemoveField(
            model_name='stats',
            name='stories_yolo',
        ),
        migrations.AddField(
            model_name='stats',
            name='stories_yolo',
            field=models.ManyToManyField(blank=True, related_name='stories_yolo', to='scenario.Story'),
        ),
    ]