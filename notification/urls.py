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
from . import views as notification_view

urlpatterns = [
    url(r'^comments/$', notification_view.comments, name='comments'),
    url(r'^follows/$', notification_view.follows, name='follows'),
    url(r'^likes/$', notification_view.likes, name='likes'),
    url(r'^systems/$', notification_view.systems, name='systems'),
]