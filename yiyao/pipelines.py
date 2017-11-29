# -*- coding: utf-8 -*-

import redis
import logging
import pymysql

logger =logging.getLogger(__name__)
logger.setLevel('INFO')

class RedisPipeline(object):
    """
    这里通过redis的集合去重，同时保存一些数据。
    """
    def __init__(self):
        self.r = redis.Redis(host='x.x.x.x',port=6379,password='xxxxxx')
    def process_item(self,item,spider):
        if self.r.sadd(spider.name,item['splink']):
            logger.info('redis: add%s to set %s'%(item['spname'],spider.name))
            return item

class MysqlPipeline(object):
    """
    永久存储到MySQL
    """
    def __init__(self):
        self.conn =None
        self.cur = None
    def open_spider(self,spider):
        self.conn = pymysql.connect(
            host = 'x.x.x.x',
            port = 3306,
            user = 'root',
            passwd = 'xxxxxx',
            db = 'yiyao',
            charset = 'utf8'
        )
        self.cur = self.conn.cursor()
    def close_spider(self,spider):
        """
        当spider关闭时，这个方法被调用
        """
        self.cur.close()
        self.conn.close()
    def process_item(self,item,spider):
        """
        在MySQL中插入数据。
        """
        # sql = "INSERT INTO `yiyao` (`spname`, `spbrand`, `spdosage`," \
        #       " `spuselevel`, `spcompany`, `speffect`, `spprice`, `sptwocata`, `sponecata`," \
        #       " `splink`, `sporigin`, `spimg`) VALUES (" +",".join(['%s']*12)+");"
        # logger.info(sql)
        # self.cur.execute(sql,(item['spname'],item['spbrand'],item['spdosage'],
        #                       item['spuselevel'],item['spcompany'],item['speffect'],
        #                       item['spprice'],item['sptwocata'],item['sponecata'],item['splink'],
        #                       item['sporigin'],item['spimg']))
        cols = item.keys()
        values = [item[col] for col in cols]
        sql = "INSERT INTO `yiyao` ("+','.join(cols)+") VALUES ("+','.join(['%s']*13)+");"
        self.cur.execute(sql,values)
        self.conn.commit()
        logger.info('mysql: add %s to mysql'%item['spname'])
        return item
