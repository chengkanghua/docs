"""
    https://api.bilibili.com/x/click-interface/click/web/h5
    POST

"""

import requests
import time
import random


def get_video_info(video_url):
    bvid = video_url.rsplit('/')[-1]

    res = requests.get(
        url="https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp".format(bvid)
    )

    duration = res.json()['data'][0]['duration']
    cid = res.json()['data'][0]['cid']

    res = requests.get(
        url="https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}".format(cid, bvid),
    )

    res_json = res.json()
    aid = res_json['data']['aid']
    view_count = res_json['data']['stat']['view']
    print("播放量：", view_count)
    return aid, bvid, cid, duration, view_count


def get_body(url):
    aid, bvid, cid, duration, view_count = get_video_info(url)

    current_time = int(time.time())
    info = {
        "aid": aid,
        "cid": cid,
        "bvid": bvid,
        "part": "1",
        "mid": "0",
        "lv": "0",
        "ftime": current_time - random.randint(100, 1000),
        "stime": current_time,
        "jsonp": "jsonp",
        "type": "3",
        "sub_type": "0"
    }
    return info


def play(url):
    data_dict = get_body(url)

    res = requests.post(
        url="https://api.bilibili.com/x/click-interface/click/web/h5",
        data=data_dict,
        headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
    )

    print(res.text)


if __name__ == '__main__':
    # 可以刷播放，但由于B站内部对IP进行限制。如果无限制刷的太快，B站还会锁视频。
    while True:
        play("https://www.bilibili.com/video/BV1nf4y1L7Mz")
        break
