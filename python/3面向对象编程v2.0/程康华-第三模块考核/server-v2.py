'''
程康华-模块3考核 第二次编写代码版本v2.0
'''
import socket
import struct
import json
import os


class Server():
    msg_dict = {
        200: 'registry seuccess',
        201: 'registry error, user is exists',
        300: 'login seuccess',
        301: 'login error, user or pwd error',
    }

    def __init__(self):
        self.ip = 'localhost'
        self.port = 8001
        self.sock = self.servie()
        self.conn, self.addr = self.sock.accept()
        self.user_dict = {}
        self.file_path = './userinfo.json'

    def servie(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.listen(10)
        return sock

    def read_db(self):
        '''数据格式{"aa": {"user": "aa", "password": "202cb962ac59075b964b0715270"}, "bb": {"user": "bb", "password": "202cb964b07152d234b70"}}}
'''
        if not os.path.isfile(self.file_path):
            open(self.file_path, mode='wb').close()
        with open('userinfo.json', mode='r', encoding='utf-8') as f_r:
            data = f_r.read()
            # print(data)
            if data:
                return json.loads(data)
            else:
                return {}
    def write_db(self, data):
        with open('userinfo.json', 'w', encoding='utf-8') as f_w:
            return json.dump(data, f_w)

    def send_data(self, data):
        data = json.dumps(data).encode('utf-8')
        length_data = struct.pack('i', len(data))
        self.conn.send(length_data)
        self.conn.send(data)

    def recv_data(self):
        '''接受数据格式{'user': 'ee', 'password': '202cb962ac59075b964b07152d234b70', 'method': 'login'}'''
        head_data = self.conn.recv(4)
        length_data = struct.unpack('i', head_data)[0]
        # print(length_data)
        data = self.conn.recv(length_data)
        data = json.loads(data.decode('utf-8'))
        # print(data)
        return data

    def registry(self, data):
        self.user_dict = self.read_db()
        # print(self.user_dict)
        if data['user'] in self.user_dict:
            data['status'] = 201
            data['content'] = self.msg_dict[201]
        else:
            self.user_dict[data['user']] = {'user': data['user'], 'password': data['password']}
            self.write_db(self.user_dict)
            data['status'] = 200
            data['content'] = self.msg_dict[200]
        self.send_data(data)

    def login(self, data):
        self.user_dict = self.read_db()
        if not data['user'] in self.user_dict:
            data['status'] = 301
            data['content'] = self.msg_dict[301]
        else:
            line = self.user_dict.get(data['user'])
            if data['user'] == line['user'] and data['password'] == line['password']:
                data['status'] = 300
                data['content'] = self.msg_dict[300]
        self.send_data(data)

    def _quit(self,data):
        exit('Server---exit....')

    def handle(self):
        while True:
            data = self.recv_data()
            # print(data)
            if hasattr(self, data['method']):
                getattr(self, data['method'])(data)

if __name__ == '__main__':
    Server().handle()
