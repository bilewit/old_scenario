# Generated by Django 2.2.4 on 2019-08-07 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0006_auto_20190807_0728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='end_f',
            new_name='choice_end_fail',
        ),
        migrations.RenameField(
            model_name='choice',
            old_name='end_s',
            new_name='choice_end_success',
        ),
    ]