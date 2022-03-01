from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ReferredForm
from . models import (Profile, Awards, ReportCategories,
                      SupportCategories, ReportPost, ReportProfile,
                      SupportTicket, Notifications, NotificationCategories, Thread, Thread_Message, Stats)
from scenario.models import Story
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm

class Terms(TemplateView):
    template_name = 'users/terms.html'
class Privacy(TemplateView):
    template_name = 'users/privacy.html'
class Careers(TemplateView):
    template_name = 'users/careers.html'
class Support(TemplateView):
    template_name = 'users/support.html'

class loladmin(TemplateView):
    template_name = 'users/loladmin.html'



class SearchView(ListView):
    model = Profile
    template_name = 'users/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['tag_search'] = Story.objects.filter(tags__name__in=[search])
        context['all_search_results'] = User.objects.filter(username__icontains=search)
        context['search'] =search
        return context

class SearchUserView(ListView):
    model = Profile
    template_name = 'users/search_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['all_search_results'] = User.objects.filter(username__icontains=search)
        return context

class SearchStoryView(ListView):
    model = Story
    template_name = 'users/search_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        context['tag_search'] = Story.objects.filter(tags__name__in=[search])
        context['search'] = search

        return context


class SignUpView(FormView):
    form_class = UserCreationForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)

        login(self.request, user)
        return redirect('my-profile')

class ProfileUpdate(UpdateView):
    model = Profile
    #fields = ['profile_pic', 'bio', 'private_profile']

    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        user = self.request.user
        if user.profile.referrer_code == None:
            self.fields = ['profile_pic', 'profile_banner', 'bio', 'private_profile', 'referrer_code', 'website', 'instagram', 'twitter', 'tiktok', 'youtube']
        else:
            referred_user = Profile.objects.all().filter(referral_code=user.profile.referrer_code)
            x = referred_user.count()
            x = int(x)
            if x < 1:
                user.profile.referrer_code = None
                user.save()
                pass
            else:
                print(referred_user)
                referred_user_ = referred_user[0]
                if user in referred_user_.referrals.all():
                    print('fixed')
                    pass
                else:
                    #print()
                    referred_user_.referrals.add(user)
                    referred_user_.save()
            #print(user.profile.referrer_code)
            self.fields = ['profile_pic', 'profile_banner', 'bio', 'private_profile', 'website', 'instagram', 'twitter', 'tiktok', 'youtube']
            user.save()
        return super().dispatch(request, *args, **kwargs)


class UserListView(ListView):
    model = Profile
    template_name = 'users/profile_list.html'
    context_object_name = 'profiles'

class ProfileView(TemplateView):
    model = Profile
    template_name = 'users/user-profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=user)
        obj = get_object_or_404(Profile, id=profile.id)
        thread_check = Thread.objects.filter(room__id=self.request.user.id).filter(room__id=obj.user.id)
        if not thread_check:
            thread_created = False
            context['messages'] = None
        else:
            thread_created = True
            messages = Thread.objects.filter(room__id=self.request.user.id).filter(room__id=obj.user.id)
            thread_id = messages[0].id
            real_thread = get_object_or_404(Thread, id=thread_id)
            #print(real_thread)
            thread_messages = Thread_Message.objects.filter(thread=real_thread)
            #print(thread_messages)
            context['messages'] = thread_messages
            context['thread_id'] = real_thread.id


        context['thread_created'] = thread_created
        context['profile'] = profile
        user_stories = Story.objects.filter(author=user)
        user_reshares = Story.objects.filter(reshares=user)
        context['user_stories'] = user_stories
        context['user_reshares'] = user_reshares
        #user_liked_stories = Liked_Story.objects.filter(user=user).filter(like_story=1)
        #context['user_liked_stories'] = user_liked_stories
        return context





    def post(self, request, **kwargs):
        return HttpResponseRedirect(self.request.path_info)

class myProfileView(TemplateView):
    model = Profile
    template_name = 'users/myprofile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        stats = Stats.objects.get(player=user)
        inbox = profile.inbox.all()
        print(profile.inbox.all())
        context['profile'] = profile
        context['inbox'] = inbox
        user_stories = Story.objects.filter(author=user)
        user_favorites = Story.objects.filter(favorites=user)
        user_reshares = Story.objects.filter(reshares=user)
        context['user_stories'] = user_stories
        context['user_favorites'] = user_favorites
        context['user_reshares'] = user_reshares
        context['stats'] = stats
        #user_liked_stories = Liked_Story.objects.filter(user=user).filter(like_story=1)
        #context['user_liked_stories'] = user_liked_stories

        return context

    def post(self, request, **kwargs):
        return HttpResponseRedirect(self.request.path_info)


class CreateThread(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Profile, id=pk)
        user = self.request.user
        updated = False
        thread_created = False
        data = {
            "updated": updated,
            "thread_created": thread_created
        }
        if user.is_authenticated:
            check = Thread.objects.filter(room__id=self.request.user.id).filter(room__id=obj.user.id)
            print(check)
            print(check.count())
            check_count = int(check.count())
            if check_count > 0:
                print('passed ;)')
                thread_created = True
                data = {
                    "updated": updated,
                    "thread_created": thread_created
                }
                pass
            else:
                print('else')
                thread = Thread.objects.create()
                thread.room.add(obj.user.id)
                thread.room.add(self.request.user.id)
                thread.save()
                self.request.user.profile.inbox.add(thread)
                self.request.user.save()
                obj.inbox.add(thread)
                obj.save()
                print(thread)
                print('thread above?')
                updated = True
                thread_created = True
                data = {
                    "updated": updated,
                    "thread_created": thread_created
                }
            #check to see if you two are already in a thread
            # if so then pass
            #else create a thread and hide that link on template
        return Response(data)


class ThreadMessageCreateView(CreateView):
    model = Thread_Message
    fields = ['message']
    template_name = 'users/create-message.html'
    success_url = '/myprofile'
    def form_valid(self, form):
        form.instance.sender = self.request.user
        thread = Thread.objects.get(pk=self.kwargs['pk'])
        form.instance.thread = thread

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ThreadView(ListView):
    model = Thread
    context_object_name = 'thread'
    template_name = 'users/messages.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = Thread.objects.get(pk=self.kwargs['pk'])
        messages = Thread_Message.objects.all().filter(thread=thread)
        context['messages'] = messages
        context['thread'] = thread
        return context





class PrivateProfileAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        obj = get_object_or_404(Profile, id=pk)
        updated = False
        status_private = False
        data ={
            "updated": updated,
            "Private": status_private,
        }
        if obj.private_profile == True:
            obj.private_profile = False
            obj.save()
            status_private = obj.private_profile
            updated = True
        else:
            obj.private_profile = True
            obj.save()
            status_private = obj.private_profile
            updated = True
        data = {
            "updated": updated,
            "Private": status_private,
                }
        return Response(data)

class Notifications(ListView):
    model = Notifications
    template_name = 'users/notifications.html'
    context_object_name = 'notifications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        context['notifications'] = profile.notifications.all()
        context['old_notifications'] = profile.old_notifications.all()
        return context

class NotificationsClear(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        user = self.request.user
        profile = user.profile
        notifications = profile.notifications.all()
        updated = False
        num_notifications = notifications.count()
        num_notifications = int(num_notifications)
        num_old_notifications = profile.old_notifications.count()
        num_old_notifications = int(num_old_notifications)
        data = {
            "updated": updated,
            "num_notifications": num_notifications,
            "num_old_notifications": num_old_notifications
        }
        if user.is_authenticated:
            for x in notifications:
                profile.old_notifications.add(x)
                profile.notifications.remove(x)
                profile.save()
            updated = True
            num_notifications = notifications.count()
            num_notifications = int(num_notifications)
            num_old_notifications = profile.old_notifications.count()
            num_old_notifications = int(num_old_notifications)
            data = {
                "updated": updated,
                "num_notifications": num_notifications,
                "num_old_notifications": num_old_notifications
            }
        return Response(data)



class FollowAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        obj = get_object_or_404(Profile, id=pk) #followee/person being followed
        url_ = obj.get_absolute_url()
        user = self.request.user
        obj_1 = get_object_or_404(Profile, id=user.profile.id) #follower/self
        updated = False
        follow = False
        num_followers = obj.followers.count()
        follow_notification = get_object_or_404(NotificationCategories, id=2)
        notification = Notifications(reciever=obj.user, sender=user, reason=follow_notification)

        print(notification)
        #notification.save()
        #print(notification)
        data ={
            "updated": updated,
            "following": follow,
            "num_followers": num_followers
        }
        if user.is_authenticated:
            if user in obj.followers.all():
                follow = False
                obj.followers.remove(user)
                obj_1.following.remove(obj.user)
                #obj.notifications.remove(notification)
                # Notifications.objects.filter(notification=notification).delete()
                obj.save()
                obj_1.save()
                num_followers = obj.followers.count()
            else:
                if obj.private_profile == True:
                    obj.pending_followers.add(user)
                    obj.save()
                    follow = False
                    updated = True
                    num_followers = obj.followers.count()
                    data = {
                        "updated": updated,
                        "following": follow,
                        "num_followers": num_followers
                    }
                    return Response(data)
                if obj_1.user in obj.block_list.all():
                    follow = False
                    updated = True
                    num_followers = obj.followers.count()
                    data = {
                        "updated": updated,
                        "following": follow,
                        "num_followers": num_followers
                    }
                    return Response(data)

                obj.followers.add(user)
               # obj.notifications.add(notification)
                obj_1.following.add(obj.user)
                obj.save()
                obj_1.save()
                follow = True
                num_followers = obj.followers.count()
            updated = True
            data = {
                "updated": updated,
                "following": follow,
                "num_followers": num_followers
            }
        return Response(data)

class AwardsCreateView(CreateView):
    model = Awards
    fields = ['award_title', 'award_description', 'award_image']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AwardsUpdateView( UpdateView):
    model = Awards
    fields = ['award_title', 'award_description', 'award_image']

class AwardsDeleteView( DeleteView):
    model = Awards
    success_url = '' #need to redirect to story detail instead

class ReportCategoriesCreateView(CreateView):
    model = ReportCategories
    fields = ['report_category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ReportCategoriesUpdateView( UpdateView):
    model = ReportCategories
    fields = ['report_category']

class ReportCategoriesDeleteView( DeleteView):
    model = ReportCategories
    success_url = ''  # need to redirect to story detail instead

class SupportCategoriesCreateView(CreateView):
    model = SupportCategories
    fields = ['support_category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SupportCategoriesUpdateView( UpdateView):
    model = SupportCategories
    fields = ['support_category']

class SupportCategoriesDeleteView( DeleteView):
    model = ReportCategories
    success_url = ''  # need to redirect to story detail instead

class AwardsListView(ListView):
    model = Awards
    template_name = 'users/awards_list.html'
    context_object_name = 'awards'

class PendingFollowersList(ListView):
    model = Profile
    template_name = 'users/pending_followers.html'
    context_object_name = None

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return profile



class BlockList(ListView):
    model = Profile
    template_name = 'users/block_list.html'
    context_object_name = 'profile'

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return profile[0]


class PendingFollowAcceptAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(Profile, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        following = False
        data ={
            "updated": updated,
            "following": following,
        }
        if user.is_authenticated:
                user.profile.pending_followers.remove(obj.user)
                user.profile.followers.add(obj.user)
                user.save()
                following = True
                updated = True
                data = {
                "updated": updated,
                "following": following,
            }
        return Response(data)

class PendingFollowDeclineAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        #pk = self.kwargs.get("pk")
        # print(pk)
        obj = get_object_or_404(Profile, id=pk)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        following = False
        data ={
            "updated": updated,
            "following": following,
        }
        if user.is_authenticated:
                user.profile.pending_followers.remove(obj.user)
                user.save()
                following = False
                updated = True
                data = {
                "updated": updated,
                "following": following,
            }
        return Response(data)

class BlockAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        obj = get_object_or_404(Profile, id=pk) #blocked/person being blocked
        url_ = obj.get_absolute_url()
        user = self.request.user
        obj_1 = get_object_or_404(Profile, id=user.profile.id) #follower/self
        updated = False
        blocked = False
        data ={
            "updated": updated,
            "blocked": blocked,
        }
        if user.is_authenticated:
            if obj.user in obj_1.block_list.all():
                blocked = False
                obj_1.block_list.remove(obj.user)
                obj_1.save()
            else:
                if obj.user in obj_1.followers.all():
                    obj.following.remove(obj_1.user)
                    obj.save()
                    obj_1.followers.remove(obj.user)
                    obj_1.save()
                if obj_1.user in obj.followers.all():
                    obj_1.following.remove(obj.user)
                    obj_1.save()
                    obj.followers.remove(obj_1.user)
                    obj.save()
                obj_1.block_list.add(obj.user)
                obj.save()
                obj_1.save()
                blocked = True
            updated = True
            data = {
                "updated": updated,
                "blocked": blocked,
            }
        return Response(data)


class FavoriteAPIToggle(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk=None, format=None):
        """
        Return a list of all users.
        """
        obj = get_object_or_404(Profile, id=pk) #followee/person being followed
        url_ = obj.get_absolute_url()
        user = self.request.user
        obj_1 = get_object_or_404(Profile, id=user.profile.id) #follower/self
        updated = False
        favorite = False
        data ={
            "updated": updated,
            "favorite": favorite,
        }
        if user.is_authenticated:
            if obj.user in obj_1.favorites.all():
                favorites = False
                obj_1.favorites.remove(obj.user)
                obj_1.save()
            else:
                if obj_1.user in obj.block_list.all():
                    favorites = False
                    updated = True
                    data = {
                        "updated": updated,
                        "favorites": favorites,
                    }
                    return Response(data)

                obj_1.favorites.add(obj.user)
                obj_1.save()
                favorites = True
            updated = True
            data = {
                "updated": updated,
                "favorites": favorites,
            }
        return Response(data)


class ReportPostCreateView(CreateView):
    model = ReportPost
    fields = ['reason','other']

    def form_valid(self, form):
        c_story = Story.objects.get(pk=self.kwargs['pk'])
        form.instance.story = c_story
        form.instance.reporter = self.request.user.profile
        redirect('scenario-list')
        return super().form_valid(form)


class ReportProfileCreateView(CreateView):
    model = ReportProfile
    fields = ['reason','other']

    def form_valid(self, form):
        c_story = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = c_story
        form.instance.reporter = self.request.user.profile
        return super().form_valid(form)


class SupportTicketCreateView(CreateView):
    model = SupportTicket
    fields = ['reason','other']

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)













