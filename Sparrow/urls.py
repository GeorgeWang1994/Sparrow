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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^album/', include('album.urls', namespace='album')),
    url(r'^comment/', include('comment.urls', namespace='comment')),
    url(r'^post/', include('post.urls', namespace='post')),
    url(r'^tag/', include('tag.urls', namespace='tag')),
    url(r'^follow/', include('follow.urls', namespace='follow')),
    url(r'^like/', include('like.urls', namespace='like')),
    url(r'^explore/', include('explore.urls', namespace='explore')),
    url(r'^notification/', include('notification.urls', namespace='notification')),
    url(r'^rest/', include('rest.urls', namespace='rest')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
