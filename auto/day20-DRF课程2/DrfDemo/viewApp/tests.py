class Animal(object):

    def sleep(self):
        print("sleep...")



class Fly(object):

    def fly(self):
        print("fly...")


class Dog(Animal):
    pass


class Bat(Animal,Fly):
    pass


class Bird(Animal,Fly):
    pass


alex = Dog()
alex.sleep()


b = Bat()
b.fly()

