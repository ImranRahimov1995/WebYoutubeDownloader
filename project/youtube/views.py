from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.sessions.models import Session
from .forms import Getlink
from .models import MyYoutube
import os
from django.http.response import HttpResponse


def index(request):
    if request.method == "POST":
        form = Getlink(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            yt = MyYoutube.objects.create(link=link)
            request.session['user'] = yt.id
            info = MyYoutube.get_info(yt,link=link)

            return redirect('index')

    if request.method == "GET":
        form = Getlink()
        id =request.session.get('user',None)
        if id:
            yt = get_object_or_404(MyYoutube,id=id)
            info = MyYoutube.get_info(yt,link=yt.link)
        else:
            info=None
        
    return render(request,'index.html',{'form':form,'info':info},)


def download_file(request,yt,res):
    filename = yt.sl_title
    filepath = yt.abs_path
    f = open(filepath, 'rb')

    if res == "mp3":
        filename += '.mp3'

        response = HttpResponse(f.read(), content_type='audio/mp3')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; filename*=utf-8''%s" % (filename, filename)
    else:   
        filename += '.mp4'

        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; filename*=utf-8''%s" % (filename, filename)
    f.close()
    os.remove(filepath)
    del request.session['user']
    return response

def upload_file(request,res):
    id =request.session.get('user',None)
    yt = get_object_or_404(MyYoutube,id=id)
    up = yt.download(res)
    return download_file(request,yt,res)


