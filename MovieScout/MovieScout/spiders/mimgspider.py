# configure spider 
# referenced Scrapy Documentation 
#https://doc.scrapy.org/en/latest/intro/tutorial.html
import scrapy
# import the scrapy object to populate
from MovieScout.MovieScout.items import MoviescoutItem


class mimgSpider(scrapy.Spider):
    name= "mimgspider"
    # for each spider instance, pass in new start url using a file
    def __init__(self, file=None):
        self.file= file
        with open(file, 'r') as f:
            # add name of movie to end of the IMDB search engine url
            self.start_urls= ["https://www.imdb.com/find?ref_=nv_sr_fn&q=%s" %(l.strip()) for l in f.readlines()]

    def parse(self, response):
        # In the search results, grab the link to the first movie on the list
        link= response.xpath("//td[@class='result_text']/a/@href").extract_first()
        # url to the actual movie page
        newurl= "https://www.imdb.com" + str(link)
        # tell spider to crawl the movie page and then call parseMovePage function
        yield scrapy.Request(newurl, callback= self.parseMoviePage)
    
    def getImageName(self):
        with open(self.file, 'r') as f:
            imgName= f.readlines()[0]
        return imgName
    
    def parseMoviePage(self,response):
        # initalize an item to hold the scraped data
        item= MoviescoutItem()
        # populate image name field with the reformated movie title from file
        name= self.getImageName()
        # get the image urls on the page
        url= response.xpath("//div[@class='poster']/a/img/@src").extract_first()
        # populate the respective fields and send to the image pipelines for 
        # further processing
        item['image_name']= name
        item['image_urls']= url
        yield item
    
