# coding: utf-8

import time
import pycurl
import random
from multiprocessing.dummy import Pool

from cool_proxy import Proxy as CoolProxy
from ip_txt import Proxy as IpTxtProxy
from ip181 import Proxy as Ip181Proxy
from proxydb import Proxy as ProxyDB
from kuaidaili import Proxy as KuaidailiProxy
from ip_chi import Proxy as IpChiProxy
from goubanjia import Proxy as GoubanjiaProxy
from mysql_conn.mysql_connect import MySQLConn
from process_data.process import process_data
from proxy_log.logs import logs


class CheckProxy(object):
    """
    检查获取的ip,并且存入数据库
    缺陷：因为多线程的缺陷，没有使用多线程，其实可以将线程用来访问网络，多进程用来写入数据库。
    """
    def __init__(self):
        self.url = 'http://httpbin.org/ip'
        self.ip181 = Ip181Proxy()
        self.ip_txt = IpTxtProxy()
        self.cool_proxy = CoolProxy()
        self.proxy_db = ProxyDB()
        self.kuaidaili = KuaidailiProxy()
        self.ip_chi = IpChiProxy()
        self.goubanjia = GoubanjiaProxy()
        self.ip_list = []
        self.proxy_num = 0
        self.user_agent = [
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) '
            'Chrome/24.0.1292.0 Safari/537.14',
            'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/29.0.1547.62 Safari/537.36',
            'Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
        ]

    def get_proxy(self,):
        """
        获取的所有的ip地址的list
        :return: IP地址
        """
        for proxy in self.ip181.start():
            self.ip_list.append(proxy)
        for proxy in self.proxy_db.start():
            self.ip_list.append(proxy)
        for proxy in self.kuaidaili.start():
            self.ip_list.append(proxy)
        for proxy in self.ip_chi.start():
            self.ip_list.append(proxy)
        for proxy in self.goubanjia.start():
            self.ip_list.append(proxy)
        # 可用代理太少
        for proxy in self.ip_txt.start():
            self.ip_list.append(proxy)
        for proxy in self.cool_proxy.start():
            self.ip_list.append(proxy)
        return self.ip_list

    def check_proxy(self, proxy):
        """
        通过请求检查ip地址是否能用，
        :param proxy: proxy为代理IP。
        :return: 写到数据库。
        """
        conn = MySQLConn()
        proxy = process_data(proxy)
        (ip, port, country, anonymous, http_type, from_site, crawl_time) = proxy
        if not conn.check_if_exist(proxy):
            try:
                c = pycurl.Curl()
                c.setopt(c.URL, self.url)
                c.setopt(c.USERAGENT, random.choice(self.user_agent))
                c.setopt(pycurl.PROXY,
                         '{http_type}://{ip}:{port}'.format(http_type=http_type, ip=ip, port=port))
                c.setopt(pycurl.CONNECTTIMEOUT, 10)
                c.setopt(pycurl.TIMEOUT, 10)
                c.perform()
                time.sleep(0.1)
                http_status = c.getinfo(pycurl.HTTP_CODE)
                c.close()
                if http_status == 200:
                    self.proxy_num += 1
                    conn.insert_proxy_to_mysql(proxy)
                    logs.debug('-----proxy is useful-----%s://%s:%s----' % (http_type, ip, port))
                else:
                    logs.debug('-----http_status: %s-----proxy: %s--' % (http_status, ip + ':' + port))
            except Exception as e:
                logs.debug('-----proxy can not be used-----%s' % e)
            finally:
                conn.close()
        else:
            conn.close()
            logs.debug('-----proxy already exists-----%s://%s:%s----' % (http_type, ip, port))

    def start(self):
        """
        多进程实现检查，因为网络I/O比较费时。但是小心，这里有个错误。在有些python2中运行错误
        """
        ip_list = self.get_proxy()
        pool = Pool()
        pool.map(self.check_proxy, ip_list)
        pool.close()
        logs.debug('-----new proxy num-----%s--' % self.proxy_num)


if __name__ == '__main__':
    check = CheckProxy()
    check.start()
