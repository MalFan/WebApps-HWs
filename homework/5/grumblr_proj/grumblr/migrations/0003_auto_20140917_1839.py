# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_auto_20140916_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
