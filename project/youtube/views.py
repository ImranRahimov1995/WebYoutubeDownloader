from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.sessions.models import Session
from .forms import Getlink
from .models import MyYoutube
import os
from django.http.response import HttpResponse





def download_file(request,yt,res):
    filename = yt.sl_title
    filepath = yt.abs_path
    f = open(filepath, 'rb')

    if res == "audio":
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
    return response

def upload_file(request,res):
    id =request.session.get('user',None)
    yt = get_object_or_404(MyYoutube,id=id)
    up = yt.download(res)
    return download_file(request,yt,res)


def index(request):
    if request.method == "POST":
        form = Getlink(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            choose = form.cleaned_data['choose']
            request.session['user'] = str(choose)
            
            yt = MyYoutube.objects.create(link=link)
            status = yt.downloadV2(choose=choose)
            if status == "Failed":
                return redirect('index')
            else:
                return download_file(request,yt=yt,res=str(choose))
    

    if request.method == "GET":
        sv =request.session.get('user', None)
        if not sv:
            sv = 'video'
        form = Getlink(initial={'choose': sv})
        info = None
        
    return render(request,'index.html',{'form':form,'info':info},)