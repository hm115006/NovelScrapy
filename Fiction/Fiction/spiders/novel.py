# -*- coding: utf-8 -*-
import scrapy
import re
import string
from spiders.sjzh import Cn2An, get_tit_num

from Fiction.items import FictionItem
from Fiction.items import ContentItem
from scrapy.http import Request


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['quanshuwang.com']
    start_urls = [
        'http://www.quanshuwang.com/list/1_1.html',
    ]

    # 获取每一本书的URL
    def parse(self, response):
        book_urls = response.xpath('//li/a[@class="l mr10"]/@href').extract()
        for book_url in book_urls:
            yield Request(book_url, callback=self.parse_read)

    # 获取每一本书的信息并获取开始阅读按钮的URL，进入章节目录
    def parse_read(self, response):
        # 小说id
        novelid_first = response.xpath('//div[@class="b-oper"]/a/@href').extract_first()
        novelid_second = novelid_first.split('/')[5]
        novelid = int(novelid_second)
        # 小说类型名
        sort = response.xpath('//div[@class="main-index"]/a[@class="c009900"]/text()').extract_first()
        # 小说书名
        bookname = response.xpath('//div[@class="b-info"]/h1/text()').extract_first()
        # 小说图片
        novelimg = response.xpath('//div[@class="detail"]/a/img/@src').extract_first()
        # 获取作者
        author = response.xpath('//div[@class="bookDetail"]/dl[@class="bookso"]/dd/text()').extract_first()
        # 小说描述
        description = response.xpath('//div[@style="height:72px;width:690px;overflow:hidden;"]/text()').extract_first()
        # 连载状态
        status = response.xpath('//div[@class="bookDetail"]/dl/dd/text()').extract_first()
        print('小说信息获取成功！')
        item = FictionItem()
        item['sort'] = sort
        item['novelid'] = novelid
        item['name'] = bookname
        item['novelimg'] = novelimg
        item['author'] = author
        item['status'] = status
        item['description'] = description
        yield item
        read_url = response.xpath('//a[@class="reader"]/@href').extract()[
            0]  # http://www.quanshuwang.com/book/154/154796
        yield Request(read_url, callback=self.parse_chapter)

    # 获取小说章节的URL
    def parse_chapter(self, response):
        chapter_urls = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
        for chapter_url in chapter_urls:
            yield Request(chapter_url, callback=self.parse_content)

    # 获取章节的名字，用于排序的章节ID和内容
    def parse_content(self, response):
        result = response.text
        # 小说名字
        name = response.xpath('//div[@class="main-index"]/a[@class="article_title"]/text()').extract_first()
        chapter_name_tmp = response.xpath('//strong[@class="l jieqi_title"]/text()').extract_first()
        chapter_name = ''
        chapter_name_id = ''
        chapter_content = ''
        novelid = ''
        name1 = ''
        sort = ''
        try:
            if '第.*?卷' in chapter_name_tmp:
                chapter_name_tmp_reg = r'第.*?卷.*?(第.*?章[\s][\u4e00-\u9fa5]{2,20})'
                chapter_name = re.findall(chapter_name_tmp_reg, chapter_name_tmp, re.S)[0]
            else:
                chapter_name_tmp_reg = r'(第.*?章[\s][\u4e00-\u9fa5]{2,20})'
                chapter_name = re.findall(chapter_name_tmp_reg, chapter_name_tmp, re.S)[0]
            # 获取章节ID
            chapter_name_id_reg = r'第(.*?)章'
            chapter_name_id = re.findall(chapter_name_id_reg, chapter_name)[0]
            # 小说章节内容
            chapter_content_reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'
            chapter_content = re.findall(chapter_content_reg, result, re.S)[0]
            # chapter_content_1 = chapter_content_2.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '')
            # chapter_content = chapter_content_1.replace('<br />', '')
            name1 = response.xpath('//div[@class="attention"]/a/em/text()').extract_first()
            novelid_first = response.xpath('//div[@class="backs"]/a[2]/@href').extract_first()
            novelid_second = novelid_first.split('/')[5]
            novelid = int(novelid_second)

            sort = response.xpath('//div[@class="main-index"]/a[2]/text()').extract_first()
            print('正在爬取的小说: ' + name + '\t' + '章节: ' + chapter_name + '\t' + '入库成功！')
        except Exception as err:
            print(err)

        # 三个属性均获取到
        if chapter_name != None and chapter_name_id != None and chapter_content != None:
            item = ContentItem()
            item['name1'] = name1
            item['sort'] = sort
            item['novelid'] = novelid
            item['chapter_name'] = chapter_name
            item['chapter_content'] = chapter_content
            item['order_id'] = Cn2An(get_tit_num(chapter_name_id))
            yield item
