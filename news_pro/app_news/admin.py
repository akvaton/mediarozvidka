#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    news_pro.app_news.admin
    ~~~~~~~~~

    :copyright: (c) 2015 by dorosh.
"""

__author__ = 'dorosh'
__date__ = '11.06.2015'

from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import NewsModel, ArticleModel, StatisticArticle


class NewsResource(resources.ModelResource):

    class Meta:
        model = NewsModel


@admin.register(NewsModel)
class NewsModelAdmin(ImportExportModelAdmin):
    resource_class = NewsResource


class ArticleResource(resources.ModelResource):

    class Meta:
        model = ArticleModel


@admin.register(ArticleModel)
class ArticleModelAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource


class StatisticArticleResource(resources.ModelResource):

    class Meta:
        model = StatisticArticle


@admin.register(StatisticArticle)
class StatisticArticleAdmin(ImportExportModelAdmin):
    resource_class = StatisticArticleResource
