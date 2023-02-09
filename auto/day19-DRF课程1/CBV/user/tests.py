from django.test import TestCase


# Create your tests here.

# class B(object):
#     name = "A"
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.foo()
#
#     def foo(self):
#         print("B foo")
#
#
# class Animal(B):
#     name = "xxx"
#     foo = 100
#
#     def foo(self):
#         print("A foo")
#
#
# alex = Animal("alex", 23)
# print(alex.foo())

# class A(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def name(self):
#         print("name")
#
#
# alex = A("alex", 22)
#
# alex.name()


class Animal(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def foo(self,x):
        print("foo")


alex = Animal("alex", 32)

alex.foo(10)





# attr = input(">>>查看alex的哪一个属性") # "name"

# print(getattr(alex,attr))


getattr(alex,"foo")()
