import pytest


@pytest.fixture(scope="class")
def fixture_01_data():
    print("test_01_data")
    a = 10
    b = 20
    return a, b

@pytest.fixture(scope="class")
def fixture_02_data():
    print("test_02_data")
    a = "10"
    b = "20"
    return a, b


def add(x, y):
    return x + y


@pytest.mark.usefixtures("fixture_01_data")  #  此处参数为脚手架函数名
@pytest.mark.usefixtures("fixture_02_data")
class TestAddFunc(object):
    def test_01(self, fixture_01_data):
        res = add(fixture_01_data[0], fixture_01_data[1])
        assert res == 30

    def test_02(self, fixture_02_data):
        res = add(fixture_02_data[0], fixture_02_data[1])
        assert res == 30
