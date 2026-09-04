import time
import threading

"""
{
    1190:{num:1},
    1888:{num:2}
    ...
    9000:{num:10}
}
"""
obj = threading.local()  # 为线程进行隔离。


# 函数=任务
def task(index):
    obj.num = index  # 在内部读取线程ID
    time.sleep(2)  # 线程1停住；线程2停住；.... 线程10

    message = "当前线程是{}，内部读取num等于{}".format(index, obj.num)  # 1
    print(message)


# 创建了10个线程（类似于创建了10个人，每个人都执行一次task任务）
for i in range(1, 11):  # 1、2、3、4、5..10
    t = threading.Thread(target=task, args=(i,))
    t.start()
