# print("hello world")
# import time
# time.sleep(100)

# l = []
# for i in range(1, 11):
#     l.append(i)


class Person:
    def __init__(self, name):
        self.name = name


l = []
for i in range(5):
    p = Person(i)
    l.append(p)

for obj in l: # [Person(0),Person(1),Person(i),...]
    print(obj.name)

