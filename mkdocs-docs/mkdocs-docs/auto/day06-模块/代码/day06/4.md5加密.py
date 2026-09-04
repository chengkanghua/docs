import hashlib

DATA_DICT = {}


def md5(data_string):
    """ MD5加密"""
    salt = "xdqadkfjasdkjfa".encode('utf-8')
    obj = hashlib.md5(salt)
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


def register():
    user = input("用户名：")
    pwd = input("密码：")
    encrypt_pwd = md5(pwd)
    DATA_DICT[user] = encrypt_pwd


def login():
    user = input("用户名：")
    pwd = input("密码：")
    encrypt_pwd = md5(pwd)

    db_pwd = DATA_DICT.get(user)
    if encrypt_pwd == db_pwd:
        print("登录成功")
    else:
        print("登录失败")


if __name__ == '__main__':
    register()
