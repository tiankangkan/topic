# -*- coding:utf-8 -*-

import shelve
import os
from file_op import make_sure_file_dir_exists


class KVStoreShelve(object):
    def __init__(self, data_dir='', db_name=None, writeback=True):
        self.db_name = db_name or 'kv_database'
        self.file_path = os.path.join(data_dir, self.db_name)
        self.inst = None
        self.writeback = writeback
        self.make_db_open()

    def make_db_open(self):
        if self.inst is None:
            make_sure_file_dir_exists(self.file_path)
            self.inst = shelve.open(self.file_path, writeback=self.writeback)

    def close(self):
        if self.inst:
            self.inst.close()
        self.inst = None

    def format_key(self, key):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        return key

    def put(self, key, value):
        key = self.format_key(key)
        self.make_db_open()
        self.inst[key] = value
        self.sync()

    def __setitem__(self, key, value):
        key = self.format_key(key)
        self.put(key, value)

    def get(self, key, default=None):
        key = self.format_key(key)
        self.make_db_open()
        value = self.inst.get(key, default)
        self.sync()
        return value

    def pop(self, key):
        key = self.format_key(key)
        self.inst.pop(key)

    def __getitem__(self, key):
        self.get(key)

    def sync(self):
        self.inst.close()

    def __contains__(self, key):
        self.make_db_open()
        key = self.format_key(key)
        is_contain = key in self.inst
        self.sync()
        return is_contain

    def __iter__(self):
        self.make_db_open()
        return self.inst.__iter__()

    def keys(self):
        self.make_db_open()
        keys = map(self.format_key, self.inst.keys())
        self.sync()
        return keys

    def __str__(self):
        self.make_db_open()
        return str(self.inst)


if __name__ == '__main__':
    kv = KVStoreShelve()
    key = u'我apd, '
    c = ['sdf', 'erty']
    kv.put(key, ['apd, ''erty'])
    print kv
    c.append('sdasas')
    kv.put(key, c)
    print kv
