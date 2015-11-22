# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0011_auto_20151120_1202'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewsModel',
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(default=1, choices=[(b'1', b'pravda.com.ua'), (b'2', b'blog')]),
            preserve_default=False,
        ),
    ]
