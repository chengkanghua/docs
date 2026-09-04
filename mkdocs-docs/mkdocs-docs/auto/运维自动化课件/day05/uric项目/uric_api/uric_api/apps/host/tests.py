import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException

# if __name__ == '__main__':
#     # 通过parammiko创建一个ssh短连接客户端实例对象
#     ssh = paramiko.SSHClient()
#     # 自动在本机第一次连接远程服务器时，记录主机指纹
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     try:
#         # 1. 直接密码远程连接的方式
#         ssh.connect(hostname='47.112.179.213', port=22, username='root', password='', timeout=10)
#
#         # 连接成功以后，就可以发送操作指令
#         # stdin 输入[本机发送给远程主机的信息]
#         # stdout 输出[远程主机返回给本机的信息]
#         # stderr 错误
#         stdin, stdout, stderr = ssh.exec_command('ls')
#         # 读取stdout对象中返回的内容，返回结果bytes类型数据
#         result = stdout.read()
#         print(result.decode())
#         # 关闭连接
#         ssh.close()
#     except AuthenticationException as e:
#
#         print("连接参数有误，请检查连接信息是否正确！~")


######################################################
import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException
from paramiko.rsakey import RSAKey
from io import StringIO

if __name__ == '__main__':
    # 通过parammiko创建一个ssh短连接客户端实例对象
    ssh = paramiko.SSHClient()
    # 自动在本机第一次连接远程服务器时，记录主机指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 1. 直接密码远程连接的方式
        # ssh.connect(hostname='47.112.179.213', port=22, username='root', password='', timeout=10)
        # 注意，如果你测试某个服务器的连接时，如果你本地已经配置了这个远程服务器的免密登录(公私钥模式)，那么就不能测试出密码是否正确了，因为首先会通过公私钥模式登录，不会使用你的密码的。
        # 2. 使用秘钥免密登录的方式
        # pkey = PkeyModel.objects.get(name='').private
        private_key ='''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA9LMOlN+7xmF2TVJI+xXMSJGK3jype8d829Vo28Kopb2bVpNm
7UVjYLKRRzNG9QtG+5s4EiG4XWJfjD4tEpZkVBINTAMVUa4PJH9nqLMKxqH9YQGl
QN9R/iwmPMYDTHHNND+0OqdmvY3JHozZ1qufrYqXaL3AMpPudzh16nEhfhxKXoKc
ho7gvE70nhmhkxbCf97AaI2lAPsBV6l/1FdBLvJQ47F1vsoti2/UHYu77HidsP8t
ok++rShEkFXBtrHpV2vAdD+A+N9RO2bNSKh/OAltYqfPX83s/mTMGhAR2K+sLhm9
H16v6KLVEXEFUzRtHVghMH17zydvxS0iRCX18wIDAQABAoIBAAY9sOAEKs5e+vzy
3dClmC27pI6RfoMdLeaPdVqxhsqfYOBe5w+jJus28rSdrrAeRwOwzEfOG10qXqR9
i3m/YzSvty4aoAcSyOkV5MdtNZemVweL2rKiX317k8gWBsyC1IiCHW8niNvJy3jf
f8jVXL+42q69tDK2Ci15P6yokQGd21VWlbzcTaEQU23Y9s49ZIoqLAtnF1MKnWv3
qAzT+22UC5hDp906MCFjCYurROznXNV0GxAXahAcqlVB2su3leSzBXbxVT3b+YAz
994CF8JGHf/ziEshFsVG2IsOdBQeBQIh+b6RZ9j+ry0D0XFB0AtE9gKvYMnO0sjZ
ref2+50CgYEA+hk5PZ3t2jhw1XB5Gsq4oXyyxXLh2IcNmRvHMoc4ADWDYkjr1x7E
pjfcXIhuX8stkugeNu30dA/v9sk+fVuvGoLFuNKRQ/5+JDIQqTplrqksbSApx7bb
6p3OLpC2BcA4cD7i4bSxRceef6xKRqDKysEIndOD4z2rAO5cTGOR7K8CgYEA+nk4
DXAqaGbtl3ShkzvRGy8EvYhfpT+B+VYjY/h/oE36vKDcHSZUzv3vrWKaA6fzGCMs
Y/N11yFvXyw4uTPSPZhlEQ5gLVOi5rXyp8X6QSXk2LwrcQGj/eE4ro1B+yk4ppWL
Q8kmzbIM9fLSSTcBq/8w6mop2Bl4qp6wjo+nA/0CgYEAqZ+r6/eOF4BKPuj+qkYt
/RDXKwWk2beXaG2np8SAHdwtlN6CXi+3Dkk6wuOhgIUMDuQxge3X61PX29hX8qvZ
UjC5q4XdEnGr2h6+oBhEWLbSs9ypmZOTCkgnS/vICJR7ct2kAZMM3JfsDwmqgsaR
Y/ySPID1pYzwyzvfC8xIb28CgYAJacrYfnGpkMy3F3QHE4VtTxwPf3OQw01AMKON
20X4oVWeBzGeitU/Hj4GtyDwqDwzmQbPDtRL7H7CBehv1Wm+VN7fgDnPGkiSAR6I
faFFF4Z9Or0rNxORtAgsTzS+mrL9V7tvJb0ml91y1NhgVgfjDekptimybGqjhuk9
wlpVhQKBgQCkzWj+TTx3knfEQgwgidss1l4Mt8qgbo+1XP9Avt3i5O0KFISo9K2j
ScpFGCtBno0TQidmZs/q3djWG5tFahdi0Ao56E4x9EFvGF0MTTEhNFkot3X4XO97
VRNkz/1BoZE+VGhQ8tvvz5dyBYNFS75fqdJmBGBNk9fbKYbZ0Twwvg==
-----END RSA PRIVATE KEY-----'''
        pkey = RSAKey.from_private_key(StringIO(private_key))
        ssh.connect(hostname='47.112.179.213', port=22, username='root', pkey=pkey, timeout=10)

        # 连接成功以后，就可以发送操作指令
        # stdin 输入[本机发送给远程主机的信息]
        # stdout 输出[远程主机返回给本机的信息]
        # stderr 错误
        stdin, stdout, stderr = ssh.exec_command('ls -la')
        # 读取stdout对象中返回的内容，返回结果bytes类型数据
        result = stdout.read()
        print(result.decode())
        # 关闭连接
        ssh.close()
    except AuthenticationException as e:
        print(traceback.format_exc())
        print("连接参数有误，请检查连接信息是否正确！~")
