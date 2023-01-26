import unittest


def add(x, y):
    return x + y


version = (2, 7, 0)

class AddTest(unittest.TestCase):
    def setUp(self):
        print("setUP执行....")

    @unittest.skipIf(version <= (3, 5, 0), "版本低于3.5，所以不测试test_01")
    def test_01(self):
        res = add(1, 2)
        self.assertIn(res, [1, 3], msg="断言失败！一般会错误的结果与原因")

    def test_02(self):
        res = add("a", "B")
        self.assertEqual(res, "aB", msg="断言失败！一般会错误的结果与原因")


if __name__ == '__main__':
    unittest.main()
