import redis
import time

conn = redis.Redis(host='127.0.0.1', port=6379, password='qwe123', encoding='utf-8')

# 1. 在有序集合中放入数据
# add_time = int(time.time())
# conn.zadd("xxxxxxx", {"alex": add_time}),
# conn.zadd("xxxxxxx", {"wupeiqi": add_time + 15}),
# conn.zadd("xxxxxxx", {"ritian": add_time + 30}),

# 2. 根据分值排序并获取数据
current_time = int(time.time())

# 2.1 获取 0 ~ current_time 分数之间的所有数据
data_list = conn.zrangebyscore("xxxxxxx", 0, current_time, withscores=True, score_cast_func=int)
print(data_list)

# # 2.2 删除 0 ~ current_time 分数之间的所有数据
conn.zremrangebyscore("xxxxxxx", 0, current_time)



# print(data_list)
