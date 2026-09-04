class MyType(type):
    def __init__(self, *args, **kwargs):
        # 类成员的初始化
        super().__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        return obj

    def __call__(self, *args, **kwargs):
        obj = self.__new__(self, *args, **kwargs)
        self.__init__(obj, *args, **kwargs)
        return obj


class Foo(object, metaclass=MyType):
    v1 = 123
    def f1(self):
        print('f1')
        return 666

class BB(Foo):
    pass

