"""
前置步骤，安装插件：
pip install pytest-ordering
"""
import pytest


class TestAdd(object):

    @pytest.mark.run(order=-1)
    def test_01(self):
        print(f"test_01执行了，order=-1")

    @pytest.mark.run(order=-10)
    def test_02(self):
        print(f"test_02执行了，order=-10")

    @pytest.mark.run(order=10)
    def test_03(self):
        print(f"test_03执行了，order=10")

    @pytest.mark.run(order=3)
    def test_04(self):
        print(f"test_04执行了，order=3")

    def test_05(self):
        print(f"test_05执行了，没有指定排序值")

    def test_06(self):
        print(f"test_06执行了，没有指定排序值")

"""
多个方法排序值为正整数的情况：以小为先
test_04
test_03
没有排序值的情况下，源代码中先写的先执行，后写的后执行：先写为先
test_05
test_06
多个方法排序值为负整数的情况：以小为先
test_02
test_01
"""