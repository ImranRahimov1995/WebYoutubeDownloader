from django.contrib import admin
from youtube.models import MyYoutube,Visitor


class MyYoutubeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']

class VisitorAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'visit_time']


admin.site.register(MyYoutube,MyYoutubeAdmin)
admin.site.register(Visitor,VisitorAdmin)