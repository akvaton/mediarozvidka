# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0023_auto_20151129_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticarticle',
            name='shares_twitter',
            field=models.PositiveIntegerField(default=0, verbose_name='\u041f\u043e\u0448\u0438\u0440\u044e\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438 \u0443 \u0446\u0435\u0439 \u0447\u0430\u0441 \u0443 Twitter'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(null=True, choices=[(1, b'pravda.com.ua'), (2, b'site_ua'), (3, b'NewYork times')]),
            preserve_default=True,
        ),
    ]
