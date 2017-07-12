from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from home.models import EventType
from post.models import Post
from album.models import Album
from notification.models import NotificaitonType, Notificaiton, createNotification
from .models import Like
import logging, json

logging = logging.getLogger('like.views')


@login_required()
def like(request):
    try:
        if request.method == 'POST':
            object_type = int(request.POST['object_type'])
            object_id = request.POST['object_id']

            if object_type == EventType.POST.value:
                post = Post.objects.get(pk=object_id)
                if not Like.objects.filter(liker=request.user, liking_id=post.id).exists():
                    like = Like.objects.create(liker=request.user, liking_id=post.id)
                    like.save()
                    Post.objects.filter(pk=object_id).update(like_count=F('like_count') + 1)

                    notification = Notificaiton.objects.create(object_id=object_id, type = NotificaitonType.LIKE.value,
                                                               object_type=EventType.POST.value, object_title = post.title,
                                                               notifiee=post.author,notifier=request.user)

                    createNotification(notification)

                    data = {'status': '116000'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
            elif object_type == EventType.ALBUM.value:
                album = Album.objects.get(pk=object_id)
                if not Like.objects.filter(liker=request.user, liking_id=album.id).exists():
                    like = Like.objects.create(liker=request.user, liking_id=album.id)
                    like.save()
                    Album.objects.filter(pk=object_id).update(like_count=F('like_count') + 1)

                    notification = Notificaiton.objects.create(object_id=object_id,
                                                               type=NotificaitonType.LIKE.value,
                                                               object_type=EventType.ALBUM.value,
                                                               object_title=album.title,
                                                               notifiee=album.author, notifier=request.user)

                    createNotification(notification)

                    data = {'status': '116002'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '015000'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def unlike(request):
    try:
        if request.method == 'POST':
            object_type = int(request.POST['object_type'])
            object_id = request.POST['object_id']

            if object_type == EventType.POST.value:
                post = Post.objects.get(pk=object_id)
                Like.objects.filter(liker=request.user, liking_id=post.id).delete()
                data = {'status': '116001'}
                Post.objects.filter(pk=object_id).update(like_count=F('like_count') - 1)
                return HttpResponse(json.dumps(data), content_type="application/json")
            elif object_type == EventType.ALBUM.value:
                post = Album.objects.get(pk=object_id)
                Like.objects.filter(liker=request.user, liking_id=post.id).delete()
                Album.objects.filter(pk=object_id).update(like_count=F('like_count') - 1)
                data = {'status': '116003'}
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
        data = {'status': '015001'}
        return HttpResponse(json.dumps(data), content_type="application/json")