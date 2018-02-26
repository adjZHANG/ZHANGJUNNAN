# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem


class SearchSpider(scrapy.Spider):
    name = 'Search'
    allowed_domains = ['forum.kernelnewbies.org']
    start_urls = ['https://forum.kernelnewbies.org/search.php?0,search=recover+photos,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=',
                   'https://forum.kernelnewbies.org/search.php?0,search=recover+messages,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=0',
                   'https://forum.kernelnewbies.org/search.php?0,search=recover+videos,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=0',
                   'https://forum.kernelnewbies.org/search.php?0,search=recover+whatsapp,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=0',
                    'https://forum.kernelnewbies.org/search.php?0,search=recover+call+history,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=0',
                   'https://forum.kernelnewbies.org/search.php?0,search=recover+contacts,author=,page=1,match_type=ALL,match_dates=365,match_forum=ALL,match_threads=0'

]#此网站搜索的内容可直接在网址上面该search后面的内容

    def parse(self, response):
        node_list = response.xpath("//*[@id='phorum']/div[7]/div")
        for node in node_list:
            item = SimpleItem()
            item['title'] = node.xpath(".//h4/a/text()").extract()[0]
            item['sourceURL'] = node.xpath(".//h4/a/@href").extract()[0]
            item['time'] = node.xpath(".//h4/small/text()").extract()[0]
            item['host'] = node.xpath(".//strong/text()").extract()[0]
            yield item

            if len(response.xpath("//a[@title='Next']/@href")):
                url = response.xpath("//a[@title='Next']/@href").extract()[0]
                yield scrapy.Request(url, callback=self.parse)
