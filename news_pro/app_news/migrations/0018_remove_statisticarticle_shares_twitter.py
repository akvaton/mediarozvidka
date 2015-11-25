# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0017_statisticarticle_shares_twitter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statisticarticle',
            name='shares_twitter',
        ),
    ]
