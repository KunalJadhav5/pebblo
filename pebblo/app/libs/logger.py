"""
Module to handle logging functionality
"""
import logging
import os
from pebblo.app.daemon import config_details


def get_logger(log_level):
    """Get object of logger"""
    print('-----logger details for pebblo-----')
    print(os.environ.get('PEBBLO_LOG_LEVEL', 'ABC'))
    logger_obj = logging.getLogger("Pebblo Logger")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handle = logging.StreamHandler()
    console_handle.setFormatter(formatter)
    logger_obj.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))
    logger_obj.propagate = False
    if not logger_obj.handlers:
        logger_obj.addHandler(console_handle)
    return logger_obj


logger = get_logger()
