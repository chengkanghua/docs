import threading
import time

try:
    from greenlet import getcurrent as get_ident   # 协程ID
except ImportError:
    from threading import get_ident                # 线程ID


storage = {}


class Local(object):

    def __setattr__(self, key, value):
        ident = get_ident()  # 获取当前线程ID
        if ident in storage:
            storage[ident][key] = value
        else:
            storage[ident] = {key: value}

    def __getattr__(self, item):
        ident = get_ident()  # 获取当前线程ID
        return storage[ident][item]


local = Local()


# 函数=任务
def task(index):
    local.num = index  # 调用 Local.__setattr__
    print(storage)
    time.sleep(2)
    print(local.num)  # 调用 Local.__getattr__


# 创建了10个线程（类似于创建了10个人，每个人都执行一次task任务）
for i in range(1, 11):  # 1、2、3、4、5..10
    t = threading.Thread(target=task, args=(i,))
    t.start()
