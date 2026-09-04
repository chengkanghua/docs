import os
import random
import pytest
import shutil
import allure
from allure_commons.types import LinkType


def add(x, y):
    return x + y


@allure.testcase("http://www.luffycity.com", "测试地址站点的首页地址")
@allure.issue("http://www.luffycity.com", "软件缺陷的管理站点的首页地址")
class TestAdd(object):
    @allure.feature("测试用例模块的描述: 购物车模块，用户模块")
    @allure.story("测试用例的分类描述")
    @allure.title("测试用例test_01的标题描述")
    @allure.description("测试用例test_01的详细描述")
    @allure.severity(allure.severity_level.MINOR)  # 较小缺陷等级的用例，如果不设置这个，默认是NORMAL普通缺陷等级的用例
    def test_01(self):
        res = add(10, 20)
        assert res == 30

    @allure.feature("测试用例模块的描述: 购物车模块，用户模块")
    @allure.story("测试用例的分类描述")
    @allure.title("测试用例test_02的标题描述")
    # @allure.description("测试用例test_02的详细描述")    # 纯文本描述
    @allure.description_html("<b style='color: red;'>测试用例test_02的详细描述</b>")  # HTML文本描述
    @allure.severity(allure.severity_level.BLOCKER)  # 阻塞缺陷等级的用例
    @allure.link("http://test.luffycity.com/test_02", link_type=LinkType.LINK, name="测试用例：02")

    # 只设置当前测试用例方法失败重试
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_02(self):
        # 注意是使用with上下文管理器语句
        with allure.step("步骤1：内容描述"):
            result = 1+1

        with allure.step("步骤2：内容描述"):
            result +=1

        print(f"测试结果是：{result}")
        assert result == 3

    @allure.feature("测试用例模块的描述: 购物车模块，用户模块")
    @allure.story("测试用例的分类2描述")
    @allure.title("测试用例test_03的标题描述")
    @allure.description("测试用例test_03的详细描述")
    @allure.severity(allure.severity_level.CRITICAL)  # 致命缺陷等级的用例
    def test_03(self):
        # 图片附件
        allure.attach.file("./images/demo.jpg", 'demo.jpg', allure.attachment_type.JPG)
        # 文本附件
        allure.attach("""<h1>Test with some complicated html description</h1>
<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr align="center">
    <td>William</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr align="center">
    <td>Vasya</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>""", "Test with some complicated html attachment", allure.attachment_type.HTML)

        ret = random.randint(1, 3)
        assert ret % 2 == 0

# __name__ 是一个魔术变量，在当前文本被python解释器作为主程序运行是，值固定就是 "__main__"，
# 如果当前文件作为模块被其他文件导包使用，则__name__的值，则为当前文件名或者其他的自定义名称，总之不是 "__main__"了。
if __name__ == '__main__':
    try:
        # 删除之前的测试结果与测试文件目录内容
        shutil.rmtree("reports")
        shutil.rmtree("results")
    except:
        pass
    pytest.main(["-sv", "main.py", "--alluredir", "./results"])
    # 生成报告html文件
    os.system('allure generate ./results -o ./reports --clean')
    # 基于http协议打开HTML测试报告
    os.system('allure open ./reports')
