v1 = [11, 22, 33]

print(v1[2])

res = v1.__getitem__(2)
print(res)

method = getattr(v1, '__getitem__')
res = method(2)
print(res)
