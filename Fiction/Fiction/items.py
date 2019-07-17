# -*- coding: utf-8 -*-
import scrapy

class FictionItem(scrapy.Item):
    novelid = scrapy.Field() #小说标志号
    type = scrapy.Field()    #小说类型代号
    sort = scrapy.Field()    #小说类型名
    name = scrapy.Field()   #小说名字
    novelimg = scrapy.Field()     #小说图片地址
    author = scrapy.Field()     #小说作者
    status = scrapy.Field()      #小说连载状态
    description = scrapy.Field()    #小说简介

class ContentItem(scrapy.Item):
    #name1 =scrapy.Field()
    #novelid = scrapy.Field()
    #sort = scrapy.Field()
    chapter_name = scrapy.Field()   #小说章节名字
    chapter_content = scrapy.Field()    #小说章节内容
    order_id = scrapy.Field()  #小说章节ID