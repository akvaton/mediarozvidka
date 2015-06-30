# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0008_articlemodel_shares_fb_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='comments',
            field=models.PositiveIntegerField(default=0, verbose_name='\u041a\u043e\u043c\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
