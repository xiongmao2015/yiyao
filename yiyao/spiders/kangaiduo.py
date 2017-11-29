# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from yiyao.items import YiyaoItem
import re

def judge(list):
    if len(list)==0:
        return ''
    else:
        return list[0]

class KangaiduoSpider(scrapy.Spider):
    name = 'kangaiduo'
    allowed_domains = ['www.360kad.com']
    start_urls = ['http://www.360kad.com/']

    def __init__(self,max_num=0,*args,**kwargs):
        "初始化数据，主要是加入了max_num，控制流程"
        super(KangaiduoSpider,self).__init__(*args,**kwargs)
        self.max_num=max_num

    def parse(self, response):
        "解析首页中的二级分类"
        yaopins = []
        links = response.xpath('//ul[@id="kinds_lists"]/li')
        # 使用枚举类加索引
        for link in links:
            sponecata = link.xpath('./a/text()').extract()[0]
            sptwocata_list = link.xpath('./div/div/div//h3/span/a')
            # sptwocata_list2 = link.xpath('./div/div/div//h3/span/a')
            for sptwocata_html in sptwocata_list:
                item = YiyaoItem()
                sptwocata = sptwocata_html.xpath('./text()').extract()[0]
                sp2link = sptwocata_html.xpath('./@href').extract()[0]
                item['sponecata']=sponecata,
                item['sptwocata']=sptwocata,
                item['sp2link']=sp2link
                yaopins.append(item)
        for item in yaopins:
            if item['sp2link'].endswith('aspx'):
                yield  Request(url=item['sp2link'],meta={'meta_1':item},callback=self.parse_list_link)

    def parse_list_link(self,response):
        """
        解析各个药品的页面连接,注意到这些网址里面有三种格式，所以还是比较麻烦的，解决分类多的。
        还有另外一种想法是通过crawl,直接筛选出所有的药品。通过药品上的分类实现所有药品的抓取。
        先来这个试一下。
        
        """
        meta_1 = response.meta['meta_1']
        startpage = response.xpath('/html/body/div[5]/div[2]/div/div/span/span[1]/a[1]/@href').extract()
        if len(startpage)!=0:
            startpage = 1
        else:
            startpage = 1
        endpage= response.xpath('/html/body/div[5]/div[2]/div/div/span/span[3]/a[2]/@href').extract()
        print endpage
        # 注意正则的使用
        page_pattern = re.compile("page=(\d*)")
        if len(endpage)!=0:
            endpage = int(re.search(page_pattern,endpage[0]).group(1))+1
        else:
            endpage=2
        for page in range(1,endpage):
            urlpage = response.url+"?page=%d"%page
            yield Request(url=urlpage,meta={'meta_1': meta_1},callback=self.parse_link)


    def parse_link(self,response):
        """
        解析网页中的商品的链接
        """
        meta_1 = response.meta['meta_1']
        links = response.xpath('//div[@class="Yright"]//a[contains(@href,"shtml")]/@href').extract()
        if len(links)!=0:
            for i,link in enumerate(links):
                if self.max_num and i >= self.max_num:
                    break
                pagelink = "http://www.360kad.com"+link
                yield Request(url=pagelink,meta={'meta_1': meta_1},callback=self.parse_detail_page)

    def parse_detail_page(self,response):
        """
        解析详情页面，获取商品信息，并且输出到pipeline
        """
        meta_1 =response.meta['meta_1']

        item = YiyaoItem()
        # 图片
        spimg = response.xpath('//div[@id="minPicScroll"]/div/ul/li[1]/img/@src').extract()
        spimg = judge(spimg)
        # 价格
        price_pattern = re.compile('marketPrice : (.*?),',re.S)
        spprice = re.search(price_pattern,response.text).group(1)
        print re.search(price_pattern,response.text).group(1)

        splink = response.url

        spinfo_list = response.xpath('//div[@id="wrap990list1"]/ul')
        for spinfo in spinfo_list:
            # 商品品牌
            spbrand=spinfo.xpath('./li[1]/@title').extract()
            if len(spbrand) == 0:
                spbrand = '无'
            else:
                spbrand = spbrand[0].split(' ')[0]

            # 规格
            spdosage = spinfo.xpath('./li[2]/@title').extract()
            spdosage = judge(spdosage)
            # 公司
            spcompany = spinfo.xpath('./li[3]/@title').extract()
            spcompany = judge(spcompany)
            # 商品名称
            spname = spinfo.xpath('./li[4]/@title').extract()
            spname = judge(spname)
            # 商品用量
            spuselevel = spinfo.xpath('./li[10]/@title').extract()
            spuselevel=judge(spuselevel)
            # 商品作用
            speffect = spinfo.xpath('./li[9]/@title').extract()
            speffect = judge(speffect)
            # 商品二级分类
            sptwocata = meta_1['sptwocata']
            # 商品二级分类
            sponecata = meta_1['sponecata']
            # 商品来源
            sporigin = "康爱多网上药店"

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
            yield item
















