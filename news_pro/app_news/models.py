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
from datetime import datetime, timedelta
from pytz import timezone


from django.db import models
from django.db.models import Sum


def get_today_visits(date):
    try:
        page = urllib2.urlopen('http://www.liveinternet.ru/stat/ua/media/index.html?lang=en&date=%s-%s-%s' %
                               (date.year, date.month, date.day)).read()
        soup = BeautifulSoup(page)
        soup.prettify()

        #Get today views count
        pageviews = soup.find(text="Pageviews")
        b_tag = pageviews.parent
        td_tag = b_tag.parent
        visits_td = td_tag.findNext('td')

        #Get today date
        tr_tag = td_tag.parent.findPrevious('tr')
        td =  tr_tag.findAll('td')[1]
        date_for_visits = datetime.strptime(td.text, '%A, %d of %B')

        #Check if date in args equal today date on site
        if date_for_visits.month == date.month and date_for_visits.day == date.day:
            return int(visits_td.contents[0].replace(',', ''))
        else:
            return False
    except Exception as e:
        print e


class InternetTime(models.Model):

    minute = 100000.0

    date = models.DateField()
    visits = models.FloatField(null=True)

    @classmethod
    def get_internet_time(cls):
        moscow_time = datetime.now(timezone('Europe/Moscow')).date()
        all_visits = InternetTime.objects.filter(date__lt=moscow_time).\
                     aggregate(Sum('visits'))['visits__sum'] or .0
        today_visits = get_today_visits(moscow_time)
        if today_visits:
            stored_visits = InternetTime.objects.get_or_create(
                            date=moscow_time)[0]
            stored_visits.visits = today_visits/cls.minute
            stored_visits.save()
        else:
            print 'Wrong day'
        print "Moscow time ",datetime.now(timezone('Europe/Moscow')).date()
        print "Date now ", datetime.now().date()
        print "Today visits ", today_visits
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
