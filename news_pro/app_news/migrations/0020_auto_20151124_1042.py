# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0019_auto_20151123_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statisticarticle',
            name='order',
        ),
        migrations.AddField(
            model_name='statisticarticle',
            name='datetime',
            field=models.DateTimeField(default=datetime.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statisticarticle',
            name='internet_time',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(null=True, choices=[(1, b'pravda.com.ua'), (2, b'blog')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internettime',
            name='visits',
            field=models.FloatField(),
            preserve_default=True,
        ),
    ]
