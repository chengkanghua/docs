import datetime
from utils.db import Connect

''' 账户登录注册 功能'''


def login(username, password):
    with Connect() as conn:
        # sql = "select id,nickname from user where username=%s and password=%s"
        # result = conn.fetch_one(sql, username, password)

        sql = "select id,nickname from user where username=%(username)s and password=%(password)s"
        result = conn.fetch_one(sql, username=username, password=password)

        return result  # 返回是的 {username: value ,password: value }


def register(user, pwd, nickname, cellphone, email):
    with Connect() as conn:
        sql = "insert into user(username,password,nickname,cellphone,email,ctime) values(%s,%s,%s,%s,%s,%s)"
        result = conn.exec(sql, user, pwd, nickname, cellphone, email, datetime.datetime.now())
        return result
