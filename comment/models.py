from django.db import models
from account.models import User


class Comment (models.Model):
    id = models.AutoField(primary_key=True)
    object_type = models.IntegerField()  # 评论的文章类型，可能是文章，相册等等
    object_id = models.CharField(max_length=20, null=False)  # 评论的主体id
    comment_author = models.ForeignKey(User, related_name='comment_author', null=True, on_delete=models.CASCADE)  # 作者
    time = models.DateTimeField(auto_now_add=True)  # 评论时间
    content = models.TextField()  # 评论内容
    parent = models.IntegerField(default=0)  # 父级评论id
    parent_author = models.ForeignKey(User, related_name='parent_author', on_delete=models.CASCADE, null=True)  # 文章类型作者
