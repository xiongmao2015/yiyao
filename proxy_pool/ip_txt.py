# coding: utf-8

import re
import retrying
import requests
from datetime import datetime

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.urls = [
            'http://www.proxylists.net/http_highanon.txt',
            'http://www.proxylists.net/http.txt',
            'http://ab57.ru/downloads/proxylist.txt',
        ]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/27.0.1453.90 Safari/537.36',
        }
        self.ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})')

    @retrying.retry(stop_max_attempt_number=3)
    def get_ip(self, url):
        r = requests.get(url, headers=self.headers)
        all_ip_port = self.ip_pattern.findall(r.content)
        logs.debug('-----all ip num-----%s-----' % len(all_ip_port))
        for ip_port in all_ip_port:
            (ip, port) = ip_port
            if all((ip, port)):
                http_type = 'http'
                anonymous = 'HighAnonymous' if 'highanon' in url else 'Unknown'
                country = 'Unknown'
                from_site = url.split('/')[2]
                crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield (ip, port, country, anonymous, http_type, from_site, crawl_time)

    def start(self):
        for url in self.urls:
            for proxy in self.get_ip(url):
                yield proxy


if __name__ == '__main__':
    p = Proxy()
    for i in p.start():
        print i
