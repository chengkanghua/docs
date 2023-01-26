import unittest

import unittest_01_测试用例的编写 as unittest_01

suite = unittest.TestSuite()

# # 添加测试用例方法
# suite.addTest(unittest_01.FuncTest("test_01"))
# suite.addTest(unittest_01.FuncTest("test_02"))

# # 批量添加测试用例方法
# test_data = (unittest_01.FuncTest("test_01"), unittest_01.FuncTest("test_02"))
# suite.addTests(test_data)


# # 添加测试用例类
# suite.addTest(unittest.makeSuite(unittest_01.FuncTest))


# 批量添加测试用例类
test_data = (unittest.makeSuite(unittest_01.FuncTest),  unittest.makeSuite(unittest_01.FuncTest))
suite.addTests(test_data)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite)