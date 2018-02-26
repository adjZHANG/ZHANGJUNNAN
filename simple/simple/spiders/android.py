# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem


class AndroidSpider(scrapy.Spider):
    name = 'android'
    #allowed_domains = ['http://www.androidquestions.org']
    def start_requests(self):
        url = 'http://www.androidquestions.org/search.php?do=process'
        key_list = ['recover message', 'recover photos', 'recover contacts', 'recover messages',
                    'recover call history', 'recover whatsapp']
        for key in key_list:
            yield scrapy.FormRequest(
                url=url,
                formdata={'query': key},
                callback=self.parse
            )

    def parse(self, response):
        node_list = response.xpath("//li[starts-with(@id,'thread_')]")
        for node in node_list:
            item = SimpleItem()
            item['title'] = node.xpath(".//a[starts-with(@id,'thread_title')]/text()").extract()[0]
            item['sourceURL'] = "http://www.androidquestions.org/"+node.xpath(".//a[starts-with(@id,'thread_title')]/@href").extract()[0]
            time0 = node.xpath(".//div[@class='author']/span")
            time1 = time0[0].xpath('string(.)').extract()[0]
            time2 = time1[-20:]
            item['time'] = time2
            item['host'] = node.xpath("//div[@class='author']/span/a/text()").extract()[0]
            yield item

            if len(response.xpath("//a[@rel='next']/@href")):
                url = response.xpath("//a[@rel='next']/@href").extract()[0]
                yield scrapy.Request("http://www.androidquestions.org/" + url, callback=self.parse)
