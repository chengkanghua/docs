import pymysql
from dbutils.pooled_db import PooledDB
from config import settings

POOL = PooledDB(creator=pymysql, **settings.DB_POOL_CONN)
''' 数据连接处理方法'''

class Connect(object):
    def __init__(self):
        self.conn = conn = POOL.connection()
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def exec(self, sql, *args, **kwargs):
        params = args or kwargs
        # 执行SQL受影响的行数
        row = self.cursor.execute(sql, params)
        self.conn.commit()
        return row

    def fetch_one(self, sql, *args, **kwargs):
        params = args or kwargs

        # sql = "xxxxx %s %s"
        # self.cursor.execute(sql, [1,2])

        # sql = "xxxxx %(k1)s %(k2)s"
        # self.cursor.execute(sql, {"k1":xxx,"k2":xxxx})

        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        return result

    def fetch_all(self, sql, *args, **kwargs):
        params = args or kwargs
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result
