# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem


class AsusSpider(scrapy.Spider):
    name = 'asus'
    allowed_domains = ['cse.google.com']
    start_urls = ['https://cse.google.com/cse?cx=008543022935876211394%3A94vzevcyurc&cof=FORID%3A0&q=recover+message#gsc.tab=0&gsc.q=recover%20message&gsc.page=1']

    def parse(self, response):
        node_list = response.xpath("//div[@class='gsc-webResult gsc-result']")
        for node in node_list:
            item = SimpleItem()
            title = node.xpath(".//tbody/tr/td/div/a")
            item['title'] = title[0].xpath('string(.)').extract()[0]
            item['sourceURL'] = node.xpath(".//div[starts-with(@class,'gs-title gsc')]/a/@href").extract()[0]
            time0=node.xpath("//div[starts-with(@class,'gs-bidi-start-align gs-snippet') and @dir='ltr']")
            time1=time0[0].xpath('string(.)').extract()[0]
            time2=time1[0:12]
            item['time']=time2
            item['host'] = "***"
            yield item