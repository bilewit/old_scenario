from django.contrib import admin
from . models import (Profile,Counter,StoryComment,Awards,ReportCategories,
                      SupportCategories,ReportPost,ReportProfile,SupportTicket,
                        Notifications, NotificationCategories, Thread, Stats
                      )
# Register your models here.

admin.site.register(Profile)
admin.site.register(Counter)
admin.site.register(Awards)
admin.site.register(StoryComment)
admin.site.register(SupportTicket)
admin.site.register(ReportPost)
admin.site.register(ReportProfile)
admin.site.register(ReportCategories)
admin.site.register(SupportCategories)
admin.site.register(Notifications)
admin.site.register(NotificationCategories)
admin.site.register(Thread)
admin.site.register(Stats)

