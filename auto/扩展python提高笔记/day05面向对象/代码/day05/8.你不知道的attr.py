# 当前类中为定义 __attr__
"""
class Foo(object):
    pass


obj = Foo()
# obj.v1 = 123  # object.__setattr__
object.__setattr__(obj, 'v1', 123)

# print(obj.v1)  # object.__getattr__
object.__getattr__(obj, 'v1')
"""

# 当前类中有 __attr__
"""
class Foo(object):

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, item):
        pass
"""

# 请大家帮我做一下优化
import threading


class Local(object):

    def __init__(self):
        object.__setattr__(self, 'storage', {})  # self对象中存储 storage={}

    def __setattr__(self, key, value):
        print(1)
        ident = threading.get_ident()  # 获取当前线程ID
        # self.storage 是否 Local.__getattr__ or object.__getattr__ ?
        # self.storage   --> 执行 object.__getattr__ 直接去取值了。
        if ident in self.storage:
            self.storage[ident][key] = value
        else:
            self.storage[ident] = {key: value}

    def __getattr__(self, item):
        ident = threading.get_ident()  # 获取当前线程ID
        return self.storage[ident][item]


local = Local()
local.x1 = 123  # Local.__setattr__
print(local.x1)
