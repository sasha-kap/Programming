import scrapy
#from hotel_sentiment.items import HotelSentimentItem, HotelItem
#NEED TO CONFIRM PROPER DIRECTORY STRUCTURE AND WHERE TO STORE FILES
from nyc_hotels.items import HotelItem

class TripadvisorSpider(scrapy.Spider):
    name = 'nyc_hotels'
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
        hotel_item = HotelItem()

        hotel_item['name'] = response.xpath('//*[@id="HEADING"]/text()').extract()
        #hotel_item['name'] = response.xpath('//div[@class="heading_name_wrapper"]/h1[@id="HEADING"]').extract()
        hotel_item['n_reviews'] = response.xpath('//div/a[@class="more taLnk"]/text()').extract()
        hotel_item['st_addr'] = response.xpath('//div[@class="header_address fl blLinks contact_item"]/span[@class="format_address"]/span[@class="street-address"]/text()').extract()
        hotel_item['city'] = response.xpath('//span[@class="format_address"]/span[@class="locality"]/span[1]/text()').extract()
        hotel_item['state'] = response.xpath('//span[@class="format_address"]/span[@class="locality"]/span[2]/text()').extract()
        hotel_item['zip_cd'] = response.xpath('//span[@class="format_address"]/span[@class="locality"]/span[3]/text()').extract()

        hotel_item['excellent_ct'] = response.xpath('//*[@id="ratingFilter"]/ul/li[1]/label/span[2]/text()').extract()
        hotel_item['verygood_ct'] = response.xpath('//*[@id="ratingFilter"]/ul/li[2]/label/span[2]/text()').extract()
        hotel_item['average_ct'] = response.xpath('//*[@id="ratingFilter"]/ul/li[3]/label/span[2]/text()').extract()
        hotel_item['poor_ct'] = response.xpath('//*[@id="ratingFilter"]/ul/li[4]/label/span[2]/text()').extract()
        hotel_item['terrible_ct'] = response.xpath('//*[@id="ratingFilter"]/ul/li[5]/label/span[2]/text()').extract()

        hotel_item['families'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[2]/ul/li[1]/label/span/text()').extract()
        hotel_item['couples'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[2]/ul/li[2]/label/span/text()').extract()
        hotel_item['solo'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[2]/ul/li[3]/label/span/text()').extract()
        hotel_item['business'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[2]/ul/li[4]/label/span/text()').extract()
        hotel_item['friends'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[2]/ul/li[5]/label/span/text()').extract()
        #hotel_item['trav_types'] = response.xpath('//div[@class="col segment "]/ul/li/label').extract()

        hotel_item['spring'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[3]/ul/li[1]/label/span/text()').extract()
        hotel_item['summer'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[3]/ul/li[2]/label/span/text()').extract()
        hotel_item['fall'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[3]/ul/li[3]/label/span/text()').extract()
        hotel_item['winter'] = response.xpath('//*[@id="taplc_prodp13n_hr_sur_review_filter_controls_0_form"]/div[3]/ul/li[4]/label/span/text()').extract()
        #hotel_item['trav_time'] = response.xpath('//div[@class="col season "]/ul/li/label').extract()

        hotel_item['rank'] = response.xpath('//div[@class="popRanking popIndexValidation rank_text wrap"]/b/text()').extract()
        hotel_item['highlights'] = response.xpath('//*[@id="AMENITIES_TAB"]/div/div[1]/div[2]/ul/li/text()').extract()
        #hotel_item['highlights'] = response.xpath('//div[@id="AMENITIES_TAB"]/div[@class="content"]/div[@class="amenity_cnt first"]/div[@class="property_tags_wrap"]/ul[@class="property_tags"]/li').extract()
        hotel_item['prange'] = response.xpath('//div[@class="additional_info"][1]/span/text()').extract()
        hotel_item['rooms'] = response.xpath('//div[@class="additional_info"][2]/span[@class="tabs_num_rooms"]/text()').extract()
        hotel_item['hclass'] = response.xpath('//div[@class="additional_info stars"]/text()').extract()
        hotel_item['description'] = response.xpath('//div[@class="tabs_description_content"]/span[@class="tabs_descriptive_text"]/text()').extract()

        return hotel_item

#Gramercy Park Hotel
#Amazing hotel and even better employees
#the following code returns review topic text (not bubble information)
#//ul[@class="recommend-column"]/li[descendant-or-self::text()]
