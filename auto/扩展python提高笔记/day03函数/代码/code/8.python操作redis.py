import redis

# 直接连接redis
conn = redis.Redis(host='127.0.0.1', port=6379, password='qwe123', encoding='utf-8')

"""
for i in range(300):
    key = "k{}".format(i)
    conn.set(key, "alexsb", ex=60)
"""

# 获取所有的数据并打印出来。
#   - 1次性全取出来。
#   - 逐一获取。
#   - 连接一次取1000条（一点的一点的获取）


gen_object = conn.scan_iter(count=100)
for item in gen_object:
    print(item)







