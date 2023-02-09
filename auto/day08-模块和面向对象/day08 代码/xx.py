# class ConfigContext:
#     def __init__(self):
#         self.wx_url = None
#         self.min_inventory = None
#         self.pool_size = None
#         self.max_error_count = None
#
#
# obj = ConfigContext()
# obj.wx_url = 123
# obj.pool_size = 123
#
# # 基于反射的机制进行赋值
# setattr(obj, "wx_url", "xxx") # obj.wx_url = "xxx"
# setattr(obj, "pool_size", 123)


# class ConfigContext:
#     def __init__(self):
#         self.wx_url = None
#         self.min_inventory = None
#         self.pool_size = None
#         self.max_error_count = None
#
#
# obj = ConfigContext()
# obj.wx_url = "123"


class ConfigContext:
    def __init__(self):
        self.wx_url = str
        self.min_inventory = float
        self.pool_size = int
        self.max_error_count = int


config = ConfigContext()
for k, v in config.__dict__.items():
    print(k, v("123"))
