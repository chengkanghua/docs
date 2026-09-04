data = [11, 22, 33, 4, 5]


def func(arg):
    arg.append(999)


func(data)
print(data)
