import queue

q = queue.Queue()
q.put(123)
q.put("666")

v1 = q.get()
print(v1, type(v1))
v2 = q.get()
print(v2, type(v2))

try:
    v3 = q.get(timeout=10)
    print(v3, type(v3))
except queue.Empty as e:
    pass
