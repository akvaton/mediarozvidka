from django.db import models
from scrapy.contrib.djangoitem import DjangoItem


class NewsModel(models.Model):
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.title


class ArticleModel(models.Model):
    # define the fields for your item here like:
    title =  models.CharField(max_length=160, blank=True, null=True)
    link = models.URLField(max_length=160, blank=True, null=True)
    datetime = models.DateTimeField()
    shares = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title
