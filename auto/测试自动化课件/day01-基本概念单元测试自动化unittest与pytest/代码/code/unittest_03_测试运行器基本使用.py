import unittest

import unittest_01_测试用例的编写 as unittest_01

suite = unittest.TestSuite()

# 批量添加测试用例类
test_data = (unittest.makeSuite(unittest_01.FuncTest),  unittest.makeSuite(unittest_01.FuncTest))
suite.addTests(test_data)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)