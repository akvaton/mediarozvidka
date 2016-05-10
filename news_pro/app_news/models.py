##! /usr/bin/python
##-*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone

import logging
from django.db import models
from django.db.models import Sum, ObjectDoesNotExist

URLS = {
'pravda': ['http://www.pravda.com.ua/rss/view_pubs/'],
'site_ua': ['https://site.ua/rss-all.xml', 'https://site.ua/rss.xml'],
'pravda_news':['http://www.pravda.com.ua/rss/view_news/'],
'nyt': 'http://topics.nytimes.com/top/news/international/countriesandterritories/ukraine/index.html?inline=nyt-geo'
}

logger = logging.getLogger('error')


def get_visits_count(date):
    """
    Get total count of visits from liveinternet, to get actual 'internet time'
    """
    visits_count = 0
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
        td = tr_tag.findAll('td')[1]
        date_for_visits = datetime.strptime(td.text, '%A, %d of %B')

        # Check if date in args equal today date on site
        if date_for_visits.month == date.month and date_for_visits.day == date.day:
            visits_count = int(visits_td.contents[0].replace(',', ''))
    except (urllib2.HTTPError, urllib2.URLError, AttributeError) as err:
        logger.error(err)
    finally:
        return visits_count


class InternetTime(models.Model):
    """
    Model for storing total count of everyday visits to get "Internet time".
    """
    internet_minute = 100000.0

    date = models.DateField()
    visits = models.FloatField(default=.0)

    def save(self, *args, **kwargs):
        self.visits /= self.internet_minute
        super(InternetTime, self).save()

    @classmethod
    def get_internet_time(cls):
        # We need the Moscow time because liveinternet.ru lives in Moscow TZ
        moscow_time = datetime.now(timezone('Europe/Moscow')).date()
        all_visits = InternetTime.objects.filter(date__lt=moscow_time).\
            aggregate(Sum('visits'))['visits__sum'] or .0
        today_visits_count = get_visits_count(moscow_time)
        if today_visits_count > 0:
            (stored_visits, cr) = InternetTime.objects.get_or_create(
                            date=moscow_time)
            stored_visits.visits = today_visits_count
            stored_visits.save()
            # Geting right count of yesterday visits if new day starts
            if cr:
                try:
                    yesterday = moscow_time - timedelta(days=1)
                    yesterday_visits = InternetTime.objects.get(date=yesterday)
                    yesterday_visits_on_site = get_visits_count(yesterday)
                    if yesterday_visits_on_site / cls.internet_minute > yesterday_visits.visits:
                        yesterday_visits.visits = yesterday_visits_on_site
                        yesterday_visits.save()
                except ObjectDoesNotExist:
                    logger.error("There is no yesterday visits in db")
        else:
            logger.error('Wrong day %s' % str(moscow_time))

        return all_visits + float(today_visits_count) / cls.internet_minute

    def __unicode__(self):
        return u'%s' % self.date


class ArticleModel(models.Model):
    """
    Model for agregate article from news source.
    """
    SOURCE_TYPE_OPTIONS = ((1, 'Pravda article'),
                           (2, 'Site.ua'),
                           (3, 'NewYork times'),
                           (4, 'Pravda news'))

    title = models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    internet_time = models.FloatField(default=0)
    source = models.IntegerField(choices=SOURCE_TYPE_OPTIONS, null=True)

    @property
    def attendance(self):
        att = StatisticArticle.objects.filter(article=self).last()
        return getattr(att, 'attendance', 0)


    @property
    def shares_fb_total(self):
        fb = StatisticArticle.objects.filter(article=self).last()
        return getattr(fb, 'shares_fb', 0)


    @property
    def shares_vk_total(self):
        vk = StatisticArticle.objects.filter(article=self).last()
        return getattr(vk, 'shares_vk', 0)


    @property
    def shares_twitter_total(self):
        twitter = StatisticArticle.objects.filter(article=self).last()
        return getattr(twitter, 'shares_twitter', 0)


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
    fb_total = models.PositiveIntegerField(
        u'Загальне поширювання новини у цей час у FB', default=0
    )
    shares_vk = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у VK', default=0
    )
    shares_twitter = models.PositiveIntegerField(
        u'Поширюваність новини у цей час у Twitter', default=0
    )

    def __unicode__(self):
        return self.article.title
