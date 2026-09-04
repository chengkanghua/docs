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


if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV18y4y137sW"
    info = get_body(url)
    print(info)
