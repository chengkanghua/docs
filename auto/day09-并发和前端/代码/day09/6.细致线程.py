import threading

LK = threading.RLock()

DATA = 0


def task():
    # 申请锁
    with LK:
        global DATA
        DATA += 1
        # 释放锁


for i in range(10):
    t = threading.Thread(target=task)
    t.start()
