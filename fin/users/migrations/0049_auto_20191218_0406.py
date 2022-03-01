# Generated by Django 2.2.4 on 2019-12-18 04:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_auto_20191218_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='joined'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='B4E5O4IRSH', max_length=10),
        ),
    ]