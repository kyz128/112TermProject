from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
def runSpider():
    process= CrawlerProcess(get_project_settings())
    process.crawl("mimgspider")
    process.start()