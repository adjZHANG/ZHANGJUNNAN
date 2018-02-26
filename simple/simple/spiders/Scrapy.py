# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class ScrapySpider(scrapy.Spider):
    name = 'Scrapy'
  #  allowed_domains = ['forum.innjoo.com']
    def start_requests(self):
        url='http://forum.innjoo.com/search.php?searchsubmit=yes'
        key_list=['recover message','recover photos','recover contacts','recover messages','recover call history','recover whatsapp']
        for key in key_list:
            yield scrapy.FormRequest(
               url=url,
              formdata={'srchtxt':key},
                callback=self.parse
         )





    def parse(self, response):
        node_list = response.xpath("//li[@class='pbw']")
        for node in node_list:
            item = SimpleItem()
            item['title'] = node.xpath("./h3/a/text()").extract()[0]
            item['sourceURL'] = "http://forum.innjoo.com/" + node.xpath("./h3/a/@href").extract()[0]
            item['time'] = node.xpath("./p/span[1]/text()").extract()[0]
            item['host'] = node.xpath("./p/span[2]/a/text()").extract()[0]
            yield item


            if  len(response.xpath("//a[@class='nxt']/@href")):
                url=response.xpath("//a[@class='nxt']/@href").extract()[0]
                yield scrapy.Request("http://forum.innjoo.com/" + url,callback=self.parse)