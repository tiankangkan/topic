# -*- coding:utf-8 -*-

from kafka import KafkaConsumer
from sysutil import get_current_ip
import random


class KafkaUtil(object):
    def __init__(self, broker_list=None):
        self.producer = None
        self.broker_list = broker_list or ['localhost:9092']
        print 'KafkaUtil, init broker_list with: %s' % self.broker_list
        self.consumer = KafkaConsumer(bootstrap_servers=self.broker_list)

    def set_consumer(self, topics, group_id=None, client_id=None, value_deserializer=None):
        """
        :param topics: topic name or list of topic name. like: 'upload-topic', ['upload-topic', 'upload-topic-2']
        :param group_id:
        :param client_id:
        :param value_deserializer: like: value_deserializer=lambda m: json.loads(m.decode('utf8'))
        :return:
        """
        self.close()
        group_id = group_id or 'default_group'
        client_id = client_id or 'kafka-client-%s.%d' % (get_current_ip(), random.randint(1000000, 9999999))
        consumer_para = dict()
        if value_deserializer:
            if hasattr(value_deserializer, '__call__'):
                consumer_para['value_deserializer'] = value_deserializer
            else:
                raise RuntimeError('value_deserializer must be function.')
        print "KafkaUtil.set_consumer, bootstrap_servers is: %s" % self.broker_list
        consumer_para['bootstrap_servers'] = self.broker_list
        consumer_para['request_timeout_ms'] = 10000
        consumer_para['metadata_max_age_ms'] = 15000
        consumer_para['client_id'] = client_id
        consumer_para['group_id'] = group_id

        if isinstance(topics, basestring):
            self.consumer = KafkaConsumer(topics, **consumer_para)
        elif isinstance(topics, list):
            self.consumer = KafkaConsumer(*topics, **consumer_para)
        else:
            raise RuntimeError('the type of "topics" must be str or list.')

    def topics(self):
        if not self.consumer:
            raise RuntimeError("please set_consumer() to init consumer.")
        return self.consumer.topics()

    def close(self):
        if isinstance(self.consumer, KafkaConsumer):
            try:
                self.consumer.close()
            except:
                print 'Try close the old consumer failed...'

