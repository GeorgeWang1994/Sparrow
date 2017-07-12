from django.shortcuts import render, HttpResponse
from django.db.models import Count
from home.models import Event
from tag.models import Tag
from account.models import User


def index(request):
    tags = Tag.objects.annotate(num_event=Count('event')).order_by('num_event')[0:8]
    events = Event.objects.order_by('-like_count', '-share_count', '-comment_count', '-time')
    users = User.objects.annotate(num_like=Count('event_author__like_count'),
                                  num_share=Count('event_author__share_count'),
                                  num_comment=Count('event_author__comment_count'), num_event=Count('event_author')). \
                order_by('-num_like', '-num_share', '-num_comment', '-num_event')[0:8]
    return render(request, 'explore.html', locals())