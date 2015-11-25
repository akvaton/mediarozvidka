import feedparser
import json
import requests
import re
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

from  models import ArticleModel, StatisticArticle, InternetTime

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


def get_attendances(full_url):
    for num in range(1,10):
        try:
            page = urllib2.urlopen(
                'http://www.liveinternet.ru/stat/ukrpravda/pages.html?page=%s&per_page=200' % num
                                  ).read()
            soup = BeautifulSoup(page)
            soup.prettify()
            for each in soup.findAll('a', href=True):
                if full_url[11:] in each.get('href'):
                    td_tag = each.parent
                    next_td_tag = td_tag.findNext('td')
                    return int(next_td_tag.contents[0].replace(',', ''))
        except Exception as e:
            print e
    return 0


def get_new_articles():
    rssfeed = feedparser.parse(pravda_url)
    internet_time = InternetTime.get_internet_time()
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
        attendance = get_attendances(each.link)
        stat = StatisticArticle(article=each,
                                shares_fb=shares_fb,
                                internet_time=internet_time - float(each.internet_time),
                                shares_vk=shares_vk,
                                attendance = attendance)
        stat.save()
