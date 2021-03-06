# Generated by Django 2.2.4 on 2019-12-19 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0062_auto_20191219_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stats',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Stats'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='GzYiti39pQ', max_length=10),
        ),
        migrations.AlterField(
            model_name='stats',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
