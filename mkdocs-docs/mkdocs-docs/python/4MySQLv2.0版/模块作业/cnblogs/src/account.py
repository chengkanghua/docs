import datetime
from utils.db_pool import db


# 登陆
def login(username, password):
    sql = 'select id,nickname from user where username=%(username)s and password=%(password)s  '
    result = db.fetch_one(sql, username=username, password=password)
    return result


# 注册
def registry(username, nickname, password, cellphone, email):
    # 检查用户是否已经注册
    name_sql = 'select count(1) as ct from user where username=%s'
    result = db.exec(name_sql,username)
    # print(result) # 1
    if result:
        print('用户已经注册,请重试')
        return False

    sql = 'insert into user(username,nickname,password,cellphone,email,ctime) values(%s,%s,%s,%s,%s,%s)'
    result = db.exec(sql, username, nickname, password, cellphone, email, datetime.datetime.now())
    return result


# if __name__ == '__main__':
    # print(datetime.datetime.now())
    # result = registry('bb', 'bb','123','18679886499','bb@qq.com')
    # print(result)

