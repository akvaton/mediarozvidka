#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    an.items
    ~~~~~~~~~

    :copyright: (c) 2015 by dorosh.
"""

__author__ = 'dorosh'
__date__ = '11.06.2015'

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from app_news.models import NewsModel, ArticleModel, StatisticArticle


class ArticleItem(DjangoItem):
    django_model= ArticleModel


class NewsItem(DjangoItem):
    django_model = NewsModel


class StatisticArticleItem(DjangoItem):
    django_model= StatisticArticle
