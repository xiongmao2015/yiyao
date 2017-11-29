# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

from yiyao.items import YiyaoItem
import re


class KangaiduocrawlSpider(CrawlSpider):
    name = 'kangaiduocrawl'
    allowed_domains = ['www.360kad.com']
    start_urls = ['http://www.360kad.com/']

    rules = (
        Rule(link_extractor=LinkExtractor(allow=('/Category_\d+/Index\.aspx')),follow=True),
        Rule(link_extractor=LinkExtractor(allow=('/product/\d+\.shtml')),callback='parse_detail_page',follow=False),
        Rule(link_extractor=LinkExtractor(allow=('/Category_\d+/Index\.aspx\?page=\d+')),follow=True),
    )


    def parse_detail_page(self,response):
        """
        解析详情页面，获取商品信息，并且输出到pipeline
        """
        item = YiyaoItem()
        # 图片
        spimg = response.xpath('//div[@id="minPicScroll"]/div/ul/li[1]/img/@src').extract_first(default = '')
        # 价格，价格是在js中的。
        price_pattern = re.compile('marketPrice : (.*?),',re.S)
        spprice = re.search(price_pattern,response.text).group(1)
        saleprice_pattern = re.compile('salePrice : (.*?),',re.S)
        spsaleprice = re.search(saleprice_pattern,response.text).group(1)
        print spprice,spsaleprice

        # 链接，
        splink = response.url
        # 商品二级分类
        sptwocata =response.xpath('//div[@class="wrap-dtl-nav"]/a[3]/@title').extract_first(default = '')
        # 商品一级分类
        sponecata = response.xpath('//div[@class="wrap-dtl-nav"]/a[2]/@title').extract_first(default = '')
        print sponecata,sptwocata
        spinfo_list = response.xpath('//div[@id="wrap990list1"]/ul')
        for spinfo in spinfo_list:
            # 商品品牌
            spbrand=spinfo.xpath('./li[1]/@title').extract()
            if len(spbrand) == 0:
                spbrand = '无'
            else:
                spbrand = spbrand[0].split(' ')[0]
            # 规格
            spdosage = spinfo.xpath('./li[2]/@title').extract_first(default = '')
            # 公司
            spcompany = spinfo.xpath('./li[3]/@title').extract_first(default = '')
            # 商品名称
            spname = spinfo.xpath('./li[4]/@title').extract_first(default = '')
            # 商品用量
            spuselevel = spinfo.xpath('./li[10]/@title').extract_first(default = '')
            # 商品作用
            speffect = spinfo.xpath('./li[9]/@title').extract_first(default = '')
            # 商品来源
            sporigin = "康爱多网上药店"

            item['spimg']=spimg
            item['spname']=spname
            item['spprice']=spprice
            item['spsaleprice'] = spsaleprice
            item['splink']=splink
            item['speffect'] = speffect
            item['sptwocata'] = sptwocata
            item['sponecata'] = sponecata
            item['sporigin'] = sporigin
            item['spuselevel'] = spuselevel
            item['spcompany'] = spcompany
            item['spbrand'] = spbrand
            item['spdosage'] = spdosage
            yield item















