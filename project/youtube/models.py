from django.db import models
from pytube import YouTube
from django.utils.text import slugify
from django.conf import settings
import re


def cjk_detect(texts):
    # korean
    if re.search("[\uac00-\ud7a3]", texts):
        return "ko"
    # japanese
    if re.search("[\u3040-\u30ff]", texts):
        return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return "zh"
    return None

class Visitor(models.Model):
    user_info = models.CharField(max_length=255,blank=True)
    visit_time = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ('-visit_time',)
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'


class MyYoutube(models.Model):


    link = models.URLField()

    title = models.CharField(max_length=255,
                             null=True,blank=True)
    absolute_path = models.CharField(max_length=255,
                                     null=True,blank=True)
    slug_title = models.CharField(max_length=255,
                                 null=True,blank=True)

    created = models.DateTimeField(auto_now_add=True)

    user_info = models.CharField(max_length=255,blank=True)


    def download(self,choosed_format):
        """
        This method download audio track if is exists.
        Download video quality=720p, if is exists ,
        if not download 480p.
        
        If the method worked correctly,and download file , 
        the method returns the string Done

        """        
        yt = YouTube(str(self.link))
        self.title = yt.title
        check_for_other_symb = cjk_detect(yt.title)
        if check_for_other_symb:
            self.slug_title = 'noname'
        else:
            self.slug_title = slugify(yt.title)

        self.absolute_path = str(settings.MEDIA_ROOT) + "/" \
                                         + self.slug_title
        self.save()
        
        if choosed_format == "audio":
            stream = yt.streams.get_by_itag(140)
            if stream:
                stream.download('media',filename=self.slug_title) 
                return('Done')           
            else:
                return('Failed')
        else:
            stream = yt.streams.get_by_itag(22)
            if not stream:
                stream = yt.streams.get_by_itag(18)
            stream.download('media',filename=self.slug_title) 
            return('Done')

 
    def __str__(self):
        return self.title
    

    class Meta:
        ordering = ('-created',)   
        verbose_name = 'Youtube object'
        verbose_name_plural = 'Youtube objects'

