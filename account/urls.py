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
from . import views as account_view

urlpatterns = [
    url(r'^signin/$', account_view.signin, name='signin'),
    url(r'^signup/$', account_view.signup, name='signup'),
    url(r'^signout/$', account_view.signout, name='signout'),
    url(r'^email_activate/(?P<activation_key>\w+)/$', account_view.email_activate, name='email_activate'),
    url(r'^(?P<id>\w+)/$', account_view.user, name='user'),
    url(r'^setting/info/$', account_view.getInfo, name='getInfo'),
    url(r'^setting/avatar/$', account_view.getAvatar, name='getAvatar'),
    url(r'^setting/uploadavatar/$', account_view.uploadAvatar, name='uploadAvatar'),
    url(r'^setting/saveavatar/$', account_view.saveavatar, name='saveavatar'),
    url(r'^setting/security/$', account_view.getSecurity, name='getSecurity'),
]