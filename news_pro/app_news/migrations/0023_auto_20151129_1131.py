# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0022_auto_20151128_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internettime',
            name='visits',
            field=models.FloatField(default=0.0, null=True),
            preserve_default=True,
        ),
    ]
