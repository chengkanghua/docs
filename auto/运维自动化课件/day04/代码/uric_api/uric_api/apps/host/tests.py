import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException

if __name__ == '__main__':
    # 通过parammiko创建一个ssh短连接客户端实例对象
    ssh = paramiko.SSHClient()
    # 自动在本机第一次连接远程服务器时，记录主机指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 1. 直接密码远程连接的方式
        ssh.connect(hostname='47.112.179.213', port=22, username='root', password='Yuan0316', timeout=10)

        # 连接成功以后，就可以发送操作指令
        # stdin 输入[本机发送给远程主机的信息]
        # stdout 输出[远程主机返回给本机的信息]
        # stderr 错误
        stdin, stdout, stderr = ssh.exec_command('ls')
        # 读取stdout对象中返回的内容，返回结果bytes类型数据
        result = stdout.read()
        print(result.decode())
        # 关闭连接
        ssh.close()
    except AuthenticationException as e:

        print("连接参数有误，请检查连接信息是否正确！~")
