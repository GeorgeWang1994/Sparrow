from django.db import models
from django.utils import timezone
from tag.models import Tag
from account.models import User


# 一个Album里可以有多个Photo，多个Tag
class Album (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    author = models.ForeignKey(User, related_name='album_author', on_delete=models.CASCADE)  # 作者
    time = models.DateTimeField(default=timezone.now)
    lasttime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, default='New Album')
    content = models.CharField(max_length=200, blank=True)
    visible_status = models.IntegerField(default=1)  # 状态，是否可见
    comment_status = models.IntegerField(default=1)  # 评论状态，是否允许评论
    pwd = models.CharField(max_length=100, blank=True)  # 密码
    like_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)


class Photo (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    url = models.URLField(max_length=100, blank=True)
    time = models.DateTimeField(default=timezone.now)
    desc = models.CharField(max_length=200, blank=True, null=True)
    photos = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE, null=True)