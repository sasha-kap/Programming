# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

#from hotel_sentiment.items import HotelSentimentItem
#NEED TO CONFIRM PROPER DIRECTORY STRUCTURE AND WHERE TO STORE FILES
from nyc_reviews.items import HotelSentimentItem

#class ReviewSpiderSpider(scrapy.Spider):
class TripadvisorSpider(scrapy.Spider):
    name = 'nyc_reviews'
    allowed_domains = ['tripadvisor.com']
    start_urls = [
        "https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"
    ]

    #rules=(Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]')),follow=True,callback='self.parse'),
        #Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@class="unified pagination "]/child::*[2][self::a]')),follow=True,callback='parse_hotel'))

    def parse(self, response):
        for href in response.xpath('//div[@class="listing_title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_hotel)

        next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]/@href')
        #print "next listings page is:", next_page
        if next_page:
            url = response.urljoin(next_page[0].extract())
            #print url
            yield scrapy.Request(url, self.parse)

    def parse_hotel(self, response):
        #counter_page_review = 0
        for href in response.xpath('//div[starts-with(@class,"quote")]/a/@href'):
            url = response.urljoin(href.extract())
            #yield scrapy.Request(url, callback=self.parse_review)
            ta_review_id = "review_" + href.extract().split('-')[3][1:]
            ur_review_id = "UR" + href.extract().split('-')[3][1:]
            #counter_page_review += 1
            #if counter_page_review <= 500:
            yield scrapy.Request(url, callback=self.parse_review, meta={'ta_review_id':ta_review_id,'ur_review_id':ur_review_id})
            #yield scrapy.Request(url, callback=self.parse_review, meta={'ta_review_id':ta_review_id,'ur_review_id':ur_review_id,'counter_page_review':0})

        next_page2 = response.xpath('//div[@class="unified pagination "]/child::*[2][self::a]/@href')
        #print "next reviews page is:", next_page
        if next_page2:
            next_url = response.urljoin(next_page2[0].extract())
            #print url
            yield scrapy.Request(next_url, self.parse_hotel)

    def parse_review(self, response):
        # counter_page_review = response.meta['counter_page_review']
        # if counter_page_review < 500:
        #     counter_page_review = counter_page_review + 1
        #
        ta_review_id = response.meta['ta_review_id']
        xpath_string = '//*[@id="' + ta_review_id + '"]/text()'
        ur_review_id = response.meta['ur_review_id']
        #print ta_review_id, ur_review_id
        ur_xpath_string = '//div[@id="' + ur_review_id + '"]/div[@class="col2of2"]/div[@class="innerBubble"]/div[@class="rating-list"]/ul[@class="recommend"]/li/span[@class="recommend-titleInline"]/text()'
        ur_xpath_str_v2 = '//div[@id="' + ur_review_id + '"]/div[@class="col2of2"]/div[@class="innerBubble"]/div[@class="rating-list"]/div[@class="recommend"]/span[@class="recommend-titleInline noRatings"]/text()'
        #//div[@id='UR472614481']/div[@class='col2of2']/div[@class='innerBubble']/div[@class='rating-list']/div[@class='recommend']/span[@class='recommend-titleInline noRatings']
        ur_str_loc = '//div[@id="' + ur_review_id + '"]/div[@class="col1of2"]/div[@class="member_info"]/div[@class="location"]/text()'
        ur_str_cnt = '//div[@id="' + ur_review_id + '"]/div[@class="col2of2"]/div[@class="innerBubble"]/div[@class="entry"]/p[@id="' + ta_review_id + '"]/text()'
        #//div[@id='UR472753334']/div[@class='col2of2']/div[@class='innerBubble']/div[@class='entry']/p[@id='review_472753334']
        item = HotelSentimentItem()
        #hotel name
        item['name'] = response.xpath('//div/span[@class="altHeadInline"]/a/text()').extract()
        #title of review
        try:
            item['title'] = response.xpath('//div[@class="quote"]/text()').extract()[0][1:-1] #strip the quotes (first and last char)
        except IndexError:
            #item['title'] = response.xpath('//div[@class="quote"]/text()').extract()[0].decode("utf-8")[1:-1]
            item['title'] = response.xpath('//div[@class="quote"]/text()').extract()
        except:
            pass
        #full text of review
        #item['content'] = response.xpath('{}'.format(xpath_string)).extract()
        item['content'] = response.xpath('{}'.format(ur_str_cnt)).extract()
        #item['content'] = response.xpath('//div[@class="entry"]/p/text()').extract()
        #recency of review
        try:
            item['recency'] = response.xpath('//div[@class="rating reviewItemInline"]/span[2]/@title').extract()[0]
        except IndexError:
            item['recency'] = response.xpath('//div[@class="rating reviewItemInline"]/span[2]/text()').extract()[0]
        except:
            pass
        #item['recency'] = response.xpath('//div[@class='rating reviewItemInline']/span[@class='ratingDate relativeDate']/text()').extract()[0]
        #quick summary of stay (type of travel and when)
        #if response.xpath('{}'.format(ur_xpath_string)) != []:
            #item['staysum'] = response.xpath('//div[@class="rating-list"]/ul[@class="recommend"]/li/span[@class="recommend-titleInline"]/text()').extract()[0]
        somedata = response.xpath('{}'.format(ur_xpath_string))
        if somedata:
            item['staysum'] = response.xpath('{}'.format(ur_xpath_string)).extract()
        else:
            item['staysum'] = response.xpath('{}'.format(ur_xpath_str_v2)).extract()
        #stars given (overall rating, not by topic)
        item['stars'] = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()[0]
        #stars given by topic
        #item[] = response.xpath('//span[@class="rate sprite-rating_ss rating_ss"]/img/@alt').extract()
        #reviewer location
        #item['reviewer_loc'] = response.xpath('//div[@class="member_info"]/div[@class="location"]/text()').extract()[1]
        item['reviewer_loc'] = response.xpath('{}'.format(ur_str_loc)).extract()
        #try:
            #item['reviewer_loc'] = response.xpath('//div[@class='member_info']/div[@class='location']/text()').extract()[1]
        #except:
            #pass
        return item
