from scrapy import Spider
from scrapy.selector import Selector
from app_news.models import NewsItem



class BlogSpider(Spider):
    name, start_urls = 'blogspider', ['http://blog.scrapinghub.com']

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)
        sel = Selector(response)
        p = NewsItem()
        p['title'] = sel.xpath('//title/text()').extract()[0]
        p['content'] = sel.xpath('//div[contains(@class,"entry clear")]/p').extract()
        p['link'] = self.start_urls
        p.save()
