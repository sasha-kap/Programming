import scrapy
#from hotel_sentiment.items import HotelSentimentItem, HotelItem
#NEED TO CONFIRM PROPER DIRECTORY STRUCTURE AND WHERE TO STORE FILES
from nyc_images.items import NycImagesItem

class TripadvisorSpider(scrapy.Spider):
    name = 'nyc_images'
    allowed_domains = ['tripadvisor.com']
    start_urls = [
        "https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html"
    ]

    def parse(self, response):
        #loop over hotels on one page of hotel listings, direct scrapy to each hotel's page and call parse_hotel method
        for href in response.xpath('//div[@class="listing_title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_hotel)

        #direct scrapy to next page of hotel listings and repeat steps above
        next_page = response.xpath('//div[@class="unified pagination standard_pagination"]/child::*[2][self::a]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_hotel(self, response):
        #scrape hotel information:
        image_item = NycImagesItem()

        image_item['name'] = response.xpath('//*[@id="HEADING"]/text()').extract()
        url_path = response.xpath('//*[@id="BIG_PHOTO_CAROUSEL"]/div/div/img//@src').extract()[-1]
        #url_path = response.xpath('//div[@class="carouselPhoto border inView"]/@src').extract()
        print "URL PATH IS: ", url_path
        image_item['image_urls'] = self.url_list(url_path)
        #image_item['image_urls'] = self.url_list(response.xpath('//div[@class="carouselPhoto border inView"]//@src').extract_first())

        return image_item

		# grab the URL of the image
		#img = response.xpath('//div[@class="carouselPhoto border inView"]//@src')
		#imageURL = img.extract_first()

    def url_list(self, url_str):
        url_list = []
        url_list.append(url_str)
        return url_list


#Gramercy Park Hotel
#Amazing hotel and even better employees
#the following code returns review topic text (not bubble information)
#//ul[@class="recommend-column"]/li[descendant-or-self::text()]
