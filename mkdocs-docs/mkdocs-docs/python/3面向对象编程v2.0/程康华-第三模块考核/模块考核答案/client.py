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
        """发送数据{'user': 'aa', 'pwd': '202cb962ac59075b964b07152d234b70', 'action_type': 'register'}"""
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