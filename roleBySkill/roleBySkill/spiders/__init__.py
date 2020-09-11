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
    url = 'http://jishi.woniu.com/9yin/anonymous/findNoticeGoods.do?serverId=186100101&gameId=10'
    time_stamp = str(int(time.time()*1000))
    allowed_domains = ['woniu.com']
    start_urls = [url+'&filterItem=4&_='+time_stamp]

    def _parse(self, response):
        sites = json.loads(response.body_as_unicode())
        totalPages = sites[0]['pageInfo']['totalPages']
        for i in range(1,totalPages+1):
            new_time_stamp = str(int(time.time()*1000))
            newUrl = self.url + '&pageIndex=' +str(i) +'&filterItem=4&_=' + new_time_stamp
            yield scrapy.Request(newUrl, callback=self.parse_content)

    def parse_content(self, response):
        sites = json.loads(response.body_as_unicode())
        for i in sites[0]['pageData']:
            roleUid = i['sellerGameId']
            print(roleUid)

            newSkill_time_stamp = str(int(time.time()*1000))
            skillUrl = 'http://jishi.woniu.com/9yin/roleMsg.do?serverId=186100101&roleUid='+roleUid+'&type=SkillContainer&_='+newSkill_time_stamp
            print(skillUrl)
            yield scrapy.Request(skillUrl, callback=self.parse_skillcontent,meta={'name':i['itemName'],'id':i['id'],'price':i['price']})

    def parse_skillcontent(self, response):
        sites = json.loads(response.body_as_unicode())
        msg = json.loads(sites[0]['msg'])
        flag = False
        for i in msg:
            if i['type']=="双刺套路/伏月刺诀" :
                flag=True
                break
        if flag == True:
            item = RolebyskillItem()
            item['name'] = response.meta['name']
            item['id'] = response.meta['id']
            item['price'] = response.meta['price']
            yield item