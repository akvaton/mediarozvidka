# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0012_auto_20151122_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='source',
            field=models.IntegerField(null=True, choices=[(b'1', b'pravda.com.ua'), (b'2', b'blog')]),
            preserve_default=True,
        ),
    ]
