import os
import random
import pytest
import shutil

def add(x, y):
    return x + y


class TestAdd(object):
    def test_01(self):
        res = add(10, 20)
        assert res is 30

    # 只设置当前测试用例方法失败重试
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_02(self):
        ret = random.randint(1, 3)
        assert ret % 2 == 0

    def test_03(self):
        ret = random.randint(1, 3)
        assert ret % 2 == 0

if __name__ == '__main__':
    try:
        shutil.rmtree("./results")
        shutil.rmtree("./resports")
    except:
        pass
    pytest.main()
    os.system("allure generate ./results -o ./reports --clean")
