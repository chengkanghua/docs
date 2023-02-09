import unittest


def setUpModule():
    print("当前模块执行前都会执行一遍setUpModule函数，用于完成通用的前置操作或初始化工作")


def tearDownModule():
    print("当前模块执行前都会执行一遍tearDownModule函数，用于完成通用的前置操作或初始化工作")


# 被测试的代码单元
def add(x, y):
    return x + y


class AddTest1(unittest.TestCase):
    """测试用例"""

    @classmethod
    def setUpClass(cls):
        print("当前类执行前都会执行一遍setUpClass类方法，用于完成通用的前置操作或初始化工作")

    @classmethod
    def tearDownClass(cls):
        print("当前类执行后都会执行一遍tearDownClass类方法，用于完成通用的后置操作或销毁工作")

    def test_01(self):
        print(add(10, 20))


class AddTest2(unittest.TestCase):
    """测试用例"""

    @classmethod
    def setUpClass(cls):
        print("当前类执行前都会执行一遍setUp方法，用于完成通用的前置操作或初始化工作")

    @classmethod
    def tearDownClass(cls):
        print("当前类执行后都会执行一遍tearDown方法，用于完成通用的后置操作或销毁工作")

    def test_03(self):
        print(add("hello", 20))


# 因为pycharm本身内置了执行unittest的功能，所以不适用以下代码也能执行，但是终端下或者使用其他的代码编辑器时，则需要加上。
if __name__ == '__main__':
    unittest.main()