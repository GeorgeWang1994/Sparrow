from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import FollowTag, Follow
from account.models import User
from tag.models import Tag
from notification.models import NotificaitonType, Notificaiton, createNotification
import json, logging

logging = logging.getLogger('follow.views')


@login_required()
def follow(request):
    try:
        if request.method == 'POST':
            follow_id = request.POST['follow_id']
            followee = User.objects.get(pk=follow_id)
            if not Follow.objects.filter(followee=followee, follower=request.user).exists():
                follow = Follow.objects.create(followee=followee, follower=request.user)
                follow.save()

                notification = Notificaiton.objects.create( object_id=follow_id, notifier=request.user,
                                                            notifiee=followee, type = NotificaitonType.FOLLOW.value)

                createNotification(notification)

                data = {'status': '111000'}
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = {'status': '011002'}
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '011000'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def unfollow(request):
    try:
        if request.method == 'POST':
            follow_id = request.POST['follow_id']
            followee = User.objects.get(pk=follow_id)
            Follow.objects.filter(followee=followee, follower=request.user).delete()
            data = {'status': '111001'}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '011001'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def follow_tag(request):
    try:
        if request.method == 'POST':
            tag_id = request.POST['tag_id']
            tag = Tag.objects.get(pk=tag_id)
            if not FollowTag.objects.filter(tag=tag, follower=request.user).exists():
                FollowTag.objects.create(tag=tag, follower=request.user)
                data = {'status': '112000'}
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '011001'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def unfollow_tag(request):
    try:
        if request.method == 'POST':
            tag_id = request.POST['tag_id']
            tag = Tag.objects.get(pk=tag_id)
            FollowTag.objects.filter(tag=tag, follower=request.user).delete()
            data = {'status': '112001'}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '011001'}
        return HttpResponse(json.dumps(data), content_type="application/json")