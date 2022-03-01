"""fin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import (UserListView,
                         ProfileView,
                         PendingFollowersList,
                        PendingFollowAcceptAPI,
                        PendingFollowDeclineAPI,
                        PrivateProfileAPIToggle,
                            SignUpView,
                            ProfileUpdate,
                            myProfileView,
                        ThreadMessageCreateView,
                            ThreadView,
BlockList,
loladmin,
                         )
    #, FollowersListView, FollowingListView




urlpatterns = [
    path('admin/', loladmin.as_view(), name='admin'),
    path('notadmin/', admin.site.urls),
    path('', include('scenario.urls')),
    path('register/', SignUpView.as_view(), name='register'),
    path('myprofile/', myProfileView.as_view(), name='my-profile'),
    path('myprofile/thread/<int:pk>/reply/', ThreadMessageCreateView.as_view(), name='reply-thread'),
    path('myprofile/thread/<int:pk>/view/', ThreadView.as_view(), name='view-thread'),
    path('profile/<int:pk>/update/', ProfileUpdate.as_view(), name='profile'),
    path('profile_list/', UserListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('pending_followers/', PendingFollowersList.as_view(), name='pending-followers'),
    path('blocked/', BlockList.as_view(), name='blocked'),
    path('api/profile/<int:pk>/private/', PrivateProfileAPIToggle.as_view(), name='profile-private-toggle'),
    path('api/pending_followers/<int:pk>/accept/', PendingFollowAcceptAPI.as_view(), name='pending-follower-accept'),
    path('api/pending_followers/<int:pk>/decline/', PendingFollowDeclineAPI.as_view(), name='pending-follower-decline'),
    #path('terms', template_name='users/terms.html'),


    # path('followers_list/<int:pk>/', FollowersListView.as_view(), name='followers_list'),
    # path('following_list/<int:pk>/', FollowingListView.as_view(), name='following_list'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login_.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
