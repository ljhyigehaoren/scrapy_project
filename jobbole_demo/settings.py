# -*- coding: utf-8 -*-

# Scrapy settings for jobbole_demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# 使用 startproject 命令创建项目时会被自动赋值。
BOT_NAME = 'jobbole_demo'

#指定爬虫文件的存储路径
SPIDER_MODULES = ['jobbole_demo.spiders']
NEWSPIDER_MODULE = 'jobbole_demo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT：模拟浏览器访问对方服务器
USER_AGENT = 'jobbole_demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
#是否遵循robot协议
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#设置最大的请求并发数量default: 16
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:

#设置最大请求的并发数量，CONCURRENT_REQUESTS_PER_DOMAIN是针对域的
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#爬虫中间件,可以在这里激活，数字越小，优先级越高
#SPIDER_MIDDLEWARES = {
#    'jobbole_demo.middlewares.JobboleDemoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

#下载中间件,可以在这里激活，数字越小，优先级越高
#DOWNLOADER_MIDDLEWARES = {
#    'jobbole_demo.middlewares.JobboleDemoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# #设置扩展插件
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

################scrapy_redis配置#####################
# 设置DUPEFILTER_CLASS,使用scrapy_redis的去重组件,
# 不再使用scrapy自带的去重组件了
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 设置SCHEDULER，使用scrapy_redis的调度器组件
# 不再使用scrapy自带的调度器组件了
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#不清除redis的请求记录（队列）, 允许暂停和停止爬取
SCHEDULER_PERSIST = True

#设置请求任务的队列模式
#SpiderPriorityQueue 是scrapy_redis框架默认的队列模式(有自己的优先级)
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SpiderQueue 是请求的队列模式(FifoQueue),先进先出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SpiderStack 是请求的队列模式(LifoQueue),后进先出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

#设置redis数据库的ip和端口
REDIS_HOST = '118.24.255.219'
REDIS_PORT = 6380

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 激活管道，后面的数字表示优先级,数字越小优先级越高
ITEM_PIPELINES = {
   #激活图片下载管道
   # 'jobbole_demo.pipelines.MyImagesPipeline':299,
   # 'jobbole_demo.pipelines.JobboleDemoPipeline': 300,
   # 'jobbole_demo.pipelines.JobboleDemoPipeline2': 301,
   #RedisPipeline,将所有爬虫所获取的数据，统一存储在redis数据库
   'scrapy_redis.pipelines.RedisPipeline': 400,
}

#设置图片存储的路径
IMAGES_STORE = '/Users/ljh/Desktop/chinazimage/'




# 自动限速扩展（默认是关闭的）
# # Enable and configure the AutoThrottle extension (disabled by default)
# # See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# #初始下载延时
# AUTOTHROTTLE_START_DELAY = 1
# # The maximum download delay to be set in case of high latencies
# #最大下载延时
# AUTOTHROTTLE_MAX_DELAY = 20
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False


#缓存区
# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 24*60*60
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = [404,500]
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#设置mysql配置
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ljh1314'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'class1811'
MYSQL_CHARSET = 'utf8'


MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_DATABASE = 'class1811'


# LOG_ENABLED = False
#将日志信息保存在本地文件
# LOG_FILE = "chinaz.log"
# #设置日志的等级
# LOG_LEVEL = "DEBUG"