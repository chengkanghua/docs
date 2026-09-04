import time
from multiprocessing import Process
import fcntl


def task():
    while True:
        f = open('x1.txt', mode='a+')
        f.write("666\n")
        time.sleep(1)
        f.close()


if __name__ == '__main__':

    for i in range(5):
        p = Process(target=task)
        p.start()
