##! /usr/bin/python
##-*- coding: utf-8 -*-
"""
    news_pro.app_news.models
    ~~~~~~~~~

    :copyright: (c) 2015 by vZ.
"""

__author__ = 'vZ'
__date__ = '21.11.2015'

import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone

from django.db import models
from django.db.models import Sum, ObjectDoesNotExist


def get_visits(date):
    try:
        page = urllib2.urlopen('http://www.liveinternet.ru/stat/ua/media/index.html?lang=en&date=%s-%s-%s' %
                               (date.year, date.month, date.day)).read()
        soup = BeautifulSoup(page)
        soup.prettify()

        # Get today views count
        pageviews = soup.find(text="Pageviews")
        b_tag = pageviews.parent
        td_tag = b_tag.parent
        visits_td = td_tag.findNext('td')

        # Get today date
        tr_tag = td_tag.parent.findPrevious('tr')
        td =  tr_tag.findAll('td')[1]
        date_for_visits = datetime.strptime(td.text, '%A, %d of %B')

        # Check if date in args equal today date on site
        if date_for_visits.month == date.month and date_for_visits.day == date.day:
            return int(visits_td.contents[0].replace(',', ''))
        else:
            return False
    except Exception as e:
        print e

#
# def get_google_searches():
#     print '*'*50
#     try:
#         # driver = webdriver.PhantomJS(executable_path='/Users/vZ/Downloads/phantomjs-2.0.0-macosx/bin/phantomjs')
#         # driver.get('http://www.internetlivestats.com/google-search-statistics/')
#         # print driver.find_element_by_class_name('innercounter')
#         opener = urllib2.build_opener()
#         # opener.addheaders.append(('Cookie', '__cfduid=d6ec5425d2e97b035e7787585d47a1fa71449646570'))
#         page = opener.open('http://pennystocks.la/internet-in-real-time/').read()
#         soup = BeautifulSoup(page)
#         soup.prettify()
#         print soup
#         # Get today views count
#         pageviews = soup.find('div',{'class':'innercounter'})
#         print pageviews
#         # b_tag = pageviews.parent
#         # td_tag = b_tag.parent
#         # visits_td = td_tag.findNext('td')
#         #
#         # # Get today date
#         # tr_tag = td_tag.parent.findPrevious('tr')
#         # td =  tr_tag.findAll('td')[1]
#         # date_for_visits = datetime.strptime(td.text, '%A, %d of %B')
#         #
#         # # Check if date in args equal today date on site
#         # if date_for_visits.month == date.month and date_for_visits.day == date.day:
#         #     return int(visits_td.contents[0].replace(',', ''))
#         # else:
#         #     return False
#     except Exception as e:
#         print e


class InternetTime(models.Model):
    """
    Model for storing total count of everyday visits to get "Internet time".
    """
    internet_minute = 100000.0

    date = models.DateField()
    visits = models.FloatField(default=.0, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.visits /= self.internet_minute
        super(InternetTime, self).save()

    @classmethod
    def get_internet_time(cls):
        moscow_time = datetime.now(timezone('Europe/Moscow')).date()
        all_visits = InternetTime.objects.filter(date__lt=moscow_time).\
            aggregate(Sum('visits'))['visits__sum'] or .0
        today_visits = get_visits(moscow_time)
        if today_visits:
            (stored_visits, cr) = InternetTime.objects.get_or_create(
                            date=moscow_time)
            stored_visits.visits = today_visits
            stored_visits.save()

            # Geting right count of yesterday visits if new day starts
            if cr:
                try:
                    yesterday = moscow_time - timedelta(days=1)
                    yesterday_visits = InternetTime.objects.get(date=yesterday)
                    yesterday_visits_on_site = get_visits(yesterday)
                    if yesterday_visits_on_site/cls.internet_minute > yesterday_visits.visits:
                        yesterday_visits.visits = yesterday_visits_on_site
                        yesterday_visits.save()
                except ObjectDoesNotExist:
                    print "There is no yesterday visits in db"
        else:
            print 'Wrong day'
        print "Moscow time ",datetime.now(timezone('Europe/Moscow')).date()
        print "Date now ", datetime.now().date()
        print "Today visits ", today_visits
        return all_visits + float(today_visits)/cls.internet_minute

    def __unicode__(self):
        return u'%s' % self.date


# class GoogleSearches(InternetTime):
#     """
#     Model for storing total count of everyday Google searches.
#     """
#     internet_minute = 100000.0
#
#     @classmethod
#     def get_internet_time(cls):
#         pass


class ArticleModel(models.Model):
    """
    Model for agregate article from news source.
    """
    SOURCE_TYPE_OPTIONS = ((1, 'pravda.com.ua'),
                           (2, 'site_ua'),
                           (3, 'NewYork times'))

    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.FloatField(default=0)
    source = models.IntegerField(choices=SOURCE_TYPE_OPTIONS, null=True)

    @property
    def attendance(self):
        att = StatisticArticle.objects.filter(article=self).last()
        if att:
            return getattr(att, 'attendance')
        else:
            return 0

    @property
    def shares_fb_total(self):
        fb = StatisticArticle.objects.filter(article=self).last()
        if fb:
            return getattr(fb, 'shares_fb')
        else:
            return 0

    @property
    def shares_vk_total(self):
        vk = StatisticArticle.objects.filter(article=self).last()
        if vk:
            return getattr(vk, 'shares_vk')
        else:
            return 0

    @property
    def shares_twitter_total(self):
        vk = StatisticArticle.objects.filter(article=self).last()
        if vk:
            return getattr(vk, 'shares_twitter')
        else:
            return 0

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
    shares_twitter = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у Twitter', default=0
    )

    def __unicode__(self):
        return self.article.title
