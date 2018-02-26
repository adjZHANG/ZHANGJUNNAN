# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class ScottSpider(scrapy.Spider):
    name = 'scott'
 #   allowed_domains = ['http://forum.rspwfaq.net']
    start_urls = ['http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+contacts&days=0',
                  'http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+message&days=0',
                  'http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+photos&days=0',
                  'http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+videos&days=0',
                  'http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+whatsapp&days=0',
                  'http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+call+history&days=0'
                   ]
#                   ['http://forum.rspwfaq.net/template/NamlServlet.jtp?macro=search_page&node=1&query=recover+contacts&days=0']
    def parse(self, response):
        node_list = response.xpath("//div[@style='margin-bottom:1.5em']")
        for node in node_list:
            item = SimpleItem()
            title = node.xpath(".//span[@class='second-font big-title']/a")
            item['title'] = title[0].xpath('string(.)').extract()[0]
            item['sourceURL'] = node.xpath(".//span[@class='second-font big-title']/a/@href").extract()[0]
            if len(node.xpath("//div[@class='weak-color']/span/@title")):
                item['time']=node.xpath("//div[@class='weak-color']/span/@title").extract()
            else:
                item['time'] = "****"
            #时间获取不到

            item['host'] = node.xpath(".//div[@class='weak-color']/a[last()]/text()").extract()[0]
            yield item

            if response.xpath("//div[starts-with(@style,'font-size:90%')]/a[last()]/text()").extract()[0] == "Next 12 »" :
                url = response.xpath("//div[starts-with(@style,'font-size:90%')]/a[last()]/@href").extract()[0]
                yield scrapy.Request("http://forum.rspwfaq.net" + url,
                                     callback=self.parse)
