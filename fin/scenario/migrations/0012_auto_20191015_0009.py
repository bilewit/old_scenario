# Generated by Django 2.2.4 on 2019-10-15 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0011_story_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='choice_end_success',
        ),
        migrations.AlterField(
            model_name='story',
            name='story_description',
            field=models.TextField(max_length=500),
        ),
    ]