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
from . import views as follow_view

urlpatterns = [
    url(r'^do/$', follow_view.follow, name='follow'),
    url(r'^undo/$', follow_view.unfollow, name='unfollow'),
    url(r'^tag/do/$', follow_view.follow_tag, name='follow_tag'),
    url(r'^tag/undo/$', follow_view.unfollow_tag, name='unfollow_tag')
]
