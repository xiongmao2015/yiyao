# -*- coding: utf-8 -*-
import re
import time
from lxml import etree

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from yiyao.items import YiyaoItem

'''
京东大药房里面的药品不多
而且，详细页面需要selenium抓取
其他属性通过xpath等获取
京东医药有点乱。
京东医疗主体不同页面不同。导致需要对应。解决办法:通过查找后面一个节点来实现。

'''

def value(yilist,n=0):
    '''针对列表取值的情况'''
    if len(yilist)!=0:
        return yilist[n]
    else:
        return ''

class JDyiyaoSpider(CrawlSpider):
    name = 'jdyiyao'
    allowed_domains = ['jd.com']
    start_urls = ['http://pharma.jd.com/']

    rules = (
        # 注意点和？需要转义。
        Rule(link_extractor=LinkExtractor(allow=('//coll\.jd\.com/list\.html\?sub=\d+')),callback='parse_list_page',follow=True),
    )
    def parse_list_page(self,response):
        '''
        这个页面解析出地址，然后调用parse_detail_page,因为我担心，selenium处理的值不能返回到pipeline中，通过那个返回
        把地址传给parse_detail_page,让他进行解析，解析完成后，把值再传回来。
        //div[@id="plist"]//div[@class="p-img"]/a/@href
        '''
        url_list = response.xpath('//div[@id="plist"]//div[@class="p-img"]/a/@href').extract()
        if len(url_list)!=0:
            for url in url_list:
                url = 'http:'+ url
                print url
                item = self.parse_detail_page(url)
                yield item

    def parse_detail_page(self,url):
        """
        解析详情页面，获取商品信息，并且输出到pipeline
        难点：价格在js中，通过正则筛选,需要先将response转为text.
        """
        driver = webdriver.PhantomJS()
        driver.get(url)
        time.sleep(2)
        r = driver.page_source
        response = etree.HTML(r)

        item = YiyaoItem()
        # 图片
        spimg = response.xpath('//img[@id="spec-img"]/@src')
        if value(spimg)=='':
            spimg = value(spimg)
        else:
            spimg = 'http:'+value(spimg)
        # 价格，价格是动态加载的,所以需要selenium
        spprice = response.xpath('//span[@class="p-price"]/span[2]/text()')
        spprice = value(spprice)
        print spprice
        # 链接，
        splink = driver.current_url
        # 关闭页面。
        driver.close()
        # 商品二级分类
        sptwocata =response.xpath('//div[@id="crumb-wrap"]/div/div[1]/div[5]/a/text()')
        sptwocata = value(sptwocata)
        # 商品一级分类
        sponecata = response.xpath('//div[@id="crumb-wrap"]/div/div[1]/div[3]/a/text()')
        sponecata = value(sponecata)
        print sponecata,sptwocata
        spbrand = response.xpath('//ul[@id="parameter-brand"]/li/a/text()')
        spbrand = value(spbrand)
        spinfo_list = response.xpath('//div[@class="Ptable-item"]/dl')
        # 商品品牌
        for spinfo in spinfo_list:
            # 规格
            spdosage = spinfo.xpath('./dd[9]/text()')
            spdosage = value(spdosage)
            # 公司
            spcompany = spinfo.xpath('./dd[3]/text()')
            spcompany = value(spcompany)
            # 商品名称
            spname = spinfo.xpath('./dd[1]/text()')
            spname = value(spname)
            # 商品用量
            spuselevel = spinfo.xpath('./dd[8]/text()')
            spuselevel = value(spuselevel)
            # 商品作用
            speffect = spinfo.xpath('./dd[12]/text()')
            speffect = value(speffect)
            # 商品来源
            sporigin = "京东大药房"

            item['spimg']=spimg
            item['spname']=spname
            item['spprice']=spprice
            item['splink']=splink
            item['speffect'] = speffect
            item['sptwocata'] = sptwocata
            item['sponecata'] = sponecata
            item['sporigin'] = sporigin
            item['spuselevel'] = spuselevel
            item['spcompany'] = spcompany
            item['spbrand'] = spbrand
            item['spdosage'] = spdosage
        return item















