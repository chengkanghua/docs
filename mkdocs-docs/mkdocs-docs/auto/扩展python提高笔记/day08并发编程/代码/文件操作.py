import time

f1 = open('v1.log', 'a', encoding='utf-8')

while True:
    # 判断，文件是否被更改。
    # 如果更改过，就重新打开； 未更改，就继续用。
    f1.write("xxxx\n")
    f1.flush()
    time.sleep(1)
