'''
程康华-模块3考核 第二次编写代码版本v2.0
'''
import socket
import json
import struct
import hashlib


class Client(object):

    def __init__(self):
        self.ip = 'localhost'
        self.port = 8001
        self.client = self.connent_server()
    def connent_server(self):
        client = socket.socket()
        client.connect((self.ip,self.port))
        return client
    def get_md5(self, data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def send_data(self, data):
        data = json.dumps(data).encode('utf-8')
        len_data = struct.pack('i',len(data))
        self.client.send(len_data)
        self.client.send(data)

    def recv_data(self):
        head_data = self.client.recv(4)
        length_data = struct.unpack('i',head_data)[0]
        data = self.client.recv(length_data).decode('utf-8')
        return json.loads(data)
    def registry(self):
        print('welcome registry')
        username, password = input('please username: '), input('please password: ')
        data = {'user': username, 'password': self.get_md5(password), 'method': 'registry'}
        self.send_data(data)
        reply_data = self.recv_data()
        print(reply_data['content'])

    def login(self):
        print('welcome login')
        username, password = input('please username: '), input('please password: ')
        data = {'user': username, 'password': self.get_md5(password), 'method': 'login'}
        self.send_data(data)
        reply_data = self.recv_data()
        print(reply_data['content'])


    def _quit(self):
        data = {'method':'_quit'}
        self.send_data(data)
        exit('client -- exit...')
    def handler(self):
        message = {
            '1': {'msg': '注册', 'method': self.registry},
            '2': {'msg': '登陆', 'method': self.login},
            '3': {'msg': '退出', 'method': self._quit},
        }
        for k, v in message.items():
            print(k, v['msg'])  # 打印功能选项
        while True:
            cmd = input('select num: ')
            if not cmd in message.keys():
                print('输入错误，请重试')
                continue
            message[cmd]['method']()




if __name__ == '__main__':
    Client().handler()
