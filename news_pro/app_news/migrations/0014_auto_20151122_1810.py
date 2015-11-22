# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0013_auto_20151122_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='internet_time',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
