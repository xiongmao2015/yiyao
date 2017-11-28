# coding: utf-8

import base64
import codecs
import re
from datetime import datetime

import requests
import retrying
from lxml import etree

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.url = 'http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:{page}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/27.0.1453.90 Safari/537.36'
                        }
        self.ip_patter = re.compile(r'Base64.decode\(str_rot13\("([^"]+)')

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, page_num):
        try:
            r = requests.get(self.url.format(page=page_num), headers=self.headers, timeout=10)
            html = etree.HTML(r.content)
            all_proxy = html.xpath('//table//tr[td]')
            logs.debug('-----all ip num-----%s-----' % len(all_proxy))
            for proxy in all_proxy:
                try:
                    ip_base64 = self.ip_patter.findall(proxy.xpath('./td[1]/script/text()')[0])[0]
                    ip = base64.b64decode(codecs.decode(ip_base64, 'rot-13'))
                    port = proxy.xpath('./td[2]/text()')[0]
                    country = proxy.xpath('./td[4]/text()')[0]
                    anonymous = proxy.xpath('./td[6]/text()')[0]
                    http_type = 'http'
                    from_site = 'cool-proxy'
                    crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    yield (ip, port, country, anonymous, http_type, from_site, crawl_time)
                except Exception as e:
                    logs.debug('-----no ip-----%s' % e)
        except Exception as e:
            logs.debug('-----request error-----%s' % e)

    def start(self):
        for i in range(1, 11):
            for proxy in self.extract_proxy(page_num=i):
                yield proxy


if __name__ == '__main__':
    p = Proxy()
    for i in p.start():
        print i
