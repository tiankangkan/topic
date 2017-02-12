# -*- coding: utf-8 -*-

import scrapy
import urllib


class BaseSpider(scrapy.Spider):
    def __init__(self):
        super(BaseSpider, self).__init__()

    def parse_cookie(self, cookie):
        if isinstance(cookie, str):
            values = cookie.split('; ')
            ret_cookie = {v.split('=')[0]: v.split('=')[1] for v in values}
        elif isinstance(cookie, dict):
            ret_cookie = cookie
        else:
            ret_cookie = cookie
        return ret_cookie

    def format_text(self, text):
        if isinstance(text, str) or isinstance(text, unicode):
            return text.strip('\n\r\t')
        else:
            return text

