# 传统方式创建类（直观）
"""
class Foo(object):
    v1 = 123

    def func(self):
        return 666
print(Foo)  # <class '__main__.Foo'>
"""


# 非传统方式（一行）
# 1.创建类型
#   - 类名
#   - 继承类
#   - 成员
def do(self):
    pass


Fa = type("Foo", (object,), {"v1": 123, "func": lambda self: 666, 'do': do})

# 2.根据类创建对象
obj = Fa()

# 3.调用对象中v1变量（类变量）
print(obj.v1)

# 4.执行对象的func方法
result = obj.func()
print(result)
