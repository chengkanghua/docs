import functools

li = [1, 2, 3, 4, 5]


def func(a1, a2):
    print(a1, a2)
    return a1 + a2


result = functools.reduce(func, li)
print(result)
