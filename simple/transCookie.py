# -*- coding: utf-8 -*-

class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = "bblastvisit=1518055038; PHPSESSID=ulu8lio3c5kk7ohtgro3vtcut3; _ga=GA1.2.684442029.1518055042; _gid=GA1.2.1097327920.1518055042; bblastactivity=1518055466; bbsessionhash=95b0ecf068f4df4cdf1bef69c2226b33; bbpassword=d0c82adfb1dfe6c645565441bc23e6a8356ac47b315ffc13229f8610; bbuserid=91150; bbdiscussion_view=%7B.3307.-1518055041%2C.24306.-1518056510%7D"
    trans = transCookie(cookie)
    print trans.stringToDict()