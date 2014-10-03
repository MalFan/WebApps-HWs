# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0018_auto_20141002_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='block_list',
            field=models.ManyToManyField(related_name=b'block_list', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='follow_list',
            field=models.ManyToManyField(related_name=b'follow_list', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
