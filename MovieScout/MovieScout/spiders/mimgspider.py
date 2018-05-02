import scrapy
from MovieScout.MovieScout.items import MoviescoutItem


class mimgSpider(scrapy.Spider):
    name= "mimgspider"
    start_urls=["https://www.imdb.com/find?ref_=nv_sr_fn&q=%s" %(l.strip()) for l in open("C:/Users/kimbe/Documents/15112/Term Project/urls.txt").readlines()]
    
    def parse(self, response):
        item= MoviescoutItem()
        url= response.xpath("//td[@class='primary_photo']/a/img/@src").extract_first()
        item['image_urls']= [url]
        yield item

    