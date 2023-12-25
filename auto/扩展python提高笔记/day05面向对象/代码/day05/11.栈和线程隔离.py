try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident


class Local(object):
    __slots__ = ("__storage__", "__ident_func__")  # object去创建变量时，约束。

    def __init__(self):
        object.__setattr__(self, "__storage__", {})  # self.__storage__ = {}
        object.__setattr__(self, "__ident_func__", get_ident)  # self.__ident_func__ = get_ident

    def __iter__(self):
        return iter(self.__storage__.items())

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # key=stack,value=[]
        ident = self.__ident_func__()  # 线程/协程ID
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)


class Stack(object):

    def __init__(self):
        self.local = Local()

    def push(self, item):
        """ 在栈中压入一个数据 """
        # self.local.stack ，如果有对应值返回，如果没有就返回None
        rv = getattr(self.local, "stack", None)
        if rv is None:
            # 调用Local对象的stack字段，会执行  Local.__setattr__ 方法（key=stack,value=[])
            self.local.stack = rv = []
            # rv = []
            # self.local.stack = rv
        rv.append(item)

    def pop(self):
        """ 从栈中弹出一个数据 """

        # self.local.stack ，如果有对应值返回，如果没有就返回None
        # [11,22,33]
        rv = getattr(self.local, "stack", None)
        return rv.pop(-1)


obj = Stack()

obj.push(11)
obj.push(22)
obj.push(33)

v1 = obj.pop()  # 33
print(v1)
v2 = obj.pop()  # 22
print(v2)
v3 = obj.pop()  # 11
print(v3)
