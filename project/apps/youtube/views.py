from django.shortcuts import render, redirect

from .forms import Getlink
from .models import Visitor
from .services import *


def index(request):
    user_info = get_info_about_user(request)

    if request.method == "POST":
        form = Getlink(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            selected_format = form.cleaned_data['choose']
            status, yt = create_myyoutube_object(
                request, link, selected_format, user_info
            )
            if status == "Failed":
                return redirect('index')
            else:
                return download_file_from_server(
                    request,
                    yt_object=yt,
                    resolution=str(selected_format),
                )

    if request.method == "GET":
        Visitor.objects.create(user_info=user_info)
        choose = request.session.get('user', None)

        if not choose:
            choose = 'video'
        form = Getlink(initial={'choose': choose})

    return render(request, 'index.html', {'form': form, })
