from logger import LogHandle

logger = LogHandle().get_logger()


def assertor(assert_list, response):
    """断言函数"""
    if type(assert_list) is not list:
        assert_list = [assert_list]

    for expr in assert_list:
        logger.info(f"开始断言：assert {expr}")
        if expr:
            # exec 内置解释器，可以把符合python语法的字符串当成代码来运行
            exec(f"assert {expr}", {
                "code": response.status_code,
                "json": response.json(),
                "text": response.text,
                "content": response.content,
                "headers": response.headers,
            })

        logger.info(f"断言通过：assert {expr}")

if __name__ == '__main__':
    # Response就是模拟requests HTTP请求工具的返回结果对象
    class Response(object):
        status_code = 400
        text = "对不起，登陆失败!"
        content = "对不起，登陆失败!"
        headers = []

        @classmethod
        def json(cls):
            return {"id": 1},

    assert_list = [
        "code == 400",
        "'失败'in text",
    ]

    assertor(assert_list, Response())
