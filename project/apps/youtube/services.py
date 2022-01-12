import os
import requests

from django.http.response import HttpResponse
from django.conf import settings

from .models import MyYoutube


def get_info_about_user(request):
    user_agent = request.META['HTTP_USER_AGENT']
    if not settings.DEBUG:
        ip = request.META['HTTP_X_REAL_IP']
    else:
        ip = "139.162.175.79"
    about_device = user_agent.split(')')[0].split('(')[1]
    url = f'https://api.iplocation.net/?ip={ip}'
    country = requests.get(url).json()['country_name']
    return country + " | " + ip + " | " + about_device


def download_file_from_server(request, yt_object, resolution):
    filename = yt_object.slug_title
    filepath = yt_object.absolute_path
    file = open(filepath, 'rb')

    if resolution == "audio":
        filename += '.mp3'
        response = HttpResponse(file.read(), content_type='audio/mp3')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; \
                                filename*=utf-8''%s" % (filename, filename)

    else:
        filename += '.mp4'
        response = HttpResponse(file.read(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(filepath)
        response['Content-Disposition'] = "attachment; filename=\"%s\"; \
                                filename*=utf-8''%s" % (filename, filename)

    file.close()
    # Delete downloaded file for so as not to take up space
    os.remove(filepath)

    return response


def create_myyoutube_object(request, link, selected_format, user_info):
    # Save user selected format in session
    # for initial data for new download

    request.session['user'] = str(selected_format)
    request.session.modified = True

    yt = MyYoutube.objects.create(link=link, user_info=user_info)
    # Status return form download method of class My_Youtube
    status = yt.download(selected_format=selected_format)

    return status, yt


