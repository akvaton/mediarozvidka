# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0018_remove_statisticarticle_shares_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='internet_time',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
