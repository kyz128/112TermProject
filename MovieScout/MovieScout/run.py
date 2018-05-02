from scrapy.crawler import CrawlerProcess
# from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
# from twisted.internet import reactor
def runSpider():
    process= CrawlerProcess(get_project_settings())
    process.crawl("mimgspider")
    process.start()

# def runSpider():
#     runner= CrawlerRunner(get_project_settings())
#     newSpider= runner.crawl('mimgspider')
#     newSpider.addBoth(lambda _: reactor.stop())
#     reactor.run(stop_after_crawl=False)