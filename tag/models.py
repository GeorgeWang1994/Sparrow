from django.db import models
from django.utils import timezone


class Tag (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100, blank=True)  # 标签名字
    time = models.DateTimeField(default=timezone.now)  # 标签添加时间
    cover = models.URLField(blank=True, default='http://upload.jianshu.io/collections/images/13/IMG_3003.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/240/h/240')  # 标签图片

    def __str__(self):
        return self.name