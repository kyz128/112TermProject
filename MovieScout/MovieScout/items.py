# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# referenced Scrapy documentation; see link above

class MoviescoutItem(scrapy.Item):
    # create fields to hold scraped data
    image_name= scrapy.Field()
    image_urls= scrapy.Field()
    images= scrapy.Field()
