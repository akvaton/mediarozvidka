# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from app_news.models import NewsModel, ArticleModel

# class ArticleItem(scrapy.Item):
#     # define the fields for your item here like:
#     title = scrapy.Field()
#     link = scrapy.Field()
#     datetime = scrapy.Field()
#     shares = scrapy.Field()
#     comments = scrapy.Field()


class ArticleItem(DjangoItem):
    django_model= ArticleModel

class NewsItem(DjangoItem):
    django_model = NewsModel
