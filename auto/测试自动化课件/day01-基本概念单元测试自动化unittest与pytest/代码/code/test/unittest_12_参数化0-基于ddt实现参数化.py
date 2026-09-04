import unittest
from ddt import ddt, data, unpack


def add(a,b,c):
    return a+b+c

@ddt
class MyTest(unittest.TestCase):
    @data((1,2,3),(1,2,1),(1,3,1),(1,1,3))
    @unpack
    def test(self,a,b,c):
        add(a,b,c)

if __name__ == '__main__':
    unittest.main()
