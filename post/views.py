from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from tag.models import Tag
from follow.models import Follow
from home.models import Event, EventType, toAddEvent, toDelEvent, toEditEvent
from like.models import Like
from comment.models import Comment
from Sparrow.select_result import getRandomID
from pyquery import PyQuery
import json, logging

logger = logging.getLogger('post.views')


def getPost(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(object_id=id).order_by('-time')
    if request.user.is_authenticated:
        follow = Follow.objects.filter(followee=post.author, follower=request.user).exists()
        is_like = Like.objects.filter(liker=request.user, liking_id=post.id).exists()
    else:
        follow = False
        is_like = False

    return render(request, 'post/index.html', locals())


@login_required()
def newpost(request):
    try:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            doc = PyQuery(content).text()
            summary = doc[:100]
            tags = request.POST['tags'].split(' ')
            visible_status = request.POST['visible_status'],
            comment_status = request.POST['comment_status'],
            id = getRandomID()
            post = Post.objects.create(id=id, author=request.user, title=title, content=content,
                                       summary=summary, content_nohtml=doc,
                                       visible_status=int(request.POST['visible_status']),
                                       comment_status=int(request.POST['comment_status']))
            for i in tags:
                try:
                    tag = Tag.objects.get(name=i)
                except Tag.DoesNotExist:
                    id = getRandomID()
                    tag = Tag.objects.create(name=i, id=id)

                post.tags.add(tag)

            post.save()

            toAddEvent(EventType.POST, post)

            data = {'status': '105000'}
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        logger.error(e)
        data = {'status': '0'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'post/create.html', locals())


@login_required()
def delpost(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    toDelEvent(event_id=id)
    data = {'status': '105002'}
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required()
def editpost(request, id):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        summary = content[:100]
        tags = request.POST['tags'].split(' ')
        visible_status = request.POST['visible_status']
        comment_status = request.POST['comment_status']
        post = Post.objects.get(id=id)

        if post is None:
            logger.error('post is None')
            data = {'status': '0'}
            return HttpResponse(json.dumps(data), content_type="application/json")

        post.tags.clear()
        for i in tags:
            try:
                tag = Tag.objects.get(name=i)
            except Tag.DoesNotExist:
                id = getRandomID()
                tag = Tag.objects.create(name=i, id=id)
            post.tags.add(tag)

        post.save()

        Post.objects.filter(pk=id).update(title=title, content=content, summary=summary, visible_status=visible_status, comment_status=comment_status)

        # tags可能会有问题
        toEditEvent(event_id=id, title=title, content=content, summary=summary, visible_status=visible_status, comment_status=comment_status, tags=post.tags.all())

        data = {'status': '105001'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        post = Post.objects.get(id=id)
        # tags = ' '.join([i.name for i in post.tags.all()])
        return render(request, 'post/editpost.html', locals())