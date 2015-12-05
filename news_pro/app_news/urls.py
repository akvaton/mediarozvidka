from __future__ import absolute_import

from django.conf.urls import url
from .views import (Index, get_articles, get_shares, get_time,
                    AllNews, OneNews, save_to_excel)

urlpatterns = [
        url(r'^$', Index.as_view(), name='index'),
        url(r'^get_new$', get_articles, name='get_new'),
        url(r'^get_shares$', get_shares, name='get_shares'),
        url(r'^get_time$', get_time, name='get_time'),
        url(r'^all$', AllNews.as_view(), name='all'),
        url(r'^all/(?P<source>\d+)$', AllNews.as_view(), name='news_type'),
        url(r'^news/(?P<pk>\d+)$', OneNews.as_view(), name='news'),
        url(r'^xls$', save_to_excel, name='xls'),
]
