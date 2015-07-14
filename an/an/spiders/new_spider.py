"""
Facebook API:
https://graph.facebook.com/fql?q=select%20%20total_count%20from%20link_stat%20where%20url=%22http://www.pravda.com.ua/articles/2014/11/20/7044675/22


scrapy crawl up
# main_news = res.xpath(".//div[@class='fblock']/div[@class='topblock2']/div/div/div[@class='summary big']/h3/a/@href").extract()[0]
title = res.xpath(".//div[@class='fblock']/div[@class='topblock2']/div/div/div[@class='summary big']/h3/a/text()").extract()[0]

scrapy crawl up -o items.json
"""

import json
import re
import requests
import scrapy

from an.items import ArticleItem, StatisticArticleItem
from cookie import get_cookie


class UkrPravdaSpider(scrapy.Spider):
    name = "up"
    allowed_domains = ["pravda.com.ua"]
    start_urls = [
        "http://www.pravda.com.ua",
    ]

    def parse(self, response):
        cookie = get_cookie()
        page = requests.get('http://pravda.com.ua/articles', cookies=cookie)
        assert page.ok
        # create new resposne with new text for xpathing
        res = scrapy.http.HtmlResponse(url='http://pravda.com.ua/articles', body=page.text, encoding='utf8')
        all_links = res.xpath(".//div[@class='summary sec']/h4/a/@href").extract()
        all_names = res.xpath(".//div[@class='summary sec']/h4/a/text()").extract()
        filtered_links = [(all_links.index(link), link) for link in all_links if "http" not in link]
        filtered_names_and_links = [(all_names[i[0]], i[1]) for i in filtered_links]
        # other_links = [link for link in all_links if "http" in link]

        for name, link in filtered_names_and_links:
            full_url = response.url + link
            item = ArticleItem()
            item['title'] = name
            item['link'] = full_url
            item['comments'] = self.get_comments(full_url)
            item['shares_fb_total'] = self.get_shares_fb_total(full_url)
            item['shares_vk_total'] = self.get_shares_vk_total(full_url)
            yield item

    def get_shares_fb_total(self, full_url):
        return json.loads(requests.get("http://graph.facebook.com/?id={}".format(full_url)).text)['shares']

    def get_shares_vk_total(self, full_url):
        re_mask = '^VK.Share.count\([\d+], (\d+)\);$'
        rq_text = requests.get("http://vk.com/share.php?act=count&url={}".format(full_url)).text
        match = re.match(re_mask, rq_text)
        return int(match.groups()[0]) if match else 0

    def get_comments(self, full_url):
        cookie = get_cookie()
        page = requests.get(full_url, cookies=cookie)
        res = scrapy.http.HtmlResponse(url=full_url, body=page.text, encoding='utf8')
        comments = res.xpath(".//a[@class='but4 m pic4']/span/text()").extract()
        return int(comments[0]) if comments else 0
