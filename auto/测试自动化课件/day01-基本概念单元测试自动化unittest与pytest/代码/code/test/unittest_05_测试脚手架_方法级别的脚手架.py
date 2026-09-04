import unittest

# 被测试的代码单元
def add(x, y):
    return x + y

class AddTest(unittest.TestCase):
    def setUp(self):
        print("每个方法执行前都会执行一遍setUp实例方法，用于完成通用的前置操作或初始化工作")

    def tearDown(self):
        print("每个方法执行后都会执行一遍tearDown实例方法，用于完成通用的后置操作或销毁工作")

    def test_01(self):
        print(add(10, 20))

    def test_03(self):
        print(add("hello", 20))
