# coding:utf8
from faker import Faker

class UserAgentMiddlerware(object):
    """
    随机请求头
    """
    def __init__(self,settings):
        self.faker = Faker()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings)
    def process_request(self,request,spider):
        request.headers['User_agent']=self.faker.user_agent()
