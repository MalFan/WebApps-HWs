# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0020_auto_20141018_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationship',
            name='block_list',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='follow_list',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='user',
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
        migrations.AddField(
            model_name='profile',
            name='block_list',
            field=models.ManyToManyField(related_name=b'block_list', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='follow_list',
            field=models.ManyToManyField(related_name=b'follow_list', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
