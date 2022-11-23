"""
2.搜索专区
用户输入关键字，根据关键词筛选出所有匹配成功的短视频资讯。
支持的搜索两种搜索格式：
    -`id=1715025`，筛选出id等于1715025的视频（video.csv的第一列）。
    -`key=文本`，模糊搜索，筛选包含关键字的所有新闻（video.csv的第二列）
"""

# 模块导入
import config


def id_seek(news_id):
    """根据id搜索"""
    with open(config.video_file_path, mode="r", encoding="utf-8") as video_object:
        id_list = []
        for line in video_object:
            if news_id == line.split(",")[0]:
                id_list.append(line)
                break
    return id_list


def key_seek(news_key):
    """根据文本模糊搜索"""
    with open(config.video_file_path, mode="r", encoding="utf-8") as video_object:
        key_list = []
        for line in video_object:
            if news_key in line:
                key_list.append(line)
    return key_list


def title_show(news_list):
    """提取新闻中的标题并附上序号"""
    for index, value in enumerate(news_list, 1):
        data = value.split(",")
        data1 = data[1: len(data) - 1]
        print(index, data1)


def seek():
    print("进入搜索专区")
    while True:
        user_choice = input("请输入搜索条件，支持[id=1715025 或 key=文本]（Q/q退出）:")
        if user_choice.upper() == "Q":
            break
        if "id=" in user_choice:
            news_id = user_choice.split("=")[1]
            news_list = id_seek(news_id)
            title_show(news_list)
        elif "key=" in user_choice:
            news_key = user_choice.split("=")[1]
            news_list = key_seek(news_key)
            title_show(news_list)
        else:
            print("请按提示格式输入")