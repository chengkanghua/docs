"""
弹夹
"""


class Stack(object):

    def __init__(self):
        self.data = []

    def push(self, item):
        """ 在栈中压入一个数据 """
        self.data.append(item)

    def pop(self):
        """ 从栈中弹出一个数据 """
        return self.data.pop(-1)

    def top(self):
        """ 取栈顶的数据 """
        return self.data[-1]


obj = Stack()
obj.push(11)
obj.push(22)
obj.push(33)

v1 = obj.pop()  # 33
v2 = obj.pop()  # 22
v3 = obj.pop()  # 11
