# Generated by Django 2.2.4 on 2019-08-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0007_auto_20190807_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='choice_end_fail',
        ),
    ]
