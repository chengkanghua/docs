# websocket的视图类代码
# channels中所有的webscoetk视图类，都必须直接或间接继承于WebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from host.models import Host
from threading import Thread
from uric_api.utils.key import PkeyManager
from django.conf import settings
from uric_api.utils.ssh import SSHParamiko

class SSHCmdConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = self.scope['url_route']['kwargs']['id']
        # websocket通讯的管道对象
        self.ssh_chan = None
        # 这就是基于paramiko连接远程服务器时的ssh操作对象
        self.ssh = None

    def read_response(self):
        while True:
            data = self.ssh_chan.recv(64 * 1024)
            if not data:
                self.close()
                break
            self.send(data.decode())

    # 4 接收客户端发送过来的指令，并发送给主机执行指令
    def receive(self, text_data=None, bytes_data=None):
        data = text_data or bytes_data
        print('receive:', data, type(data))
        if data:
            self.ssh_chan.send(data + '\r\n')

    def disconnect(self, code):
        """websocket断开连接以后，服务端这边也要和远程主机关闭ssh通信"""
        self.ssh_chan.close()
        self.ssh.close()
        print('Connection close')

    # 1 请求来了自动触发父类connect方法，我们继承拓展父类的connect方法，因为我们和客户端建立连接的同时，就可以和客户端想要操作的主机建立一个ssh连接通道。
    def connect(self):
        print('connect连接来啦')
        self.accept()  # 建立websocket连接，进行连接的三次握手
        self.send('Connecting ...\r\n')
        host = Host.objects.filter(pk=self.id).first()
        try:
            private_key, public_key = PkeyManager.get(settings.DEFAULT_KEY_NAME)
            print(private_key, public_key)
            self.ssh = SSHParamiko(host.ip_addr, host.port, host.username, private_key)
            self.client = self.ssh.get_connected_client()
        except Exception as e:
            self.send(f'Exception: {e}\r\n')
            self.close()
            return

        self.ssh_chan = self.client.invoke_shell(
            term='xterm')  # invoke_shell激活shell终端模式，也就是长连接模式，exec_command()函数是将服务器执行完的结果一次性返回给你；invoke_shell()函数类似shell终端，可以将执行结果分批次返回，所以我们接受数据时需要循环的取数据
        self.ssh_chan.transport.set_keepalive(30)  # 连接中没有任何信息时，该连接能够维持30秒
        # 和主机的连接一旦建立，主机就会将连接信息返回给服务端和主机的连接通道中，并且以后我们还要在这个通道中进行指令发送和指令结果的读取，所以我们开启单独的线程，去连接中一直等待和获取指令执行结果的返回数据
        t = Thread(target=self.read_response)
        t.start()