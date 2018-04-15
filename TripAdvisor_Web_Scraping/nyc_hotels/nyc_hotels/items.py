# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class NycHotelsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

class HotelItem(scrapy.Item):
    name = scrapy.Field()
    n_reviews = scrapy.Field()
    st_addr = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_cd = scrapy.Field()
    excellent_ct = scrapy.Field()
    verygood_ct = scrapy.Field()
    average_ct = scrapy.Field()
    poor_ct = scrapy.Field()
    terrible_ct = scrapy.Field()
    #trav_types = scrapy.Field()
    families = scrapy.Field()
    couples = scrapy.Field()
    solo = scrapy.Field()
    business = scrapy.Field()
    friends = scrapy.Field()
    #trav_time = scrapy.Field()
    spring = scrapy.Field()
    summer = scrapy.Field()
    fall = scrapy.Field()
    winter = scrapy.Field()
    rank = scrapy.Field()
    highlights = scrapy.Field()
    prange = scrapy.Field()
    rooms = scrapy.Field()
    hclass = scrapy.Field()
    description = scrapy.Field()
