# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import connections
from twisted.enterprise import adbapi
from pymysql.cursors import Cursor
import logging
from  scrapy.xlib.pydispatch import dispatcher

class BiqugebookPipeline(object):
    def process_item(self, item, spider):
        return item

class PymongoPipeline(object):


    @classmethod
    def from_crawler(cls,crawler):

        params = dict(
            host = crawler.settings.get('HOST'),
            user = crawler.settings.get('USER'),
            passwd = crawler.settings.get('PASSWD'),
            db =crawler.settings.get('DB'),
            cursorclass = Cursor,
            charset = 'utf8',
            use_unicode = True,
        )
        apipool = adbapi.ConnectionPool('pymysql',params)
        return cls(apipool)

    def __init__(self,apipool):
        self.dbpool = apipool
        self.logger = logging.getLogger(__file__)

    def process_item(self,item,spider):
        query = self.dbpool.runinteraction(self.do_insert,item)
        self.logger.log(query)
        return item

    def do_insert(self,cursor,item):
        sql,params = item.get_insert()
        cursor.execute(sql,params*2)


