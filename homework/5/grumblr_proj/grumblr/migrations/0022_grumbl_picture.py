# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0021_auto_20141018_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='grumbl',
            name='picture',
            field=models.ImageField(null=b'True', upload_to=b'grumbl-pics'),
            preserve_default=True,
        ),
    ]
