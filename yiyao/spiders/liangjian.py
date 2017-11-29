# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

from yiyao.items import YiyaoItem
import re

'''
亮健的药店与康爱多相差不大，只有部分修改。
不同之处。列表页的内容有些参数感觉没用。
'''

class liangjianSpider(CrawlSpider):
    name = 'liangjian'
    allowed_domains = ['www.360lj.com']
    start_urls = ['http://www.360lj.com/']

    rules = (
        Rule(link_extractor=LinkExtractor(allow=('/list-\d+\.html')),follow=True),
        Rule(link_extractor=LinkExtractor(allow=('/product/\d+\.html')),callback='parse_detail_page',follow=False),
        Rule(link_extractor=LinkExtractor(allow=('/list-\d+-0-\d+-0-1-0-0-0-0-0\.html')),follow=True),
    )

    def parse_detail_page(self,response):
        """
        解析详情页面，获取商品信息，并且输出到pipeline
        """
        print response.url
        item = YiyaoItem()
        # 图片
        spimg = response.xpath('//div[@class="jk_de_cont_img_big"]/img/@src').extract_first(default = '')
        # 价格
        spprice = response.xpath('//dd[@class="market_price"]/text()').extract_first(default='')
        # 售价
        spsaleprice = response.xpath('//dd[@class="jk_price"]/span/text()').extract_first(default='')
        # 链接，
        splink = response.url
        print splink
        # 商品二级分类
        sptwocata =response.xpath('//p[@class="jk_de_nav"]/a[3]/text()').extract_first(default = '')
        # 商品一级分类
        sponecata = response.xpath('//p[@class="jk_de_nav"]/a[2]/text()').extract_first(default = '')
        spname = response.xpath('//dd[@class="goods_name"]/text()').extract_first(default='')
        print spname
        # 公司
        spcompany = response.xpath('//dd[@class="factory_name"]/text()').extract_first(default='')
        # 规格
        spdosage = response.xpath('//dd[@class="on"]/text()').extract_first(default='')
        # 商品作用
        speffect = response.xpath('//p[@class="show_p"]/text()').extract_first(default='')
        # 商品品牌
        spbrand_list = response.xpath('//table/tbody/tr[1]/td[2]/p/text()').extract()
        if len(spbrand_list) != 0:
            spbrand_list1 = spbrand_list[0].split(' ')
            if len(spbrand_list1) < 3:
                spbrand = '无'
            else:
                spbrand = spbrand_list1[0]
        else:
            spbrand = '无'
        # 商品用量
        spuselevel = response.xpath('//table/tbody/tr[6]/td[2]/p/text()').extract_first(default='')
        # 商品来源
        sporigin = "亮健好药"


        item['spimg']=spimg
        item['spname']=spname
        item['spprice']=spprice
        item['spsaleprice']=spsaleprice
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















