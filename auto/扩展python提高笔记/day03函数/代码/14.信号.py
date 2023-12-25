from blinker import signal

X1 = signal("XXOO")


# 在信号中注册一个功能
@X1.connect
def sms(sender, *args, **kwargs):
    print(sender, args, kwargs)


@X1.connect
def wechat(sender, *args, **kwargs):
    print(sender, args, kwargs)


@X1.connect
def dingding(sender, *args, **kwargs):
    print(sender, args, kwargs)


def f4():
    print(123)
    X1.send("F4", k1="123")
    print(666)


def f3():
    print(123)
    print(666)
    X1.send("F3", k1="666", k2="999")


def f2():
    print(123)
    f3()
    X1.send("F2", k1="666", k2="999")
    f4()
    print(666)


def f1():
    print(123)
    f2()
    print(666)


if __name__ == '__main__':
    f1()
