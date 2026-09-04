#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json
import time
import random
import queue
import collections
import requests
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class JsonFileHelper(object):
    def __init__(self, file_name):
        folder = os.path.join(BASE_DIR, "db")
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.db_file_path = os.path.join(BASE_DIR, "db", file_name)

    def read(self):
        if not os.path.exists(self.db_file_path):
            return
        file_object = open(self.db_file_path, mode='r', encoding="utf-8")
        data = json.load(file_object)
        file_object.close()
        return data

    def write(self, data):
        file_object = open(self.db_file_path, mode='w', encoding='utf-8')
        json.dump(data, file_object)
        file_object.close()


class V3ProxyHandler(object):
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"
    ]

    PROXY_LIST = []

    def __init__(self, file_name):
        folder = os.path.join(BASE_DIR, "db")
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.db_file_path = os.path.join(BASE_DIR, "db", file_name)
        self.initial()

    def initial(self):
        if os.path.exists(self.db_file_path):
            with open(self.db_file_path, mode='r', encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                self.PROXY_LIST = list(content.split("\n"))

    def get_random_proxy(self):
        if not self.PROXY_LIST:
            return
        return random.choice(self.PROXY_LIST)

    def write(self, data):
        # 写入文件
        file_object = open(self.db_file_path, mode='w', encoding='utf-8')
        file_object.write(data)
        file_object.close()

        # 写入集合和队列
        data = data.strip()
        if not data:
            self.PROXY_LIST = []
        else:
            self.PROXY_LIST = list(data.split("\n"))

    def read(self):
        if not os.path.exists(self.db_file_path):
            return
        file_object = open(self.db_file_path, mode='r', encoding="utf-8")
        result = file_object.read()
        file_object.close()
        return result

    def request(self, url, retry=3):
        for i in range(retry):
            agent = random.choice(self.USER_AGENT_LIST)
            proxy = self.get_random_proxy()
            try:
                headers = {
                    "User-Agent": agent,
                    "pragma": "no-cache",
                    "upgrade-insecure-requests": "1",
                    "cache-control": "no-cache",
                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
                    "accept-encoding": "gzip, deflate, br",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                }
                if proxy:
                    proxies = {"http": proxy, "https": proxy}
                else:
                    proxies = None
                res = requests.get(url=url, headers=headers, proxies=proxies, timeout=10)
                res.close()
                if res.status_code == 200:
                    return True, res.text, proxy
            except Exception as e:
                return False, str(e), proxy
        return False, res.text, proxy


ALERT = JsonFileHelper("alert.json")
PROXY = V3ProxyHandler("proxy.json")
