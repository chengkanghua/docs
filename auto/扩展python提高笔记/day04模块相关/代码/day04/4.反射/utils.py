# 定义类
class Settings(object):
    def __init__(self):
        setattr(self, "NAME", "alex")  # self.NAME = "alex"
        setattr(self, "AGE", "73")


# 实例化一个类的对象，在settings对象中存储了两对值
"""
    "NAME", "alex"
    "AGE", "73"
"""
settings = Settings()  # 实例1

