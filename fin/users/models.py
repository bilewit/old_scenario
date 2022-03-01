from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from scenario.models import Story
from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string


#CrEAtE MoDEls hERe

class Awards(models.Model):
    award_title = models.TextField()
    award_description = models.TextField()
    award_image = models.ImageField(default='default.jpg', upload_to='award_pics')
    created_date = models.DateTimeField('date reported', default=timezone.now)

    def __str__(self):
        return self.award_title

    def get_absolute_url(self):
        return reverse('award-update', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Awards, self).save(*args, **kwargs)

        img = Image.open(self.award_image.path)

        if img.height > 30 or img.width > 30:
            output_size = (30,30)
            img.thumbnail(output_size)
            img.save(self.award_image.path)

class NotificationCategories(models.Model):
    notification_category = models.CharField(max_length=20)

    def __str__(self):
        return self.notification_category

class Notifications(models.Model):
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_reciever')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_sender')
    reason = models.ForeignKey(NotificationCategories, on_delete=models.CASCADE, related_name='notification_reason')
    post = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    time = models.DateTimeField('time', default=timezone.now)

class Thread(models.Model):
    room = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='chat_room')
    created = models.TimeField('thread created', default=timezone.now)

class Thread_Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='sender', on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='thread', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(max_length=1200)
    time_sent = models.TimeField('sent at', default=timezone.now)

class Stats(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stories_played = models.ManyToManyField(Story, blank=True, related_name='stories_played')
    stories_finished = models.ManyToManyField(Story, blank=True, related_name='stories_finished')
    stories_yolo = models.ManyToManyField(Story, blank=True, related_name='stories_yolo')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    profile_banner = models.ImageField(default='default.jpg', upload_to='profile_banner')
    bio = models.TextField(max_length=300, default=('im new'))
    private_profile = models.BooleanField(default=False)
    pending_followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='pending_followers')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='profile_followers')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='profile_following')
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favorites')
    block_list = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='block_list')
    awards = models.ManyToManyField(Awards, blank=True, related_name='awards')
    banned = models.BooleanField(default=False)
    referrer_code = models.CharField(max_length=10, null=True, blank=True)
    referral_code = models.CharField(max_length=10, default=get_random_string(length=10))
    referrals = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='referrals')
    joined = models.DateTimeField('joined', default=timezone.now)
    website = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=20, null=True, blank=True)
    twitter = models.CharField(max_length=20, null=True, blank=True)
    tiktok = models.CharField(max_length=20, null=True, blank=True)
    youtube = models.CharField(max_length=20, null=True, blank=True)
    notifications = models.ManyToManyField(Notifications, blank=True, related_name='notifications')
    old_notifications = models.ManyToManyField(Notifications, blank=True, related_name='old_notifications')
    inbox = models.ManyToManyField(Thread, blank=True, related_name='inbox')
    stats = models.ForeignKey(Stats, on_delete=models.CASCADE, blank=True, null=True)



    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        img_b = Image.open(self.profile_banner.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

        if img_b.height > 1280 or img_b.width > 400:
            output_size_b = (1280,300)
            img_b.thumbnail(output_size_b)
            img_b.save(self.profile_banner.path)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk': self.pk})

    def get_api_follow_url(self):
        return reverse('profile-follow-toggle', kwargs={'pk': self.pk})





class CounterManager(models.Manager):
    def update_counter(self, pk):
        self.filter(id=pk).update(count=F('story_progress')+1)

class Counter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    story_progress = models.PositiveIntegerField(default=0)
    story_finish = models.BooleanField(default=False) #Just to play yenno -
    story_finished = models.BooleanField(default=False) #finished in general -- Sorry future Dev these names annoying
    finish_ft = models.BooleanField(default=False)#finished the first time -
    choice_chose = models.IntegerField(default=0)
    restarted = models.BooleanField(default=False)
    times_restarted = models.IntegerField(default=0)
    objects = CounterManager()

    def __str__(self):
        return f'{self.story} {self.user.username}'

class StoryComment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comment_story')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=1100)
    created = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'{self.author} commented on {self.story}'

    def get_absolute_url(self):
        return reverse('story-detail', kwargs={'pk': self.story_id})

    def get_api_like_url(self):
        return reverse('comment-like-toggle', kwargs={'pk': self.pk})

class ReportCategories(models.Model):
    report_category = models.TextField()

    def __str__(self):
        return self.report_category

    def get_absolute_url(self):
        return reverse('report-category-update', kwargs={'pk': self.pk})

class ReportPost(models.Model):
    # we wont delete profile jus ban it ?
    # if we delete then report deletes
    # if report delete then rip logs?
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    reason = models.ForeignKey(ReportCategories, on_delete=models.CASCADE)
    other = models.TextField(max_length=1100)
    reporter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_reporter')
    report_date = models.DateTimeField('date reported', default=timezone.now)
    status = models.BooleanField(default=False)
    notes = models.TextField()

    def get_absolute_url(self):
        return reverse('story-detail', kwargs={'pk': self.story.pk})

    def __str__(self):
        return (self.reason, 'Handled: ',self.status)



class ReportProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reason = models.ForeignKey(ReportCategories, on_delete=models.CASCADE)
    other = models.TextField(max_length=1100)
    reporter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_reporter')
    report_date = models.DateTimeField('date reported', default=timezone.now)
    status = models.BooleanField(default=False)
    notes = models.TextField()

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk':self.profile.pk})

class SupportCategories(models.Model):
    support_category = models.TextField()


    def __str__(self):
        return self.support_category

    def get_absolute_url(self):
        return reverse('support-category-update', kwargs={'pk': self.pk})

class SupportTicket(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    reason = models.ForeignKey(SupportCategories, on_delete=models.CASCADE)
    other = models.TextField(max_length=1200)
    pub_date = models.DateTimeField('Ticket Created', default=timezone.now)
    status = models.BooleanField(default=False)
    notes = models.TextField()

    def __str__(self):
        return (str(self.reason) + 'Handled:' +str(self.status))

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'pk':self.user.pk})









