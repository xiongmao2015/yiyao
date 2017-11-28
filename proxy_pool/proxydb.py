# coding: utf-8

import re
import time
import random
from StringIO import StringIO
from datetime import datetime

import pycurl
from lxml import etree

from proxy_log.logs import logs


class Proxy(object):
    def __init__(self):
        self.url = 'http://proxydb.net/?protocol=http&protocol=https&offset={offset}'  # 0,20,40,60
        self.ip_part_1_p = re.compile(r'var x = \'([^\']+)')
        self.ip_part_2_p = re.compile(r'var y = \'([^\']+)')
        self.port_p = re.compile(r'var p = ([^;]+)')
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
        ]

    def get_html(self, url):
        try:
            c = pycurl.Curl()
            s = StringIO()
            c.setopt(c.USERAGENT, random.choice(self.user_agent))
            c.setopt(c.URL, url)
            c.setopt(c.CONNECTTIMEOUT, 15)
            c.setopt(c.TIMEOUT, 15)
            c.setopt(c.WRITEDATA, s)
            c.perform()
            time.sleep(3)
            http_status = c.getinfo(pycurl.HTTP_CODE)
            logs.debug('-----http_status: %s-----url: %s-----' % (http_status, url))
            c.close()
            body = s.getvalue()
            html = etree.HTML(body)
            return html
        except Exception as e:
            logs.debug('-----request error-----%s' % e)
            return None

    def parse_html(self, html):
        all_proxy = html.xpath('//table//tr[td]')
        logs.debug('-----all ip num-----%s-----' % len(all_proxy))
        for i in all_proxy:
            ip_port = i.xpath('./td[1]/script/text()')[0]

            ip = self.ip_part_1_p.findall(ip_port)[0][::-1] + self.ip_part_2_p.findall(ip_port)[0]
            port = str(eval(self.port_p.findall(ip_port)[0]))

            http_type = i.xpath('./td[2]/text()')[0].strip()
            country = i.xpath('./td[3]/abbr/text()')[0]
            anonymous = i.xpath('./td[4]/span/text()')[0]
            from_site = 'proxydb.net'
            crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            proxy = (ip, port, country, anonymous, http_type, from_site, crawl_time)
            yield proxy

    def start(self):
        for offset in range(0, 201, 20):
            url = self.url.format(offset=offset)
            html = self.get_html(url=url)
            if html is not None:
                for proxy in self.parse_html(html):
                    yield proxy


if __name__ == '__main__':
    p = Proxy()
    for p_ip in p.start():
        print p_ip
