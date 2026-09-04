import time
from concurrent.futures import ThreadPoolExecutor


def task(v1):
    time.sleep(1)
    return v1


pool = ThreadPoolExecutor(10)
fu_list = []
for i in range(100):
    future = pool.submit(task, i)
    fu_list.append(future)

pool.shutdown()
# 执行完毕之后，自行此处代码
for obj in fu_list:
    data = obj.result()
    print(data)
