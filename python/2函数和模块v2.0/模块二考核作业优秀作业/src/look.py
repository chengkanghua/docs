"""
1.分页看新闻（每页显示10条）:
    -提示用户输入页码，根据页码显示指定页面的数据。
    -当用户输入的页码不存在时，默认显示第1页
"""
# 导入模块
import config


def get_page(user_page):
    """用于根据用户输入的页码找到对应的十条新闻"""
    start_path = 10 * user_page - 10  # 计算显示序号的开头
    end_path = 10 * user_page - 1  # 计算显示序号的结尾
    page_result = 0
    news_list = []
    # 将范围内的序号添加到列表中
    with open(config.video_file_path, mode="r", encoding="utf-8") as video_object:
        for line in video_object:
            if start_path <= page_result <= end_path:
                news_list.append(line.strip())

            page_result += 1
    return news_list


def sum_title(news_list, user_page):
    """提取每一条新闻中的标题并附上序号"""
    for key, value in enumerate(news_list, user_page * 10 - 9):
        data = value.split(",")
        data1 = data[1: len(data) - 1]
        print(key, data1)


def look():
    """分页看新闻"""
    print("进入分页看新闻界面，每页显示10条新闻。")
    row_num, total_row = 10, 999
    row = total_row / row_num
    if row != int:
        row = row // 1 + 1  # 计算最大页码
    while True:
        user_page = input("请按页码范围输入页码：1~{}页(q/Q退出)".format(row))
        if user_page.upper() == "Q":
            break
        if not user_page.isdecimal:
            print("请输入正确的页码范围")
            continue
        user_page = int(user_page)
        if user_page < 1 or user_page > row:
            print("第1页")

        print("第{}页".format(user_page))
        news_list = get_page(user_page)
        sum_title(news_list, user_page)
