# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0019_auto_20141002_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='intro',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
