from . models import Story,Scene,Choice
from users.models import Profile, StoryComment, Notifications, Thread
from rest_framework import viewsets, permissions
from .serializers import (StorySerializer,SceneSerializer,ChoiceSerializer,
                          ProfileSerializer,StoryCommentSerializer,NotificationsSerializer,
                            ThreadSerializer)





#Story Viewset
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StorySerializer

class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SceneSerializer

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ChoiceSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProfileSerializer

class StoryCommentViewSet(viewsets.ModelViewSet):
    queryset = StoryComment.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StoryCommentSerializer

class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = NotificationsSerializer

class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ThreadSerializer