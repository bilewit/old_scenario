# Generated by Django 2.2.4 on 2019-12-18 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0046_auto_20191216_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_banner',
            field=models.ImageField(default='default.jpg', upload_to='profile_banner'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='w0GmkcLLNZ', max_length=10),
        ),
    ]
