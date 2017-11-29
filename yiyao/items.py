# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YiyaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 商品名称
    spname = scrapy.Field()
    # 商品品牌
    spbrand=scrapy.Field()
    # 商品规格
    spdosage = scrapy.Field()
    # 商品用量
    spuselevel = scrapy.Field()
    # 商品公司
    spcompany = scrapy.Field()
    # 商品作用
    speffect = scrapy.Field()
    # 商品价格
    spprice = scrapy.Field()
    # 商品售价
    spsaleprice = scrapy.Field()
    # 商品二级分类
    sptwocata= scrapy.Field()
    # 商品一级分类
    sponecata = scrapy.Field()
    # 商品链接
    splink = scrapy.Field()
    # 商品二级分类链接
    sp2link = scrapy.Field()
    # 商品来源
    sporigin = scrapy.Field()
    # 商品图片
    spimg = scrapy.Field()

