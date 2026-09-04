def desc(count):
    def outer(func):
        def inner(*args, **kwargs):
            result_list = []
            for i in range(count):
                res = func(*args, **kwargs)
                result_list.append(res)
            return result_list

        return inner

    return outer


@desc(2)
def index(a1, a2):
    return a1 + a2


data = index(1, 1)
print(data)  # []
