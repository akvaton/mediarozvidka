from celery import Task

from feed import get_site_ua_articles, get_pravda_articles, check_articles_shares


class GetShares(Task):

    def run(self, *args, **kwargs):
        check_articles_shares()


class GetNews(Task):

    def run(self, *args, **kwargs):
        get_pravda_articles()
        get_site_ua_articles()
