'''
- 用户作为socket客户端

  - 输入`景区名称`，用来查询景区的余票。
  - 输入`景区名称-预订者-8`，用于预定门票。

- socket服务端，可以支持并发多人同时查询和购买。（为每个客户度创建一个线程）。
'''

import socket
import threading
import os, re, datetime

class handle:
    def __init__(self, conn: socket.socket):
        self.conn = conn
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.tickets_path = os.path.join(self.base_dir, 'db/tickets/')
        self.users_path = os.path.join(self.base_dir, 'db/users/')
        self.lock = threading.RLock()
        self.excute()

    def ticket_list(self):
        floder = os.listdir('db/tickets')
        place_list = [word.split(".")[0] for word in floder]
        return place_list

    def query(self, file_name):
        file_object = open('{}{}.txt'.format(self.tickets_path, file_name), mode='r', encoding='utf-8')
        num = file_object.read()
        file_object.close()
        return num

    def reserve(self, place, user, num):
        place_list = self.ticket_list()
        if not place in set(place_list):
            info = '景点不存在，请重试'
            return info
        self.lock.acquire()
        with open(file='{}{}.txt'.format(self.tickets_path, place), mode="r", encoding='utf-8') as f_read:
            place_number = f_read.read()
        place_number = int(place_number) - int(num)
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_number = f'{date_time},{place},{num}\n'
        # 写入文件
        with open(file='{}{}.txt'.format(self.tickets_path, place), mode="w", encoding='utf-8') as f1, \
                open('{}{}.txt'.format(self.users_path, user), mode='a', encoding='utf-8') as f2:
            f1.write(str(place_number))
            f2.write(user_number)
        self.lock.release()
        return '预定成功'

    def excute(self):
        place_list = self.ticket_list()  # 可查询景区名称
        message = """
            - 输入`景区名称`，用来查询景区的余票。
            - 输入`景区名称-预订者-8`，用于预定门票。
            可查询的景区：{}
            q/Q 退出
        """.format(' '.join(place_list))
        self.conn.sendall(message.encode('utf-8'))
        print('有新客户端来了')
        while True:
            try:
                client_data = self.conn.recv(1024)
            except ConnectionError as e:
                print('客户端异常断开：{}'.format(e))
                break
            info = client_data.decode('utf-8')
            if info.upper() == 'Q':
                break
            # 判断是查询 还是 预定
            num = re.findall('-', info)
            if len(num) == 2:
                place, user, num = info.strip().split('-')
                info = self.reserve(place, user, num)
                self.conn.sendall(info.encode('utf-8'))
                continue
            if info in set(place_list):
                num = self.query(info)
                self.conn.sendall('余票：{}'.format(num).encode('utf-8'))
                continue
            else:
                self.conn.sendall('输入有误，重试：'.encode('utf-8'))
                continue
        print('客户端断开了')
        self.conn.close()


class thread_socket:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8001

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(10)

        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=handle, args=(conn,))
            t.start()
            # t.join()


server = thread_socket()
server.run()
