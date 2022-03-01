from django.db import models
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager



# Create your models here.

class Story(models.Model):
    story_title = models.CharField(max_length= 100)
    story_description = models.TextField(max_length=500)
    story_pic = models.ImageField(default='default.jpg', upload_to='story_pics')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    likes =  models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    reshares = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='reshares_list')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favorite_stories')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    tags = TaggableManager()
    draft = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)



    def save(self):
        super().save()

        img = Image.open(self.story_pic.path)

        if img.height > 600 or img.width > 400:
            output_size = (600,400)
            img.thumbnail(output_size)
            img.save(self.story_pic.path)



    def __str__(self):
        return self.story_title

    def get_absolute_url(self):
        return reverse('story-detail', kwargs={'pk': self.pk})

    def get_like_url(self):
        return reverse('post-like', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('post-api-like', kwargs={'pk': self.pk})

    def get_api_reshare_url(self):
        return reverse('post-api-reshare', kwargs={'pk': self.pk})

    def get_api_favorite_url(self):
        return reverse('post-api-favorite', kwargs={'pk': self.pk})

    #need to make a absolute reshare/favorite url


class Scene(models.Model):
    scene_description = models.TextField(max_length=600)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='scenestory')
    scene_pic = models.ImageField(default='default.jpg', upload_to='scene_pics')

    def save(self):
        super().save()

        img = Image.open(self.scene_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.scene_pic.path)

    def __str__(self):
        return self.scene_description

    def get_absolute_url(self):
        return reverse('story-update', kwargs={'pk': self.story_id})

class Choice(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='choicescene')
    choice_text = models.TextField(max_length=400)
    choice_do = models.TextField(max_length=250, default='this text will show before scene text / What does this choice do ?')
    choice_end = models.BooleanField(default=False)
    choice_end_fail_text = models.TextField(max_length=400, default='explain fail ending if box is checked')
    choice_end_success = models.BooleanField(default=False)
    choice_end_success_text = models.TextField(max_length=400,default='explain success ending if box is checked')
    choice_pic = models.ImageField(default='default.jpg', upload_to='choice_pic')


    def save(self):
        super().save()

        img = Image.open(self.choice_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.choice_pic.path)

    def __str__(self):
        return self.choice_text

    def get_absolute_url(self):
        return reverse('scene-update', kwargs={'pk': self.scene_id})





