import multiprocessing
import requests


def download(url):
    res = requests.get(url)
    print(res)


def run():
    url_list = [
        "https://space.bilibili.com/283478842",
        "https://www.luffycity.com/",
        "https://www.cnblogs.com/wupeiqi"
    ]

    for url in url_list:
        # download(url)
        t = multiprocessing.Process(target=download, args=(url,))
        t.start()

    print("END")


if __name__ == '__main__':
    run()
