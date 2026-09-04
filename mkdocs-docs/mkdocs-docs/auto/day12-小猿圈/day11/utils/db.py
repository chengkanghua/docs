import pymysql
from dbutils.pooled_db import PooledDB

MYSQL_DB_POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=5,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=3,  # 链接池中最多闲置的链接，0和None不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    host='101.35.49.95', port=3306, user='luffy', passwd='root123', charset="utf8", db='luffy'
)


def execute(sql, *args, **kwargs):
    params = args or kwargs

    # 获取一个连接（去连接池）
    conn = MYSQL_DB_POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql, params)
    conn.commit()
    cursor.close()

    # 连接交还给连接池
    conn.close()


def fetch_all(sql, *args, **kwargs):
    params = args or kwargs
    conn = MYSQL_DB_POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql, params)
    data_list = cursor.fetchall()

    # 关闭连接
    cursor.close()
    conn.close()

    return data_list


def fetch_one(sql, *args, **kwargs):
    params = args or kwargs
    conn = MYSQL_DB_POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql, params)
    data_list = cursor.fetchone()

    # 关闭连接
    cursor.close()
    conn.close()

    return data_list
