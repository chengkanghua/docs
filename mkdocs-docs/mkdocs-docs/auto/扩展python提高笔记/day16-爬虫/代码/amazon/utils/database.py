import os
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FileDBHelper(object):
    CACHE_LIST = []
    CACHE_DICT = {}

    def __init__(self, file_name):
        folder = os.path.join(BASE_DIR, "db")
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.db_file_path = os.path.join(BASE_DIR, "db", file_name)

        self.initial()

    def initial(self):
        if not os.path.exists(self.db_file_path):
            return
        file_object = open(self.db_file_path, mode='r', encoding="utf-8")
        data = json.load(file_object)
        file_object.close()

        self.CACHE_LIST = data
        self.CACHE_DICT = {item[0]: item for item in data}

    def get_by_asin(self, asin):
        return self.CACHE_DICT.get(asin)

    def get_by_index(self, index):
        return self.CACHE_LIST[index]

    def add(self, row_data_list):
        """
        在文件中添加一行
        :param row_data_list:
        :return:
        """
        self.CACHE_LIST.append(row_data_list)
        self.CACHE_DICT[row_data_list[0]] = row_data_list
        self.write(self.CACHE_LIST)

    def update_title_url_status(self, asin, title, url, status):
        """
        更新文件中的 标题、URL、状态
        """
        row_list = self.CACHE_DICT.get(asin)
        row_list[1] = title
        row_list[2] = url
        row_list[6] = status
        self.write(self.CACHE_LIST)

    def update_status(self, asin, status):
        row_list = self.CACHE_DICT.get(asin)
        row_list[6] = status
        self.write(self.CACHE_LIST)

    def update_status_by_index(self, index, status):
        self.CACHE_LIST[index][6] = status

        self.write(self.CACHE_LIST)

    def update_count_by_index(self, index, count):
        self.CACHE_LIST[index][4] = count
        self.write(self.CACHE_LIST)

    def update_error_count_by_index(self, index, count):
        self.CACHE_LIST[index][5] = count
        self.write(self.CACHE_LIST)

    def update_by_asin(self, asin, column, value):
        row_list = self.CACHE_DICT.get(asin)
        row_list[column] = value
        self.write(self.CACHE_LIST)

    def remove_by_asin_list(self, asin_list):
        for index in range(len(self.CACHE_LIST) - 1, -1, -1):
            asin = self.CACHE_LIST[index][0]
            if asin in asin_list:
                del self.CACHE_LIST[index]
                del self.CACHE_DICT[asin]
        self.write(self.CACHE_LIST)

    def get_index_by_asin(self, asin):
        for index in range(len(self.CACHE_LIST)):
            if asin == self.CACHE_LIST[index][0]:
                return index

    def clear_count_and_error_count(self, index_list):
        for index in index_list:
            self.CACHE_LIST[index][4] = 0
            self.CACHE_LIST[index][5] = 0
        self.write(self.CACHE_LIST)

    def read(self):
        if not os.path.exists(self.db_file_path):
            return []
        file_object = open(self.db_file_path, mode='r', encoding="utf-8")
        data = json.load(file_object)
        file_object.close()
        return data

    def write(self, data):
        file_object = open(self.db_file_path, mode='w', encoding='utf-8')
        json.dump(data, file_object)
        file_object.close()


DB = FileDBHelper("db.json")
