#! /usr/bin/python
# -*- coding: utf-8 -*-
import feedparser
import json
import requests
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta, tzinfo
from pytz import timezone

from  models import ArticleModel, StatisticArticle, InternetTime

urls = {
'pravda':'http://www.pravda.com.ua/rss/view_pubs/',
'site_ua': 'https://site.ua/rss-all.xml'
}

class FixedOffset(tzinfo):
    """Fixed offset in minutes: `time = utc_time + utc_offset`."""
    def __init__(self, offset):
        self.__offset = timedelta(minutes=offset)
        hours, minutes = divmod(offset, 60)
        #NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
        #  that have the opposite sign in the name;
        #  the corresponding numeric value is not used e.g., no minutes
        self.__name = '<%+03d%02d>%+d' % (hours, minutes, -hours)
    def utcoffset(self, dt=None):
        return self.__offset
    def tzname(self, dt=None):
        return self.__name
    def dst(self, dt=None):
        return timedelta(0)
    def __repr__(self):
        return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


def get_shares_fb_total(full_url):
    try:
        return json.loads(requests.get(
            "http://graph.facebook.com/?id={}".format(full_url)).text
                          )['shares']
    except KeyError:
        return 0


def get_shares_vk_total(full_url):
    re_mask = '^VK.Share.count\([\d+], (\d+)\);$'
    rq_text = requests.get(
        "http://vk.com/share.php?act=count&url={}".format(full_url)
        ).text
    match = re.match(re_mask, rq_text)
    return int(match.groups()[0]) if match else 0


def get_attendances(article):
    try:
        moscow_time = datetime.now(timezone('Europe/Moscow')).date()
        all_visits = 0
        for day in daterange(article.datetime.date(), moscow_time):
            page = urllib2.urlopen(
                'http://www.liveinternet.ru/stat/ukrpravda/pages.html?type=only&filter=%s&date=%s-%s-%s&lang=en&ok=+OK+&report=pages.html' %
                (article.link[11:], day.year, day.month, day.day)).read()

            soup = BeautifulSoup(page)
            soup.prettify()
            total = soup.find(text="total")
            td_tag = total.parent
            today_visit = td_tag.findNext('td')
            all_visits += int(today_visit.contents[0].replace(',', ''))
        return all_visits
    except Exception as e:
        print e
    return 0


def get_pravda_articles():
    rssfeed = feedparser.parse(urls['pravda'])
    internet_time = InternetTime.get_internet_time()
    for each in rssfeed.entries:
        if 'pravda.com.ua' in each['link']:
            print each['link'], each['title']
            (article, cr) = ArticleModel.objects.get_or_create(link=each['link'])
            if cr:
                naive_date_str, _, offset_str = each['published'].rpartition(' ')
                naive_dt = datetime.strptime(naive_date_str, '%a, %d %b %Y %H:%M:%S')
                article.title = each['title']
                article.datetime = naive_dt
                article.source = 1
                article.internet_time = internet_time
                article.save()
            else:
                break


def get_pravda_articles():
    rssfeed = feedparser.parse(urls['pravda'])
    internet_time = InternetTime.get_internet_time()
    for each in rssfeed.entries:
        if 'pravda.com.ua' in each['link']:
            print each['link'], each['title']
            (article, cr) = ArticleModel.objects.get_or_create(link=each['link'])
            if cr:
                naive_date_str, _, offset_str = each['published'].rpartition(' ')
                naive_dt = datetime.strptime(naive_date_str, '%a, %d %b %Y %H:%M:%S')
                article.title = each['title']
                article.datetime = naive_dt
                article.source = 1
                article.internet_time = internet_time
                article.save()
            else:
                break


def get_site_ua_articles():
    rssfeed = feedparser.parse(urls['site_ua'])
    internet_time = InternetTime.get_internet_time()
    for each in rssfeed.entries:
        (article, cr) = ArticleModel.objects.get_or_create(link=each['link'])
        if cr:
            naive_date_str, _, offset_str = each['published'].rpartition(' ')
            naive_dt = datetime.strptime(naive_date_str, '%a, %d %b %Y %H:%M:%S')
            article.title = each['title']
            article.datetime = naive_dt
            article.source = 2
            article.internet_time = internet_time
            article.save()
        else:
            break


def check_articles_shares():
    now_minus_48 = datetime.today()-timedelta(hours=48)
    internet_time = InternetTime.get_internet_time()
    active_articles = ArticleModel.objects.filter(datetime__gte = now_minus_48).\
        order_by('datetime')
    for each in active_articles:
        print 'Get shares for %s' % each.title
        shares_fb = get_shares_fb_total(each.link)
        shares_vk = get_shares_vk_total(each.link)
        attendance = get_attendances(each) if each.source == 1 else None
        stat = StatisticArticle(article=each,
                                shares_fb=shares_fb,
                                internet_time=internet_time - float(each.internet_time),
                                shares_vk=shares_vk,
                                attendance = attendance)
        stat.save()
