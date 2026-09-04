import pytest


@pytest.fixture(scope="class", autouse=True)
def fixture_open_browser():
    print("打开浏览器")  # 相当于setup
    yield "xiaoming", "123456"
    # 生成器函数中的暂停关键字，作用是当代码运行到yield时，把yield右边的数据作为返回值提供给调用处，把代码执行权交出去。
    print("关闭浏览器")  # 相当于teardown


class TestUser(object):
    def test_01(self, fixture_open_browser):
        print(f"fixture_open_browser={fixture_open_browser}")
        print("注册流程，测试用户是否能注册成功")

    def test_02(self, fixture_open_browser):
        print(f"fixture_open_browser={fixture_open_browser}")
        print("登陆流程，测试用户是否能登陆成功")
