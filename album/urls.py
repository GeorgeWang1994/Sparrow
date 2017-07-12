"""Sparrow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views as album_view

urlpatterns = [
    url(r'^upload/$', album_view.upload, name='upload'),  # 上传主界面
    url(r'^detail/(?P<id>[^/]+)/$', album_view.index, name='detail'),  # 显示相册
    url(r'^edit/(?P<id>[^/]+)/$', album_view.editAlbum, name='edit_album'),  # 编辑相册
    url(r'^photo/(?P<id>[^/]+)/$', album_view.photo, name='photo'),  # 显示照片
    url(r'^upload/photo/$', album_view.uploadPhoto, name='upload_photo'),  # 上传照片
    url(r'^delete/photo/(?P<id>[^/]+)/$', album_view.delPhoto, name='del_photo'),  # 删除照片
    url(r'^upload/album/$', album_view.uploadAlbum, name='upload_album'),  # 上传相册
    url(r'^del/album/(?P<id>[^/]+)/$', album_view.delAlbum, name='del_album'),  # 删除相册
]