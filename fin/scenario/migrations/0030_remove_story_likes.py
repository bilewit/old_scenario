# Generated by Django 2.2.4 on 2019-12-12 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0029_auto_20191212_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='likes',
        ),
    ]
