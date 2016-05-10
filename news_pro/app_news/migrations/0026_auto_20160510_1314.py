# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0025_auto_20151215_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticarticle',
            name='fb_total',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0417\u0430\u0433\u0430\u043b\u044c\u043d\u0435 \u043f\u043e\u0448\u0438\u0440\u044e\u0432\u0430\u043d\u043d\u044f \u043d\u043e\u0432\u0438\u043d\u0438 \u0443 \u0446\u0435\u0439 \u0447\u0430\u0441 \u0443 FB'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(null=True, choices=[(1, b'Pravda article'), (2, b'Site.ua'), (3, b'NewYork times'), (4, b'Pravda news')]),
            preserve_default=True,
        ),
    ]
