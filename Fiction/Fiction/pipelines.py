# -*- coding: utf-8 -*-
import pymongo
from Fiction.items import FictionItem
from Fiction.items import ContentItem
from Fiction import settings

class FictionPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=settings.MONGO_HOST,
            port=settings.MONGO_PORT
        )
        self.db = self.client[settings.MONGO_DB]  # 获得数据库的句柄
        #self.coll = self.db[settings.MONGO_COLL]  # 获得collection的句柄
        # 数据库登录需要帐号密码的话
        self.db.authenticate(settings.MONGO_USER, settings.MONGO_PSW)

    def process_item(self, item, spider):
        '''
        将爬到的小数写入数据库
        '''
        # 与本地数据库建立联系

        if isinstance(item, FictionItem):
            # 从items里取出数据
            sort = item['sort']
            novelid = item['novelid']
            name = item['name']
            novelimg = item['novelimg']
            author = item['author']
            status = item['status']
            description = item['description']
            try:
                with self.client.start_session() as s:
                    doc_novel = {'novelid': novelid, 'sort': sort, 'name': name, 'img': novelimg, 'author': author,
                                 'status': status, 'description': description}
                    db = self.client['noveltest']

                    coll = db.novel_info
                    coll.insert_one(doc_novel, session=s)
            finally:
                self.client.close()

        elif isinstance(item, ContentItem):
            novelname = item['name1']
            novelid = item['novelid']
            sort = item['sort']
            order_id = item['order_id']
            chapter_name = item['chapter_name']
            chapter_content = item['chapter_content']
            try:
                with self.client.start_session() as s:
                    doc_chapter = {'novelid':novelid,'novelname':novelname,'sort':sort,'order_id':order_id,'chapter_name':chapter_name,'chapter_content':chapter_content}
                    db = self.client['noveltest']
                    coll = db.chapter_info
                    coll.insert_one(doc_chapter, session=s)
            finally:
                # 关闭连接
                self.client.close()
            return item
