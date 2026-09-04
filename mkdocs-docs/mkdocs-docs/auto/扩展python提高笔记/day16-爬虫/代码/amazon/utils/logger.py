#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Logging(object):

    def __init__(self):
        self.folder = folder = os.path.join(BASE_DIR, "log")
        if not os.path.exists(folder):
            os.makedirs(folder)

    def get_logger(self, asin):
        file_path = os.path.join(self.folder, "{}.log".format(asin))
        file_handler = logging.FileHandler(file_path, 'w', encoding='utf-8')
        fmt = logging.Formatter(fmt="%(asctime)s :  %(message)s")
        file_handler.setFormatter(fmt)

        logger = logging.Logger(asin, logging.ERROR)
        logger.addHandler(file_handler)
        return logger

    def log(self, asin, title, message):
        logger = self.get_logger(asin)
        content = "{}\n{}".format(title, message)
        logger.error(content)

    def get_log(self, asin):
        file_path = os.path.join(self.folder, "{}.log".format(asin))
        if not os.path.exists(file_path):
            return ""
        with open(file_path, mode='r', encoding='utf-8') as f:
            result = f.read()
        return result

    def clear_log(self, asin):
        file_path = os.path.join(self.folder, "{}.log".format(asin))
        if not os.path.exists(file_path):
            return
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write("")

    def remove_by_asin_list(self, asin_list):
        for asin in asin_list:
            file_path = os.path.join(self.folder, "{}.log".format(asin))
            if not os.path.exists(file_path):
                continue
            os.remove(file_path)


LOGGER = Logging()
