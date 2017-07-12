from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import User
from follow.models import Follow
from tag.models import Tag
from .models import Event, getFeeds


@login_required()
def home(request):
    follower_count = Follow.objects.filter(followee=request.user).count()  # 粉丝
    following_count = Follow.objects.filter(follower=request.user).count()  # 关注的人
    all_post_count = Event.objects.filter(author=request.user).count()  # 所有文章
    users = User.objects.annotate(num_like=Count('event_author__like_count'), num_share=Count('event_author__share_count'), num_comment=Count('event_author__comment_count'), num_event=Count('event_author')).\
                order_by('-num_like', '-num_share', '-num_comment', '-num_event')[0:5]
    tags = Tag.objects.annotate(num_event=Count('event')).order_by('num_event')[0:5]
    feeds = getFeeds(request.user.id)

    # per page show 25 item
    paginator = Paginator(feeds, 25)
    page_idx = int(request.GET.get('page', 1))
    try:
        feeds = paginator.page(page_idx)
    except PageNotAnInteger:
        feeds = paginator.page(1)
    except EmptyPage:
        feeds = paginator.page(paginator.num_pages)

    return render(request, 'index.html', locals())


def welcome(request):
    return render(request, 'welcome.html', locals())


def explore(request):
    return render(request, 'explore.html', locals())


# 粉丝
@login_required()
def follower(request):
    if request.user.is_authenticated():
        # 粉丝的被关注者是自己
        followers = User.objects.filter(follower__followee=request.user)
    return render(request, 'follower.html', locals())


# 我的关注
@login_required()
def following(request):
    if request.user.is_authenticated():
        # 被关注的人的粉丝是自己
        followings = User.objects.filter(followee__follower=request.user)
    return render(request, 'following.html', locals())