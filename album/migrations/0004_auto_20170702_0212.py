# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-02 02:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20170626_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='content',
            new_name='desc',
        ),
    ]
