# Generated by Django 2.2.4 on 2019-12-10 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0018_auto_20191210_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='fail_pic',
            field=models.ImageField(default='default.jpg', upload_to='choice_pics'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='success_pic',
            field=models.ImageField(default='default.jpg', upload_to='choice_pics'),
        ),
    ]
