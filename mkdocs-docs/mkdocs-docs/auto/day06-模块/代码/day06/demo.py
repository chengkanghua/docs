import subprocess

# res = subprocess.getoutput("ls")
# print(res)

# res = subprocess.check_output("ls", shell=True, cwd="/Users/wupeiqi/PycharmProjects/day06/pearvideo")
# print(res)


import paramiko

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='10.211.55.6', port=22, username='root', password='123')
# 执行命令
stdin, stdout, stderr = ssh.exec_command("ls")
# 获取命令结果
result = stdout.read()
# 关闭连接
ssh.close()

print(result)
