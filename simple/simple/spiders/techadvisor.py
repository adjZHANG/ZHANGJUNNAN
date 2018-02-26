# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem

class TechadvisorSpider(scrapy.Spider):
    name = 'techadvisor'
    allowed_domains = ['www.techadvisor.co.uk']
    start_urls = ['https://www.techadvisor.co.uk/search/run/?searchTerm=recover+contacts']
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }
    def parse(self,response):
        node_list1=response.xpath("//div[@class='gsc-webResult gsc-result']")
        for URL in node_list1:
            global URL1
            URL1= URL.xpath(".//div[@class='gs-title']/a[@class='gs-title']/@href").extract()[0]
            yield scrapy.Request(URL1,callback=self.parse1)



    def parse1(self, response):
        node_list = response.xpath("//header[@id='articleWideHeader']")
        for node in node_list:
            item = SimpleItem()
            item["title"] = node.xpath("./h1/text()").extract[0]
            item['sourceURL'] = URL1
            time0 = node.xpath(".//span[@class='publicationDate']/time")
            time1 = time0[0].xpath('string(.)').extract()[0]
            time2 = time1[2:]
            item['time'] = time2
            item['host'] = node.xpath("//span[@class='author']/a/text()").extract()[0]
            yield item