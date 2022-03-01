# Generated by Django 2.2.4 on 2019-12-19 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0061_auto_20191219_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='referral_code',
            field=models.CharField(default='4TH5WHdRZw', max_length=10),
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stories_played', models.IntegerField(default=0)),
                ('stories_finished', models.IntegerField(default=0)),
                ('stories_yolo', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
    ]
