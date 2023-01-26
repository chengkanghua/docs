import paramiko

transport = paramiko.Transport(('10.211.55.6', 22))
transport.connect(username='root', password='123')
sftp = paramiko.SFTPClient.from_transport(transport)

# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/Users/wupeiqi/PycharmProjects/day08/v1.py', '/tmp/test666.py')

# 将remove_path 下载到本地 local_path
# sftp.get('remote_path', 'local_path')

transport.close()
