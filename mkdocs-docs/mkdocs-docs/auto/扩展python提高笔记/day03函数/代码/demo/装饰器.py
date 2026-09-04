def ck(func):
    print(3)

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner


def lock(func):
    print(2)

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner


def outer(func):
    print(1)

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner


@ck
@lock
@outer
def do():
    print(123)
