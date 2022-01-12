import os
import requests
from django.shortcuts import render,redirect
from .forms import Getlink
from .models import MyYoutube,Visitor
from django.http.response import HttpResponse
from django.conf import settings

def get_info_about_user(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if not settings.DEBUG:
        ip = request.META['HTTP_X_REAL_IP']
    else:
        ip = "139.162.175.79"
    about_device  = user_agent.split(')')[0].split('(')[1]
    url = f'https://api.iplocation.net/?ip={ip}'
    country = requests.get(url).json()['country_name']
    return country+" | "+ip+" | "+about_device


def download_file(request,obj,resolution):

    filename = obj.slug_title
    filepath = obj.absolute_path
    f = open(filepath, 'rb')

    if resolution == "audio":
        filename += '.mp3'
        response = HttpResponse(f.read(), content_type='audio/mp3')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; \
                                filename*=utf-8''%s" % (filename, filename)

    else:   

        filename += '.mp4'
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; \
                                filename*=utf-8''%s" % (filename, filename)

    f.close()
    #Delete downloaded file for so as not to take up space
    os.remove(filepath)
    
    return response



def index(request):
    user_info = get_info_about_user(request)
    if request.method == "POST":
        form = Getlink(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            choosed_format = form.cleaned_data['choose']
            #Save user selected format in session 
            # for inital data for new download
            request.session['user'] = str(choosed_format)
            request.session.modified = True
            
            yt = MyYoutube.objects.create(link=link,user_info=user_info)
            #Status return form download method of class My_Youtube
            status = yt.download(choosed_format=choosed_format)
            if status == "Failed":
                return redirect('index')
            else:
                return download_file(request,obj=yt,
                                    resolution=str(choosed_format))
    

    if request.method == "GET":
        Visitor.objects.create(user_info=user_info)
        choose =request.session.get('user', None)
        if not choose:
            choose = 'video'
        form = Getlink(initial={'choose': choose})
    info = None

    return render(request,'index.html',{'form':form,'info':info},)