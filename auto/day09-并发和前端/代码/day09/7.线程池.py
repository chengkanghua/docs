import time
from concurrent.futures import ThreadPoolExecutor


def task(v1):
    time.sleep(1)
    print(v1)


# 创建线程池，做多有10个线程
pool = ThreadPoolExecutor(10)

# 100任务丢给线程池
for i in range(100):
    pool.submit(task, i)

print(1)
pool.shutdown()
print(2)  # 执行完毕的动作
