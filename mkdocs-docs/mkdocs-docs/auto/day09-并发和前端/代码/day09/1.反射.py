class Foo(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


obj1 = Foo("欧阳", 99)
print(obj1.name)

delattr(obj1, 'name')

print(obj1.name)

