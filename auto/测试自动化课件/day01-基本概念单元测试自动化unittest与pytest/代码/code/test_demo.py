def add(x, y):
    return x + y

class TestAddFunc(object):  # 测试用例类名必须用Test开头
    def test_01(self):   # 方法名与函数名必须要用test_开头
        print(add(10, 20))

    def test_02(self):
        print(add("a", "B"))

    def test_03(self):
        print(add(20, 20))
