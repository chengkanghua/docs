"""
下载专区：
用户输入视频id，根据id找到对应的mp4视频下载地址，然后下载视频到项目的files目录。
    -视频的文件名为：`视频id-年-月-日-时-分-秒.mp4`
    -
"""


# 模块导入
import re
import time
from datetime import datetime
import os
import config
import requests


def video_url(user_id):
    """获取下载链接"""
    with open(config.video_file_path, mode="r", encoding="utf-8") as video_object:
        for line in video_object:
            data_list = line.split(",")
            news_id = data_list[0]
            url = data_list[-1]
            if user_id == news_id:
                return url


def download_video(user_id, news_url):
    """下载视频"""
    # 文件名处理
    now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path_name = os.path.join(config.file_video, "files", "{}-{}.mp4".format(user_id, now_time))

    res = requests.get(url=news_url)
    print("正在下载中...")

    # 视频总大小（字节）
    file_size = int(res.headers['Content-Length'])
    download_size = 0
    with open(path_name, mode='wb') as video_object:
        for chunk in res.iter_content(128):
            download_size += len(chunk)
            video_object.write(chunk)
            video_object.flush()
            download_percent = "\r{}%".format(int(download_size / file_size) * 100)
            print(download_percent, end="")
        video_object.close()
    print("\n下载完成")
    res.close()


def download():
    print("进入下载专区：")
    while True:
        user_id = input("请输入要下载的视频id(Q/q退出)：")
        if user_id.upper() == "Q":
            break
        match_id = re.match("\d{7}", user_id.strip())
        if not match_id:
            print("id输入错误，请重新输入")
            continue
        news_url = video_url(user_id)
        if not news_url:
            print("id不存在，请重新输入")
        download_video(user_id, news_url)

