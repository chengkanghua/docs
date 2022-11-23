import re
import os
import socket
import config as config
import utils.req as req


class client():
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        welcome = """
        用户登录：login 用户名 密码
        用户注册：register 用户名 密码
        查看网盘：ls 目录
        上传文件：upload 本地目录 远程目录
        下载文件：download 本地目录 远程目录
        """
        print(welcome)
        # client = socket.socket()
        self.conn.connect((config.HOST, config.PORT))
        while True:
            text = input("输入内容(Q/q退出):").strip()
            if text.upper() == "Q":
                break
            func, *args = re.split(r"\s+", text)
            method = {
                "login": self.login,
                "register": self.register,
                "ls": self.ls,
                "upload": self.upload,
                "download": self.download,
            }
            method_tf = method.get(func)
            if not method_tf:
                print("输入格式错误")
                continue
            else:
                method_tf(*args)

        self.conn.close()

    def login(self, *args):
        if len(args) != 2:
            print("格式错误")
            return
        user, pwd = args
        content = f"login {user} {pwd}"
        req.send_data(self.conn, content)
        reply = req.recv_data(self.conn)
        print(reply.decode("utf-8"))

    def register(self, *args):
        if len(args) != 2:
            print("格式错误")
            return
        user, pwd = args
        content = f"register {user} {pwd}"
        req.send_data(self.conn, content)
        reply = req.recv_data(self.conn)
        print(reply.decode("utf-8"))

    def ls(self, dir):
        content = f"ls {dir}"
        req.send_data(self.conn, content)
        dir = req.recv_data(self.conn)
        print(dir.decode("utf-8"))

    def upload(self, *args):
        if len(args) != 2:
            print("格式错误")
            return
        local_path, remote_path = args
        # 默认文件都存在files中
        local_path = os.path.join(config.SAVE_PATH, local_path)
        if not os.path.exists(local_path):
            print("未找到本地文件")
            return

        content = f"upload {remote_path}"
        req.send_data(self.conn, content)

        reply = req.recv_data(self.conn).decode("utf-8")
        print(reply)
        if reply == "开始上传":
            req.send_file(self.conn, local_path)
            print("上传完毕")

    def download(self, *args):
        if len(args) != 2:
            print("格式错误")
            return

        local_path, remote_path = args
        seek = 0
        local_path = os.path.join(config.SAVE_PATH, local_path)
        local_path_dir = os.path.dirname(local_path)
        if not os.path.exists(local_path_dir):
            os.makedirs(local_path_dir)
        if not os.path.exists(local_path):
            content = f"download {remote_path}"
            req.send_data(self.conn, content)
            mode = "wb"
        else:
            choice = input("是否续传（Y/N）")
            if choice.upper() == "Y":
                seek = os.stat(local_path).st_size
                req.send_data(self.conn, f"download {remote_path} {seek}")
                mode = "ab"
            else:
                req.send_data(self.conn, f"download {remote_path}")
                mode = "wb"
        reply = req.recv_data(self.conn).decode("utf-8")
        print(reply)
        if reply == "开始下载":
            req.recv_save_file_by_seek(self.conn, local_path, mode, seek)
            print("下载完成")
