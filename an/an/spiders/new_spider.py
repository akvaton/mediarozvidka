"""
Facebook API:
https://graph.facebook.com/fql?q=select%20%20total_count%20from%20link_stat%20where%20url=%22http://www.pravda.com.ua/articles/2014/11/20/7044675/22


scrapy crawl up
# main_news = res.xpath(".//div[@class='fblock']/div[@class='topblock2']/div/div/div[@class='summary big']/h3/a/@href").extract()[0]
title = res.xpath(".//div[@class='fblock']/div[@class='topblock2']/div/div/div[@class='summary big']/h3/a/text()").extract()[0]

scrapy crawl up -o items.json
"""

import scrapy
import requests
import time
import json
import datetime

from an.items import ArticleItem
from cookie import get_cookie

class UkrPravdaSpider(scrapy.Spider):
    name = "up"
    allowed_domains = ["pravda.com.ua"]
    start_urls = [
        "http://www.pravda.com.ua",
    ]

    def parse(self, response):
        cookie = get_cookie()
        print cookie
        page = requests.get('http://pravda.com.ua/articles', cookies=cookie)
        assert page.ok
        # create new resposne with new text for xpathing
        res = scrapy.http.HtmlResponse(url='http://pravda.com.ua/articles', body=page.text, encoding='utf8')

        all_links = res.xpath(".//div[@class='summary sec']/h4/a/@href").extract()
        all_names = res.xpath(".//div[@class='summary sec']/h4/a/text()").extract()

        filtered_links = [(all_links.index(link), link) for link in all_links if "http" not in link]
        # import ipdb; ipdb.set_trace()
        filtered_names_and_links = [(all_names[i[0]], i[1]) for i in filtered_links]
        # other_links = [link for link in all_links if "http" in link]

        for name, link in filtered_names_and_links:
            full_url = response.url + link
            item = ArticleItem()
            item['title'] = name
            item['link'] = full_url
            item['datetime'] = datetime.datetime.now() # int(time.time())
            item['comments'] = 0
            item['shares'] = json.loads(
                requests.get(
                    """https://graph.facebook.com/fql?q=select%20%20share_count%20from%20link_stat%20where%20url=%22{}%22""".format(full_url)
            ).text)['data'][0]['share_count']
            yield item

