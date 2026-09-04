import os


def message():
    """ 发送消息 """

    msg = os.environ.get("MSG")
    if msg == "sms":
        print("发送短信")
    elif msg == "wechat":
        print("发送微信")


if __name__ == '__main__':
    # os.environ.setdefault("MSG", "wechat")

    # 第一步：os.environ，默认读取系统的环境变量
    # 第二步：在os.environ中在设置 "临时" 的环境变量

    # 对我们自己而言
    # 1.设置临时（程序员）
    #     os.environ.setdefault("MSG", "wechat")
    # 2.系统环境变量中设置
    #     去系统中修改
    message()
