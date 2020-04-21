import scrapy
from memebot.items import MemeImage


class QuotesSpider(scrapy.Spider):
    name = "memebot"
    allowed_domains = ['https://www.reddit.com', 'www.reddit.com']
    start_urls = ['https://www.reddit.com/r/meme/']
    page_count = 0
    page_limit = 5
    '''
    def start_requests(self):
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    '''
    def parse(self, response):
        '''page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)'''
        titles = response.xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]/text()').extract()
        imgs = response.xpath('//img[@alt="Post image"]/@src').extract()
        self.page_count = self.page_count + 1
        if self.page_count > self.page_limit:
            return
        for(title, img) in zip(titles, imgs):
            self.log("Title: " + title)
            yield MemeImage(image_urls=[img])

        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page is not None and self.page_count < self.page_limit:
            yield response.follow(next_page, self.parse)