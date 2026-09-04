import redis

r = redis.Redis(host='127.0.0.1', port=6379, password="qwe123")
# r.set('foo1', 'Bar', ex=10)
# r.set('foo2', 'Bar', ex=10)
# r.set('foo3', 'Bar', ex=10)
# r.set('foo4', 'Bar', ex=10)
# r.set('foo5', 'Bar', ex=10)

data = r.scan_iter("foo*")
for item in data:
    print(item)
