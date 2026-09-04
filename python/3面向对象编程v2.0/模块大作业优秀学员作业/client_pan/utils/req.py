# -*- code:utf-8 -*-
import os
import time
import struct
import config as config


def send_data(conn, content):
    data = content.encode("utf-8")
    header = struct.pack("i", len(data))
    conn.sendall(header)
    conn.sendall(data)


def recv_data(conn, chunk_size=1024):
    # 获取头部信息，长度
    has_read_size = 0
    bytrs_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        has_read_size += len(chunk)
        bytrs_list.append(chunk)
    header = b"".join(bytrs_list)
    data_length = struct.unpack("i", header)[0]

    # 获取数据
    data_list = []
    has_read_data_size = 0
    while has_read_data_size < data_length:
        size = chunk_size if (data_length - has_read_size) > chunk_size else data_length - has_read_data_size
        chunk = conn.recv(size)
        data_list.append(chunk)
        has_read_data_size += len(chunk)
    data = b"".join(data_list)

    return data


def recv_save_file_by_seek(conn, file_path, mode, seek=0, chunk_size=1024):
    file_path = os.path.join(config.SAVE_PATH, file_path)
    # 获取头文件
    has_read_size = 0
    bytes_list = []
    while has_read_size < 4:
        chunk = conn.recv(4 - has_read_size)
        bytes_list.append(chunk)
        has_read_size += len(chunk)
    header = b"".join(bytes_list)
    data_length = struct.unpack("i", header)[0]

    # 读与写
    with open(file_path, mode=mode) as file_object:
        file_object.seek(seek)
        has_read_data_size = 0
        while has_read_data_size < data_length:
            size = chunk_size if (data_length - has_read_data_size) > chunk_size else (data_length - has_read_data_size)
            chunk = conn.recv(size)
            file_object.write(chunk)
            file_object.flush()
            has_read_data_size += len(chunk)

            percent = "\r{}%".format(int(has_read_data_size * 100 / (data_length - seek)))
            print(percent, end="")
            time.sleep(0.5)
        print("")


def send_file(conn, file_path):
    file_size = os.stat(file_path).st_size
    header = struct.pack("i", file_size)
    conn.sendall(header)

    has_send_size = 0
    with open(file_path, mode="rb") as file_object:
        while has_send_size < file_size:
            chunk = file_object.read(1024)
            conn.sendall(chunk)
            has_send_size += len(chunk)
