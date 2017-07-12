from django.db import models
import django.utils.timezone as timezone
from tag.models import Tag
from account.models import User


class Post (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    author = models.ForeignKey(User, related_name='post_author', on_delete=models.CASCADE)  # 作者
    time = models.DateTimeField(auto_now_add=True)  # 提交时间
    lasttime = models.DateTimeField(auto_now=True)  # 最新修改时间
    title = models.CharField(max_length=100, default="New Post")  # 标题
    summary = models.CharField(max_length=200, blank=True, default="")  # 摘抄
    content = models.TextField(blank=False, null=False)  # 提交内容
    content_nohtml = models.TextField(blank=False, default="")  # 无html内容
    visible_status = models.IntegerField(default=1)  # 状态，是否可见
    comment_status = models.IntegerField(default=1)  # 评论状态，是否允许评论
    pwd = models.CharField(max_length=100, blank=True)  # 密码
    like_count = models.IntegerField(default=0)  # 喜欢人数
    share_count = models.IntegerField(default=0)  # 分享人数
    comment_count = models.IntegerField(default=0)  # 评论人数
    tags = models.ManyToManyField(Tag)  # 标签
    cover = models.URLField(default='http://upload-images.jianshu.io/upload_images/3332049-05db6a6ce0d71f47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240')  # 封面

    def __str__(self):
        return self.title
