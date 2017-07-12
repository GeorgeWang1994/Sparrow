# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 08:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        ('album', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('like_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_album', to='album.Album')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album_liker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('like_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_post', to='post.Post')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_liker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
