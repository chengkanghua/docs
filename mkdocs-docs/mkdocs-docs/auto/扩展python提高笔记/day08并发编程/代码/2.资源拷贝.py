import time
import multiprocessing


def task(new_name):
    new_name.append(123)
    print(name)  # [123]


if __name__ == '__main__':
    multiprocessing.set_start_method("fork")  # 拷贝
    # multiprocessing.set_start_method("spawn")  # 报错
    # multiprocessing.set_start_method("forkserver")  # 报错
    name = []
    p1 = multiprocessing.Process(target=task, args=(name,))
    p1.start()

    time.sleep(2)
    print(name)  # []
