# Generated by Django 2.2.4 on 2019-12-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0056_auto_20191219_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='9hDzY7he1F', max_length=10),
        ),
    ]