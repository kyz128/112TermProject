# run the entire spider as a script 
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
# crochet to handle twisted reactor restart error when same spider called 
# multiple times in same process
# referenced https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
from crochet import setup

setup()
def runSpider():
    # initalize crawler with current project settings
    crawler = CrawlerRunner(get_project_settings())
    # crawl the mimgspider and pass in the filename below for start url config
    crawler.crawl('mimgspider', 'C:/Users/kimbe/Documents/15112/TermProject/urls.txt')  
