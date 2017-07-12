# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-02 01:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170626_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_nohtml',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]