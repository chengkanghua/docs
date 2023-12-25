import requests
import uuid
import time
import random


class PcBili(object):
    def __init__(self, video_url, aid, bvid, cid, duration, view_count, proxies):
        self.video_url = video_url
        self.aid, self.bvid, self.cid, self.duration, self.view_count = aid, bvid, cid, duration, view_count
        self.proxies = proxies

        self.session = requests.Session()
        self.session.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
        }
        self.session.proxies = proxies

        self._uuid = self.gen_uuid()
        self.start_ts = None

    @staticmethod
    def get_video_id_info(video_url, proxies=None):
        session = requests.Session()
        bvid = video_url.rsplit('/')[-1]
        res = session.get(
            url="https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp".format(bvid),
            proxies=proxies
        )

        cid = res.json()['data'][0]['cid']

        res = session.get(
            url="https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}".format(cid, bvid),
            proxies=proxies
        )
        res_json = res.json()
        aid = res_json['data']['aid']
        view_count = res_json['data']['stat']['view']
        duration = res_json['data']['duration']
        print("\n开始：{}，初始播放量为：{}".format(bvid, view_count))
        session.close()
        return aid, bvid, cid, duration, int(view_count)

    def gen_uuid(self):
        uuid_sec = str(uuid.uuid4())
        time_sec = str(int(time.time() * 1000 % 1e5))
        time_sec = time_sec.ljust(5, "0")

        return "{}{}infoc".format(uuid_sec, time_sec)

    def get_buvid(self):
        res = self.session.get(
            url="https://www.bilibili.com/video/BV1YB4y1F7pg"
        )
        res.close()

    def get_bfe_id(self):
        self.session.cookies.set("_uuid", self._uuid)
        self.session.cookies.set("CURRENT_FNVAL", "80")
        self.session.cookies.set("blackside_state", "1")

        res = self.session.get(
            url="https://api.bilibili.com/x/web-interface/nav",
        )
        res.close()

    def get_sid(self):
        res = self.session.get(
            url="https://api.bilibili.com/x/player/v2",
            params={
                "aid": self.aid,
                "bvid": self.bvid,
                "cid": self.cid,
            },
        )
        res.close()

    def play_and_get_rpdid(self):
        self.start_ts = ctime = int(time.time())

        data_dict = {
            "aid": self.aid,
            "cid": self.cid,
            "bvid": self.bvid,
            "part": "1",
            "mid": "0",
            "lv": "0",
            "ftime": ctime - random.randint(100, 1000),  # 首次启动运行时间
            "stime": ctime,  # 当前时间
            "jsonp": "jsonp",
            "type": "3",
            "sub_type": "0"
        }

        res = self.session.post(
            url="https://api.bilibili.com/x/click-interface/click/web/h5",
            data=data_dict
        )
        res.close()

    def heartbeat_start(self):
        data_dict = {
            "aid": self.aid,
            "cid": self.cid,
            "bvid": self.bvid,
            "mid": "0",
            "csrf": "",
            "played_time": 0,
            "real_played_time": 0,
            "realtime": 0,
            "start_ts": self.start_ts,
            "type": 3,
            "dt": 2,
            "play_type": 1
        }

        res = self.session.post(
            url="https://api.bilibili.com/x/click-interface/web/heartbeat",
            data=data_dict
        )
        res.close()
        print("心跳开始")

    def heartbeat(self):
        """ 后续心跳，默认：15s一次，最后一次可能不是15s"""
        # 15s发送一次心跳
        # divmod(50,15): 3/5
        loop_count, div = divmod(self.duration, 15)
        if not div:
            div = 15
            loop_count -= 1

        for i in range(1, loop_count + 1):
            time.sleep(15)
            value = 15 * i
            # 发送心跳请求
            data_dict = {
                "aid": self.aid,
                "cid": self.cid,
                "bvid": self.bvid,
                "mid": "0",
                "csrf": "",
                "played_time": value,  # 播放到了视频的第n秒
                "real_played_time": value,  # 真实播放时间（默认应该是15的倍数，但如果有暂停的话，就不是15倍数了）
                "realtime": value,  # 真实播放时间
                "start_ts": self.start_ts,
                "type": 3,
                "dt": 2,
                "play_type": 0
            }
            res = self.session.post(
                url="https://api.bilibili.com/x/click-interface/web/heartbeat",
                data=data_dict
            )
            res.close()
            print("心跳", value)

        # 再等5s发送最后一次心跳
        time.sleep(div)

        data_dict = {
            "aid": self.aid,
            "cid": self.cid,
            "bvid": self.bvid,
            "mid": "0",
            "csrf": "",
            "played_time": -1,  # 播完了
            "real_played_time": self.duration,
            "realtime": self.duration,
            "start_ts": self.start_ts,
            "type": 3,
            "dt": 2,
            "play_type": 4
        }
        res = self.session.post(
            url="https://api.bilibili.com/x/click-interface/web/heartbeat",
            data=data_dict
        )
        res.close()
        print("心跳结束")


def run():
    proxies = None
    # url = "https://www.bilibili.com/video/BV1ax411m7UB"
    url = "https://www.bilibili.com/video/BV1Np4y147Do"
    aid, bvid, cid, duration, view_count = PcBili.get_video_id_info(url, proxies)

    bili = PcBili(url, aid, bvid, cid, duration, view_count, proxies)

    bili.get_buvid()
    bili.get_bfe_id()
    bili.get_sid()

    bili.play_and_get_rpdid()

    # 心跳开始
    bili.heartbeat_start()

    # 后续的心跳15s一次；50s
    bili.heartbeat()

    bili.session.close()


if __name__ == '__main__':
    run()
