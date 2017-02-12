# -*- coding: utf-8 -*-
# import this file to init django models.


import os, sys
import django

settings_path = 'topic.settings'

django_version = list(django.VERSION[:3])    # (1, 4, 22, 'final', 0)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = settings_path

if django_version >= [1, 8, 0]:
    print('Django Version: %s, bigger than 1.8' % django_version)
    django.setup()
elif django_version >= [1, 6, 0]:
    print('Django Version: %s, >= 1.6 and < 1.8' % django_version)
    pass
else:
    print('Django Version: %s, less than 1.6' % django_version)
    settings = __import__('topic.settings')
    # 避免django取了错误的 project_directory, 详见 django/core/management/__init__.py:404
    settings.__file__ = os.path.join(BASE_DIR, 'topic/settings.py')
    from django.core.management import setup_environ
    setup_environ(settings)
