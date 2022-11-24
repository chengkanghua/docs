import requests

from UserInfo_pb2 import Request, Response

def test_protobuf_api():
    """
    测试 接口
    :return:
    """
    request_data = Request()
    # 编写请求信息
    request_data.data = "user"
    request_data.page = 1
    request_data.pageSize = 10
    req_data = request_data.SerializeToString()  # 序列化
    response = requests.post("http://127.0.0.1:6666/api/user", data=req_data)

    # 获取响应内容
    res = Response()
    # response.content 原生响应体内容
    res.ParseFromString(response.content)  # 反序列化
    print(res.code)  # 200
    print(res.message)  # Success
    for data in res.dataList:
        print(f"用户名: {data.username}, 年龄:{data.age}, 邮箱: {data.email}")


if __name__ == '__main__':
    test_protobuf_api()