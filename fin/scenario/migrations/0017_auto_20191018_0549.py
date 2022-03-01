# Generated by Django 2.2.4 on 2019-10-18 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0016_scene_scene_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='choice_end_fail_text',
            field=models.TextField(default='explain fail ending if box is checked', max_length=400),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_end_success',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='choice',
            name='choice_end_success_text',
            field=models.TextField(default='explain success ending if box is checked', max_length=400),
        ),
    ]