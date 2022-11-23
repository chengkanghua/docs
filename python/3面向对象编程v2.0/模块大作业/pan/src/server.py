import socket
from config import settings

class Server(object):
    def __init__(self):
        self.host = settings.HOST
        self.port = settings.PORT

    def run(self, handler):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        while True:
            conn, addr = sock.accept()
            print("新客户端来连接")
            instance = handler(conn)
            while True:
                result = instance.execute()
                if not result:
                    break
            conn.close()
        sock.close()
