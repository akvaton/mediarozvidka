#! /usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pytz import timezone
import json
import requests
import re
import urllib2

import feedparser
from twython import Twython
from BeautifulSoup import BeautifulSoup

from django.conf import settings
from models import ArticleModel, StatisticArticle, InternetTime



URLS = {
'pravda': 'http://www.pravda.com.ua/rss/view_pubs/',
'site_ua': ['https://site.ua/rss-all.xml', 'https://site.ua/rss.xml'],
'nyt': 'http://topics.nytimes.com/top/news/international/countriesandterritories/ukraine/index.html?inline=nyt-geo'
}


def daterange(start_date, end_date):
    """
    Return all dates in range from start_date to end_date
    """
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


def get_shares_fb_total(full_url):
    """
    Get fb shares for specific url
    """
    return json.loads(requests.get("http://graph.facebook.com/?id={}".
                                   format(full_url)).text).get('shares', 0)


def get_shares_vk_total(full_url):
    """
    Get vk shares for specific url
    """
    re_mask = '^VK.Share.count\([\d+], (\d+)\);$'
    rq_text = requests.get(
        "http://vk.com/share.php?act=count&url={}".format(full_url)
        ).text
    match = re.match(re_mask, rq_text)
    return int(match.groups()[0]) if match else 0


def get_shares_twitter(full_url):
    """
    Get twitter shares for specific url
    """
    twitter = Twython(settings.APP_KEY,
                      settings.APP_SECRET,
                      settings.OAUTH_TOKEN,
                      settings.OAUTH_TOKEN_SECRET)
    search = twitter.search(q=full_url)['statuses']
    return len(search)


def get_attendances(article):
    """
    Get attendances for specific url
    """
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
    except (urllib2.HTTPError, urllib2.URLError, AttributeError) as e:
        print e
    return 0


def get_pravda_articles():
    """
    Get rss feed from pravda.com.ua and get new articles from it
    """
    rssfeed = feedparser.parse(URLS['pravda'])
    internet_time = InternetTime.get_internet_time()
    for each in rssfeed.entries:
        if 'pravda.com.ua' in each['link']:
            (article, cr) = ArticleModel.objects.get_or_create(link=each['link'])
            if cr:
                naive_date_str = each['published'].rpartition(' ')[0]
                naive_dt = datetime.strptime(naive_date_str,
                                             '%a, %d %b %Y %H:%M:%S')
                article.title = each['title']
                article.datetime = naive_dt
                article.source = 1
                article.internet_time = internet_time
                article.save()


def get_site_ua_articles():
    """
    Get rss feed from site.ua and get new articles from it
    """
    for rss_link in URLS['site_ua']:
        rssfeed = feedparser.parse(rss_link)
        internet_time = InternetTime.get_internet_time()
        for each in rssfeed.entries:
            article, cr = ArticleModel.objects.get_or_create(link=each['link'])
            if cr:
                naive_date_str, _, offset_str = each['published'].rpartition(' ')
                naive_dt = datetime.strptime(naive_date_str,
                                             '%a, %d %b %Y %H:%M:%S')
                article.title = each['title']
                article.datetime = naive_dt
                article.source = 2
                article.internet_time = internet_time
                article.save()


def get_nyt_articles():
    """
    Parse NYT site and new articles from it
    """
    page = urllib2.urlopen(URLS['nyt']).read()
    soup = BeautifulSoup(page)
    today = datetime.now()
    soup.prettify()
    internet_time = InternetTime.get_internet_time()
    searcn_div = soup.find('div', {"id": "searchList"})
    for each in searcn_div.findAll('h4'):
        link = each.find('a')['href']
        title = each.find('a').text
        time = datetime.strptime(each.findNext('h6').text, '%B %d, %Y, %A')
        time = time.replace(hour=today.hour, minute=today.minute)
        (article, cr) = ArticleModel.objects.get_or_create(link=link)
        if cr:
            article.title = title
            article.datetime = time
            article.source = 3
            article.internet_time = internet_time
            article.save()


def check_articles_shares():
    """
    Get all shares data for articles that were published less
    then 48 hours from now
    """
    now_minus_48 = datetime.today() - timedelta(hours=48)
    internet_time = InternetTime.get_internet_time()
    active_articles = ArticleModel.objects.filter(datetime__gte=now_minus_48).\
                      order_by('datetime')
    for each in active_articles:
        shares_twitter = get_shares_twitter(each.link)
        shares_fb = get_shares_fb_total(each.link)
        shares_vk = get_shares_vk_total(each.link)
        attendance = get_attendances(each) if each.source == 1 else None
        stat = StatisticArticle(
                        article=each,
                        shares_fb=shares_fb,
                        shares_twitter=shares_twitter,
                        internet_time=internet_time-float(each.internet_time),
                        shares_vk=shares_vk,
                        attendance=attendance
                                )
        stat.save()
