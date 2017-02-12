import logging
import os


def create_file_logger(file_path, has_prefix=False):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    logger = logging.getLogger()
    handler = logging.FileHandler(file_path)
    if has_prefix:
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    else:
        formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


LOG_DIR = '/data/sngapm-data/logs'
dc_logger = create_file_logger(os.path.join(LOG_DIR, 'dc_upload.log'))
