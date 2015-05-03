# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from app_news.models import NewsModel, ArticleModel


class AnPipeline(object):
    def process_item(self, item, spider):

        this_item_saved = ArticleModel.objects.filter(link=item['link'])
        assert (len(this_item_saved)) < 2
        if this_item_saved:
            saved_item = this_item_saved[0]
            if item['comments'] > saved_item.comments or item['shares'] > saved_item.shares:
                saved_item.comments = item['comments']
                saved_item.shares = item['shares']
                saved_item.save()
        else:
            item.save()
        return item
