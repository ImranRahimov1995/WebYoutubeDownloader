from django.contrib import admin
from youtube.models import MyYoutube


class MyYoutubeAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']

admin.site.register(MyYoutube,MyYoutubeAdmin)