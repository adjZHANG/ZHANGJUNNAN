# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class OneplusSpider(scrapy.Spider):
    name = 'OnePlus'
    allowed_domains = ['forums.oneplus.net']
    start_urls = ['https://forums.oneplus.net/search/19411723/?q=recover+phone&o=relevance&c[title_only]=1'
                    'https://forums.oneplus.net/search/19413758/?q=recover+messages&o=relevance&c[title_only]=1',
                  'https://forums.oneplus.net/search/19412735/?q=recover+videos&o=relevance&c[title_only]=1',
                  'https://forums.oneplus.net/search/19413797/?q=recover+whatsapp&o=relevance&c[title_only]=1',
                  'https://forums.oneplus.net/search/19412751/?q=recover+call+history&o=relevance&c[title_only]=1',
                  'https://forums.oneplus.net/search/19412730/?q=recover+contacts&o=relevance&c[title_only]=1'
                  ]

    def parse(self, response):
        node_list = response.xpath("//li[starts-with(@id,'thread')]")
        for node in node_list:
            item = SimpleItem()
            title = node.xpath(".//h3[@class='title']/a")
            item['title']=title[0].xpath('string(.)').extract()[0]
            item['sourceURL'] = "https://forums.oneplus.net/" + node.xpath("//h3/a/@href").extract()[0]
            item['time'] = node.xpath(".//span[@class='DateTime']/text() | .//abbr[@class='DateTime']/text()").extract()[0]
            item['host'] = node.xpath(".//a[@class='username']/text()").extract()[0]
            yield item

            # if len(response.xpath("//a[@class='nxt']/@href")):
            #     url = response.xpath("//a[@class='nxt']/@href").extract()[0]
            #     yield scrapy.Request("http://forum.innjoo.com/" + url, callback=self.parse)
