from django.test import TestCase


# Create your tests here.
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __setattr__(self, key, value):
        print(key, value)

        if key == "age" and value > 100:
            print("age的年龄不能超过100")
            return
        self.__dict__[key] = value

p = Person("yuan", 22)
p.age = 10000

print(":::", p.age)
