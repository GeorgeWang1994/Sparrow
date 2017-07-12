from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Tag
from account.models import User
from follow.models import FollowTag
from home.models import Event


def getTag(request, id):
    tag = get_object_or_404(Tag, id=id)

    # 查找对应标签的所有文章，并且进行排序
    feeds = Event.objects.filter(tags__id=id).order_by('-like_count', '-share_count', '-comment_count', '-time')

    # 查找对应标签的所有文章的作者，并且进行排序
    users = User.objects.annotate(like_count=Count('event_author'))

    if request.user.is_authenticated:
        try:
            FollowTag.objects.get(follower=request.user)
            isInterest = True
        except FollowTag.DoesNotExist:
            isInterest = False
    return render(request, 'tag/index.html', locals())