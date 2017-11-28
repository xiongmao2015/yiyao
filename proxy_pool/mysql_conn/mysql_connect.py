# coding: utf-8

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import MySQLdb
from proxy_log.logs import logs
from process_data.process import transform_md5


class MySQLConn(object):
    """
    连接mysql数据库，并进行增删改查等方法
    获取查询的ip,并输出。
    """
    def __init__(self):
        self.db = MySQLdb.connect(
            host='127.0.0.1',
            passwd='111111',
            user='root',
            db='proxy_ip',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            logs.debug('-----insert failed-----%s' % e)
            return False

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            logs.debug('-----update failed-----%s' % e)

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except Exception as e:
            logs.debug('-----select failed-----%s' % e)
            return ''

    def close(self,):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            logs.debug('-----close failed-----%s' % e)

    def check_if_exist(self, proxy):
        (ip, port, country, anonymous, http_type, from_site, crawl_time) = proxy
        ip_md5 = transform_md5(ip + port + http_type)
        select_sql = 'select count(id) from ip_t where ip_md5="%s";' % ip_md5
        result = self.select(select_sql)
        if result[0][0] == 1:
            return True
        else:
            return False

    def insert_proxy_to_mysql(self, proxy):
        if not self.check_if_exist(proxy):
            (ip, port, country, anonymous, http_type, from_site, crawl_time) = proxy
            ip_md5 = transform_md5(ip + port + http_type)
            insert_sql = 'insert into ip_t(ip, port, country, anonymous, http_type, from_site, crawl_time, ' \
                         'ip_md5) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % \
                         (ip, port, country, anonymous, http_type, from_site, crawl_time, ip_md5)
            logs.debug('-----insert_sql-----%s' % insert_sql)
            succeed = self.insert(insert_sql)
            if not succeed:
                logs.debug('-----insert failed-----%s' % insert_sql)

    def get_proxy(self, num=1):
        sql = 'select http_type, ip, port from ip_t where status="0" order by crawl_time desc limit %s;' % num
        update_sql = 'update ip_t set status="1" where ip_md5="%s";'
        s = list()
        d = dict()
        proxies = self.select(sql)
        for p in proxies:
            (http_type, ip, port) = p
            ip_md5 = transform_md5(ip + port + http_type)
            self.update(update_sql % ip_md5)
            s.append({http_type:http_type+'://'+ip+':'+ port})
        return s

    def get_proxy_num(self):
        sql = 'select count(id) from ip_t where status="0";'
        count =self.select(sql)
        return count

if __name__ == '__main__':

    m = MySQLConn()
    print m.get_proxy(5)
    print m.get_proxy_num()