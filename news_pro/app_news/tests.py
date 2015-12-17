import urllib2
from BeautifulSoup import BeautifulSoup
from mock import patch, Mock
from django.test import TestCase

from django.conf import settings
from feed import *
from models import *


# Create your tests here.

class FeedTest(TestCase):
    def setUp(self):
        ArticleModel.objects.create(title='test',
                                    link='test')

    @patch('app_news.feed.BeautifulSoup')
    def test_for_get_attendances(self, mocked):
        mocked.return_value = BeautifulSoup(urllib2.urlopen('file:///%s/app_news/html_for_tests/get_attendances.html' %
                                              settings.BASE_DIR).read()
                                            )

        visits = get_attendances(ArticleModel.objects.first())
        self.assertEqual(visits, 6165)

    @patch('app_news.feed.BeautifulSoup')
    def test_get_nyt_articles(self, mocked):
        mocked.return_value = BeautifulSoup(urllib2.urlopen('file://%s/app_news/html_for_tests/get_nyt_articles.html' %
                                              settings.BASE_DIR).read())
        get_nyt_articles()
        self.assertEqual(ArticleModel.objects.filter(source=3).count(), 10)
        self.assertEqual(ArticleModel.objects.filter(source=3).first().title,
                         'Has Europe Reached the Breaking Point?')


class ModelsTest(TestCase):

    @patch('app_news.models.BeautifulSoup')
    def test_get_visits_count(self, mocked):
        mocked.return_value = BeautifulSoup(urllib2.urlopen('file://%s/app_news/html_for_tests/get_visits_count.html' %
                                              settings.BASE_DIR).read())

        visits = get_visits_count(datetime.now())
        InternetTime.objects.create(visits=visits, date=datetime.now())

        self.assertEqual(visits, 19925258)
        self.assertEqual(InternetTime.objects.first().visits, 199.25258)

    @patch('app_news.models.BeautifulSoup')
    def test_get_internet_time(self, mocked):
        mocked.return_value = BeautifulSoup(urllib2.urlopen('file://%s/app_news/html_for_tests/get_visits_count.html' %
                                              settings.BASE_DIR).read())
        InternetTime.objects.create(visits=10, date=datetime.now()-timedelta(days=1))
        self.assertEqual(InternetTime.get_internet_time(), 199.25258+0.0001)
