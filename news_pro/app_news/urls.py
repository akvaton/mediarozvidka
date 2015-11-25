from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import (Index, get_articles_from_pravda, get_shares, get_time,
                    AllNews, OneNews)

urlpatterns = [
        url(r'^$', Index.as_view(), name='index'),
        url(r'^get_new$', get_articles_from_pravda, name='get_new'),
        url(r'^get_shares$', get_shares, name='get_shares'),
        url(r'^get_time$', get_time, name='get_time'),
        url(r'^all$', AllNews.as_view(), name='all'),
        url(r'^news/(?P<pk>\d+)$', OneNews.as_view(), name='news'),

]