import unittest
from parameterized import parameterized

def add(x, y):
    return x + y


version = (2, 7, 0)

class AddTest(unittest.TestCase):
    def setUp(self):
        print("setUP执行....")

    @parameterized.expand([(10,20), ("a","B"), (50, 20)])
    def test_00(self, x, y):
        res = add(x, y)
        self.assertIn(res, [1, 30, "aB", 70], msg="断言失败！一般会错误的结果与原因")


    # def test_01(self):
    #     res = add(1, 2)
    #     self.assertIn(res, [1, 3], msg="断言失败！一般会错误的结果与原因")
    #
    # def test_02(self):
    #     res = add("a", "B")
    #     self.assertEqual(res, "aB", msg="断言失败！一般会错误的结果与原因")
    #
    # def test_03(self):
    #     print(add("a", 20))

if __name__ == '__main__':
    unittest.main()
