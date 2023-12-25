import threading

POOL = PersistentDB(
    threadlocal=None,  # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123',
    database='pooldb',
    charset='utf8'
)

def task():
    # 去DBUtils中获取一个连接，读取线程ID，为你创建连接并保存。
    conn = POOL.conn()
    conn.send('xxxxx')
    conn.get()


def run():
    for i in range(3):
        t = threading.Thread(target=task)
        t.start()


if __name__ == '__main__':
    pass
