from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import user_can_authenticate
from .models import Notificaiton, NotificaitonType, updateNotificaitonRread


@login_required()
def comments(request):
    if user_can_authenticate(request.user):
        dict = Notificaiton.getComments(request.user.id)
        count = Notificaiton.getNotificaitonsCount(request.user.id)
        type = {"POST_COMMENT": NotificaitonType.POST_COMMENT.value,
                "ALBUM_COMMENT": NotificaitonType.ALBUM_COMMENT.value,
                "": NotificaitonType.REPLY.value}
        if count["comments_cnt"] > 0:
            updateNotificaitonRread(NotificaitonType.POST_COMMENT.value, request.user.id)
        return render(request, 'notification/comment.html', locals())
    return render(request, '404.html')


@login_required()
def likes(request):
    if user_can_authenticate(request.user):
        dict = Notificaiton.getLikes(request.user.id)
        count = Notificaiton.getNotificaitonsCount(request.user.id)
        type = NotificaitonType.LIKE.value
        if count["likes_cnt"] > 0:
            updateNotificaitonRread(type, request.user.id)
        return render(request, 'notification/like.html', locals())
    return render(request, '404.html')


@login_required()
def systems(request):
    if user_can_authenticate(request.user):
        dict = Notificaiton.getSystems(request.user.id)
        count = Notificaiton.getNotificaitonsCount(request.user.id)
        type = NotificaitonType.SYSTEM.value
        if count["systems_cnt"] > 0:
            updateNotificaitonRread(type, request.user.id)
        return render(request, 'notification/system.html', locals())
    return render(request, '404.html')


@login_required()
def follows(request):
    if user_can_authenticate(request.user):
        dict = Notificaiton.getFollows(request.user.id)
        count = Notificaiton.getNotificaitonsCount(request.user.id)
        type = NotificaitonType.FOLLOW.value
        if count["follows_cnt"] > 0:
            updateNotificaitonRread(type, request.user.id)
        return render(request, 'notification/follow.html', locals())
    return render(request, '404.html')