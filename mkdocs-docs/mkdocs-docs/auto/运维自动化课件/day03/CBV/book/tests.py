from django.test import TestCase


# Create your tests here.


# class Fly(object):
#     def fly(self):
#         print("fly...")
#
#
# class Animal(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def sleep(self):
#         print("睡觉...")
#
#     def eat(self):
#         print("吃东西")
#
#
# class Dog(Animal):
#     def wangwang(self):
#         print("旺旺叫")
#
#     def sleep(self):
#         print("仰天大睡")
#
#
# class Cat(Animal):
#     pass
#
#
# class Bird(Animal, Fly):
#     pass
#
#
# class Bat(Animal, Fly):
#     pass
#
#
# b = Bird("alex", 23)
# b.fly()
#
# d = Dog("eric", 33)
# d.fly()


class A:

    def __init__(self,name):
        self.name = name

    def __getattr__(self, item):
        return f"没有属性{item}"


a = A("yuan")

print(a.gender)
