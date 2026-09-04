import os
import requests

BASE_PATH = "hauban"


def get_pic_list(pin_id):
    result = []
    res = requests.get(
        url="https://huaban.com/discovery/beauty/?kwhv837t&max={}&limit=10&wfl=1".format(pin_id),
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    )
    for item in res.json()['pins']:
        bucket = item['file']['bucket']
        if bucket != "hbimg":
            continue
        key = "{}{}".format("https://hbimg.huabanimg.com/", item['file']['key'])
        result.append((item['pin_id'], bucket, key, item['file']['type']))

    return result


def init_base_path():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)


def download(file_path, url):
    res = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    )
    with open(file_path, mode='wb') as f:
        f.write(res.content)


def run():
    init_base_path()

    pin_id = "4340125638"

    while True:
        choice = input("请选择：")
        if choice not in {"y", "n"}:
            print("输入错误")
            continue
        if choice == "n":
            return

        pic_list = get_pic_list(pin_id)

        for item in pic_list:
            pin_id, _, pic_url, image_type = item
            image_ext = image_type.split('/')[-1]
            file_name = "{}.{}".format(pin_id, image_ext)
            file_path = os.path.join(BASE_PATH, file_name)
            download(file_path, pic_url)


if __name__ == '__main__':
    run()
