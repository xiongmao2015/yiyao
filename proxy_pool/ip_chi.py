# coding: utf-8

import requests
from lxml import etree
from datetime import datetime

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.url = 'http://www.ip-chi.net/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/27.0.1453.90 Safari/537.36'}

    def get_ip(self, url):
        r = requests.get(url, headers=self.headers)
        html = etree.HTML(r.content)
        all_ip = html.xpath('//table//tr[td]')
        logs.debug('-----all ip num-----%s-----' % len(all_ip))
        for i in all_ip:
            ip = i.xpath('./td[1]/text()')[0].strip()
            port = i.xpath('./td[2]/text()')[0].strip()
            country = i.xpath('./td[6]/text()')[0].strip()
            anonymous = i.xpath('./td[3]/text()')[0].strip()
            http_type = i.xpath('./td[4]/text()')[0].strip()
            from_site = 'ip_chi'
            crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('-----', ip, port, country, anonymous, http_type, from_site, crawl_time, '=====')
            proxy = (ip, port, country, anonymous, http_type, from_site, crawl_time)
            yield proxy

    def start(self):
        for proxy in self.get_ip(self.url):
            yield proxy


if __name__ == '__main__':
    p = Proxy()
    for p_ip in p.start():
        print p_ip
