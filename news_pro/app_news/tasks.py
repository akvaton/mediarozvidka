from celery import Task

from feed import get_new_articles, check_articles_shares


# class UrlCrawlerScript(Process):
#         def __init__(self, spider):
#             Process.__init__(self)
#             settings = get_project_settings()
#             self.crawler = Crawler(settings)
#
#             if not hasattr(project, 'crawler'):
#                 self.crawler.install()
#                 self.crawler.configure()
#                 self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
#             self.spider = spider
#
#         def run(self):
#             self.crawler.crawl(self.spider)
#             self.crawler.start()
#             reactor.run()
#
# def run_spider(url):
#     spider = BlogSpider(url)
#     crawler = UrlCrawlerScript(spider)
#     crawler.start()
#     log.start()
#     crawler.join()


# @task
# def test():
#     run_spider('scrapinghub.com')
#
# @shared_task
# def qqq():
#     return 2+2


# reactor.run()


class GetNewsAndShares(Task):

    def run(self, *args, **kwargs):
        get_new_articles()
        check_articles_shares()