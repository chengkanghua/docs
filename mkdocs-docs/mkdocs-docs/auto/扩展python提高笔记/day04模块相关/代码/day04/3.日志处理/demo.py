import traceback

try:
    print(123)
    int("hello")
except Exception as e:
    # 记录日志
    # print(str(e))  # invalid literal for int() with base 10: 'hello'
    print(traceback.format_exc())  # invalid literal for int() with base 10: 'hello'

    # 不是线程安全
    """
    f = open('xxx.log', mode='a+')
    f.write(traceback.format_exc())
    f.close()
    """

    # Logging模块是线程安全，10个线程（10个人）
