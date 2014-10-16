# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumbl',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='grumbl',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='grumbl',
            name='pub_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
