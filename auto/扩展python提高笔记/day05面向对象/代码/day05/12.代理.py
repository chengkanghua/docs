import functools


class HttpRequest(object):
    def method(self):
        print("method")

    def body(self):
        print("body")


class Session(object):

    def get(self):
        print("get")

    def xxxxx(self):
        print("xxxxx")


class Context(object):
    def __init__(self):
        self.request = HttpRequest()
        self.session = Session()


ctx = Context()  # 在内部 { request:HttpRequest对象， session:Session对象 }
data_list = [ctx, ]  # 栈，在栈中只有一个ctx对象。

# 直接取
"""
data_list[-1].request.method()
data_list[-1].request.body()
data_list[-1].session.get()
data_list[-1].session.xxxxx()
"""


def get_top(name):
    top = data_list[-1]  # 去栈顶取ctx对象。
    return getattr(top, name)  # ctx.request / ctx.session


class LocalProxy(object):

    def __init__(self, func):
        object.__setattr__(self, 'func', func)  # self.func = 偏函数

    def get_current_object(self):
        return self.func()  # 执行偏函数

    def __getattr__(self, name):
        # name="method"
        # self.get_current_object() 执行传入的函数（偏函数）， request对象对象。
        # 去request对象找到method
        return getattr(self.get_current_object(), name)


# self.func = 偏函数 ，以后偏函数执行，自动携带request参数，执行返回值： ctx中的request对象
request = LocalProxy(functools.partial(get_top, "request"))
request.method()  # __getattr__    name = "method"

request.body()  # __getattr__    name = "method"

# self.func = 偏函数 ，以后偏函数执行，自动携带session参数，执行返回值： ctx中的session对象
session = LocalProxy(functools.partial(get_top, "session"))
session.get()  # __getattr__    name = "method"
session.xxxxx()  # __getattr__    name = "method"
