from blinker import signal

# 自定义信号

xxxxx = signal('xxxxx')


def func(sender, *args, **kwargs):
    print(sender)


# 自定义信号中注册函数
xxxxx.connect(func)


def index():
    # 触发信号
    xxxxx.send('123123', k1='v1')
    return 'Index'


index()
