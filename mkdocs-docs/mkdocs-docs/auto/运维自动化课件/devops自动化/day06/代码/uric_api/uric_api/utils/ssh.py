from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException
from io import StringIO
from paramiko.ssh_exception import NoValidConnectionsError


class SSHParamiko(object):
    def __init__(self, hostname, port=22, username='root', pkey=None, password=None, connect_timeout=3):
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
    def get_connected_client(self):
        if self.client is not None:
            # 告知当前执行上下文，self.client已经实例化
            raise RuntimeError('已经建立连接了！！！')

        if not self.client:
            try:
                # 创建客户端连接对象
                self.client = SSHClient()
                # 在本机第一次连接远程主机时记录指纹信息
                self.client.set_missing_host_key_policy(AutoAddPolicy)
                # 建立连接: 口令密码或者密钥
                self.client.connect(**self.params)
            except (TimeoutError, NoValidConnectionsError, AuthenticationException) as e:
                return None

        return self.client

    @staticmethod
    def gen_key():
        # 生成公私钥键值对
        iodata = StringIO()
        key = RSAKey.generate(2048)  # 生成长度为2024的秘钥对
        key.write_private_key(iodata)
        # 返回值是一个元祖，两个成员分别是私钥和公钥
        return iodata.getvalue(), 'ssh-rsa ' + key.get_base64()

    # 将公钥上传到对应主机
    def upload_key(self, public_key):
        print("self.client:::", self.client)
        # 700 是文档拥有可读可写可执行，同一组用户或者其他用户都不具有操作权限
        # 600 是文件拥有者可读可写，不可执行，同一组用户或者其他用户都不具有操作权限
        cmd = f'mkdir -p -m 700 ~/.ssh && \
            echo {public_key!r} >> ~/.ssh/authorized_keys && \
            chmod 600 ~/.ssh/authorized_keys'
        code, out = self.execute_cmd(cmd)
        print("out", out)
        if code != 0:
            raise Exception(f'添加公钥失败: {out}')

    def execute_cmd(self, cmd, timeout=1800):
        # 设置执行指令过程，一旦遇到错误/异常，则直接退出操作，不再继续执行。
        cmd = 'set -e\n' + cmd
        channel = self.client.get_transport().open_session()
        channel.settimeout(timeout)
        channel.set_combine_stderr(True)  # 正确和错误输出都在一个管道对象里面输出出来
        channel.exec_command(cmd)
        try:
            out_data = channel.makefile("rb", -1).read().decode()
        except UnicodeDecodeError:
            out_data = channel.makefile("rb", -1).read().decode("GBK")

        return channel.recv_exit_status(), out_data

    def upload_file(self, fl, remote_path):
        """
        上传文件到远程主机
        :param fl: 本地文件的句柄对象  fl = open()
        :param remote_path: 远程主机保存文件的路径与文件名
        :return:
        """
        sftp = self.client.open_sftp()
        return sftp.putfo(fl, remote_path)

    def download_file(self, remote_path, local_path):
        """
        从远程主机下载文件到本地
        :param remote_path: 远程主机要下载的文件的路径+文件名
        :param local_path: 本地保存下载文件的路径地址
        :return:
        """
        sftp = self.client.open_sftp()
        return sftp.get(remote_path, local_path)

    def list_dir_attr(self, remote_path):
        """
        列出远程主机的指定路径下所有的文件/目录的相关信息
        模拟：ls -l 命令
        :param remote_path:
        :return:
        """
        sftp = self.client.open_sftp()
        return sftp.listdir_attr(remote_path)

    def remove_file(self, remote_path):
        """
        删除指定文件
        :param remote_path: 远程主机上要删除文件的路径+文件名，如果没有对应文件会报错，有返回None
        :return:
        """
        sftp = self.client.open_sftp()
        return sftp.remove(remote_path)

    # 删除远程主机上的目录
    def remove_dir(self, remote_path):
        """
        删除空目录
        :param remote_path: 远程主机上要删除的空目录的路径
        :return:
        """
        sftp = self.client.open_sftp()
        sftp.rmdir(remote_path)


