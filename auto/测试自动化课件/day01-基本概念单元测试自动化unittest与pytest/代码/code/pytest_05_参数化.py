import pytest


def add(x, y):
    return x + y


class TestAddFunc(object):  # 测试用例类名必须用Test开头
    @pytest.mark.parametrize("x,y", [(10, 20), ("a", "b"), ("a", 20)])
    def test_01(self, x, y):   # 方法名与函数名必须要用test_开头
        res = add(x, y)
        assert res == 30
