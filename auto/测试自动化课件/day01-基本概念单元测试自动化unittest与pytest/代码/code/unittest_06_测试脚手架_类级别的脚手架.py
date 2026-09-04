import unittest

# 被测试的代码单元
def add(x,y):
    return x+y


class AddTest(unittest.TestCase):
    """测试用例"""
    # 注意：类级别的脚手架的方法名，固定是setUpClass与tearDownClass，都是类方法
    @classmethod
    def setUpClass(cls):
        print("当前类执行前都会执行一遍setUpClass类方法，用于完成通用的前置操作或初始化工作")

    @classmethod
    def tearDownClass(cls):
        print("当前类执行后都会执行一遍tearDownClass类方法，用于完成通用的后置操作或销毁工作")


    def setUp(self):
        print("每个方法执行前都会执行一遍setUp实例方法，用于完成通用的前置操作或初始化工作")

    def tearDown(self):
        print("每个方法执行后都会执行一遍tearDown实例方法，用于完成通用的后置操作或销毁工作")


    def test_01(self):
        print(add(10, 20))

    def test_03(self):
        print(add("hello", 20))


# 因为pycharm本身内置了执行unittest的功能，所以不适用以下代码也能执行，但是终端下或者使用其他的代码编辑器时，则需要加上。
if __name__ == '__main__':
    unittest.main()