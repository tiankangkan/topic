# -*- coding: utf-8 -*-

import scrapy


class TuicoolSpider(scrapy.Spider):
    name = "tuicool"
    url = "http://www.tuicool.com/ah/1/0"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        page = int(response.url.split("/")[-1])
        print(response.body)
        next_page = page + 1
        next_url = "%s/%s" % (response.url.rsplit("/", 1)[0], next_page)
        yield scrapy.Request(url=next_url, callback=self.parse)
