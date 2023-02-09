from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException
from io import StringIO
from paramiko.ssh_exception import NoValidConnectionsError


class SSHParamiko(object):
    def __init__(self, hostname, port=22, username='root', pkey=None, password=None, connect_timeout=2):
        if pkey is None and password is None:
            raise SSHException('私钥或者密码必须选择传入一个')

        self.client = None

        self.params = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'pkey': RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            'timeout': connect_timeout,
        }

    # 检测连接并获取连接
    def is_validated(self):
        print(f"self.client={self.client}")
        if self.client is not None:
            # 告知当前执行上下文，self.client已经实例化
            raise RuntimeError('已经建立连接了！！！')
        print(f"正在ping通{self.client}")
        if not self.client:
            try:
                # 创建客户端连接对象
                self.client = SSHClient()
                # 在本机第一次连接远程主机时记录指纹信息
                self.client.set_missing_host_key_policy(AutoAddPolicy)
                # 建立连接
                self.client.connect(**self.params)
            except (TimeoutError, NoValidConnectionsError, AuthenticationException) as e:
                return None
        return True
