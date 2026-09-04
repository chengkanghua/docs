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
    user_info_path = './userinfo.json'   #确定文件路径

    def __init__(self):
        self.request, addr = sock.accept()  #初始化 接收客户端连接    只能连接一次  阻塞状态

    def read_file(self):
        if not os.path.isfile(self.user_info_path):
            open(self.user_info_path, 'wb').close()   #创建的空文件
        with open(self.user_info_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                return json.loads(data)   #反序列化 返回字典
            else:
                return {}

    def write_file(self, data):
        with open(self.user_info_path, 'w', encoding='utf-8') as f:
            return json.dump(data, f)  #json 序列化写入文件 正常返回None

    def send_msg(self, data):
        """发送数据{'user': 'aa', 'pwd': '202cb962ac59075b964b07152d234b70', 'action_type': 'register', 'status': 200, 'content': 'register error, user exists！'}"""
        print(data)
        head_data = json.dumps(data).encode()  #序列化数据并编码
        head_size = struct.pack('i', len(head_data))  #格式数据获取文件头
        self.request.send(head_size)     #发送文件头    这里用sendall更好一些
        self.request.send(head_data)     #发送文件      这里用sendall更好一些
        # sock.send(json.dumps(data).encode())

    def recv_msg(self):
        """接收数据"""
        head_size = self.request.recv(4)  #  接收4字节，  不保证每次一定接收的4个字节
        st_data = struct.unpack('i', head_size)[0]  #解包获取数据长度
        head_data = self.request.recv(st_data).decode()  #接收 指定的数据长度  解码后
        print(json.loads(head_data))
        return json.loads(head_data)         #返回反序列化数据

    def q(self, data):
        """ sever端退出 """
        exit('server exit......')  #结束主进程 退出程序

    def login(self, data):
        user_info = self.read_file()  #返回数据字典
        if data['user'] == user_info.get(data['user'])['user'] and data['pwd'] == user_info.get(data['user'])['pwd']:
            data['status'] = 202
            data['content'] = self.msg[202]
            data['login_status'] = True
        else:
            data['status'] = 203
            data['content'] = self.msg[203]
            data['login_status'] = False
        self.send_msg(data)    #发送登陆结果出去

    def register(self, data):
        user_info = self.read_file()  #返回数据字典
        if data['user'] in user_info:
            data['status'] = 200
            data['content'] = self.msg[200]     #注册失败
        else:
            user_info[data['user']] = {"user": data['user'], "pwd": data['pwd']}  #组装数据字典
            print(user_info)
            self.write_file(user_info)  #写入新用户
            data['status'] = 201
            data['content'] = self.msg[201]  #注册成功
        self.send_msg(data)

    def handler(self):
        while True:
            data = self.recv_msg()
            if hasattr(self, data['action_type']):  #判断类中是否有这个方法
                getattr(self, data['action_type'])(data)  #有的话执行


if __name__ == '__main__':
    Server().handler()
