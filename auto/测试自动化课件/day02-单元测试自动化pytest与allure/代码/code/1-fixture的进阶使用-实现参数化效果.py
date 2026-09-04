import pytest


# 类级别的脚手架
@pytest.fixture(scope="class")
def fixture_01_data():  # 建议脚手架的函数名以fixture开头.
    a = 10
    b = 20
    return a, b  # 脚手架的函数可以有返回值，也可以没有返回值


# 被测试的代码单元
def add(x, y):
    return x + y


class TestAddFunc(object):
    def test_01(self, test_01_data):  # 此处的参数名，就是上面的脚手架名称，注意：参数名要与上面的脚手架函数保持一致
        res = add(test_01_data[0], test_01_data[1])
        assert res == 30

if __name__ == '__main__':
    pytest.main(["-sv", "1-fixture的进阶使用-实现参数化效果.py"])