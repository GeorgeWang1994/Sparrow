from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from .models import Comment
from home.models import EventType, Event
from post.models import Post
from album.models import Album
from notification.models import Notificaiton, NotificaitonType, createNotification
import logging, json

logger = logging.getLogger('comment.views')


@login_required()
def create(request):
    try:
        if request.method == 'POST':
            object_type = int(request.POST['object_type'])
            object_id = request.POST['object_id']
            content = request.POST['content']
            parent = int(request.POST['parent'])


            if object_type == EventType.POST.value:
                post = Post.objects.get(pk=object_id)
                comment = Comment.objects.create(object_type=object_type, object_id=post.id,
                                                 comment_author=request.user, content=content,
                                                 parent=parent)

                Post.objects.filter(pk=object_id).update(comment_count=F('comment_count')+1)

                notification = Notificaiton.objects.create(type=NotificaitonType.POST_COMMENT.value,
                                                           notifiee=post.author, notifier=request.user,
                                                           object_type=EventType.POST.value, object_title=post.title,
                                                           object_id=object_id)
            else:
                post = Album.objects.get(pk=object_id)
                comment = Comment.objects.create(object_type=object_type, object_id=post.id,
                                                 comment_author=request.user, content=content,
                                                 parent=parent)
                Album.objects.filter(pk=object_id).update(comment_count=F('comment_count')+1)

                notification = Notificaiton.objects.create(type=NotificaitonType.ALBUM_COMMENT.value,
                                                           notifiee=post.author, notifier=request.user,
                                                           object_type=EventType.ALBUM.value, object_title=post.title,
                                                           object_id=object_id)


            if parent != 0:
                parent_author = Comment.objects.get(pk=parent).comment_author
                comment.parent_author = parent_author
                notification.type = NotificaitonType.REPLY.value
                notification.notifiee = parent_author


            comment.save()

            Event.objects.filter(object_id=object_id).update(comment_count=F('comment_count') + 1)

            createNotification(notification)

            data = {'status': '108000', 'avatar':request.user.user_avatar, "author_id":request.user.id,"author_name":request.user.username}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logging.error(e)
    else:
        return render(request, 'comment/index.html', locals())