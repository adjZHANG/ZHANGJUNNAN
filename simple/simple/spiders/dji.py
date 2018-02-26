# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem


class DjiSpider(scrapy.Spider):
    name = 'dji'
    # allowed_domains = ['forum.dji.com']
    start_urls = ['https://forum.dji.com/']

    def parse(self, response):
        node_URL = ['https://forum.dji.com/forum-115-1.html',
                    'https://forum.dji.com/forum-104-1.html',
                    'https://forum.dji.com/forum-68-1.html',
                    'https://forum.dji.com/forum-61-1.html',
                    'https://forum.dji.com/forum-91-1.html',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=125',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=118',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=121',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=90',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=79&filter=author&orderby=dateline',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=96',
                    'https://forum.dji.com/forum.php?mod=forumdisplay&fid=123']
        #上面是这个论坛所有的子论坛，重定向到每个子论坛里面的链接
        for node in node_URL:
            URL =  node
            print URL
            yield scrapy.Request(URL, callback=self.parse1)

    def parse1(self, response):

        node_list = response.xpath("//div[@class='thread_one'] | // tbody[starts-with(@id,'stickthread')] | //tbody[starts-with(@id,'nor')]")
        for node2 in node_list:
            item = SimpleItem()
            key_list=['photos','message','whatapp','video','call history','contact']
            # key_list=['recover message','Recover video']
            # 筛选整个论坛标题带有关键字的帖子
            title= node2.xpath(".//a[@class='s xst']/text() |  .//div[@class='thread_title']/a/text()").extract()[0]
            for key  in key_list:
                if key in title:
                    item['title']=node2.xpath(".//a[@class='s xst']/text() |  .//div[@class='thread_title']/a/text()").extract()[0]
                    item['sourceURL'] = "https://forum.dji.com/" + node2.xpath(".//div[@class='thread_title']/a/@href | .//a[@class='s xst']/@href").extract()[0]
                    time= node2.xpath(".//div[@class='thread_info']/span[2]/text() | //div[@class='h_thread_v']/span[1]/text()").extract()[0]
                    time1 = time[14:]
                    time2 = time1[:-11]
                    item['time'] = time2
                    host = node2.xpath(".//span[@class='thread_author_info']/a/text() |  .//a[@class='h_poster']/text()").extract()[0]
                    host1=host[2:]
                    host2=host1[:-7]
                    item['host']=host2

                    yield item

                    if len(response.xpath("//a[@class='nxt']/@href")):
                        url = response.xpath("//a[@class='nxt']/@href").extract()[0]
                        yield scrapy.Request("https://forum.dji.com/" + url, callback=self.parse1)



