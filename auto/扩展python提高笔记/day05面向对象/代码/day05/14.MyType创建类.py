class MyType(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        # 创建类
        new_cls = super().__new__(cls, *args, **kwargs)
        return new_cls

    def __call__(self, *args, **kwargs):
        # 1.调用自己那个类的 __new__ 方法去创建对象
        empty_object = self.__new__(self)

        # 2.调用你自己那个类 __init__放发去初始化
        self.__init__(empty_object, *args, **kwargs)

        return empty_object


# 假设Foo是一个对象，由MyType创建。
# Foo类其实是MyType的一个对象。
# Foo()    -> MyType对象()
class Foo(object, metaclass=MyType):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print("自己")


v1 = Foo()  # type.__call__
v1()
