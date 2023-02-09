import allure
import config
import pytest
from logger import LogHandle
from requestor import Request
from yamler import  Yaml
from assertor import assertor
from utils.excel import Excel

logger = LogHandle().get_logger()
SERVER_URl = f"http://{config.API_HOST}:{config.API_PORT}"
yaml = Yaml()


@allure.epic(config.WEB_NAME)
@allure.feature("用户模块")
@allure.story("登录")
class TestLogin(object):
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_username_by_empty(self,):
    #     allure.dynamic.title("用户名为空，登陆失败")
    #     allure.dynamic.description("测试用户名为空的登陆结果")
    #
    #     # 发送请求
    #     request = Request()
    #     request("POST", f"{SERVER_URl}/user/login", json={
    #         "username": "",
    #         "password": "123456"
    #     })
    #
    # def test_password_by_empty(self,):
    #     allure.dynamic.title("密码为空，登陆失败")
    #     allure.dynamic.description("测试密码为空的登陆结果")
    #
    #     # 发送请求
    #     request = Request()
    #     request("POST", f"{SERVER_URl}/user/login", json={
    #         "username": "xiaoming",
    #         "password": ""
    #     })

    # @pytest.mark.parametrize("kwargs", yaml.read(config.BASE_DIR / "data/user_login.yaml"))
    # def test_login(self, kwargs):
    #     """数据驱动自动化测试-基于yaml生成"""
    #     request = Request()
    #     allure.dynamic.title(kwargs.get('name'))
    #     request.logger.info(f"开始请求测试接口：{kwargs.get('name')}")
    #     data = kwargs.get('request')
    #     response = request(data.get("method"), f'{data.get("url")}', json=data.get("json"))
    #     assertor(kwargs.get("assert"), response)

    @pytest.mark.parametrize("kwargs", Excel(config.BASE_DIR / "data/case_user.xls").get_data(0, config.FIELD_LIST))
    def test_login(self, kwargs):
        """数据驱动自动化测试-基于excel生成"""
        request = Request()
        allure.dynamic.title(kwargs.get('case_name'))
        request.logger.info(f"开始请求测试接口：{kwargs.get('case_name')}")
        if kwargs.get("method").lower() in ["get", "delete"]:
            """发送get或delete"""
            response = request(kwargs.get("method"), f'{kwargs.get("url")}', params=kwargs.get("params"))
        else:
            """发送post，put，patch"""
            response = request(kwargs.get("method"), f'{kwargs.get("url")}', json=kwargs.get("params"))
        assertor(kwargs.get("assert_result"), response)
