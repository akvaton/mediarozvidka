#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ArticleModel, StatisticArticle, InternetTime


@admin.register(ArticleModel)
class ArticleModelAdmin(ImportExportModelAdmin):
    resource_class = ArticleModel


@admin.register(InternetTime)
class ArticleModelAdmin(ImportExportModelAdmin):
    resource_class = InternetTime


@admin.register(StatisticArticle)
class StatisticArticleAdmin(ImportExportModelAdmin):
    resource_class = StatisticArticle
