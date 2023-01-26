"""
7-pytest.ini文件改名为pytest.ini，再运行当前测试代码
"""

import random

def add(x, y):
    return x + y


class TestAdd(object):
    def test_01(self):
        res = add(10, 20)
        assert res is 30

    def test_02(self):
        ret = random.randint(1, 3)
        assert ret % 2 == 0
