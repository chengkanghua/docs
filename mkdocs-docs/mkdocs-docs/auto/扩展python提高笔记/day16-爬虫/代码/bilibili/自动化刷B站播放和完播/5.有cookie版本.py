import requests
import time
import uuid


def gen_uuid():
    uid = str(uuid.uuid4())

    div = str(int(int(time.time() * 1000) % 1e5))
    div = div.ljust(5, "0")

    return "{}{}{}".format(uid, div, "infoc")


cookie_dict = {}

res = requests.get(
    url="https://www.bilibili.com/video/BV13s41137i2",
    headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
)
cookie_dict.update(res.cookies.get_dict())

cookie_dict["CURRENT_FNVAL"] = "80"
cookie_dict["_uuid"] = gen_uuid()

res = requests.get(
    url="https://api.bilibili.com/x/web-interface/nav",
    headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    },
    cookies=cookie_dict
)
cookie_dict.update(res.cookies.get_dict())

print(cookie_dict)
cookie_dict["blackside_state"] = "1"

res = requests.get(
    url="https://api.bilibili.com/x/player/v2?cid={}&aid={}&bvid={}".format("xx", "xx", "xx"),
    headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    },
    cookies=cookie_dict
)

cookie_dict.update(res.cookies.get_dict())

print(cookie_dict)
