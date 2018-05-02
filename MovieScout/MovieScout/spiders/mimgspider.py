import scrapy
from MovieScout.MovieScout.items import MoviescoutItem
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
import time
import os
import sys


class mimgSpider(scrapy.Spider):
    name= "mimgspider"
    def __init__(self, filename=None):
        self.filename= filename
        with open(filename, 'r') as f:
            self.start_urls= ["https://www.imdb.com/find?ref_=nv_sr_fn&q=%s" %(l.strip()) for l in f.readlines()]

    def parse(self, response):
        link= response.xpath("//td[@class='result_text']/a/@href").extract_first()
        newurl= "https://www.imdb.com" + str(link)
        yield scrapy.Request(newurl, callback= self.parseMoviePage)
    
    def getImageName(self):
        with open(self.filename, 'r') as f:
            imgName= f.readlines()[0]
        return imgName
    
    def parseMoviePage(self,response):
        item= MoviescoutItem()
        name= self.getImageName()
        url= response.xpath("//div[@class='poster']/a/img/@src").extract_first()
        item['image_name']= name
        item['image_urls']= url
        yield item
    
