# -*- coding: utf-8 -*-

BOT_NAME = 'agendas'

SPIDER_MODULES = ['agendas.spiders']
NEWSPIDER_MODULE = 'agendas.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'agendas (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '32780',
    'username': 'postgres',
    'password': '',
    'database': ''
}

ITEM_PIPELINES = {
   'agendas.pipelines.AgendasPipeline': 300,
}

LOG_LEVEL='INFO'

