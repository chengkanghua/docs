import multiprocessing
import threading


def do():
    pass


def task():
    for i in range(3):
        t = threading.Thread(target=do)
        t.start()


def run():
    for i in range(2):
        # 创建多个进程
        p = multiprocessing.Process(target=task)
        p.start()


if __name__ == '__main__':
    run()
