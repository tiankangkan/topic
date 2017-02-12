# -*- coding:utf-8 -*-


class DBAdapter(object):
    def __init__(self, db_name=None, table_name=None):
        self.db_name = db_name
        self.table_name = table_name

    def create_table(self, table_name, field_dict):
        pass

    def insert(self, **fields):
        pass

    def delete(self, **delete_para):
        pass

    def filter(self, **filter_para):
        """
        :param filter_para: dict
        :return: list of dict.
        """
        pass

