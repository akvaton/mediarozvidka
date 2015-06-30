# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0006_auto_20150611_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisticarticle',
            name='article',
            field=models.ForeignKey(verbose_name='\u041d\u043e\u0432\u0438\u043d\u0430', to='app_news.ArticleModel'),
            preserve_default=True,
        ),
    ]
