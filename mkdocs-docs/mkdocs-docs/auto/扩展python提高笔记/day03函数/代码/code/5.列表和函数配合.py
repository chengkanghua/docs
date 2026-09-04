import functools


def f1():
    pass


def f2(n1):
    pass


def f3(n1, n2):
    pass


func_list = [
    f1, functools.partial(f2, 11),
    functools.partial(f3, 2, 3),
    functools.partial(f3, 100, 200)
]
for func in func_list:
    func()
