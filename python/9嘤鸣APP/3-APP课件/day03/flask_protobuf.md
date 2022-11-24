## Protobuf

### 基本介绍

Protobuf(Google Protocol Buffers)是google开发的的一套用于数据存储，网络通信时用于协议编解码的工具库.它和XML和Json数据差不多,把数据以某种格式组织并保存起来，Protobuf相对与XML和Json的不同之处，它是一种**二进制的数据格式**，具有更高的传输，打包和解包效率。Protobuf 提供了C++、java、python、nodejs、php、go语言的支持，提供了windows(proto.exe)和linux平台动态编译生成proto文件对应的源文件。proto文件定义了协议数据中的实体结构(message ,field)。因为有google背书，所以在各个语言中被迅速普及，常见的应用场景就是微服务架构和DDD架构！

protoBuf下载地址：https://github.com/protocolbuffers/protobuf/releases

## flask中基于protobuf实现api接口

### 环境搭建

```bash
# 安装格式转换工具，不同的操作系统，转换工具不同。windows->proto.exe，Linux->protobuf-compiler
sudo apt install -y protobuf-compiler
pip install flask
# python下面用于对protobuf进行编码解码的模块
pip install protobuf==3.19.0
# 网络请求工具库
pip install requests
```



### 接口代码

编写Protobuf数据数据，`UserInfo.proto`，代码：

```protobuf
syntax = "proto3";

// 请求体
message Request {
  string data = 1;
  int32 page = 2;
  int32 pageSize = 3;
}

// 响应体
message Response {
  int32 code = 1;
  string message = 3;
  repeated data dataList = 2;
  message data {
    string username = 1;
    string email = 2;
    int32 age = 3;
  }
}
```

编译转换成python格式

```bash
protoc --python_out=./   UserInfo.proto
```

服务端接口，`server.py`，代码：

```python
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

```

客户端，`client.py`，代码：

```python
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
```

先有运行服务端代码，再运行客户端代码，即可查看效果。