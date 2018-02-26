# -*- coding: utf-8 -*-
import scrapy
from simple.items import SimpleItem


class FreeSpider(scrapy.Spider):
    name = 'free'
    # allowed_domains = ['freeadzforum.com']
    baseURL_list =['http://www.freeadzforum.com/index.php?action=search2;params=eJwtzc0KwyAQBOBXKb30Moeo6d_TiNGFpNhsWY2l4MNXQ27DxwzjQnGrp1AvdajnOklPd2gDjSe0hsEVI254QI9QA5SC0lCmldPMX-v5_YmUqc06bdOLfLa8xt8hLLkloUj700E2LNI4UPJdyImf95rnQnIqSyBOf7MRNwM.;start=',
             'http://www.freeadzforum.com/index.php?action=search2;params=eJwtzc0KwjAQBOBXES9e5tBs6t_TlHSzWCVtZBMrQh7epPQ2fMwwzq9uYfHlVLpyLKO2dAVZEO4ggsUZPS64gXqYDsbAEIyt5TTF78BxfgfJUmeNPuNLOA9xCb9douaaVIJsTzsN_qmVvSRuIk552mocV9HDLCm5h6Q_IkM30Q..;start='
             # "http://www.freeadzforum.com/index.php?action=search2;params=eJwtzc0KwyAQBOBXKb30Moeo6d_TiNGFpNhsWY2l4MNXQ27DxwzjQnGrp1AvdajnOklPd2gDjSe0hsEVI254QI9QA5SC0lCmldPMX-v5_YmUqc06bdOLfLa8xt8hLLkloUj700E2LNI4UPJdyImf95rnQnIqSyBOf7MRNwM.;start="
            ]
    for baseURL in baseURL_list:
        print baseURL + "****"

        offset = 0
        start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//div[@class='search_results_posts']")
        for node in node_list:
            item = SimpleItem()
            title = node.xpath(".//h5/a[2]")
            item['title'] = title[0].xpath('string(.)').extract()[0]
            item['sourceURL'] = node.xpath(".//h5/a[2]/@href").extract()[0]
            item['time'] = node.xpath(".//span/em/text()").extract()[0]
            item['host'] = node.xpath(".//span[@class='smalltext']/strong/text() | .//span[@class='smalltext']/strong/a/text()").extract()[0]
            yield item
            if self.offset < 120:
                self.offset += 30
                url = self.baseURL + str(self.offset)
                yield scrapy.Request(url, callback=self.parse)
