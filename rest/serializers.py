from django.contrib.auth.models import Group
from rest_framework import serializers
from account.models import *
from album.models import *
from comment.models import *
from notification.models import *
from post.models import *
from tag.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest:user-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rest:group-detail")

    class Meta:
        model = Group
        fields = ('url', 'name')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'time',  'cover')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()
    tags = serializers.HyperlinkedRelatedField(
        view_name='rest:tag-detail',
        many=True,
        read_only=True
    )
    photos = serializers.HyperlinkedRelatedField(
        view_name='rest:photo-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = Album
        ordering = ['-id']
        fields = ('id', 'author', 'title', 'content', 'tags', 'photos', 'time')


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'url', 'desc', 'time')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    comment_author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'object_id', 'object_type', 'comment_author')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'author', 'time',  'content', 'title', 'summary')


class NotificaitonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notificaiton
        fields = ('id', 'type', 'object_id', 'object_type', 'time')