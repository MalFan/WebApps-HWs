# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0010_auto_20141001_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=42)),
                ('pub_time', models.DateTimeField(auto_now_add=True)),
                ('grumbl', models.ForeignKey(to='grumblr.Grumbl')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='grumblcomment',
            name='grumbl',
        ),
        migrations.RemoveField(
            model_name='grumblcomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='GrumblComment',
        ),
    ]
