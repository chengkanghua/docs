import unittest

from HTMLTestRunner import HTMLTestRunner

import unittest_01_测试用例的编写 as unittest_01

suite = unittest.TestSuite()

test_data = (unittest.makeSuite(unittest_01.FuncTest),  unittest.makeSuite(unittest_01.FuncTest))
suite.addTests(test_data)

with open("test_report.html", "wb") as file:
    runner = HTMLTestRunner(
        stream=file,
        title="单元测试的HTML格式报告",
        description="python单元测试报告",
        tester="墨落"
    )
    runner.run(suite)
