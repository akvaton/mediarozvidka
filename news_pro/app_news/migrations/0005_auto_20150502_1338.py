# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0004_articlemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='datetime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
