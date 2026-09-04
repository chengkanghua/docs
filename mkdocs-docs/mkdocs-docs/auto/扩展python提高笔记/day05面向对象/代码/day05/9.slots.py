class Foo(object):
    # 当前类的对象，只能初始化 x1、x2 变量（object的__setattr__设置值的约束）
    __slots__ = ("x1", "x2",)

obj = Foo()
obj.x1 = 123
obj.x10 = 890


class Foo(object):
    # 当前类的对象，只能初始化 x1、x2 变量（object的__setattr__设置值的约束）
    __slots__ = ("x1", "x2",)

    def __init__(self):
        # self.x1 = 123
        # self.x2 = 456
        object.__setattr__(self, 'x1', 123)
        object.__setattr__(self, 'x2', 456)

    def __setattr__(self, key, value):
        print(key, value)


obj = Foo()
obj.xxxxx = 123


from flask import globals
