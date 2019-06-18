# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobboleDemoCategoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    # 网站分类
    webcategory = scrapy.Field()
    #分类的url地址
    url = scrapy.Field()


    def get_sql_str_values(self,data):
        """获取sql语句和要插入到数据库中的数据"""
        sql_insert = """
                INSERT INTO %s (%s)
                VALUES (%s)
                """ % (
            'chinazcategory',
            ','.join(data.keys()),
            ','.join(['%s'] * len(data))
        )
        values = list(data.values())

        return sql_insert,values

    def get_collection_name(self):
        return 'chinazcategory'



class JobboleDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    # 网站分类
    webcategory = scrapy.Field()
    #封面图
    coverimage = scrapy.Field()
    #标题
    webtitle = scrapy.Field()
    #网站简介
    webinfo = scrapy.Field()
    #本地图片地址
    localimagepath = scrapy.Field()
    # ....

    def get_sql_str_values(self, data):
        """获取sql语句和要插入到数据库中的数据"""
        sql_insert = """
                INSERT INTO %s (%s)
                VALUES (%s)
                """ % (
            'chinaz',
            ','.join(data.keys()),
            ','.join(['%s'] * len(data))
        )
        values = list(data.values())

        return sql_insert, values

    def get_collection_name(self):

        return 'chinaz'
