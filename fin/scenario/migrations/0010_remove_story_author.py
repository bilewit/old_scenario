# Generated by Django 2.2.4 on 2019-08-11 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0009_auto_20190811_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='author',
        ),
    ]
