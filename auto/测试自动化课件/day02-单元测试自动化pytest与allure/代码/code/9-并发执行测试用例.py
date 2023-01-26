def add(x, y):
    return x + y


class TestAdd(object):
    def test_01(self):
        res = add(10, 20)
        assert res is 30

    def test_02(self):
        res = add("10", "20")
        assert res == "1020"

    def test_03(self):
        res = add("10", "20")
        assert res == "1020"

    def test_04(self):
        res = add("10", "20")
        assert res == "1020"

    def test_05(self):
        res = add("10", "20")
        assert res == "1020"

    def test_06(self):
        res = add("10", "20")
        assert res == "1020"
