import requests


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

    return aid, cid, duration, view_count


if __name__ == '__main__':
    url = "https://www.bilibili.com/video/BV18y4y137sW"
    aid, cid, duration, view_count = get_video_info(url)
    print(aid, cid, duration, view_count)
