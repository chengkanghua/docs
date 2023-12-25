import requests
import json
import redis
import time


class Bili(object):
    def __init__(self, proxies, data_dict, cookie_dict):
        self.proxies = proxies
        self.data_dict = data_dict
        self.cookie_dict = cookie_dict

    def heartbeat(self):
        requests.post(
            url="https://api.bilibili.com/x/click-interface/web/heartbeat",
            data=self.data_dict,
            cookies=self.cookie_dict,
            headers={
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
            }
        )


def run():
    proxies = None

    # 1. 设置代理（换代理IP需要自己写逻辑）
    #    去访问 http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=14
    """
    proxies = {
        "https": "122.143.82.96:28803",
        "http": "122.143.82.96:28803",
    }
    """
    # 2. 隧道代理
    """
    proxy_host = 'tps186.kdlapi.com:15818'
    proxy_username = 't12575892639376'
    proxy_pwd = 'ps4fmg72'
    proxies = {
        "http": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
        "https": "https://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
    }
    """

    conn = redis.Redis(host='127.0.0.1', port=6379, password='qwe123', encoding='utf-8')
    key = "bilibili_heart_beat_task"

    while True:
        try:
            # 1.获取当前时间
            current_time = int(time.time())

            # 2.有序集合中获取需要心跳的数据 并 在集合中删除
            data_list = conn.zrangebyscore(key, 0, current_time, withscores=True, score_cast_func=int)
            conn.zremrangebyscore(key, 0, current_time)

            # 3.没有要执行心跳的
            if not data_list:
                time.sleep(2)
                continue

            # 4.如果有需要执行的任务
            for value, score in data_list:
                info = json.loads(value)

                bili = Bili(proxies, **info)
                bili.heartbeat()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    run()
