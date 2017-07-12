from django.db import models
from django.utils import timezone
from account.models import User
from post.models import Post
from album.models import Album, Photo


class Like (models.Model):
    liker = models.ForeignKey(User, related_name='liker', on_delete=models.CASCADE)
    liking_id = models.CharField(max_length=20, null=False)  # 事件ID
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.liker.username + ' like ' + self.like_post.title