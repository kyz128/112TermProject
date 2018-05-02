import scrapy
from MovieScout.MovieScout.items import MoviescoutItem


class mimgSpider(scrapy.Spider):
    name= "mimgspider"
    start_urls=["https://www.imdb.com/find?ref_=nv_sr_fn&q=%s" %(l.strip()) for l in open("C:/Users/kimbe/Documents/15112/Term Project/urls.txt").readlines()]
    
    def parse(self, response):
        link= response.xpath("//td[@class='result_text']/a/@href").extract_first()
        newurl= "https://www.imdb.com" + str(link)
        yield scrapy.Request(newurl, callback= self.parseMoviePage)
    
    @staticmethod
    def getImageName():
        f= open("C:/Users/kimbe/Documents/15112/Term Project/urls.txt").readlines()[0]
        return f
        
    def parseMoviePage(self,response):
        item= MoviescoutItem()
        name= mimgSpider.getImageName()
        # name= response.xpath("//div[@class='poster']/a/img/@title").extract_first()
        url= response.xpath("//div[@class='poster']/a/img/@src").extract_first()
        item['image_name']= name
        item['image_urls']= url
        yield item