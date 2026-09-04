def add(x, y):
    return x + y


def setup_module():
    print("模块执行初始化操作")

def teardown_module():
    print("模块执行初始化putest")

class TestAddFunc(object):  # 测试用例类名必须用Test开头
    def setup(self):
        print('setup执行初始化操作')
    def teardown(self):
        print('teardown执销毁操作')

    def setup_class(self):    # 注意：此处方法类型是实例方法。
        print('类级别：setup_class执行初始化操作')

    def teardown_class(self):  # 注意：此处方法类型是实例方法。
        print('类级别：teardown_class执行初始化操作')



    def test_01(self):   # 方法名与函数名必须要用test_开头
        print(add(10, 20))

    def test_02(self):
        print(add("a", "B"))

    def test_03(self):
        print(add(20, 20))

