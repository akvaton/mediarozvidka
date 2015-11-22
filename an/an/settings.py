# -*- coding: utf-8 -*-

# Scrapy settings for an project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'an'

SPIDER_MODULES = ['an.spiders']
NEWSPIDER_MODULE = 'an.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'an (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'an.pipelines.AnPipeline': 1000,
}

#STATS_ENABLED = True
