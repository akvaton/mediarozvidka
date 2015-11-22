# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0010_auto_20150713_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlemodel',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='statisticarticle',
            name='attendance_index_site',
        ),
        migrations.RemoveField(
            model_name='statisticarticle',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='statisticarticle',
            name='site_order',
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='attendance',
            field=models.PositiveIntegerField(null=True, verbose_name='\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='internet_time',
            field=models.TimeField(default=datetime.now, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='statisticarticle',
            name='shares_fb',
            field=models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0448\u0438\u0440\u044e\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438 \u0443 \u0446\u0435\u0439 \u0447\u0430\u0441 \u0443 FB'),
            preserve_default=True,
        ),
    ]
