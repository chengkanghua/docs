'''
    - 需求：
        - 客户端运行程序后，有登录和注册、退出三个功能
        - 当用户选择注册，让用户输入用户名和密码，并对密码进行md5加密，然后将数据传给 sever 端，server校验用户名是否存在
            - 存在则返回用户已存在，让客户端重新注册
            - 如果不存在，则保存注册信息，并返回注册成功
        - 如果用户选择登录，将用户输入的信息发送到server端进行校验
            - 成功提示登录成功
            - 否则提示登录失败
            - 重复登录时，能自动登录
        - 如果用户选择退出，结束客户端程序并断开连接
'''
import socket
import hashlib
import threading
import json


def registry(user, pwd):
    # 先判断用户是否存在
    with open('userinfo.txt', mode='r', encoding='utf-8') as f_r:
        for line in f_r:
            print(line)
            username, password = line.strip().split(',')
            print(username, password)
            if username == user:
                return '用户已存在'
    # 存入用户
    with open('userinfo.txt', mode='a', encoding='utf-8') as f_w:
        line = '{},{}\n'.format(user, pwd)
        f_w.write(line)
        return '注册成功'

def login(user, pwd):
    flag = False
    with open('userinfo.txt', mode='r', encoding='utf-8') as f_r:
        for line in f_r:
            username, password = line.strip().split(',')
            if username == user and password == pwd:
                flag = True
    if flag:
        return '1'  # 成功1
    else:
        return '2'  # 失败2

def task(conn: socket.socket):
    while True:
        cmd = conn.recv(1024)
        cmd_dict = json.loads(cmd.decode('utf-8'))
        print(
            cmd_dict)  # {'user': 'aa', 'pwd': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'method': 'registry'}
        if cmd_dict['method'] == 'registry':
            info = registry(cmd_dict['user'], cmd_dict['pwd'])
            conn.sendall(info.encode('utf-8'))
            continue
        if cmd_dict['method'] == 'login':
            info = login(cmd_dict['user'], cmd_dict['pwd'])
            print(info)
            conn.sendall(info.encode('utf-8'))
            continue
        if cmd_dict['method'] == 'exit':
            break
        # print(cmd.decode('utf-8'))

    conn.close()


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 8001))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        print('new clinet is comeing ')
        t = threading.Thread(target=task, args=(conn,))
        t.start()

    sock.close()


if __name__ == '__main__':
    run()
