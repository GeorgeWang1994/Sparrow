# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 09:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liking_id', models.CharField(max_length=20)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='albumlike',
            name='like_album',
        ),
        migrations.RemoveField(
            model_name='albumlike',
            name='liker',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='like_post',
        ),
        migrations.RemoveField(
            model_name='postlike',
            name='liker',
        ),
        migrations.DeleteModel(
            name='AlbumLike',
        ),
        migrations.DeleteModel(
            name='PostLike',
        ),
    ]
