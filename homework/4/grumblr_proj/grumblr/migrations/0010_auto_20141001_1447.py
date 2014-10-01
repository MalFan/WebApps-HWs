# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0009_auto_20140930_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrumblComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=42)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('grumbl', models.ForeignKey(to='grumblr.Grumbl')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='grumbl',
            name='user',
            field=models.ForeignKey(related_name=b'grumblr_of_this_grumbl', to=settings.AUTH_USER_MODEL),
        ),
    ]
