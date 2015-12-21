import urllib2
from BeautifulSoup import BeautifulSoup
from mock import patch
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

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

        visits = get_visits_count(datetime(year=2015, month=12, day=17))
        InternetTime.objects.create(visits=visits, date=datetime.now())

        self.assertEqual(visits, 19925258)
        self.assertEqual(InternetTime.objects.first().visits, 199.25258)

    @patch('app_news.models.BeautifulSoup')
    def test_get_internet_time(self, mocked):
        with patch('app_news.models.get_visits_count') as time:
            mocked.return_value = BeautifulSoup(urllib2.urlopen('file://%s/app_news/html_for_tests/get_visits_count.html' %
                                                  settings.BASE_DIR).read())
            time.return_value = get_visits_count(datetime(year=2015, month=12, day=17))
            InternetTime.objects.create(visits=10, date=datetime(year=2015, month=12, day=16))
            self.assertEqual(InternetTime.get_internet_time(), 199.25258+0.0001)


class ViewsTest(TestCase):

    def setUp(self):
        ArticleModel.objects.create(title='should_not_be', link='test', source=1)
        a = ArticleModel.objects.create(title='filter time', link='test', source=1)
        a.datetime = datetime(year=1950, month=12, day=12)
        a.save()
        ArticleModel.objects.create(title='To find', link='test', source=1)
        fb = ArticleModel.objects.create(title='fb_test', link='test', source=1)
        StatisticArticle.objects.create(article=fb, shares_fb=201)
        User.objects.create_user('test', 'test@test.com', 'test')
        self.client.login(username='test', password='test')

    def test_filter_dates(self):
        response = self.client.get(reverse('news:all'), {'from':'1940-12-12','to':'1960-12-12'})
        self.assertContains(response,'filter time')
        self.assertNotContains(response, 'should_not_be')

    def test_filter_shares(self):
        response = self.client.get(reverse('news:all'),{'shares':'200'})
        self.assertContains(response,'fb_test')
        self.assertNotContains(response, 'should_not_be')

    def test_filter_text(self):
        response = self.client.get(reverse('news:all'),{'find':'To find'})
        self.assertContains(response,'To find')
        self.assertNotContains(response, 'should_not_be')