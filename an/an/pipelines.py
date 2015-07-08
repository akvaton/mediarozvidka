#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    an.pipelines
    ~~~~~~~~~

    :copyright: (c) 2015 by dorosh.
"""

import time
from app_news.models import NewsModel, ArticleModel, StatisticArticle


class AnPipeline(object):

    def process_item(self, item, spider):
        try:
            item_saved, cr = ArticleModel.objects.get_or_create(
                link=item['link'], defaults=item
            )
        except ArticleModel.MultipleObjectsReturned:
            obj = ArticleModel.objects.filter(link=item['link'])
            ArticleModel.objects.filter(
                id__in=obj.values_list('id', flat=True)[1:]
            ).delete()
            item_saved, cr = obj[0], False

        if cr:
            StatisticArticle.objects.create(
                article=item_saved,
                order=int(time.time()),
                site_order = 0,
                attendance = 0,
                attendance_index_site = 0,
                shares_fb = item['shares_fb_total'],
                comments = item['comments']
            )
            return item

        shares_fb = 0
        comments = 0

        if item['comments'] > item_saved.comments or \
                item['shares_fb_total'] > item_saved.shares_fb_total:
            comments = item['comments'] - item_saved.comments
            shares_fb = item['shares_fb_total'] - item_saved.shares_fb_total
            item_saved.comments = item['comments']
            item_saved.shares_fb_total = item['shares_fb_total']
            item_saved.save()

        StatisticArticle.objects.create(
            article=item_saved,
            order=int(time.time()),
            site_order = 0,
            attendance = 0,
            attendance_index_site = 0,
            shares_fb = shares_fb,
            comments = comments
        )

        return item
