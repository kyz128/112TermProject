from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from crochet import setup

setup()
def runSpider():
    crawler = CrawlerRunner(get_project_settings())
    crawler.crawl('mimgspider', 'C:/Users/kimbe/Documents/15112/TermProject/urls.txt')  
