import unittest

# 被测试的代码单元: 类、函数、模块
def add(x, y):
    return x + y

class FuncTest(unittest.TestCase):
    """添加函数的测试用例类"""
    def test_01(self):
        print(add(10,20))

    def test_02(self):
        print(add("a", "B"))

    # def test_03(self):
    #     print(add("a", 20))

if __name__ == '__main__':
    # 因为pycharm本身内置了执行unittest的功能，所以不适用以下代码也能执行，但是终端下或者使用其他的代码编辑器时，则需要加上。
    unittest.main()

