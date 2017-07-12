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
from rest_framework import routers, serializers, viewsets
from . import views as rest_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'group', rest_views.GroupViewSet)
router.register(r'album', rest_views.AlbumViewSet, 'album')
router.register(r'photo', rest_views.PhotoViewSet)
router.register(r'comment', rest_views.CommentViewSet, 'comment')
router.register(r'post', rest_views.PostViewSet, 'post')
router.register(r'tag', rest_views.TagViewSet)
router.register(r'notification', rest_views.NotificationViewSet)
router.register(r'users', rest_views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]