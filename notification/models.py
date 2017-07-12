from django.db import models
from django.db.models import Q, F
from django.utils import timezone
from account.models import User
from home.models import EventType
from enum import IntEnum


class NotificaitonType(IntEnum):
    UNKOWN = 1,
    POST_COMMENT = 2, # 文章的回复
    ALBUM_COMMENT = 3, # 相册的回复
    REPLY = 4, # 评论的回复
    LIKE = 6,
    FOLLOW = 8,
    SYSTEM = 9,


class ReadingStausType(IntEnum):
    READED = 0,
    UNREAD = 1,


class Notificaiton(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField(default=NotificaitonType.UNKOWN.value)
    object_id = models.CharField(max_length=20)
    object_type = models.IntegerField(default=0)
    object_title = models.CharField(max_length=100)  # 标题
    notifier = models.ForeignKey(User, related_name='notifier', on_delete=models.CASCADE)  # 通知者
    notifiee = models.ForeignKey(User, related_name='notifiee', on_delete=models.CASCADE)  # 被通知者
    status = models.IntegerField(default=ReadingStausType.UNREAD.value)  # 1为未读，0为已读
    time = models.DateTimeField(default=timezone.now)  # 评论时间

    @staticmethod
    def getNotificaitonsCount(user_id):
        post_query = Q(object_type=EventType.POST.value, type=NotificaitonType.POST_COMMENT.value)
        album_query = Q(object_type=EventType.ALBUM.value, type=NotificaitonType.ALBUM_COMMENT.value)
        recomment_query = Q(type=NotificaitonType.REPLY)
        # 评论
        comments_cnt = Notificaiton.objects.filter(post_query or album_query or recomment_query,
                                               notifiee__id=user_id,
                                               status=ReadingStausType.UNREAD.value).exclude(Q(notifier__id=0) and Q(notifier__id=user_id)).count()

        # 喜欢
        likes_cnt = Notificaiton.objects.filter(type=NotificaitonType.LIKE.value,
                                            notifiee__id=user_id,status=ReadingStausType.UNREAD.value).exclude(Q(notifier__id=0) and Q(notifier__id=user_id)).count()

        # 关注
        follows_cnt = Notificaiton.objects.filter(type=NotificaitonType.FOLLOW.value,
                                            notifiee__id=user_id,
                                            status=ReadingStausType.UNREAD.value).exclude(Q(notifier__id=0) and Q(notifier__id=user_id)).count()

        # 系统消息，由管理员来进行通知
        systems_cnt = Notificaiton.objects.filter(type=NotificaitonType.SYSTEM.value,
                                              notifier__id=0,
                                              notifiee__id=user_id,
                                              status=ReadingStausType.UNREAD.value).count()

        return {"comments_cnt": comments_cnt, "likes_cnt": likes_cnt,
                "follows_cnt": follows_cnt, "systems_cnt": systems_cnt}

    @staticmethod
    def getComments(user_id):
        post_query = Q(object_type=EventType.POST.value, type=NotificaitonType.POST_COMMENT.value)
        album_query = Q(object_type=EventType.ALBUM.value, type=NotificaitonType.ALBUM_COMMENT.value)
        recomment_query = Q(type=NotificaitonType.REPLY.value)
        # 评论
        comments = Notificaiton.objects.filter(post_query or album_query or recomment_query,
                                               notifiee__id=user_id).exclude(Q(notifier__id=0) and Q(notifier__id=user_id)).order_by('-time')
        unread_comments = [x for x in comments.filter(status=ReadingStausType.UNREAD.value).order_by('time')]
        readed_comments = [x for x in comments.filter(status=ReadingStausType.READED.value).order_by('time')]
        return {"comments": comments, "unread_comments": unread_comments, "readed_comments": readed_comments}

    @staticmethod
    def getLikes(user_id):
        # 喜欢
        likes = Notificaiton.objects.filter(type=NotificaitonType.LIKE.value,
                                            notifiee__id=user_id).exclude(Q(notifier__id=0) and Q(notifier__id=user_id)).order_by('-time').all()
        unread_likes = [x for x in likes.filter(status=ReadingStausType.UNREAD.value).order_by('time').all()]
        readed_likes = [x for x in likes.filter(status=ReadingStausType.READED.value).order_by('time').all()]

        return {"likes": likes, "unread_likes": unread_likes, "readed_likes": readed_likes}

    @staticmethod
    def getFollows(user_id):
        follows = Notificaiton.objects.filter(type=NotificaitonType.FOLLOW.value,
                                              notifiee__id=user_id).exclude(notifier__id=0).order_by('-time')
        unread_follows = [x for x in follows.filter(status=ReadingStausType.UNREAD.value).order_by('time')]
        readed_follows = [x for x in follows.filter(status=ReadingStausType.READED.value).order_by('time')]
        return {"follows": follows, "unread_follows": unread_follows, "readed_follows": readed_follows}

    @staticmethod
    def getSystems(user_id):
        # 系统消息，由管理员来进行通知
        systems = Notificaiton.objects.filter(type=NotificaitonType.SYSTEM.value,
                                              notifier__id=0,
                                              notifiee__id=user_id).order_by('-time')
        unread_systems = [x for x in systems.filter(status=ReadingStausType.UNREAD.value).order_by('time')]
        readed_systems = [x for x in systems.filter(status=ReadingStausType.READED.value).order_by('time')]
        return {"systems": systems, "unread_systems": unread_systems, "readed_systems": readed_systems}


def createNotification(obj, **kwargs):
    for key, val in kwargs.items():
        obj[key] = val
    obj.save()

def updateNotificaitonRread(type, user_id):
    if type == NotificaitonType.LIKE.value:
        Notificaiton.objects.filter(type=NotificaitonType.LIKE.value,
                                notifiee__id=user_id, status=ReadingStausType.UNREAD.value).exclude(
        Q(notifier__id=0) and Q(notifier__id=user_id)).update(status=0)
    elif type == NotificaitonType.POST_COMMENT.value or NotificaitonType.ALBUM_COMMENT.value or NotificaitonType.REPLY.value:
        post_query = Q(object_type=EventType.POST.value, type=NotificaitonType.POST_COMMENT.value)
        album_query = Q(object_type=EventType.ALBUM.value, type=NotificaitonType.ALBUM_COMMENT.value)
        recomment_query = Q(type=NotificaitonType.REPLY)
        Notificaiton.objects.filter(post_query or album_query or recomment_query,
                                    notifiee__id=user_id,
                                    status=ReadingStausType.UNREAD.value).exclude(
            Q(notifier__id=0) and Q(notifier__id=user_id)).update(status=0)
    elif NotificaitonType.FOLLOW.value:
        Notificaiton.objects.filter(type=NotificaitonType.FOLLOW.value,
                                    notifiee__id=user_id,
                                    status=ReadingStausType.UNREAD.value).exclude(
            Q(notifier__id=0) and Q(notifier__id=user_id)).update(status=0)
    elif NotificaitonType.SYSTEM.value:
        Notificaiton.objects.filter(type=NotificaitonType.SYSTEM.value,
                                    notifier__id=0,
                                    notifiee__id=user_id,
                                    status=ReadingStausType.UNREAD.value).update(status=0)
