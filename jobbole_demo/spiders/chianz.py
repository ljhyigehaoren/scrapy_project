# -*- coding: utf-8 -*-
import scrapy
from jobbole_demo.items import JobboleDemoItem,JobboleDemoCategoryItem
from urllib import parse
from scrapy_redis.spiders import RedisSpider


# class ChianzSpider(scrapy.Spider):
class ChianzSpider(RedisSpider):
    name = 'chianz'
    allowed_domains = ['chinaz.com']
    #设置起始url
    # start_urls = ['http://top.chinaz.com/hangyemap.html']
    #获取起始url任务
    redis_key = 'chianz:start_urls'

    def parse(self, response):
        #获取状态码
        print(response.status)
        #将获取的页面源码写入本地
        # with open('page.html','w') as file:
        #     file.write(response.text)

        ##########使用xpath获取标签
        #获取分类的a标签
        # catrgoey_elements = response.xpath('//div[@class="TopAlist clearfix"]/div[@class="Taright"]/a')
        # print(len(catrgoey_elements))
        #
        # for a_element in catrgoey_elements:
        #     #extract()节点属性或文本内容
        #     href_url = a_element.xpath('./@href').extract()[0]
        #     #extract_first(''),获取列表中的第一个元素，如果列表为空,返回None,
        #     #也可以设置默认值（即如果列表为空,返回默认值）
        #     href_url = a_element.xpath('./@href').extract_first('')
        #     #分类名称
        #     title = a_element.xpath('./text()').extract_first('')
        #
        #     print(href_url,title)

        ##########使用css获取标签
        # 获取分类的a标签
        catrgoey_elements = response.css('div.TopAlist.clearfix div.Taright a')
        for a_element in catrgoey_elements:
            category_item = JobboleDemoCategoryItem()
            # 分类的url地址
            href_url = a_element.css('::attr(href)').extract_first('')
            # 分类名称
            title = a_element.css('::text').extract_first('')
            category_item['webcategory'] = title
            category_item['url'] = href_url

            yield category_item

            # print(href_url,title)

            """
             url, 目标url地址
             callback=None, 回调函数
             method='GET', 
             headers=None, 请求头
             cookies=None, cookies
             meta=None, 字典类型，传递参数
             priority=0, 设置优先级
             dont_filter=False, 是否去重
            """
            yield scrapy.Request(url=href_url,
                           callback=self.parse_page_data,
                           meta={'title':title}
                           )

    def parse_page_data(self,response):

        print(response.status,'分类列表请求成功')
        #获取传递进来的分类标题
        category_name = response.meta['title']

        web_elements = response.xpath('//ul[@class="listCentent"]/li')

        for li in web_elements:
            #实例化
            web_item = JobboleDemoItem()
            web_item['coverimage'] = li.xpath('.//div[@class="leftImg"]/a/img/@src').extract_first('')
            web_item['webtitle'] = li.xpath('.//h3[@class="rightTxtHead"]/a/text()').extract_first('')
            url = li.xpath('.//h3[@class="rightTxtHead"]/a/@href').extract_first('')
            full_url = response.urljoin(url)
            web_item['webinfo'] = li.xpath('.//p[@class="RtCInfo"]/text()').extract_first('')
            web_item['webcategory'] = category_name
            # print(web_item)

            #将数据交给管道文件，一定要去settings文件中激活管道
            yield web_item

            yield scrapy.Request(full_url,callback=self.parse_detail_data)



        #提取下一页
        next_pages = response.xpath('//div[@class="ListPageWrap"]/a/@href').extract()
        if next_pages:
            for page_url in next_pages:
                if '.html' in page_url:
                    # full_url = 'http://top.chinaz.com/hangye/'+page_url
                    # full_url = parse.urljoin(response.url,page_url)
                    full_url = response.urljoin(page_url)
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.parse_page_data,
                        meta={'title':category_name}
                    )

    def parse_detail_data(self,response):
        print('详情',response.status)











