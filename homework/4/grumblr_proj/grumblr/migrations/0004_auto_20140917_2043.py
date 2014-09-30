# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_auto_20140917_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='intro',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
