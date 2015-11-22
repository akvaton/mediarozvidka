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
from django.db.models import Sum


class InternetTime(models.Model):
    date = models.DateField(auto_now_add=True)
    visits = models.PositiveIntegerField()

    @property
    def get_internet_time(self):
        return 0

    def __unicode__(self):
        return self.date


class ArticleModel(models.Model):
    """
    Model for agregate article from news source.
    """
    SOURCE_TYPE_OPTIONS = (('1', 'pravda.com.ua'),
                           ('2', 'blog'))

    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.TimeField(blank=True, null=True)
    source = models.IntegerField(choices=SOURCE_TYPE_OPTIONS, null=True)

    @property
    def attendance(self):
        return StatisticArticle.objects.filter(article=self).\
                    aggregate(Sum('attendance'))['attendance__sum']

    @property
    def shares_fb_total(self):
       return StatisticArticle.objects.filter(article=self).\
                    aggregate(Sum('shares_fb'))['shares_fb__sum']

    @property
    def shares_vk_total(self):
        return StatisticArticle.objects.filter(article=self).\
                    aggregate(Sum('shares_vk'))['shares_vk__sum']

    def __unicode__(self):
        return self.title or u''


class StatisticArticle(models.Model):
    """
    Model for agregate statistics from article
    """
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
