import traceback


def do():
    try:
        v8 = 666
        v5 = int('asdf')
    except Exception as e:
        message = traceback.format_exc()
        print(message)


def func():
    v1 = 123
    v2 = 456
    do()
    v3 = [11, 22, 33]
    v4 = v1 + v2


func()
