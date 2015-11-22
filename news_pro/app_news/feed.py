import feedparser
import json
import requests
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

from  models import ArticleModel, StatisticArticle



pravda_url = 'http://www.pravda.com.ua/rss/view_news/'

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


def get_shares_fb_total(full_url):
    return json.loads(requests.get(
        "http://graph.facebook.com/?id={}".format(full_url)).text
                      )['shares']

def get_shares_vk_total(full_url):
    re_mask = '^VK.Share.count\([\d+], (\d+)\);$'
    rq_text = requests.get(
        "http://vk.com/share.php?act=count&url={}".format(full_url)
        ).text
    match = re.match(re_mask, rq_text)
    return int(match.groups()[0]) if match else 0


def get_attendances(full_url):
    for num in range(1,20):
        page = urllib2.urlopen(
            'http://www.liveinternet.ru/stat/ukrpravda/pages.html?page=%s' % num
                              ).read()
        soup = BeautifulSoup(page)
        soup.prettify()
        print full_url
        for each in soup.findAll('a', href=True):
            if each.get('href')==full_url:
                b = each.parent
                print b.next_sibling
                return b
    return 1

def get_new_articles():
    rssfeed = feedparser.parse(pravda_url)
    for each in rssfeed.entries:
        if 'pravda.com.ua' in each['link']:
            (article, cr) = ArticleModel.objects.get_or_create(link=each['link'])
            if cr:
                naive_date_str, _, offset_str = each['published'].rpartition(' ')
                naive_dt = datetime.strptime(naive_date_str, '%a, %d %b %Y %H:%M:%S')
                offset = int(offset_str[-4:-2])*60 + int(offset_str[-2:])
                if offset_str[0] == "-":
                   offset = -offset
                dt = naive_dt.replace(tzinfo=FixedOffset(offset))
                article.title = each['title']
                article.datetime = dt
                article.source = 1
                article.internet_time = datetime.now()
                article.save()
                print article
            else:
                break


def check_articles_shares():
    now_minus_48 = datetime.today()-timedelta(hours=48)
    print now_minus_48
    active_articles = ArticleModel.objects.filter(datetime__gte = now_minus_48)
    for each in active_articles:
        shares_fb = get_shares_fb_total(each.link)
        shares_vk = get_shares_vk_total(each.link)
        attendance = get_attendances(each.link)
        print attendance
        stat = StatisticArticle(article=each,
                                order=1,
                                shares_fb=shares_fb,
                                shares_vk=shares_vk,
                                attendance = attendance)
        stat.save()
