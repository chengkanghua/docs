class Base(object):
    def v1(self):
        print("Base.v1")


class Foo(Base):
    def v2(self):
        print("F1.v2")


obj = Foo()
obj.v3()
