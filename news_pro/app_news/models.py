#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    news_pro.app_news.models
    ~~~~~~~~~

    :copyright: (c) 2015 by dorosh.
"""

__author__ = 'dorosh'
__date__ = '11.06.2015'

from django.db import models


class NewsModel(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.title


class ArticleModel(models.Model):
    '''
    Model for agregate article from news source.
    '''
    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    comments = models.PositiveIntegerField(
        u'Коментованість новини', default=0
    )
    shares_fb_total = models.PositiveIntegerField(
        u"Поширюваність новини у FB ", default=0
    )
    shares_vk_total = models.PositiveIntegerField(
        u'Поширюваність новини у VK', default=0
    )

    def __unicode__(self):
        return self.title


class StatisticArticle(models.Model):
    '''
    Model for agregate statistics from article
    '''
    article = models.ForeignKey(
        ArticleModel, verbose_name=u'Новина'
    )
    order = models.PositiveIntegerField(
        u'Час який минув від моменту появи новини'
    )
    site_order = models.PositiveIntegerField(
        u'Положення новини на сайті', blank=True, null=True
    )
    attendance = models.PositiveIntegerField(
        u'Відвідуваність новини', blank=True, null=True
    )
    attendance_index_site = models.PositiveIntegerField(
        u'Відвідуваність головної сторінки', blank=True, null=True
    )
    shares_fb = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у FB'
    )
    shares_vk = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у VK', default=0
    )
    comments = models.PositiveIntegerField(
        u'Коментованість новини'
    )

    def __unicode__(self):
        return self.article.title
