# Generated by Django 2.2.4 on 2019-12-14 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20191214_1923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storycomment',
            name='reply',
        ),
        migrations.AddField(
            model_name='storycomment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='users.StoryComment'),
        ),
    ]
