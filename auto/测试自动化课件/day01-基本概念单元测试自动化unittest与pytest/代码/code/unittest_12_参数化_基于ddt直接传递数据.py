import unittest
from ddt import ddt, data

def add(a,b):
    return a+b

@ddt
class AddTest(unittest.TestCase):
    # # 单次传递一个数据到测试用例方法中
    # @data(100)
    # @data([1,2,3,4])
    # @data({"a":1,"b":2})
    # @data((1,2,3))

    # # 多次传递一个数据到测试用例方法中
    # @data(*["a","b","c"]) # 字符串
    # @data(*[{"a":1}, {"a":2}, {"a":3}]) # 字典
    # @data(*[[1, 1, 1], [1, 1, 2], [1, 1, 3]])
    @data([1, 1, 1], [1, 1, 2], [1, 1, 3])
    def test_01(self, a):
        print(a)


if __name__ == '__main__':
    unittest.main()
