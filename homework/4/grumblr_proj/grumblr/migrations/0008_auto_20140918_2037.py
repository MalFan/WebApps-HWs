# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0007_profile_num_grumbls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='intro',
            field=models.CharField(default=b'What do you want to say?', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default=b'Where are you?', max_length=50),
        ),
    ]
