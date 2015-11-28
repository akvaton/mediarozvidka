# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0021_auto_20151124_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internettime',
            name='date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
