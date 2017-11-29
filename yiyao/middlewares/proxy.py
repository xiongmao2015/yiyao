# coding:utf-8
import random
from scrapy.exceptions import NotConfigured

class RandomProxyMiddlerware(object):
    """
    随机代理
    """
    def __init__(self,settings):
        self.proxies = settings.getlist('PROXIES')

    def random_proxy(self):
        print random.choice(self.proxies)
        return random.choice(self.proxies)

    @classmethod
    def from_crawler(cls,crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        if not crawler.settings.getlist('PROXIES'):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self,request,spider):
        if 'proxy' not in request.meta:
            request.meta['proxy']=self.random_proxy()