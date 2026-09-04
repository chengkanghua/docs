import socket
import hashlib
import json

client = socket.socket()
client.connect(('localhost',8001))

message = '''
            1 注册
            2 登录
            3 退出
'''
print(message)
# status = {'status':False}
status = False
while True:
    cmd = input('please cmd: ')
    if not cmd:
        continue
    if cmd == '1':  #registry
        print('welcome registry')
        user = input('please username: ')
        pwd = input('please password: ')
        pwd = hashlib.sha256('123'.encode('utf-8')).hexdigest()
        info_dict = {'user': user, 'pwd': pwd,'method':'registry'}
        client.sendall(json.dumps(info_dict).encode('utf-8'))
        recy = client.recv(1024)
        print(recy.decode('utf-8'))
        continue
    if cmd == '2':  #login
        # print(status)
        # global status
        if status:
            print('登陆过了，ok')
            continue
        print('welcome login')
        user = input('please username: ')
        pwd = input('please password: ')
        # 密码加密
        pwd = hashlib.sha256('123'.encode('utf-8')).hexdigest()
        info_dict = {'user':user,'pwd':pwd,'method':'login'}
        client.sendall(json.dumps(info_dict).encode('utf-8'))
        recy = client.recv(1024)
        recy = recy.decode('utf-8')
        if recy == '1':
            print('登陆成功')
            status = True
            continue
        else:
            print('登陆失败')
            continue

    if cmd == '3':
        info_dict = {'user':'','pass':'','method':'exit'}
        client.sendall(json.dumps(info_dict).encode('utf-8'))
        client.sendall(json.dumps(info_dict).encode('utf-8'))
        break


client.close()
