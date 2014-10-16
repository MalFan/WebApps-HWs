# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0005_auto_20140917_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumbl',
            name='pub_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
