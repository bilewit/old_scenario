from django.urls import path, reverse
from .views import (StoryListView,
                    ExploreListView,
                    StoryDetail,
                    StoryPlayView,
                    StoryCreateView,
                    StoryDeleteView,
                    StoryUpdateView,
                    PostLikeToggle,
                    PostLikeAPIToggle,
                    PostReshareAPIToggle,
                    PostFavoriteAPIToggle,

                    SceneCreateView,
                    SceneUpdateView,
                    SceneDeleteView,

                    ChoiceCreateView,
                    ChoiceUpdateView,
                    ChoiceDeleteView,

                    CommentCreateView,
                    CommentReplyView,
                    CommentDeleteView,
                    CommentLikeAPIToggle,


                    )

from users.views import (
        FollowAPIToggle,
        FavoriteAPIToggle,
        BlockAPIToggle,
        AwardsCreateView,
        AwardsUpdateView,
        AwardsDeleteView,
        AwardsListView,
        ReportCategoriesCreateView,
        ReportCategoriesUpdateView,
        ReportCategoriesDeleteView,
        SupportCategoriesCreateView,
        SupportCategoriesUpdateView,
        SupportCategoriesDeleteView,
        ReportPostCreateView,
        ReportProfileCreateView,
        SupportTicketCreateView,
        Terms,
        Privacy,
        Support,
        Careers,
        Notifications,
        NotificationsClear,
        CreateThread,
        SearchView,
        SearchUserView,
        SearchStoryView,




)

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .api import StoryViewSet,SceneViewSet,ChoiceViewSet,ProfileViewSet,StoryCommentViewSet,NotificationsViewSet,ThreadViewSet

router = routers.DefaultRouter()
router.register('story', StoryViewSet, 'storys')
router.register('scene', SceneViewSet, 'scenes')
router.register('choice', ChoiceViewSet, 'choice')
router.register('profile', ProfileViewSet, 'profile')
router.register('comment', StoryCommentViewSet, 'comment')
router.register('notifications', NotificationsViewSet, 'notifications')
router.register('thread', ThreadViewSet, 'thread')

urlpatterns = [

    path('', StoryListView.as_view(), name='scenario-list'),
    path('explore', ExploreListView.as_view(), name='explore'),
    path('terms/', Terms.as_view(), name='terms-page'),
    path('support/', Support.as_view(), name='support-page'),
    path('privacy/', Privacy.as_view(), name='privacy-page'),
    path('careers/', Careers.as_view(), name='careers-page'),
    path('api/', include(router.urls)),
    path('Story/<int:pk>/', StoryDetail.as_view(), name='story-detail'),
    path('StoryPlay/<int:pk>/', StoryPlayView.as_view(), name='story-play'),
    path('Story/<int:pk>/update/', StoryUpdateView.as_view(), name='story-update'),
    path('Story/<int:pk>/delete/', StoryDeleteView.as_view(), name='story-delete'),
    path('Story/new/', StoryCreateView.as_view(), name='story-create'),
    path('Story/<int:pk>/like/', PostLikeToggle.as_view(), name='post-like'),


    path('api/Story/<int:pk>/like/', PostLikeAPIToggle.as_view(), name='post-api-like'),
    path('api/Story/<int:pk>/reshare/', PostReshareAPIToggle.as_view(), name='post-api-reshare'),
    path('api/Story/<int:pk>/favorite/', PostFavoriteAPIToggle.as_view(), name='post-api-favorite'),
    path('api/profile/<int:pk>/follow/', FollowAPIToggle.as_view(), name='profile-follow-toggle'),
    path('api/profile/<int:pk>/favorite/', FavoriteAPIToggle.as_view(), name='profile-favorite-toggle'),
    path('api/profile/<int:pk>/block/', BlockAPIToggle.as_view(), name='profile-block-toggle'),



    path('Scene/<int:pk>/new/', SceneCreateView.as_view(), name='scene-create'),
    path('Scene/<int:pk>/update/', SceneUpdateView.as_view(), name='scene-update'),
    path('Scene/<int:pk>/delete/', SceneDeleteView.as_view(), name='scene-delete'),


    path('Choice/<int:pk>/new/', ChoiceCreateView.as_view(), name='choice-create'),
    path('Choice/<int:pk>/update/', ChoiceUpdateView.as_view(), name='choice-update'),
    path('Choice/<int:pk>/delete/', ChoiceDeleteView.as_view(), name='choice-delete'),


    path('Comment/<int:pk>/new/', CommentCreateView.as_view(), name='comment-create'),
    path('Comment/<int:pk>/reply/', CommentReplyView.as_view(), name='comment-reply'),
    path('Comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('api/comment/<int:pk>/like/', CommentLikeAPIToggle.as_view(), name='comment-like-toggle'),

    path('Awards/', AwardsListView.as_view(), name='awards-list'),
    path('Awards/new/', AwardsCreateView.as_view(), name='award-create'),
    path('Awards/<int:pk>/update/', AwardsUpdateView.as_view(), name='award-update'),
    path('Awards/<int:pk>/delete/', AwardsDeleteView.as_view(), name='award-delete'),

    path('ReportCategory/new/', ReportCategoriesCreateView.as_view(), name='report-category-create'),
    path('ReportCategory/<int:pk>/update/', ReportCategoriesUpdateView.as_view(), name='report-category-update'),
    path('ReportCategory/<int:pk>/delete/', ReportCategoriesDeleteView.as_view(), name='report-category-delete'),

    path('SupportCategory/new/', SupportCategoriesCreateView.as_view(), name='support-category-create'),
    path('SupportCategory/<int:pk>/update/', SupportCategoriesUpdateView.as_view(), name='support-category-update'),
    path('SupportCategory/<int:pk>/delete/', SupportCategoriesDeleteView.as_view(), name='support-category-delete'),

    path('StoryDetail/<int:pk>/report/', ReportPostCreateView.as_view(), name='story-report'),
    path('profile_detail/<int:pk>/report/', ReportProfileCreateView.as_view(), name='profile-report'),
    path('SupportTicket/new/', SupportTicketCreateView.as_view(), name='support-ticket'),

    path('Notifications/', Notifications.as_view(), name='notifications-list'),
    path('api/Notifications/clear', NotificationsClear.as_view(), name='notifications-clear'),
    path('api/profile/<int:pk>/CreateThread/', CreateThread.as_view(), name='profile-create-thread'),

    path('Search', SearchView.as_view(), name='search'),
    path('uSearch', SearchUserView.as_view(), name='user-search'),
    path('pSearch', SearchStoryView.as_view(), name='post-search'),










    #path('play/<int:pk>/<int:id>/', views.playscene, name='story-play'),
    #path('end/<int:pk>/<int:id>/<int:c_id>/', views.end_scene, name='story-end')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)