"""
-- 如何查看类和对象的名称空间
"""
# class Foo(object):
#     def bar(self):
#         pass
# # 类的名称空间
# print(Foo.__dict__)
# # 对象的名称空间
# f = Foo()
# f.a = 'a'
# print(f.__dict__)

"""
-- 什么是反射？反射相关的方法是什么？请用反射执行下面类中的 show_course 方法
class Foo(object):
    def show_course(self):
        print('show course')
"""
# 什么是反射？通过字符串的形式操作对象的属性或者方法。
# 反射相关的方法是： hasattr()和getattr()
# class Foo(object):
#
#     def show_course(self):
#         print('show course')
#
#
# f = Foo()
# if hasattr(f, 'show_course'):
#     obj = getattr(f, 'show_course')
#     obj()
"""
-- 列举常用的内置方法
"""
# __setattr__, __delattr__, __getattr__,__getattribute__, __getattr__
# __get__, __set__, __delete__,__enter__, __exit__,__call__
# __setitem__, __getitem__, __delitem__
# __str__, __repr__, __format__,__init__, __del__
# __slots__,__next__, __iter__,__doc__, __module__, __class__

"""
-- 编写一个学生类，并且实现一个计数器功能，统计这个类一共实例化了多少个实例对象
"""
class Student(object):
    count = 0
    def __init__(self, name):
        self.name = name
        Student.count += 1
s1 = Student('zhangkai1')
s2 = Student('zhangkai2')
s3 = Student('zhangkai3')
print(Student.count)
"""
-- 模拟tcp协议,做一个注册登录功能
    - 文件构成
        D:\demo
            - server.py
            - client.py
            - userinfo.json    # 你也可以选择其他类型的文件
    - 需求：
        - 客户端运行程序后，有登录和注册、退出三个功能
        - 当用户选择注册，让用户输入用户名和密码，并对密码进行md5加密，然后将数据传给 sever 端，server校验用户名是否存在
            - 存在则返回用户已存在，让客户端重新注册
            - 如果不存在，则保存注册信息，并返回注册成功
        - 如果用户选择登录，将用户输入的信息发送到server端进行校验
            - 成功提示登录成功
            - 否则提示登录失败
        - 如果用户选择退出，结束客户端程序并断开连接
        - 运行示例：
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 1
            user: root
            pwd: 123
            register successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 1
            user: root
            pwd: 123
            register error, user exists！
            user: admin
            pwd: 123
            register successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 2
            user: root
            pwd: 123
            login successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 2
            自动登录成功.....
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 3
            client exit.......
"""
# json文件长这样
# {"zhangkai": {"user": "zhangkai", "pwd": "202cb962ac59075b964b07152d234b70"}, "likai": {"user": "likai", "pwd": "202cb962ac59075b964b07152d234b70"}, "wangkai": {"user": "wangkai", "pwd": "202cb962ac59075b964b07152d234b70"}, "sunkai": {"user": "sunkai", "pwd": "202cb962ac59075b964b07152d234b70"}, "root": {"user": "root", "pwd": "202cb962ac59075b964b07152d234b70"}}
# ------------------ server --------------------
import os
import socket
import json
import struct
from socket import SOL_SOCKET, SO_REUSEADDR
sock = socket.socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 8888))
sock.listen(5)

class Server(object):
    msg = {
        200: "register error, user exists！",
        201: "register successful",
        202: "login successful",
        203: "login error, user or password error",
    }
    user_info_path = './userinfo.json'
    def __init__(self):
        self.request, addr = sock.accept()
    def read_file(self):
        if not os.path.isfile(self.user_info_path):
            open(self.user_info_path, 'wb').close()
        with open(self.user_info_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return {}
    def write_file(self, data):
        with open(self.user_info_path, 'w', encoding='utf-8') as f:
            return json.dump(data, f)
    def send_msg(self, data):
        """发送数据"""
        head_data = json.dumps(data).encode()
        head_size = struct.pack('i', len(head_data))
        self.request.send(head_size)
        self.request.send(head_data)
        # sock.send(json.dumps(data).encode())
    def recv_msg(self):
        """接收数据"""
        head_size = self.request.recv(4)
        st_data = struct.unpack('i', head_size)[0]
        head_data = self.request.recv(st_data).decode()
        return json.loads(head_data)
    def q(self, data):
        """ sever端退出 """
        exit('server exit......')
    def login(self, data):
        user_info = self.read_file()
        if data['user'] == user_info.get(data['user'])['user'] and data['pwd'] == user_info.get(data['user'])['pwd']:
            data['status'] = 202
            data['content'] = self.msg[202]
            data['login_status'] = True
        else:
            data['status'] = 203
            data['content'] = self.msg[203]
            data['login_status'] = False
        self.send_msg(data)
    def register(self, data):
        user_info = self.read_file()
        if data['user'] in user_info:
            data['status'] = 200
            data['content'] = self.msg[200]
        else:
            user_info[data['user']] = {"user": data['user'], "pwd": data['pwd']}
            self.write_file(user_info)
            data['status'] = 201
            data['content'] = self.msg[201]
        self.send_msg(data)

    def handler(self):
        while True:
            data = self.recv_msg()
            if hasattr(self, data['action_type']):
                getattr(self, data['action_type'])(data)

if __name__ == '__main__':
    Server().handler()
# ----------------------- client --------------------
import socket
import json
import hashlib
import struct

class Client(object):
    user_dict = {}
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8888
        self.connect_socket()
    def connect_socket(self):
        """绑定IP、端口"""
        self.request = socket.socket()
        self.request.connect((self.host, self.port), )
    def send_msg(self, data):
        """发送数据"""
        head_data = json.dumps(data).encode()
        head_size = struct.pack('i', len(head_data))
        self.request.send(head_size)
        self.request.send(head_data)
    def recv_msg(self):
        """接收数据"""
        head_size = self.request.recv(4)
        st_data = struct.unpack('i', head_size)[0]
        head_data = self.request.recv(st_data).decode()
        return json.loads(head_data)
    def get_md5(self, meg):
        return hashlib.md5(meg.encode()).hexdigest()
    def login(self, ):
        if self.user_dict.get("login_status", False):
            print('自动登录成功.....')
        else:
            while True:
                user, pwd = input('user: ').strip(), input('pwd: ').strip()
                if user and pwd:
                    data = {"user": user, "pwd": self.get_md5(pwd), 'action_type': 'login'}
                    # print(data)
                    self.send_msg(data)
                    recv_data = self.recv_msg()
                    if recv_data.get("status") == 202:
                        print(recv_data.get("content"))
                        self.user_dict = recv_data
                        break
                    else:
                        print(recv_data.get("content"))
    def register(self, ):
        while True:
            user, pwd = input('user: ').strip(), input('pwd: ').strip()
            if user and pwd:
                data = {"user": user, "pwd": self.get_md5(pwd), 'action_type': 'register'}
                # print(data)
                self.send_msg(data)
                recv_data = self.recv_msg()
                if recv_data.get("status") == 201:
                    print(recv_data.get("content"))
                    self.user_dict = recv_data
                    break
                else:
                    print(recv_data.get("content"))
    def q(self, ):
        """ client exit """
        self.send_msg({"action_type": 'q'})
        exit('client exit.......')
    def handler(self, ):
        tmp_dict = {
            "1": ['注册', self.register],
            "2": ['登录', self.login],
            "3": ['退出', self.q],
        }
        while True:
            for k, v in tmp_dict.items():
                print(k, v[0])
            choice = input('根据序号选择操作: ').strip()
            if choice in tmp_dict:
                tmp_dict[choice][-1]()
            else:
                print('输入不合法!!!')

if __name__ == '__main__':
    Client().handler()