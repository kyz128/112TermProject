# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
# referenced Scrapy Documentation on media pipelines
# see url https://doc.scrapy.org/en/latest/topics/media-pipeline.html
# processes the scraped image urls for image downloads
class MoviescoutPipeline(ImagesPipeline):
    # rename the downloaded images by overriding the default method
    def file_path(self,request, response=None, info=None):
        # get imgID from the value in the image_name field 
        imgID= request.meta['image_name']
        if ":" in imgID:
            imgID= imgID.replace(":", "")
        # return the new path of the downloaded image
        return 'full/%s.jpg' % (imgID)
    
    # return the images
    def get_media_requests(self, item, info):
        yield Request(item['image_urls'], meta=item)