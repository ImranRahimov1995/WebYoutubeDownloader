from django.contrib import admin
from .models import MyYoutube,Visitor


class MyYoutubeAdmin(admin.ModelAdmin):
    list_display = ['title','user_info', 'created']

class VisitorAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'visit_time']


admin.site.register(MyYoutube,MyYoutubeAdmin)
admin.site.register(Visitor,VisitorAdmin)