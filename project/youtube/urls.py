from django.urls import path
from . import views



urlpatterns = [
    path('',views.index,name='index'),
    path('upload/<str:res>',views.upload_file,name='upload'),
]