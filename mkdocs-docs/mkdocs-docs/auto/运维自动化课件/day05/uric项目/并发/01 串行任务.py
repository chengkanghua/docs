import time


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
foo()
# bar()
print("cost timer:", time.time() - start)
