from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import Index, get_articles_from_pravda, get_shares

urlpatterns = [
        url(r'^$', Index.as_view(), name='index'),
        url(r'^get_new', get_articles_from_pravda, name='get_new'),
        url(r'^get_shares', get_shares, name='get_shares'),
]