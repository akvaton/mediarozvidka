# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_news.models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0005_auto_20150502_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.URLField(verbose_name=app_news.models.ArticleModel)),
                ('order', models.PositiveIntegerField(verbose_name='\u0427\u0430\u0441 \u044f\u043a\u0438\u0439 \u043c\u0438\u043d\u0443\u0432 \u0432\u0456\u0434 \u043c\u043e\u043c\u0435\u043d\u0442\u0443 \u043f\u043e\u044f\u0432\u0438 \u043d\u043e\u0432\u0438\u043d\u0438')),
                ('site_order', models.PositiveIntegerField(null=True, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u043d\u044f \u043d\u043e\u0432\u0438\u043d\u0438 \u043d\u0430 \u0441\u0430\u0439\u0442\u0456', blank=True)),
                ('attendance', models.PositiveIntegerField(null=True, verbose_name='\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438', blank=True)),
                ('attendance_index_site', models.PositiveIntegerField(null=True, verbose_name='\u0412\u0456\u0434\u0432\u0456\u0434\u0443\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u0433\u043e\u043b\u043e\u0432\u043d\u043e\u0457 \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0438', blank=True)),
                ('shares_fb', models.PositiveIntegerField(verbose_name='\u041f\u043e\u0448\u0438\u0440\u044e\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438')),
                ('comments', models.PositiveIntegerField(verbose_name='\u041a\u043e\u043c\u0435\u043d\u0442\u043e\u0432\u0430\u043d\u0456\u0441\u0442\u044c \u043d\u043e\u0432\u0438\u043d\u0438')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='articlemodel',
            name='shares',
        ),
    ]
