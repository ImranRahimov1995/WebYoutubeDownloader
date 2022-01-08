from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.sessions.models import Session
from .forms import Getlink
from .models import MyYoutube
import os
from django.http.response import HttpResponse





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

    if request.method == "POST":
        form = Getlink(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            choosed_format = form.cleaned_data['choose']
            #Save user selected format in session 
            # for inital data for new download
            request.session['user'] = str(choosed_format)
            request.session.modified = True
            
            yt = MyYoutube.objects.create(link=link)
            #Status return form download method of class My_Youtube
            status = yt.download(choosed_format=choosed_format)
            if status == "Failed":
                return redirect('index')
            else:
                return download_file(request,obj=yt,
                                    resolution=str(choosed_format))
    

    if request.method == "GET":
        choose =request.session.get('user', None)
        if not choose:
            choose = 'video'
        form = Getlink(initial={'choose': choose})
    info = None

    return render(request,'index.html',{'form':form,'info':info},)