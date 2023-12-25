import functools


# 创建1个函数
def func(a1, a2):
    return a1 + a2


# 又创建1个函数，在func函数基础上创建。
xxx = functools.partial(func, a2=666)

func(1, 2)
xxx(1)
