# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0004_auto_20140917_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]
