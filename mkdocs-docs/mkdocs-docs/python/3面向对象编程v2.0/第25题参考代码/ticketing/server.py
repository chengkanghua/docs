import os
import socket
import threading
import datetime
import time

BOOKING_LOCK = threading.RLock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_PATH = os.path.join(BASE_DIR, "db", 'tickets')
USERS_PATH = os.path.join(BASE_DIR, "db", 'users')


def search(conn, name):
    """
    查询
    :param conn: 客户端连接对象
    :param name: 景区名称
    """
    file_name = "{}.txt".format(name)
    file_path = os.path.join(TICKETS_PATH, file_name)

    if not os.path.exists(file_path):
        conn.sendall("暂不支持此景区{}的预定。".format(name).encode('utf-8'))
        return

    with open(file_path, mode='r', encoding='utf-8') as file_object:
        count = int(file_object.read().strip())

    conn.sendall("景区{}剩余票数为：{}。".format(name, count).encode('utf-8'))


def booking(conn, name, user, count):
    """
    预定
    :param conn: 客户端连接对象
    :param name: 景区名称
    :param user: 预订者
    :param count: 预定数量
    """
    file_name = "{}.txt".format(name)
    file_path = os.path.join(TICKETS_PATH, file_name)
    if not os.path.exists(file_path):
        conn.sendall("暂不支持此景区{}的预定。".format(name).encode('utf-8'))
        return

    if not count.isdecimal():
        conn.sendall("预定数量必须是整型。".encode('utf-8'))
        return

    booking_count = int(count)
    if booking_count < 1:
        conn.sendall("预定数量至少1张。".encode('utf-8'))
        return

    # 线程锁
    BOOKING_LOCK.acquire()

    with open(file_path, mode='r', encoding='utf-8') as file_object:
        count = int(file_object.read().strip())

    if booking_count > count:
        conn.sendall("预定失败，景区{}剩余票数为：{}。".format(name, count).encode('utf-8'))
        return

    count = count - booking_count
    with open(file_path, mode='w', encoding='utf-8') as file_object:
        file_object.write(str(count))

    user_file_name = "{}.txt".format(user)
    user_path = os.path.join(USERS_PATH, user_file_name)
    with open(user_path, mode='a', encoding='utf-8') as file_object:
        line = "{},{},{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d"), name, booking_count)
        file_object.write(line)

    # 人为让预定时间久一点
    time.sleep(5)

    conn.sendall("预定成功".encode('utf-8'))
    BOOKING_LOCK.release()


def task(conn):
    """ 当用户连接成功后，处理客户端的请求 """
    while True:
        client_data = conn.recv(1024)
        if not client_data:
            print("客户端失去连接")
            break

        data = client_data.decode('utf-8')
        if data.upper() == "Q":
            print("客户端退出")
            break

        data_list = data.split("-")

        if len(data_list) == 1:
            search(conn, *data_list)
        elif len(data_list) == 3:
            booking(conn, *data_list)
        else:
            conn.sendall("输入格式错误".encode('utf-8'))
    conn.close()


def initial_path():
    """ 初始化文件路径 """
    path_list = [TICKETS_PATH, USERS_PATH]
    for path in path_list:
        if os.path.exists(path):
            continue
        os.makedirs(path)


def run():
    """ 主函数 """

    initial_path()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8001))
    sock.listen(5)
    while True:
        # 等待客户端来连接
        conn, addr = sock.accept()

        t = threading.Thread(target=task, args=(conn,))
        t.start()

    sock.close()


if __name__ == '__main__':
    run()
