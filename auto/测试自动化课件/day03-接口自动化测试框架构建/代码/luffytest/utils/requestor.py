import requests
from logger import LogHandle


class Request(object):
    """http请求工具类"""
    def __init__(self):
        # 实例化session管理器，维持会话, 跨请求的时候保存参数
        self.session = requests.session()
        self.logger = LogHandle().get_logger()

    def send(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """
        :param method: http请求方式
        :param url: 请求地址
        :param params: 字典或bytes，作为参数增加到url中
        :param data: data类型传参，字典、字节序列或文件对象，作为Request的内容
        :param json: json传参，作为Request的内容
        :param headers: 请求头，字典
        :param kwargs: 若还有其他的参数，使用可变参数字典形式进行传递
        :return:
        """
        # 对异常进行捕获
        try:
            self.logger.info(f"请求方法：{method}")
            self.logger.info(f"请求地址：{url}")
            self.logger.info(f"请求头：{headers}")
            if params: self.logger.info(f"查询参数：params={params}")
            if data: self.logger.info(f"请求体：data={data}")
            if json: self.logger.info(f"请求体：json={json}")
            if kwargs: self.logger.info(f"额外参数：kwargs={kwargs}")
            response = self.session.request(method, url, params=params, data=data, json=json, headers=headers, **kwargs)
            self.logger.info(f"状态码：{response.status_code}")
            self.logger.info(f"响应头：{response.headers}")
            self.logger.info(f"响应体[纯文本]：{response.text}")
            self.logger.info(f"响应体[二进制]：{response.content}")
            self.logger.info(f"响应体[json]：{response.json()}")
            # 返回响应结果
            return response

        except Exception as e:
            # 异常处理 报错在日志中打印具体信息
            self.logger.error(f"请求失败：{e}")

    def __call__(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """当把一个对象，当成函数来使用，那么就指定执行当前对象的__call__"""
        return self.send(method, url, params=params, data=data, json=json, headers=headers, **kwargs)

if __name__ == '__main__':
    """"基本使用"""
    # 实例化
    request = Request()

    """发送get请求"""
    # # response = request("GET", 'http://httpbin.org/get')
    # response = request(method="GET", url='http://httpbin.org/get')
    # # 打印响应结果
    # print(response.text)

    """发送post请求"""
    # 请求地址
    url = 'http://httpbin.org/post'
    # 请求参数
    json = {"usernam": "moluo", "password": "123456"}
    # 请求头
    headers = {"company": "luffytest"}
    response = request(method="POST", url=url, json=json, headers=headers)
    # 打印响应结果
    print(response.text)

