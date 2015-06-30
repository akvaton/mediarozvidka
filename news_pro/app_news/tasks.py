from celery import shared_task, task
from celery.task import periodic_task
from datetime import timedelta
from app_news.spider1 import BlogSpider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings


from scrapy.crawler import Crawler
from scrapy.conf import settings
from scrapy import log, project
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(settings)

            if not hasattr(project, 'crawler'):
                self.crawler.install()
                self.crawler.configure()
                self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            reactor.run()

def run_spider(url):
    spider = BlogSpider(url)
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    log.start()
    crawler.join()


@task
def test():
    run_spider('scrapinghub.com')

@shared_task
def qqq():
    return 2+2


# reactor.run()
