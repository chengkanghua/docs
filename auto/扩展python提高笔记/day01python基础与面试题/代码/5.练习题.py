"""
{
    k1:[]
    k2:[]
}

"""
# v = dict.fromkeys(['k1', 'k2'], [])
# v['k1'].append(666)
# print(v) # {'k1': [666], 'k2': [666]}
#
# v['k1'] = 777 # # {'k1': 777, 'k2': [666]}
# print(v)

#
# v1 = [11, 22, 33, 44]
# v2 = [55, 66, 77, 88]
# v3 = [55, 66, 77, 88]
# a= [ [11, 22, 33, 44],[55, 66, 77, 88],[55, 66, 77, 88] ]
# import itertools
#
# itertools.chain(v1, v2, v3)  # *args
# itertools.chain(*a)  # *args
#
# result = list(itertools.chain(v1, v2, v3))
# print(result)

# data = itertools.chain(v1,v2)
# for item in data:
#     print(item)


# import itertools
#
# lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#
# val = list(itertools.chain(*lst))
# print(val)

# import copy
# a = [1,2,3,[4,5],6]
# b = a
# c = copy.copy(a)
# d = copy.deepcopy(a)
# b.append(10)
# print(a,b,c,d)

alist = [2,4,5,6,7]
for var in alist:
    if var % 2 ==0:
        alist.remove(var)

print(alist) # [4, 5, 7]