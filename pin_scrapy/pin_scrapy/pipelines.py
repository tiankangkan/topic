# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db_adapter.models_adapter import ModelsAdapter


class PinScrapyPipeline(object):
    def process_item(self, item, spider):
        print('PinScrapyPipeline: spider is: %s' % spider)
        if spider.name == 'km_ask':
            print('insert item into PinKMAsk: %s', item['title'])
            model = ModelsAdapter(table_name='wall.models.PinKMAsk')
            model.insert(**item)
        return item
