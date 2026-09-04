v1 = ["alex",9, "eric",4,"xx"]

def func(a1):
    if type(a1) == str:
        return True
    return False

result = filter(func,v1) # ["alex","eric","xx"]
res = list( result )
print(res)