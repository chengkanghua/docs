import requests
import time
import uuid


def gen_uuid():
    uid = str(uuid.uuid4())

    div = str(int(int(time.time() * 1000) % 1e5))
    div = div.ljust(5, "0")

    return "{}{}{}".format(uid, div, "infoc")


cookie_dict = {}

session = requests.Session()
session.headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

res = session.get(
    url="https://www.bilibili.com/video/BV13s41137i2"
)
res.close()
session.cookies.set("CURRENT_FNVAL", "80")
session.cookies.set("_uuid", gen_uuid())

res = session.get(
    url="https://api.bilibili.com/x/web-interface/nav"
)
res.close()
session.cookies.set("blackside_state", "1")

res = requests.get(
    url="https://api.bilibili.com/x/player/v2?cid={}&aid={}&bvid={}".format("xx", "xx", "xx"),
)
res.close()

print(session.cookies.get_dict())

session.close()
