import os

# -*- coding: utf-8 -*-

base_dir = os.path.abspath(os.path.dirname(__file__))

BOT_NAME = 'agendas'
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2

SPIDER_MODULES = ['agendas.spiders']
NEWSPIDER_MODULE = 'agendas.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'agendas (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False

# DATABASE = {
#     'drivername': 'postgres',
#     'host': 'localhost',
#     'port': '32780',
#     'username': 'postgres',
#     'password': '',
#     'database': ''
# }

DATABASE = {'drivername': 'sqlite', 'database': 'app.db'}

ITEM_PIPELINES = {
   'agendas.pipelines.AgendasPipeline': 300,
}

LOG_LEVEL='INFO'

