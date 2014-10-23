# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0022_grumbl_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grumbl',
            name='picture',
            field=models.ImageField(null=b'True', upload_to=b'grumbl-pics', blank=b'True'),
        ),
    ]
