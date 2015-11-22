# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0014_auto_20151122_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlemodel',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='shares_fb_total',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='shares_vk_total',
        ),
    ]
