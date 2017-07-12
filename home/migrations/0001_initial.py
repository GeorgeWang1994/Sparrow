# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 08:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '0001_initial'),
        ('album', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('object_type', models.IntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('lasttime', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='New Post', max_length=100)),
                ('summary', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField()),
                ('visible_status', models.IntegerField(default=1)),
                ('comment_status', models.IntegerField(default=1)),
                ('pwd', models.CharField(blank=True, max_length=100)),
                ('like_count', models.IntegerField(default=0)),
                ('share_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('cover', models.URLField(default='http://upload-images.jianshu.io/upload_images/3332049-05db6a6ce0d71f47.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240')),
                ('event_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_author', to=settings.AUTH_USER_MODEL)),
                ('photos', models.ManyToManyField(to='album.Photo')),
                ('tags', models.ManyToManyField(to='tag.Tag')),
            ],
        ),
    ]
