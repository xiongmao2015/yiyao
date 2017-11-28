# coding: utf-8

import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def transform_md5(data):
    if data:
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
    else:
        return ' '


def process_data(proxy):
    proxy = tuple(map(lambda x: x.strip(), proxy))
    ip, port, country, anonymous, http_type, from_site, crawl_time = proxy
    if anonymous in [u'普匿', 'Anonymous']:
        anonymous = 'Anonymous'
    elif anonymous in [u'高匿', u'高匿名', 'HighAnonymous']:
        anonymous = 'HighAnonymous'
    elif anonymous in [u'透明', 'Transparent']:
        anonymous = 'Transparent'

    http_type = http_type.lower()
    if 'https' in http_type:
        http_type = 'https'
    else:
        http_type = 'http'

    proxy = (ip, port, country, anonymous, http_type, from_site, crawl_time)
    return proxy


if __name__ == '__main__':
    p = ('122.152.194.123', '8088', '北京市 歌华有线', '透明', 'HTTP', 'ip181', '2017-07-20 17:19:48')
    print process_data(p)
