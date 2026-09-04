import time

# 所有用户访问记录
record = {
    "alex": [1615102211, 1615102211]
}

# 第一步：提示用户去配置频率（1/s、5/m）
rate = input("请输入限制频率：")
num, period = rate.split('/')
num_requests = int(num)
duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[0]]

# 第二步：用户可以开始访问
while True:
    name = input(">>>")  # alex  / eric
    history = record.get(name, [])  # None
    ctime = time.time()

    while history and history[-1] <= ctime - duration:
        history.pop()
    if len(history) >= num_requests:
        print("频率限制请稍等访问")
        continue
    if name in record:
        record[name].insert(0, ctime)
    else:
        record[name] = [ctime, ]
    print("访问成功", ctime)
