import os
import requests
from bs4 import BeautifulSoup

BASE_DIR = "pearvideo"


def get_mp4_url(video_id):
    """ 根据视频ID构造视频的下载地址（已破解）"""
    data = requests.get(
        url="https://www.pearvideo.com/videoStatus.jsp?contId={}".format(video_id),
        headers={
            "Referer": "https://www.pearvideo.com/video_{}".format(video_id),
        }
    )
    response = data.json()
    image_url = response['videoInfo']['video_image']
    video_url = response['videoInfo']['videos']['srcUrl']
    middle = image_url.rsplit('/', 1)[-1].rsplit('-', 1)[0]
    before, after = video_url.rsplit('/', 1)
    suffix = after.split('-', 1)[-1]
    url = "{}/{}-{}".format(before, middle, suffix)
    return url


def get_video_list(page):
    """
    获取梨视频最新视频列表
    :param page: 页码
    :return:
    """
    data_list = []
    res = requests.get(
        url="https://www.pearvideo.com/category_loading.jsp?reqType=14&categoryId=&start={}".format(page)
    )
    bs = BeautifulSoup(res.text, 'lxml')
    a_list = bs.find_all("a", attrs={'class': "vervideo-lilink"})
    for tag in a_list:
        title = tag.find('div', attrs={'class': "vervideo-title"}).text.strip()
        video_id = tag.get('href').split('_')[-1]
        mp4_url = get_mp4_url(video_id)
        data_list.append([video_id, title, mp4_url])
    return data_list


def download(file_name, url):
    res = requests.get(
        url=url
    )

    with open(file_name, mode='wb') as file_object:
        # 分块读取下载的视频文件（最多一次读512字节），并逐一写入到文件中。 len(chunk)表示实际读取到每块的视频文件大小。
        for chunk in res.iter_content(512):
            file_object.write(chunk)
            file_object.flush()
        file_object.close()

    res.close()


def init_base_path():
    """ 视频根目录的初始化 """
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)


def run():
    init_base_path()

    while True:
        page = input("请输入页面：")
        page = int(page)
        # 获取第n页新闻资讯的 ID/标题/视频地址
        data_list = get_video_list(page)
        for idx, item in enumerate(data_list, 1):
            message = "{}.{}".format(idx, item[1])
            print(message)
        choice = int(input("请选择视频："))
        index = choice - 1
        video_id, title, video_url = data_list[index]

        # 视频目录是否存在？
        video_folder = os.path.join(BASE_DIR, video_id)
        if os.path.exists(video_folder):
            print("视频已存在")
            continue

        # 视频目录不存在，创建视频目录
        os.makedirs(video_folder)

        # 写文件的内容
        f = open(os.path.join(video_folder, 'info.txt'), mode="w", encoding="utf-8")
        f.write(title)
        f.close()

        # 下载视频
        file_name = video_url.split("/")[-1]
        file_path = os.path.join(video_folder, file_name)
        download(file_path, video_url)


if __name__ == '__main__':
    run()
