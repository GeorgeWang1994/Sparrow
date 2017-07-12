from django.db import models
from django.db.models import Q
from django.utils import timezone
from album.models import Album, Photo
from tag.models import Tag
from account.models import User
from post.models import Post
from enum import IntEnum
from Sparrow.select_result import getRandomID
from like.models import Like


class EventType(IntEnum):
    POST = 1,
    ALBUM = 2,


# 用作feed流
class Event(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    object_type = models.IntegerField(default=0)  # 事件类型
    object_id = models.CharField(max_length=20, null=False)
    author = models.ForeignKey(User, related_name='event_author', on_delete=models.CASCADE)  # 作者
    time = models.DateTimeField(auto_now_add=True)  # 提交时间
    lasttime = models.DateTimeField(auto_now=True)  # 最新修改时间
    title = models.CharField(max_length=100, default="New Post")  # 标题
    summary = models.CharField(max_length=200, blank=True)  # 摘抄
    content = models.TextField(blank=False, null=False)  # 提交内容
    visible_status = models.IntegerField(default=1)  # 状态，是否可见
    comment_status = models.IntegerField(default=1)  # 评论状态，是否允许评论
    pwd = models.CharField(max_length=100, blank=True)  # 密码
    like_count = models.IntegerField(default=0)  # 喜欢人数
    share_count = models.IntegerField(default=0)  # 分享人数
    comment_count = models.IntegerField(default=0)  # 评论人数
    tags = models.ManyToManyField(Tag)  # 图片
    photos = models.ManyToManyField(Photo)  # 图片
    cover = models.URLField(
        default='http://upload-images.jianshu.io/upload_images/3332049-05db6a6ce0d71f47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240')  # 封面


def getFeeds(id):
    feeds = Event.objects.filter(Q(author__id=id) or Q(author__followee__follower__id=id)).\
        order_by('-time', '-like_count', '-share_count', '-comment_count')
    for x in feeds.all():
        if Like.objects.filter(liker=x.author, liking_id=x.id).exists():
            setattr(x, 'is_like', True)
        else:
            setattr(x, 'is_like', False)
    return feeds


# 添加事件
def toAddEvent(type, obj):
    event = Event.objects.create(id=getRandomID(), object_type=type, object_id=obj.id, author=obj.author, time=obj.time, lasttime=obj.lasttime,
                                 title=obj.title, content=obj.content, visible_status=obj.visible_status,
                                 comment_status=obj.comment_status, pwd=obj.pwd, like_count=obj.like_count,
                                 share_count=obj.share_count, comment_count=obj.comment_count)
    event.tags = obj.tags.all()
    if type == EventType.POST:
        event.summary = obj.summary
        event.cover = obj.cover
    else:
        event.photos = obj.photos.all()
        event.cover = obj.photos[0]

    event.save()


# 删除事件
def toDelEvent(event_id):
    Event.objects.filter(object_id=event_id).delete()


# 更新事件
def toEditEvent(event_id, **kwargs):
    try:
        event = Event.objects.get(object_id=event_id)
        for key in list(kwargs.keys()):
            if key == 'tags':
                for tag in kwargs[key]:
                    event.tags.add(tag)
                event.save()
                kwargs.pop(key)
            elif key == 'photos':
                for photo in kwargs[key]:
                    event.photos.add(photo)
                event.save()
                kwargs.pop(key)
        Event.objects.filter(object_id=event_id).update(**kwargs)
    except Exception as e:
        print(e)