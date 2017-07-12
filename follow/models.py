from django.db import models
from django.utils import timezone
from account.models import User
from tag.models import Tag


class Follow (models.Model):
    id = models.AutoField(primary_key=True)
    followee = models.ForeignKey(User, related_name='followee', on_delete=models.CASCADE)  # 被关注者
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)  # 粉丝
    time = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return self.follower.username + ' follow ' + self.followee.username


class FollowTag (models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(Tag, related_name='tag', on_delete=models.CASCADE)  # 关注的tag
    follower = models.ForeignKey(User, related_name='tag_follower', on_delete=models.CASCADE)  # 粉丝
    time = models.DateTimeField(default=timezone.now)  # 创建时间

    def __str__(self):
        return self.follower.username + ' follow ' + self.tag.name