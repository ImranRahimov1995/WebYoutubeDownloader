from django.db import models
from pytube import YouTube
from django.utils.text import slugify
from django.conf import settings


class MyYoutube(models.Model):


    link = models.URLField()
    title = models.CharField(max_length=255,null=True,blank=True)
    abs_path = models.CharField(max_length=255,null=True,blank=True)
    sl_title = models.CharField(max_length=255,null=True,blank=True)

    created = models.DateTimeField(auto_now_add=True)


    
    def get_info(self,link):
        yt = YouTube(str(link))
        
        sl_title = slugify(yt.title)

        resolutions = {}

        resolutions['1080'] = yt.streams.get_by_itag(137)

        resolutions['720'] = yt.streams.get_by_itag(22)

        resolutions['320'] = yt.streams.get_by_itag(18)

        resolutions['mp3'] = yt.streams.get_by_itag(140)



        info = {
            'title': yt.title,
            'slug_title': sl_title,
            'abs_path': str(settings.MEDIA_ROOT) + "/" + sl_title,
            'resolutions':resolutions
        }

        self.title = info['title']
        self.abs_path =  info['abs_path']
        self.sl_title = info['slug_title']      

        return info


    def download(self,res):
        info = self.get_info(link=self.link)
        if res == "mp3":
            self.abs_path += '.mp3'
            info['resolutions'][res].download('media',filename=self.sl_title+'.mp3')
        else:
            self.abs_path += '.mp4'
            info['resolutions'][res].download('media',filename=self.sl_title+'.mp4')
        
        return True