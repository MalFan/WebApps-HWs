# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0017_auto_20141002_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_list', models.ManyToManyField(related_name=b'block_list', to=settings.AUTH_USER_MODEL)),
                ('follow_list', models.ManyToManyField(related_name=b'follow_list', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='grumbl',
            name='dislike_list',
            field=models.ManyToManyField(related_name=b'dislike_list', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grumbl',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
