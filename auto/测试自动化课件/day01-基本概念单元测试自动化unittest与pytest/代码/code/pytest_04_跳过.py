import pytest


def add(x, y):
    return x + y

version = (2, 7, 12)

class TestAddFunc(object):  # 测试用例类名必须用Test开头
    def test_01(self):   # 方法名与函数名必须要用test_开头
        res = add(10, 20)
        assert res == 30

    @pytest.mark.skipif(version <= (2, 7, 12), reason="高于2.7以下，不测试test_02")
    def test_02(self):
        res = add("a", "B")
        assert type(res) is int

    def test_03(self):
        res = add(20, 20)
        assert res != 20

