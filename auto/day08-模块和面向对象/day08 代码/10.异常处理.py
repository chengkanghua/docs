try:
    print(666)
    raise Exception("我错误了") # 主动抛出异常
    # print(999)
except Exception as e:
    print("异常了", str(e))
