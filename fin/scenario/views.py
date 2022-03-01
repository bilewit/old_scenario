from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, request, HttpResponseRedirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Story,Scene,Choice
from django.contrib import messages
from users.models import Counter, StoryComment, Notifications, NotificationCategories, Stats
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import authentication, permissions
from django.core.paginator import Paginator
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from taggit.models import Tag
from el_pagination.views import AjaxListView


class ExploreListView(ListView):
    model = Story
    template_name = 'scenario/explore.html'
    context_object_name = 'storys'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        feed = Story.objects.filter(author__profile__private_profile=False).filter(published=True)
        context['storys'] = feed.order_by('-likes').order_by('-pub_date')

        return context


#
# class StoryListView(ListView):
#     model = Story
#     paginate_by = 1
#     template_name = 'scenario/feed.html'
#     context_object_name = 'storys'
#
#
#     def get_queryset(self):
#         return Story.objects.all() #.filter(author__profile__following=self.request.user).filter(published=True)
#





class StoryListView(AjaxListView):
    context_object_name = "storys"
    template_name = "scenario/feed.html"
    page_name = "scenario/feed_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:#move this to login
            player = Stats.objects.filter(player=user)
            print(player.count())
            if player.count() == 0:
                stats = Stats.objects.create(player=user)
                #stats = State(player=)
                print(stats)
            else:
                print('we got stats')
                pass
        return Story.objects.all() #.filter(author__profile__following=user).filter(published=True)









class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        #print(pk)
        obj = get_object_or_404(Story, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        like_notification = get_object_or_404(NotificationCategories, id=1)
        notification = Notifications(reciever=obj.author,sender=user,reason=like_notification, post=obj)
        notification.save()
        #print(notification)
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
                obj.author.profile.notifications.remove(notification)
                obj.save()
                #print('hi')
                #print(obj.likes)
            else:
                obj.likes.add(user)
                obj.author.profile.notifications.add(notification)
                obj.save()
                #print('else')
                #print(obj.likes)
                #print(user.likes)
        return url_




class PostLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(Story, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        counts = obj.likes.count()
        like_notification = get_object_or_404(NotificationCategories, id=1)
        notification = Notifications(reciever=obj.author, sender=user, reason=like_notification, post=obj)
        notification.save()
        #print(counts)
        data ={
            "updated": updated,
            "liked": liked,
            "num_likes": counts
        }
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                obj.author.profile.notifications.remove(notification)
                obj.save()
                counts = obj.likes.count()
            else:
                obj.likes.add(user)
                obj.author.profile.notifications.add(notification)
                obj.save()
                liked = True
                counts = obj.likes.count()
            updated = True
            data = {
                "updated": updated,
                "liked": liked,
                "num_likes": counts
            }
        # if request.is_ajax():
        #     print('in if')
        #     storys = Story.objects.all()
        #     # new calculation of the items QuerySet
        #     # depending on the data passed through the $.ajax
        #     return render(request, 'scenario/feed.html', locals())
        return Response(data)

#finish
class PostReshareAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(Story, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        reshared = False
        counts = obj.reshares.count()
        reshare_notification = get_object_or_404(NotificationCategories, id=4)
        notification = Notifications(reciever=obj.author, sender=user, reason=reshare_notification, post=obj)
        notification.save()
        data ={
            "updated": updated,
            "reshared": reshared,
            "num_reshares": counts
        }
        if user.is_authenticated:
            if user in obj.reshares.all():
                liked = False
                obj.reshares.remove(user)
                obj.author.profile.notifications.remove(notification)
                obj.save()
                counts = obj.reshares.count()
            else:
                obj.reshares.add(user)
                obj.author.profile.notifications.add(notification)
                obj.save()
                reshared = True
                counts = obj.reshares.count()
            updated = True
            data = {
                "updated": updated,
                "reshared": reshared,
                "num_reshares": counts
            }
        return Response(data)

class PostFavoriteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(Story, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        favorites = False
        counts = obj.favorites.count()
        #print(counts)
        data ={
            "updated": updated,
            "favorites": favorites,
            "num_favorites": counts
        }
        if user.is_authenticated:
            if user in obj.favorites.all():
                favorites = False
                obj.favorites.remove(user)
                obj.save()
                counts = obj.favorites.count()
            else:
                obj.favorites.add(user)
                obj.save()
                favorites = True
                counts = obj.favorites.count()
            updated = True
            data = {
                "updated": updated,
                "favorites": favorites,
                "num_favorites": counts
            }
        return Response(data)



class CommentLikeAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(StoryComment, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        counts = obj.likes.count()
        print(counts)
        data ={
            "updated": updated,
            "liked": liked,
            "num_likes": counts
        }
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
                obj.save()
                counts = obj.likes.count()
            else:
                obj.likes.add(user)
                obj.save()
                liked = True
                counts = obj.likes.count()
            updated = True
            data = {
                "updated": updated,
                "liked": liked,
                "num_likes": counts
            }
        return Response(data)






class StoryDetail(TemplateView):
    model = Story
    template_name = 'scenario/story_detail.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Story.objects.get(pk=self.kwargs['pk'])  # gets self
        pk = event.pk  # gets self pk
        story = Story.objects.get(id=pk)
        user = self.request.user
        counter = Counter.objects.filter(user=user).filter(story=story)[0]
        context['finished'] = counter.story_finished
        context['story'] = story
        comments = story.comment_story.all()
        context['comments'] = comments
        return context



class StoryCreateView(CreateView):
    model = Story
    fields = ['story_title', 'story_description', 'story_pic', 'tags']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StoryUpdateView(UpdateView):
    model = Story
    fields = ['story_title', 'story_description', 'story_pic', 'tags', 'published']

    def dispatch(self, request, *args, **kwargs):
        story = Story.objects.get(pk=self.kwargs['pk'])
        if story.published == True:
            self.fields = ['story_title', 'story_description', 'story_pic', 'tags', 'archive']
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.published == True:
            story = Story.objects.get(pk=self.kwargs['pk'])
            scenes = Scene.objects.filter(story=story)
            for scene in scenes:
                choices = Choice.objects.filter(scene=scene)
                if choices.count() > 0:

                    pass
                else:

                    form.instance.published = False
                    form.instance.draft = True
                    return super().form_valid(form)
        else:
            pass
            #check to see if every scene has a choice
            # if it does then boom good if not change to false lmao
            # n be like hey


        return super().form_valid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Story.objects.get(pk=self.kwargs['pk']) #gets self
        pk = event.pk #gets self pk
        story = Story.objects.get(id=pk) #Parent and children in story
        scenes = story.scenestory.all() #gets all scenes from self
        # print(scenes)
        context['scenes'] = scenes
        return context

    def test_func(self):
        story = self.get_object()
        if self.request.user == story.author:
            return True
        return False

class StoryDeleteView(DeleteView):

    model = Story
    success_url = '/'


    def test_func(self):
        story = self.get_object()
        if self.request.user == story.author:
            return True
        return False

class StoryPlayView(TemplateView):
    model = Story
    template_name =  'scenario/story_play.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Story.objects.get(pk=self.kwargs['pk'])  # gets self
        pk = event.pk  # gets self pk
        user = self.request.user
        story = Story.objects.get(id=pk)  # Parent and children in story
        scenes = story.scenestory.all()  # gets all scenes from self
        # counter asigned to player and story
        if Counter.objects.filter(user=self.request.user).filter(story=story).exists():
            pass
        else:
            counter = Counter(story=story, user=user)
            counter.save()
        counter = Counter.objects.filter(user=self.request.user).filter(story=story)[0]
        if counter.story_progress > 0:
            pre_scene = Choice.objects.get(id=counter.choice_chose) #prev chosen choice id
            context['pre_scene'] = pre_scene.choice_do
            print(pre_scene)
        context['scene'] = scenes[counter.story_progress]

        #add story to stories played in stats
        player_stats = Stats.objects.filter(player=user)[0]
        if user in player_stats.stories_played.all():
            pass
        else:
            player_stats.stories_played.add(story)
            player_stats.save()


        return context

    def post(self, request, *args, **kwargs):   #required post method
        user = self.request.user
        context = super().get_context_data(**kwargs)
        event = Story.objects.get(pk=self.kwargs['pk'])  # gets self
        pk = event.pk  # gets self pk
        story = Story.objects.get(id=pk)  # Parent and children in story
        context['story'] = story
        scenes = story.scenestory.all()  # gets all scenes from self
        counter = Counter.objects.filter(user=self.request.user).filter(story=story)[0]
        player_stats = Stats.objects.filter(player=user)[0]



        if counter.choice_chose > 0:
            pre_scene = Choice.objects.get(id=counter.choice_chose)  # prev chosen choice id
            context['pre_scene'] = pre_scene.choice_do
        num_scenes = len(scenes)-1


        if self.request.POST.get('choice'):
            chosen_choice = self.request.POST.get('choice')
            choice = Choice.objects.get(id=chosen_choice)
            if counter.story_progress > num_scenes:
                counter.story_progress -= 1
            if counter.choice_chose > 0:
                context['pre_scene'] = pre_scene.choice_do

        #if user picks an ok choice continue
            if (self.request.method == 'POST' and
                    counter.story_progress < num_scenes and
                    choice.choice_end == False):

                counter.choice_chose = choice.id
                counter.save()
                counter.story_progress += 1
                counter.save()
                if counter.choice_chose > 0:
                    pre_scene = Choice.objects.get(id=counter.choice_chose)
                    context['pre_scene'] = pre_scene.choice_do
                context['scene'] = scenes[counter.story_progress]
                return render(request, 'scenario/story_play.html', context) #returns self, with the next scene/new context
        #if user makes it to the end and picks the right choice
            elif (self.request.method == 'POST' and
                    counter.story_progress == num_scenes and
                    choice.choice_end == False):
                success_counter = counter.story_progress
                context['choice'] = choice.choice_end_success_text
                context['choice_pic'] = choice.choice_pic.url
                counter.story_finish = True
                counter.story_finished = True
                if story in player_stats.stories_finished.all():
                    print('already finished')
                else:
                    player_stats.stories_finished.add(story)
                    player_stats.save()
                counter.story_progress = 0
                counter.choice_chose = 0

                if counter.restarted == False:
                    if story in player_stats.stories_yolo.all():
                        print('damn you already yolod')
                    else:
                        player_stats.stories_yolo.add(story)
                        print('added to yolo')
                        player_stats.save()

                counter.save()
                return render(request, 'scenario/story_end.html', context)


        #if user picks a bad choice
            elif (self.request.method == 'POST' and
                    choice.choice_end == True):
                death_counter = counter.story_progress
                counter.story_progress = 0 #no mercy keep until JAN 2020 ;)
                counter.choice_chose = 0
                counter.restarted = True
                counter.times_restarted += 1
                counter.save()
                context['choice'] = choice.choice_end_fail_text
                context['choice_pic'] = choice.choice_pic.url
                return render(request, 'scenario/story_end.html', context) #returns self, with the next scene/new context
        #Post with no choice then you get a message
        else:
            messages.add_message(request, messages.INFO, 'Pick a choice')
        return HttpResponseRedirect(self.request.path_info) #required return

#===============================================================#

class SceneCreateView(LoginRequiredMixin, CreateView):
    model = Scene
    fields = ['scene_description', 'scene_pic']

    def form_valid(self, form):
        c_story = Story.objects.get(pk=self.kwargs['pk']) #this needs to stay Story because it creates scene ?
        form.instance.story_id = c_story.pk #this needs to stay story_id
        return super().form_valid(form)

class SceneUpdateView(LoginRequiredMixin,UpdateView):
    model = Scene
    fields = ['scene_description', 'scene_pic']


    def form_valid(self, form):
        c_story = Scene.objects.get(pk=self.kwargs['pk']) #scene finally has a name so its updating itself
        form.instance.scene_id = c_story.pk
        #print(c_story)
        #print('hi')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Scene.objects.get(pk=self.kwargs['pk']) #gets self
        pk = event.pk #gets self pk
        scene = Scene.objects.get(id=pk) #Parent and children in story
        choice = scene.choicescene.all() #gets all scenes from self
        #print(choice)
        context['choice'] = choice
        return context

class SceneDeleteView(LoginRequiredMixin,  DeleteView):
    model = Scene
    success_url = '/scenario/' #need to redirect to story detail instead

#===============================================================#
class ChoiceCreateView(LoginRequiredMixin, CreateView):
    model = Choice
    fields = ['choice_text','choice_do','choice_end','choice_end_fail_text','choice_end_success','choice_end_success_text','choice_pic']
    # need to do a check to make sure both boxes aren't checked

    def form_valid(self, form):
        c_story = Scene.objects.get(pk=self.kwargs['pk']) #this needs to stay Scene because it creates choice ?
        form.instance.scene_id = c_story.pk #this needs to stay scene_id
        if form.instance.choice_end == True and form.instance.choice_end_success == True: #if user tries to check success and fail
            form.instance.choice_end_success = False
            form.instance.choice_end = False
            form.instance.choice_id = c_story.pk
            #print(form.instance.choice_end)
            #print(form.instance.choice_end_success)
        else:
            form.instance.choice_id = c_story.pk
        return super().form_valid(form)

class ChoiceUpdateView(LoginRequiredMixin,  UpdateView):
    model = Choice
    fields = ['choice_text','choice_do','choice_end','choice_end_fail_text','choice_end_success','choice_end_success_text','choice_pic']
    # need to do a check to make sure both boxes aren't checked

    def form_valid(self, form):
        c_story = Choice.objects.get(pk=self.kwargs['pk'])  # choice finally has a name so its updating itself
        if form.instance.choice_end == True and form.instance.choice_end_success == True: #if user tries to check success and fail
            form.instance.choice_end_success = False
            form.instance.choice_end = False
            form.instance.choice_id = c_story.pk
            #print(form.instance.choice_end)
            #print(form.instance.choice_end_success)
        else:
            form.instance.choice_id = c_story.pk
        return super().form_valid(form)



class ChoiceDeleteView(LoginRequiredMixin,  DeleteView):

    model = Choice
    success_url = '/scenario/' #need to redirect to story detail instead


    # def test_func(self):
    #     story = self.get_object()
    #     if self.request.user == story.author:
    #         return True
    #     return False

class CommentCreateView(LoginRequiredMixin,  CreateView):
    model = StoryComment
    fields = ['comment_text']

    def form_valid(self, form):
        c_story = Story.objects.get(pk=self.kwargs['pk'])  # this needs to stay Story because it creates scene ?
        form.instance.story_id = c_story.pk  # this needs to stay story_id
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentReplyView(LoginRequiredMixin, CreateView):
    model = StoryComment
    fields = ['comment_text']

    def form_valid(self, form):
        c_story = StoryComment.objects.get(pk=self.kwargs['pk']) #this needs to stay Story because it creates scene ?
        form.instance.comment_id = c_story.pk #this needs to stay story_id
        form.instance.story_id = c_story.story.id  # this needs to stay story_id
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, DeleteView):

    model = StoryComment
    success_url = '' #need to redirect to story detail instead

class CommentCreateView(CreateView):
    model = StoryComment
    fields = ['comment_text']

    def form_valid(self, form):
        c_story = Story.objects.get(pk=self.kwargs['pk'])  # this needs to stay Story because it creates scene ?
        form.instance.story_id = c_story.pk  # this needs to stay story_id
        form.instance.author = self.request.user
        return super().form_valid(form)
