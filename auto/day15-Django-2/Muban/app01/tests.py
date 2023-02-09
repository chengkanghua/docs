from django.test import TestCase

# Create your tests here.



class Dog(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def __str__(self):
        return str(self.age)


d = Dog("alex",23)
print(d)