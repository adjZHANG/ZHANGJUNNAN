# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem
from scrapy.conf import settings

class AxigenSpider(scrapy.Spider):
    name = 'axigen'
    #allowed_domains = ['www.axigen.com']
    start_urls = ['https://www.axigen.com/forum/search?q=recover+message&searchJSON=%7B%22keywords%22%3A%22recover+message%22%7D',
                    'https://www.axigen.com/forum/search?q=recover+photos&searchJSON=%7B%22keywords%22%3A%22recover+photos%22%7D',
                    'https://www.axigen.com/forum/search?q=recover+videos&searchJSON=%7B%22keywords%22%3A%22recover+videos%22%7D',
                    'https://www.axigen.com/forum/search?q=recover+whatsapp&searchJSON=%7B%22keywords%22%3A%22recover+whatsapp%22%7D',
                    'https://www.axigen.com/forum/search?q=recover+call+history&searchJSON=%7B%22keywords%22%3A%22recover+call+history%22%7D',
                    'https://www.axigen.com/forum/search?q=recover+contacts&searchJSON=%7B%22keywords%22%3A%22recover+contacts%22%7D'
                    ]
    cookie = settings['COOKIE']
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookie)  # 这里带着cookie发出请求


    def parse(self, response):
        node_list = response.xpath("//li[@data-node-id]")
        for node in node_list:
            item = SimpleItem()
            item['title'] = node.xpath(".//a[@class='b-post__stream-post-title starter']/text()").extract()[0]
            item['sourceURL'] = node.xpath(".//a[@class='b-post__stream-post-title starter']/@href").extract()[0]
            item['time'] = node.xpath(".//time[@itemprop='dateCreated']/text()").extract()[0]
            item['host'] = node.xpath(".//a[@class='user-profile author']/text()").extract()[0]
            yield item
            if len(response.xpath("//a[@class='js-pagenav-button js-pagenav-next-button b-button b-button--secondary js-shrink-event-child']/@href")):
                url=response.xpath("//a[@class='js-pagenav-button js-pagenav-next-button b-button b-button--secondary js-shrink-event-child']/@href").extract()[0]
                yield scrapy.Request(url,callback=self.parse)