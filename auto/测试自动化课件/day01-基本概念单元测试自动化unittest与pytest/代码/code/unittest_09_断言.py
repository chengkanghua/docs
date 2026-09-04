import unittest

def add(x ,y):
    return x + y


class AddTest(unittest.TestCase):
    def test_01(self):
        res = add(1,2)
        # 断言结果是否与预期内容相同
        # self.assertEqual(res, 3, msg="断言失败！一般会错误的结果与原因")
        # self.assertEqual(res, 2, msg="断言失败！一般会错误的结果与原因")
        self.assertIn(res, [1, 2], msg="断言失败！一般会错误的结果与原因")

if __name__ == '__main__':
    unittest.main()
