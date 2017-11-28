# coding: utf-8

import random
from datetime import datetime

import requests
from lxml import etree

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.tm_url = 'http://www.goubanjia.com/free/anoy/%E9%80%8F%E6%98%8E/index{page}.shtml'   # 1,2,3
        self.gn_url = 'http://www.goubanjia.com/free/anoy/%E9%AB%98%E5%8C%BF/index{page}.shtml'
        self.nm_url = 'http://www.goubanjia.com/free/anoy/%E5%8C%BF%E5%90%8D/index{page}.shtml'

        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
        ]

    @staticmethod
    def get_port(port_word):
        word = port_word.split(' ')
        num_list = []
        for item in word:
            num = 'ABCDEFGHIZ'.find(item)
            num_list.append(str(num))

        port = str(int("".join(num_list)) >> 0x3)
        return port

    def get_proxy(self, url):
        r = requests.get(url, headers={
            'User-Agent': random.choice(self.user_agent)
        }, timeout=30)
        html = etree.HTML(r.content)

        all_proxy = html.xpath('//table//tr[td]')
        logs.debug('-----all_proxy_num-----%s-----' % len(all_proxy))
        for i in all_proxy:
            ip_port = ''.join(i.xpath('./td[1]/span[@style]/text()|'
                                      './td[1]/div[@style]/text()|'
                                      './td[1]/p[@style]/text()|'
                                      './td[1]/text()|'
                                      './td[1]/span[@class]/text()'))
            if ip_port and ':' in ip_port:
                ip, _ = ip_port.split(':')
                port_alpha = i.xpath('./td[1]/span[starts-with(@class, "port")]/@class')[0]
                port = self.get_port(port_alpha)
                anonymous = i.xpath('./td[2]/a/text()')[0]
                http_type = ''.join(i.xpath('./td[3]/a/text()')) or 'http'
                country = ''.join(i.xpath('./td[4]/a/text()'))
                from_site = 'goubanjia'
                crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                proxy = (ip, port, country, anonymous, http_type, from_site, crawl_time)
                yield proxy

    def start(self):
        for page in range(1, 3):
            tm_url = self.tm_url.format(page=page)
            for proxy in self.get_proxy(tm_url):
                yield proxy

        for page in range(1, 3):
            gn_url = self.gn_url.format(page=page)
            for proxy in self.get_proxy(gn_url):
                yield proxy

        for page in range(1, 3):
            nm_url = self.nm_url.format(page=page)
            for proxy in self.get_proxy(nm_url):
                yield proxy


if __name__ == '__main__':
    p = Proxy()
    for p_ip in p.start():
        print p_ip


