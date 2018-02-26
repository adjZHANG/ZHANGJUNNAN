# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class ZinfSpider(scrapy.Spider):
    name = 'zinf'
    allowed_domains = ['http://www.zinf.org']
    start_urls = ['http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+message&sa=&qtype=answered',
                  'http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+photos&sa=&qtype=answered',
                  'http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+videos&sa=&qtype=answered',
                  'http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+whatsapp&sa=&qtype=answered',
                  'http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+call+history&sa=&qtype=answered',
                  'http://www.zinf.org/qna/categorydetail.php?cmd=search&q=recover+contacts&sa=&qtype=answered',
                ]
   # '+ i for i in ("messages","photos","videos","whatsapp","call+history","contacts") + '
    def parse(self, response):
        node_list = response.xpath("//td[@class='info']")
        for node in node_list:
            item = SimpleItem()
            title=node.xpath("./span/div/a/b/text()").extract()[0]
            item['title']=title[:-1]
            item['sourceURL'] = "http://www.zinf.org/" + node.xpath("./span/div/a/@href").extract()[0]
            time = node.xpath(".//span[@style='color:#777777']")
            time2 = time[0].xpath('string(.)').extract()[0]
            item['time']=time2[-10:]
            item['host'] = node.xpath(".//span[@style='color:#777777']/a[1]/text()").extract()[0]
            yield item
