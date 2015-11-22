#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    news_pro.app_news.admin
    ~~~~~~~~~

    :copyright: (c) 2015 by dorosh.
"""

__author__ = 'dorosh'
__date__ = '11.06.2015'

import datetime
from django.contrib import admin

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from .models import ArticleModel, StatisticArticle



class ArticleResource(resources.ModelResource):

    class Meta:
        model = ArticleModel


@admin.register(ArticleModel)
class ArticleModelAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource


class StatisticArticleResource(resources.ModelResource):
    article__title = fields.Field(column_name=u'Назва новини', attribute='article__title')
    article__datetime = fields.Field(column_name=u'Астрономічні час і дата появи на сайті', attribute='article__datetime')
    order = fields.Field(column_name=u'Час, який минув від моменту появи новини(hh:mm)')
    attendance = fields.Field(column_name=u'Відвідуваність новини', attribute='attendance')
    shares_fb = fields.Field(column_name=u'Поширюваність новини у цей час у Фейсбуку', attribute='shares_fb')
    shares_vk = fields.Field(column_name=u'Поширюваність новини у цей час у ВКонтакті', attribute='shares_vk')

    class Meta:
        model = StatisticArticle
        fields = ('article', 'article__title', 'article__datetime', 'order', 'site_order', 'attendance',
                  'shares_fb', 'shares_vk')
        export_order = ('article', 'article__title', 'article__datetime', 'order', 'site_order', 'attendance',
                        'shares_fb', 'shares_vk')

    def dehydrate_order(self, statistic_article):
        td = datetime.timedelta(seconds=statistic_article.order)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{}:{:02d}'.format(int(hours), int(minutes))


@admin.register(StatisticArticle)
class StatisticArticleAdmin(ImportExportModelAdmin):
    resource_class = StatisticArticleResource
