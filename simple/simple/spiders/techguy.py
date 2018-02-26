# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class TechguySpider(scrapy.Spider):
    name = 'techguy'
  #  allowed_domains = ['forums.techguy.org']
    start_urls = ['https://forums.techguy.org/search/20842179/?q=recover+message&o=date&c[title_only]=1',
                 'https://forums.techguy.org/search/20842932/?q=recover+photos&o=date',
                 'https://forums.techguy.org/search/20842979/?q=recover+videos&o=date',
                'https://forums.techguy.org/search/20843020/?q=recover+whatsapp&o=date',
                  'https://forums.techguy.org/search/20843071/?q=recover+contacts&o=date'
    ]

    def parse(self, response):
        node_list = response.xpath("//li[starts-with(@id,'thread')] |  //li[starts-with(@id,'post')]")
        for node in node_list:
            item = SimpleItem()
            title = node.xpath(".//h3[@class='title']/a")
            item['title'] = title[0].xpath('string(.)').extract()[0]
            item['sourceURL'] = "https://forums.oneplus.net/" + node.xpath("//h3/a/@href").extract()[0]
            item['time'] = node.xpath(".//abbr/@title | .//span[@class='DateTime']/text()").extract()
            item['host'] = node.xpath(".//a[@class='username']/text()").extract()[0]
            yield item



            if len(response.xpath("//*[@id='content']/div/div/div[3]/div[2]/nav/a[last()][@class='text']/@href")):
                url = response.xpath("//*[@id='content']/div/div/div[3]/div[2]/nav/a[last()][@class='text']/@href").extract()[0]
                yield scrapy.Request("https://forums.techguy.org/" + url, callback=self.parse)

