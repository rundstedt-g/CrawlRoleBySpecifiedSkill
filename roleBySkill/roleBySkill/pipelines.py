# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

import pymysql
from itemadapter import ItemAdapter


class RolebyskillPipeline:
    def __init__(self):
        # 连接数据库
        self.connect=pymysql.connect(host='localhost',port=3307,user='root',password='root',db='crawlrolebyspecifiedskill')
        self.cursor=self.connect.cursor()

    def open_spider(self, spider):
        # 爬虫开始前，清空所有表的数据
        sqlStatement1 = "TRUNCATE TABLE role"
        self.cursor.execute(sqlStatement1);
        self.connect.commit() #执行

    def process_item(self, item, spider):
        sqlStatement = "insert into crawlrolebyspecifiedskill.role (id, name, status, price)VALUES ({},'{}','{}',{})"
        self.cursor.execute(sqlStatement.format(item['id'],item['name'],item['status'],item['price']))
        self.connect.commit()#执行添加
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()  #关闭连接
