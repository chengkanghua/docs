import os


def message():
    """ 发送消息 """
    host = os.environ.get("HOST")
    # 连接数据host


if __name__ == '__main__':
    # 对我们自己而言
    # 1.设置临时（程序员）
    #     os.environ.setdefault("MSG", "192.168.1.1")
    # 2.系统环境变量中设置
    #     去系统中修改 "192.168.1.2"
    message()