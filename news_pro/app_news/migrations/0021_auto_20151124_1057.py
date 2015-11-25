# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0020_auto_20151124_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internettime',
            name='visits',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
