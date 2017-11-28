# coding: utf-8

import time
import random
from datetime import datetime

import requests
from lxml import etree

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.ha_url = 'http://www.kuaidaili.com/free/inha/{page}/'  # 1,2,3
        self.tr_url = 'http://www.kuaidaili.com/free/intr/{page}/'
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 '
            'Chrome/59.0.3071.109 Safari/537.36'
        ]

    def get_proxy(self, url):
        r = requests.get(url, headers={
            'User-Agent': random.choice(self.user_agent)
        })
        html = etree.HTML(r.content)
        all_proxy = html.xpath('//table//tr[td]')
        print len(all_proxy), '-------len(all_proxy)------'
        logs.debug('-----all ip num-----%s-----url: %s -----' % (len(all_proxy), url))
        for i in all_proxy:
            ip = i.xpath('./td[1]/text()')[0]
            port = i.xpath('./td[2]/text()')[0]

            http_type = i.xpath('./td[4]/text()')[0]
            country = i.xpath('./td[5]/text()')[0]
            anonymous = i.xpath('./td[3]/text()')[0]
            from_site = 'kuaidaili'
            crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            proxy = (ip, port, country, anonymous, http_type, from_site, crawl_time)
            if all(proxy):
                yield proxy

    def start(self):
        for page in range(1, 5):
            ha_url = self.ha_url.format(page=page)
            time.sleep(1)
            for proxy in self.get_proxy(url=ha_url):
                yield proxy
        for page in range(1, 5):
            tr_url = self.tr_url.format(page=page)
            time.sleep(1)
            for proxy in self.get_proxy(url=tr_url):
                yield proxy


if __name__ == '__main__':
    p = Proxy()
    for p_ip in p.start():
        print p_ip
