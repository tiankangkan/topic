import os
import sys

# add project-root into sys path


def current_file_directory():
    return os.path.dirname(os.path.realpath(__file__))


BASE_DIR = os.path.dirname(os.path.dirname(current_file_directory()))
print('add sys.path: %s' % BASE_DIR)
sys.path.append(BASE_DIR)
