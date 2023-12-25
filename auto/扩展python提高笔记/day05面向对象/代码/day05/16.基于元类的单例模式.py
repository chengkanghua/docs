class MyType(type):
    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)
        self.instance = None

    def __call__(self, *args, **kwargs):
        # 1.判断是否已对象，有，则不创建；没有，则创建。
        if not self.instance:
            self.instance = self.__new__(self)

        # 2.调用你自己那个类 __init__放发去初始化
        self.__init__(self.instance, *args, **kwargs)

        return self.instance


class Singleton(object, metaclass=MyType):
    pass


class Foo1(Singleton, metaclass=MyType):
    pass


class Foo2(Singleton):
    pass


v1 = Foo1()
v2 = Foo1()

print(v1)
print(v2)
