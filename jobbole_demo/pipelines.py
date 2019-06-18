# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql,pymongo
from jobbole_demo.items import JobboleDemoCategoryItem,JobboleDemoItem

############mysql数据库插入最初版###############

# class JobboleDemoPipeline(object):
#
#     def __init__(self):
#         # 创建数据库链接
#         self.client = pymysql.Connect(
#             host='127.0.0.1', user='root',
#             password='ljh1314', database='class1811',
#             port=3306, charset='utf8'
#         )
#         # 创建游标
#         self.mycursor = self.client.cursor()
#
#     def process_item(self, item, spider):
#         """
#
#         :param item: 指的是spider爬虫文件中yield的item数据对象
#         :param spider:
#         :return:
#         """
#         item_dict = dict(item)
#         print('经过了管道', item_dict)
#         sql_insert = """
#         INSERT INTO chinaz (%s)
#         VALUES (%s)
#         """ % (
#             ','.join(item_dict.keys()),
#             ','.join(['%s'] * len(item_dict))
#         )
#         try:
#             self.mycursor.execute(sql_insert, list(item_dict.values()))
#             self.client.commit()
#         except Exception as err:
#             print(err)
#             self.client.rollback()
#
#         #
#         return item
#
#     def close_spider(self, spider):
#         """可选方法,爬虫结束的时候会执行一次"""
#         self.client.close()
#         self.mycursor.close()
#         print('爬虫结束')

# class JobboleDemoPipeline(object):
#
#     def __init__(self):
#         #创建数据库链接
#         self.client = pymysql.Connect(
#             host='127.0.0.1',user='root',
#             password='ljh1314',database='class1811',
#             port=3306,charset='utf8'
#         )
#         #创建游标
#         self.mycursor = self.client.cursor()
#
#     def process_item(self, item, spider):
#         """
#         :param item: 指的是spider爬虫文件中yield的item数据对象
#         :param spider:
#         :return:
#         """
#         item_dict = dict(item)
#
#         if isinstance(item,JobboleDemoCategoryItem):
#             print('分类的item')
#             tablename = 'chinazcategory'
#         elif isinstance(item,JobboleDemoItem):
#             print('网站信息的item')
#             tablename = 'chinaz'
#
#         print('经过了管道',item_dict)
#         sql_insert = """
#         INSERT INTO %s (%s)
#         VALUES (%s)
#         """ % (
#             tablename,
#             ','.join(item_dict.keys()),
#             ','.join(['%s']*len(item_dict))
#         )
#         try:
#             self.mycursor.execute(sql_insert,list(item_dict.values()))
#             self.client.commit()
#         except Exception as err:
#             print(err)
#             self.client.rollback()
#
#         # 注意这里只有return item，下一个管道才能接收
#         return item


###################下载项目图片###################
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
#pip3 install pillow
class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 根据图片url地址,构建请求
        if isinstance(item,JobboleDemoItem):
            image_url = 'https:'+item['coverimage']
            yield scrapy.Request(image_url)

        # for image_url in item['image_urls']:
        #     yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        """
        图片下载完成后,会走这个方法
        :param results: 图片下载后的结构
        :param item: 爬虫文件中传递的item数据
        :param info:
        :return:
        """
        """
        [(True,
          {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
           'path': 'full/7d97e98f8af710c7e7fe703abc8f639e0ee507c4.jpg',
           'url': 'http://www.example.com/images/product1.jpg'}),
         (True,
          {'checksum': 'b9628c4ab9b595f72f280b90c4fd093d',
           'path': 'full/1ca5879492b8fd606df1964ea3c1e2f4520f076f.jpg',
           'url': 'http://www.example.com/images/product2.jpg'}),
         (False,
          Failure(...))
        ]
        """
        if isinstance(item, JobboleDemoItem):
            image_paths = [image_dict['path'] for status, image_dict in results if status]
            if not image_paths:
                #DropItem：丢弃item
                raise DropItem("Item contains no images")
            #获取图片的下载路径
            item['localimagepath'] = image_paths[0]

        return item

################mysql数据库存储################
#实现item和管道文件的解藕
class JobboleDemoPipeline(object):

    # def __init__(self):
    #     #创建数据库链接
    #     self.client = pymysql.Connect(
    #         host='127.0.0.1',user='root',
    #         password='ljh1314',database='class1811',
    #         port=3306,charset='utf8'
    #     )
    #     #创建游标
    #     self.mycursor = self.client.cursor()

    def __init__(self,host,user,password,port,database,charset):
        #创建数据库链接
        self.client = pymysql.Connect(
            host=host,user=user,
            password=password,database=database,
            port=port,charset=charset
        )
        #创建游标
        self.mycursor = self.client.cursor()

    @classmethod
    def from_crawler(cls,crawler):
        # MYSQL_HOST = '127.0.0.1'
        # MYSQL_USER = 'root'
        # MYSQL_PASSWORD = 'ljh1314'
        # MYSQL_PORT = 3306
        # MYSQL_DATABASE = 'class1811'
        # MYSQL_CHARSET = 'utf8'
        host = crawler.settings['MYSQL_HOST']
        user = crawler.settings['MYSQL_USER']
        password = crawler.settings['MYSQL_PASSWORD']
        port = crawler.settings['MYSQL_PORT']
        database = crawler.settings['MYSQL_DATABASE']
        charset = crawler.settings['MYSQL_CHARSET']

        return cls(host,user,password,port,database,charset)

    def process_item(self, item, spider):
        """
        :param item: 指的是spider爬虫文件中yield的item数据对象
        :param spider:
        :return:
        """

        item_dict = dict(item)

        print('经过了管道', item_dict)

        sql_insert, values = item.get_sql_str_values(item_dict)

        try:
            self.mycursor.execute(sql_insert,values)
            self.client.commit()
        except Exception as err:
            print(err)
            self.client.rollback()

        # 注意这里只有return item，下一个管道才能接收
        return item


    def close_spider(self,spider):
        """可选方法,爬虫结束的时候会执行一次"""
        self.client.close()
        self.mycursor.close()
        print('爬虫结束')


#########mysql异步插入（提高插入数据的效率）##############

# import pymysql
#twisted是一个异步的网络框架，这里可以帮助我们
# 实现异步将数据插入数据库
# adbapi里面的子线程会去执行数据库的阻塞操作，
# 当一个线程执行完毕之后，同时，原始线程能继续
# 进行正常的工作，服务其他请求。

from twisted.enterprise import adbapi

#mysql数据异步插入
# class JobboleDemoPipeline(object):
#
#     def __init__(self,dbpool):
#         self.dbpool = dbpool
#
#     #使用这个函数来应用settings配置文件。
#     @classmethod
#     def from_crawler(cls, crawler):
#         parmas = {
#             'host':crawler.settings['MYSQL_HOST'],
#             'user':crawler.settings['MYSQL_USER'],
#             'passwd':crawler.settings['MYSQL_PASSWORD'],
#             'db':crawler.settings['MYSQL_DATABASE'],
#             'port':crawler.settings['MYSQL_PORT'],
#             'charset':crawler.settings['MYSQL_CHARSET'],
#         }
#
#         # **表示字典，*tuple元组,
#         # 使用ConnectionPool，返回的是一个ThreadPool
#         dbpool = adbapi.ConnectionPool(
#             'pymysql',
#             **parmas
#         )
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         #这里去调用任务分配的方法
#         query = self.dbpool.runInteraction(
#             self.insert_data_todb,
#             item,
#             spider
#         )
#         #数据插入失败的回调
#         query.addErrback(
#             self.handle_error,
#             item
#         )
#
#     # 执行数据插入的函数
#     def insert_data_todb(self,cursor,item,spider):
#         insert_str,parmas = item.get_sql_str_values()
#         cursor.execute(insert_str,parmas)
#         print('插入成功')
#
#     def handle_error(self,failure,item):
#         print(failure)
#         print('插入错误')
#         #在这里执行你想要的操作
#
#     def close_spider(self, spider):
#         self.pool.close()

############mongodb数据插入#################

# class JobboleDemoPipeline(object):
#
#     # def __init__(self):
#     #     #创建数据库链接
#     #     self.client = pymysql.Connect(
#     #         host='127.0.0.1',user='root',
#     #         password='ljh1314',database='class1811',
#     #         port=3306,charset='utf8'
#     #     )
#     #     #创建游标
#     #     self.mycursor = self.client.cursor()
#
#     def __init__(self, host, port, database):
#         # 创建数据库链接
#         self.client = pymongo.MongoClient(host=host,port=port)
#         #获取要操作的数据库
#         self.db = self.client[database]
#         # 创建游标
#         self.mycursor = self.client.cursor()
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         host = crawler.settings['MONGO_HOST']
#         port = crawler.settings['MONGO_PORT']
#         database = crawler.settings['MONGO_DATABASE']
#
#         return cls(host, port, database,)
#
#     def process_item(self, item, spider):
#         """
#         :param item: 指的是spider爬虫文件中yield的item数据对象
#         :param spider:
#         :return:
#         """
#
#         item_dict = dict(item)
#         print('经过了管道', item_dict)
#         #sql_insert, values = item.get_sql_str_values(item_dict)
#         collection_name = item.get_collection_name()
#         col = self.db[collection_name]
#         try:
#             col.insert(item_dict)
#         except Exception as err:
#             print(err)
#         # 注意这里只有return item，下一个管道才能接收
#         return item
#
#     def open_spider(self,spider):
#         """可选方法,爬虫开启的时候会执行一次"""
#         print('爬虫开启')
#
#     def close_spider(self,spider):
#         """可选方法,爬虫结束的时候会执行一次"""
#         self.client.close()
#         print('爬虫结束')




