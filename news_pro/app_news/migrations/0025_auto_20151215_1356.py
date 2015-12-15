# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0024_auto_20151208_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(null=True, choices=[(1, b'Pravda.com.ua'), (2, b'Site.ua'), (3, b'NewYork times')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internettime',
            name='visits',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
