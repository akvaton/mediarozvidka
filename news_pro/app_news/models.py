#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    news_pro.app_news.models
    ~~~~~~~~~

    :copyright: (c) 2015 by vZ.
"""

__author__ = 'vZ'
__date__ = '21.11.2015'

from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import datetime

from django.db import models
from django.db.models import Sum


def get_today_visits():
    try:
        page = urllib2.urlopen('http://www.liveinternet.ru/stat/ua/media/index.html?lang=en').read()
        soup = BeautifulSoup(page)
        soup.prettify()
        pageviews = soup.find(text="Pageviews")
        b_tag = pageviews.parent
        td_tag = b_tag.parent
        next_td_tag = td_tag.findNext('td')
        return int(next_td_tag.contents[0].replace(',', ''))
    except Exception as e:
        print e


class InternetTime(models.Model):

    minute = 100000.0

    date = models.DateField(auto_now_add=True)
    visits = models.FloatField(null=True)

    @classmethod
    def get_internet_time(cls):
        all_visits = InternetTime.objects.filter(date__lt=datetime.today()).\
                     aggregate(Sum('visits'))['visits__sum'] or .0
        today_visits = get_today_visits()
        a = InternetTime.objects.get_or_create(date=datetime.today())[0]
        a.visits = today_visits/cls.minute
        a.save()
        return all_visits + float(today_visits)/cls.minute

    def __unicode__(self):
        return u'%s' % self.date


class ArticleModel(models.Model):
    """
    Model for agregate article from news source.
    """
    SOURCE_TYPE_OPTIONS = ((1, 'pravda.com.ua'),
                           (2, 'blog'))

    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.FloatField(default=0)
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

    @property
    def source_name(self):
        return dict(self.SOURCE_TYPE_OPTIONS)[self.source]

    def __unicode__(self):
        return self.title or u''


class StatisticArticle(models.Model):
    """
    Model for agregate statistics from article
    """
    article = models.ForeignKey(
        ArticleModel, verbose_name=u'Новина'
    )
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.FloatField(default=0)
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
