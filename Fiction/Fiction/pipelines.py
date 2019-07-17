# -*- coding: utf-8 -*-
import pymongo
from Fiction.items import FictionItem
from Fiction.items import ContentItem
from scrapy.conf import settings

class FictionPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=settings['MONGO_HOST'],
            port=settings['MONGO_PORT']
        )
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄
        # 数据库登录需要帐号密码的话
        self.db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])

    def process_item(self, item, spider):
        '''
        将爬到的小数写入数据库
        '''
        # 与本地数据库建立联系
        # 和本地的scrapyDB数据库建立连接

        #if isinstance(item,FictionItem):
            # 首先从items里取出数据
            # sort = item['sort']
            # novelid = item['novelid']
            # name = item['name']
            # novelimg = item['novelimg']
            # author = item['author']
            # status = item['status']
            # description = item['description']
            # try:
            #     with self.client.start_session() as s:
            #         s.start_transaction()
            #         doc_one ={}
            #         #sql1 = "Insert into noveltest( novelid,sort,novelname, novelimg, description, status, author) values (%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\') on duplicate key update novelname=(novelname)" % (novelid,sort, name, novelimg, description, status, author)
            #         name.insert_one(doc_one,session=s)
            #         s.commit_transaction()
            # finally:
            #     self.client.close()

        #elif isinstance(item,ContentItem):


        sort = item['sort']
        novelid = item['novelid']
        name = item['name']
        novelimg = item['novelimg']
        author = item['author']
        status = item['status']
        description = item['description']
        #name1 = item['name1']
        #novelid = item['novelid']
        #sort = item['sort']
        order_id = item['order_id']
        chapter_name = item['chapter_name']
        chapter_content = item['chapter_content']
        try:
            with self.client.start_session() as s:
                # 数据库表的sql
                #sql2 = "Insert into chaptertest (novelid,name1,sort,chapterid,title,content) values (%d,\'%s\',\'%s\',%d,\'%s\',\'%s\') " % (novelid,name1,sort,order_id,chapter_name,chapter_content)
                doc_novel = {'_id':novelid,'sort':sort,'name':name,'img':novelimg,'author':author,'status':status,'description':description}
                doc_chapter = {'order_id':order_id,'chapter_name':chapter_name,'chapter_content':chapter_content}
                #dictget()
                db = self.client.noveltest

                #if novelid
                db.name.insert_one(doc_novel, session=s)
                db.name.insert_one(doc_chapter, session=s)
                s.commit_transaction()
            # 提交本次插入的记录
            self.client.commit()
        finally:
            # 关闭连接
            self.client.close()
        return item
