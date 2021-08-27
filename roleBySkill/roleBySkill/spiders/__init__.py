# 这个包将包含您的Scrapy项目的爬虫
#
# 有关如何创建和管理的信息，请参阅文档
# 您的爬虫

import scrapy
import time
import json

from ..items import RolebyskillItem


class RolebyskillSpider(scrapy.Spider):
    name = 'roleBySkill'
    url1 = 'http://jishi.woniu.com/9yin/anonymous/findSellingGoods.do?serverId=186100101&gameId=10&auctionFirst=1&filterItem=4'
    url2 = 'http://jishi.woniu.com/9yin/anonymous/findNoticeGoods.do?serverId=186100101&gameId=10&auctionFirst=1&filterItem=4'
    time_stamp = str(int(time.time()*1000))
    allowed_domains = ['woniu.com']
    start_urls = [url1 + '&_=' + time_stamp,url2 + '&_=' + time_stamp]

    def parse(self, response):
        print('初始请求：' + response.url)
        sites = json.loads(response.text)
        totalPages = sites[0]['pageInfo']['totalPages']
        for i in range(1,totalPages+1):
            new_time_stamp = '&_=' + str(int(time.time()*1000))
            if response.url.find('Selling') != -1 :
                newUrl = self.url1 + '&pageIndex=' +str(i) + new_time_stamp
            else:
                newUrl = self.url2 + '&pageIndex=' +str(i) + new_time_stamp
            print('目标请求：' + newUrl)
            yield scrapy.Request(newUrl, callback=self.parse_content)

    def parse_content(self, response):
        print('分页请求：' + response.url)
        sites = json.loads(response.text)
        for i in sites[0]['pageData']:
            itemId = i['id']

            newSkill_time_stamp = str(int(time.time()*1000))
            skillUrl = 'http://jishi.woniu.com/9yin/roleMsgInfo.do?serverId=186100101&itemId='+str(itemId)+'&type=SkillContainer&_='+newSkill_time_stamp
            yield scrapy.Request(skillUrl, callback=self.parse_skillcontent,meta={'name':i['itemName'],'id':i['id'],'price':i['price'],'status':i['status']})

    def parse_skillcontent(self, response):
        print('技能请求：' + response.url)
        sites = json.loads(response.text)
        msg = json.loads(sites[0]['msg'])
        flag = False
        for i in msg:
            if i['type']=="江湖散招/江湖散手" and i['dataInfo'].find("神行百变")!=-1:
                flag=True
                break
        print(response.meta['name'] + ' ' + str(flag))
        if flag == True:
            item = RolebyskillItem()
            item['name'] = response.meta['name']
            item['id'] = response.meta['id']
            item['price'] = response.meta['price']
            if response.meta['status'] == '2':
                item['status'] = '公示期'
            else:
                item['status'] = response.meta['status']
            yield item