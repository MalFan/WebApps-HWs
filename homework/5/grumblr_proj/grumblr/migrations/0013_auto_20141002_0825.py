# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_grumbl_dislike_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grumbl',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='grumbl',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='num_grumbls',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default=b'/static/img/user_default.png', upload_to=b'profile-photos'),
            preserve_default=True,
        ),
    ]
