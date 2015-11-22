#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    news_pro.app_news.models
    ~~~~~~~~~

    :copyright: (c) 2015 by vZ.
"""

__author__ = 'vZ'
__date__ = '21.11.2015'

from django.db import models


class ArticleModel(models.Model):
    '''
    Model for agregate article from news source.
    '''
    SOURCE_TYPE_OPTIONS = (('1', 'pravda.com.ua'),
                           ('2', 'blog'))

    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.TimeField(blank=True)
    source = models.IntegerField(choices=SOURCE_TYPE_OPTIONS)
    attendance = models.PositiveIntegerField(
        u'Відвідуваність новини', blank=True, null=True
    )
    shares_fb_total = models.PositiveIntegerField(
        u"Поширюваність новини у FB ", default=0
    )
    shares_vk_total = models.PositiveIntegerField(
        u'Поширюваність новини у VK', default=0
    )

    def __unicode__(self):
        return self.title or u''


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
    attendance = models.PositiveIntegerField(
        u'Відвідуваність новини', blank=True, null=True
    )
    shares_fb = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у FB', default=0
    )
    shares_vk = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у VK', default=0
    )


    def __unicode__(self):
        return self.article.title
