# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FictionItem(scrapy.Item):
    name = scrapy.Field()   #小说名字
    chapter_name = scrapy.Field()   #小说章节名字
    chapter_content = scrapy.Field()    #小说章节内容
    order_id = scrapy.Field()  #小说章节ID
