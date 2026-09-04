from UserInfo_pb2 import Request, Response
from flask import Flask, request

app=Flask(__name__)


# RPC接口规范，强调要使用post方法！！！
@app.route("/api/user", methods=["POST"])
def user_info():
    # 解析请求
    request_data = Request()
    print(request.get_data())  # 原生请求body
    request_data.ParseFromString(request.get_data())

    # 打印客户端的请求体
    print("data",request_data.data) # data user
    print("page",request_data.page) # page 1
    print("pageSize",request_data.pageSize) # pageSize 10

    # 编写响应信息
    response = Response()
    response.code = 200
    response.message = "Success"
    data_list = [
        {"username":"小明", "age": 18, "email":"xiaoming@mofang.com"},
        {"username":"小白", "age": 18, "email":"xiaobai@mofang.com"},
    ]

    for data in data_list:
        item = response.data()
        item.username = data["username"]
        item.age = data["age"]
        item.email = data["email"]
        response.dataList.append(item)

    return response.SerializeToString(), 200

if __name__ == '__main__':
    app.run("127.0.0.1", port = 6666)
