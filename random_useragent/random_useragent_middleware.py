"""Scrapy Middleware to set a random User-Agent for every Request.

Downloader Middleware which uses a file containing a list of
user-agents and sets a random one for each request.
"""

import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from . import default_user_agents


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, settings, user_agent='Scrapy'):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        user_agent_list_file = settings.get('USER_AGENT_LIST_FILE')
        if not user_agent_list_file:
            # If USER_AGENT_LIST_FILE settings is not set,
            # use the default ones provided
            self.user_agent_list = settings.get('USER_AGENT_LIST', default_user_agents.DEFAULT_USER_AGENTS)
        else:
            with open(user_agent_list_file, 'r') as f:
                self.user_agent_list = [line.strip() for line in f.readlines()]

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
