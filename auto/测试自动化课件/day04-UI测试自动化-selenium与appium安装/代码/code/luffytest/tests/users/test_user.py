import allure
import pytest
import config
from utils.requestor import Request
from utils.yamler import Yaml
from utils.assertor import assertor


yaml = Yaml()


@allure.epic(config.WEB_NAME)
@allure.feature("用户模块")
@allure.story("用户中心")
class TestUser(object):
    @pytest.mark.usefixtures("jwt_token")
    @pytest.mark.parametrize("kwargs", yaml.read(config.BASE_DIR / "data/user_info.yaml"))
    def test_user(self, jwt_token, kwargs):
        allure.dynamic.title(kwargs.get('name'))
        request = Request()
        request.logger.info(f"开始请求测试接口：{kwargs.get('name')}")
        data = kwargs.get('request')
        data['headers']["Authorization"] = data['headers']["Authorization"].format(token=jwt_token)
        response = request(data.get("method"), data.get("url"), headers=data.get("headers"))
        assertor(kwargs.get("assert"), response)
