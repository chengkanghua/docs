"""
主页选择功能区域
"""
from src import look, seek, download


def run():
    """为用户提供选择"""
    choice_dict = {"1": {"title": "分页看新闻", "func": look.look},
                   "2": {"title": "搜索专区", "func": seek.seek},
                   "3": {"title": "下载专区", "func": download.download}
                   }
    title_page = ";".join(["{}、{}".format(index, value["title"]) for index, value in choice_dict.items()])
    while True:
        print(title_page)
        user_choice = input("请选择想要浏览的专区序号：(Q/q退出):")
        if user_choice.upper() == "Q":
            break
        if user_choice not in {"1", "2", "3"}:
            print("错误输入，请重新选择专区序号：")
            continue
        choice_dict[user_choice]["func"]()


