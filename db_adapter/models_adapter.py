# -*- coding:utf-8 -*-

import imp
import os

from kutil import django_models_init
from base_adapter import DBAdapter
from django.conf import settings


class ModelsAdapter(DBAdapter):
    def __init__(self, db_name=None, table_name=None):
        super(ModelsAdapter, self).__init__(db_name=db_name, table_name=table_name)
        if not table_name:
            table_name = '.'
        module_path, class_name = table_name.rsplit('.', 1)[0], table_name.rsplit('.', 1)[1]
        py_path = os.path.join(*module_path.split('.')) + '.py'
        self.py_module = imp.load_source(module_path, os.path.join(settings.BASE_DIR, py_path))
        self.model = getattr(self.py_module, class_name)

    def create_table(self, table_name, field_dict):
        pass

    def insert(self, **fields):
        self.model(**fields).save()

    def delete(self, **delete_para):
        pass

    def filter(self, **filter_para):
        """
        :param filter_para: dict
        :return: list of dict.
        """
        return list(self.model.objects.filter(**filter_para).values())

if __name__ == "__main__":
    ModelsAdapter(table_name='wall.models.Pin')
