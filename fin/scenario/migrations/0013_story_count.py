# Generated by Django 2.2.4 on 2019-10-17 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0012_auto_20191015_0009'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]