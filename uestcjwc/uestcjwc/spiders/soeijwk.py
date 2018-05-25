# -*- coding: utf-8 -*-
import scrapy


class SoeijwkSpider(scrapy.Spider):
    name = 'soeijwk'
    allowed_domains = ['www.soei.uestc.edu.cn']
    start_urls = ['http://www.soei.uestc.edu.cn/index.php?m=article&a=lists&sortid=24']

    def parse(self, response):
        pass
