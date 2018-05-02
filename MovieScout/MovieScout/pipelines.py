# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request


class MoviescoutPipeline(ImagesPipeline):
    
    def file_path(self,request, response=None, info=None):
        imgID= request.meta['image_name']
        if ":" in imgID:
            imgID= imgID.replace(":", "")
        return 'full/%s.jpg' % (imgID)
    
    def get_media_requests(self, item, info):
        yield Request(item['image_urls'], meta=item)