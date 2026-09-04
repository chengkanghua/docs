import redis

# 直接连接redis
conn = redis.Redis(host='47.98.134.86', port=6379, password='foobared', encoding='utf-8')

# k1=abc (存活10s)
conn.set('k1', "abc", ex=10)

# 获取数据
value = conn.get('k1')
print(value)  # 字节类型
