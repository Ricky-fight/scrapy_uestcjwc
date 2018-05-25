# -*- coding: utf-8 -*-
import scrapy
from uestcjwc.items import UestcItem
import pymysql
import zmail

class UestcSpider(scrapy.Spider):
    name = 'uestcjwc'
    allowed_domains = ['www.jwc.uestc.edu.cn']
    start_urls = [
        "http://www.jwc.uestc.edu.cn/web/News!queryList.action?partId=256"
    ]

    def parse(self, response):
        def mail(url, title):
            server = zmail.server('18918735979@163.com', 'xw64153869')

            mail = {
                'subject': '教务处有新公告:%s' %(title),
                'content_html': url,
            }
            server.send_mail('18918735979@163.com', mail)
            pass
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='xingwei',
                                     password='ricky998927',
                                     db='uestcjwc',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        filename = response.url.split("/")[-2]
        # itemlist = []
        id = response.xpath('//div[@class="textAreo clearfix"]/a/@newsid').extract()
        title = response.xpath('//div[@class="textAreo clearfix"]/a/@title').extract()
        date = response.xpath('//div[@class="textAreo clearfix"]/i/text()').extract()
        # with open(filename,'wb') as file:
        #     file.write(response.body)
        # with open("news", 'a') as file:
        #     for i in range(len(id)):
        #         file.write(str(id[i]) + ":" + title[i] + '\n')
                # print(str(id[i]) + ":" + title[i] + '\n')
        try:
            with connection.cursor() as cursor:
                # Create a new record
                for i in range(len(id)):
                    selectsql = "select * from news where newsid = %s"
                    cursor.execute(selectsql, (id[i]))
                    result = cursor.fetchone()
                    if result is None:
                        print('---------!!New record!!--------')
                        insertsql = "INSERT INTO `news` VALUES (%s, %s, %s)"
                        cursor.execute(insertsql, (id[i], title[i], date[i]))
                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()
                        #send email
                        url = 'http://www.jwc.uestc.edu.cn/web/News!view.action?id=%s' % (id[i])
                        mail(url,title[i])
                    else:
                        print('---------!!Old record!!--------')
                    pass
            # mail('http://www.jwc.uestc.edu.cn/web/News!view.action?id=1', title[i])
            # mail(response.body.decode(), title[i])
        finally:
            connection.close()
        # for i in range(len(id)):
        #     item = UestcItem()
        #     item['newsid'] = id[i]
        #     item['title'] = title[i]
        #     # itemlist.append(item)
        #     yield item
