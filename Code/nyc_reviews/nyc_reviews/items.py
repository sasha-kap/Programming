# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HotelSentimentItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    recency = scrapy.Field()
    staysum = scrapy.Field()
    stars = scrapy.Field()
    reviewer_loc = scrapy.Field()
