import pytest
import config
from utils.requestor import Request
from utils.yamler import Yaml

yaml = Yaml()


@pytest.fixture(scope="class", autouse=False)
def jwt_token():
    request = Request()
    request.logger.info("获取token")
    data = yaml.read(config.BASE_DIR / "data/test_user.yaml")
    response = request(data.get("method"), data.get("url"), json=data.get("json"))
    token = response.json().get("data", {}).get("token")
    yield token
    # 生成器函数中的暂停关键字，作用是当代码运行到yield时，把yield右边的数据作为返回值提供给调用处，把代码执行权交出去。
    request.logger.info("移除token")