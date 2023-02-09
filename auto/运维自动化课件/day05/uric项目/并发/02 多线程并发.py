import time
import threading


def foo():
    print("foo start")
    time.sleep(3)
    # ret = 1
    # for i in range(1, 100001):
    #     ret *= i
    # print(ret)
    print("foo end")


def bar():
    print("bar start")
    time.sleep(5)  # read spider
    print("bar end")


start = time.time()

# 开启多线程

t1 = threading.Thread(target=foo, args=(), )
t1.start()

t2 = threading.Thread(target=bar, args=(), )
t2.start()

print("两个字线程已经启动")

# 等待两个子线程运行结束再执行
t1.join()
t2.join()
print("cost timer:", time.time() - start)
