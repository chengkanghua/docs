import unittest

loader = unittest.TestLoader()

suite1 = loader.discover("./", pattern="tests*.py")

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite1)
