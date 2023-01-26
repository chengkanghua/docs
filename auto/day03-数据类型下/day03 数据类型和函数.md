# day03 数据类型和函数

今日概要：

- 数据类型
- 函数



## 1.字典类型（dict）



### 1.1 定义

```python
info = {  键:值 , 键:值 , 键:值, 键:值 }
```

```python
data = ["123","fff",123,88,19]

info = { "name":"123", "pwd":"fff", "age":123, 'size':88, 'heigth':19}

info["name"]
```

特点：

- 动态
- 容器
- 有序 & 无序
- 值：任意类型；键：可哈希（列表不可哈希、字典、集合都不可以）。
- 查找速度快。



### 1.2 独有功能

- 获取值

  ```python
  info = {"name":"陈聪","age":18,"size":3}
  
  v1 = info.get("name")
  print(v1) # "陈聪"
  
  v2 = info.get("email")
  print(v2) # None
  
  v3 = info.get("email","123123")
  print(v3) # None
  
  
  v4 = info["name"] # "陈聪"
  v5 = info["email"]
  ```

- 获取所有的键

  ```python
  info = {"name":"陈聪","age":18,"size":3}
  
  info.keys()  # ["name","age","size"]
  
  for item in info.keys():
      print(item)
  ```

- 获取所有的值

  ```python
  info = {"name":"陈聪","age":18,"size":3}
  
  info.values()  # ["陈聪",18,3]
  
  for item in info.values():
      print(item)
  ```

- 获取所有的键值对

  ```python
  info = {"name":"陈聪","age":18,"size":3}
  
  info.items() # [ ("name","陈聪"), ("age",18), ("size",3)]
  
  for k,v in info.items():
      # item
  ```

  

### 1.3 公共

- 长度

  ```python
  info = {"name":"陈聪","age":18,"size":3}
  
  data = len(info)
  print(data)  # 3
  ```

- 索引

  ```python
  
  info = {"name":"陈聪","age":18,"size":3}
  
  info["name"]
  info["age"]
  info["size"]
  
  info['name'] = "魏志彪"
  info['email'] = "xxx@live.com"
  
  del info['name']
  ```

- 切片（不支持）

- for循环

- in是否存在

  ```python
  if "xx" in "xxxxfaj;lskdjf;kajsd":
      pass
  
  if 11 in [11,22,33,44]:
      pass
  
  if "xx" in ("xx",11,22,33):
      pass
  
  # 键中是否存在xx
  info = {"name":"陈聪","age":18,"size":3}
  if 'xx' in info:
      pass
  ```



### 1.4 嵌套

```python
info = {
    "k1":123,
    "k2":True,
    "k3":[1,22,33],
    "k4":{1:123,2:999},
    "k5":(11,22),
    "k6":[11,22,33,(111,22), {"k1":123} ]
}

info["k6"][-1]['k1']
```

```python
info = {
    0: 456,
    False: 123,

}
print(info)
```





### 案例

```python
user_dict = {
    "wupeiqi":"123",
    "chencong":"666"
}


user = input("用户名：")
pwd = input("密码：")

db_pwd = user_dict.get(user)
if db_pwd == None:
    print("用户名不存在")
else: 
	if db_pwd != pwd:
        print("密码错误")
	else:
        print("成功")
```

```python
user_list = [
    {"id":1,"name":"董国鹏","age":24},
    {"id":2,"name":"欧阳","age":44},
    {"id":3,"name":"车聪","age":24},
]

while True:
    uid = input(">>")
    name = input(">>")
    age = input(">>")
    
    item = {}
    item["id"] = uid
    item["name"] = name
    item["age"] = age
    
    user_list.append(item)
```

```python
user_list = [
    {"id":1,"name":"董国鹏","age":24},
    {"id":2,"name":"欧阳","age":44},
    {"id":3,"name":"车聪","age":24},
]

while True:
    uid = input(">>")
    name = input(">>")
    age = input(">>")
    item = {"id":uid,"name":name,"age":age}
    user_list.append(item)
```

```python
data_string = """id,name,age
1,欧阳,44
2,陈聪,23
3,懂欧朋,24
"""

data_list = data_string.strip().split('\n')
# ['id,name,age', '1,欧阳,44', '2,陈聪,23', '3,懂欧朋,24']
# print(data_list)

# ['id', 'name', 'age']
header_list = data_list[0].split(",")
print(header_list)

result = []
# 循环数据
for row_string in data_list[1:]:
    row_list = row_string.split(',')

    # row_dict = {header_list[0]: row_list[0], header_list[1]: row_list[1], header_list[2]: row_list[2]}
    row_dict = {}
    for i in range(len(header_list)):
        row_dict[header_list[i]] = row_list[i]
    result.append(row_dict)
print(result)
```

```python
# info={"k1":[123,123]}
info = {}

for i in range(3):
    if "k1" in info:
        info['k1'].append(123)
    else:
        info['k1'] = []
```

```python
data_list = [1,22,33,44,55,66,77,88]
info = {
    "k1":[],
    "k2":[]
}

# 循环data_list中的每个数据，如果小于等于50，则追加到k1对应的列表中；大于50，追加到k2对应的列表中。
for item in data_list:
    if item <= 50:
        info['k1'].append(item)
	else:
        info['k2'].append(item)
```

```python
data_list = [1,22,33,44,55,66,77,88]
info = {}

# 循环data_list中的每个数据，如果小于等于50，则追加到k1对应的列表中；大于50，追加到k2对应的列表中。
for item in data_list:
    if item <= 50:
        if "k1" in info:
            info['k1'].append(item)
        else:
            info['k1'] = [item,]
	else:
        if "k2" in info:
            info['k2'].append(item)
        else:
            info['k2'] = [item,]
```

```python
db = [
    ['王*龙', '北京市 海淀区', '苏州街大恒科技大厦南座4层'],
    ['庞*飞', '北京市 昌平区', '汇德商厦四楼403'],
    ['顾*锐', '江苏省 扬州市', '三垛镇工业集中区扬州市立华畜禽有限公司'],
    ['王*飞', '上海市 徐汇区', '上海市徐汇区H88越虹广场B座5E'],
    ['华*升', '北京市 海淀区', '杰睿大厦'],
    ['朱*锴', '上海市 浦东新区', '川沙新镇华川家园33号楼503'],
]

result = {
    # "北京": ['王*龙', ]
}

for item in db:
    name, address, _ = item
    city = address.split(' ')[0]
    if city in result:
        result[city].append(name)
    else:
        result[city] = [name, ]

print(result)
```



## 2.集合（set）

集合，无序、可变、元素必须可哈希、没有重复数据的 容器。

### 2.1 定义

```python
v1 = [11,22,33] # []   list()
v2 = (11,22,33) # ()   tuple()
v3 = { "k1":123, "k2":123 } # {}   dict()
v4 = { 11,222,333,44} # set()
```



### 2.2 独有功能

- 添加

  ```python
  v1 = {11, 22, 33}
  
  v1.add(44)
  v1.add(55)
  v1.add(22)
  
  print(v1)
  ```

- 删除

  ```python
  v1 = {11, 22, 33}
  
  v1.discard(22)
  
  print(v1)
  ```

- 交集

  ```python
  v1 = {11, 22, 33}
  v2 = {33, 44, 55}
  
  res = v1.intersection(v2)
  print(res)
  
  result = v1 & v2
  print(result)
  ```

- 并集

  ```python
  v1 = {11, 22, 33}
  v2 = {33, 44, 55}
  
  res = v1.union(v2)
  print(res)
  
  result = v1 | v2
  print(result)
  ```

- 差集

  ```python
  v1 = {11, 22, 33}
  v2 = {33, 44, 55}
  
  # res1 = v1 - v2
  res1 = v1.difference(v2)  # v1有且v2没有的数据
  print(res1)
  
  # res2 = v2 - v1
  res2 = v2.difference(v1)  # v2有且v1没有的数据
  print(res2)
  ```



### 2.3 公共

- 长度

  ```python
  v1 = {11, 22, 33}
  
  print(len(v1))
  ```

- 索引，不支持

- 切片，不支持

- 循环

  ```python
  v1 = {11, 22, 33}
  
  for item in v1:
      print(item)
  ```

- 包含

  ```python
  v1 = {11, 22, 33}
  
  # 效率和字典的键一样，效率高
  if 11 in v1:
      pass
  else:
      pass
  ```

集合，不可哈希；元素可哈希。



## 总结

1. 是否可变

   ```python
   可变：list/dict/set
   不可变：其他
   ```

2. 可哈希

   ```python
   可哈希：其他
   不可哈希：list/dict/set
   ```

3. 转换布尔值为False

   ```python
   "" 0 None 空值..
   ```

   ```python
   if 1 > 3:
       pass
   ```

   ```python
   if 999:
       pass
   ```

   ```python
   info = {"k1":123,"k2":456}
   
   data = info.get("k1")
   if data:
       pass
   else:
       pass
   ```

   ```python
   info = {"k1":123,"k2":456}
   
   data = info.get("k1")
   if not data:
       pass
   else:
       pass
   ```

4. 元组

   ```python
   - 自己儿子不能改
   - 儿子内部元素可以修改
   ```

5. 字典的键 & 集合 -> 可哈希。

6. 转换

   ```python
   str/int/list/tuple/dict/set
   
   - 字符串和整型
   	int("xx")
       str(123123)
       
   - list/tuple/set
       v1 = [11,22,33] # []   list()
       v2 = (11,22,33) # ()   tuple()
       v4 = { 11,222,333,44} # set()
       
       data = set([111,222,333,111])
   ```

   

## 3.内存/赋值 相关

```python
v1 = "武沛齐"
v1 = [111,2233]
```

```python
v1 = "武沛齐"
v2 = v1
```



```python
v1 = "root"
v2 = v1

v1.upper()

print(v2) # "root"
```



```python
v1 = [11, 22, 33, ]
v2 = v1

v1.append(44)

print(v2)  # [11, 22, 33, 44]
```

```python
v1 = [11,22,33,]
v2 = [11,22,33,]

v1.append(44)

print(v2) # 
```







```python
v1 = [ 11, 22, [33,44] ]
v2 = v1[-1]

v2.append(444)
```

```python
v1 = [ 11, 22, [33,44] ]
v2 = v1[-1]

v2 = [99,88]
print(v1)
```



```python
data_list = [
    [10,22,34,[] ],
    [20,22,34,[]],
    [30,22,34,[]],
]

data_list[0][-1].append( data_list[1] )
data_list[1].append(999)
```

```python
data_list = [
    [10,22,34,[ [20,22,34,[]],  ] ],
    [20,22,34,[]],
    [30,22,34,[]],
]
```





```python
info = {
    1:[11,22,33,44],
    2:[33,422],
    3:[99,88]
}

for k,v in info.items():
    v.append(666)
    
print(info)
```



```python
data_list = [
    
]

info = {
    1: [11, 22, 33, 44],
    2: [33, 422],
    3: [99, 88]
}

for item in info.values():
    data_list.append(item)
    
info[1].append(666)
```





### 案例

```python
data_list = [
    {"id": 1, "name": "董国鹏", "text": "这个位置真不用错", 'children': []},
    {"id": 2, "name": "陈聪", "text": "我觉得还行把", 'children': []},
    {"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'children': []},
]

result = {}
for item in data_list:
    user_id = item["id"]
    result[user_id] = item

result[1]['children'].append(999)

print(data_list)

```

```
result = {
    1:{"id":1,"name":"董国鹏","text":"这个位置真不用错", 'children':[] },
    2:{"id":2,"name":"陈聪","text":"我觉得还行把", 'children':[] },
    3:{"id":3,"name":"魏志彪","text":"我特么懵逼了", 'children':[] },
}
```



```python
data_list = [
    {"id": 1, "name": "董国鹏", "text": "这个位置真不用错", 'children': []},
    {"id": 2, "name": "陈聪", "text": "我觉得还行把", 'children': []},
    {"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'children': []},
]

result = {}
for item in data_list:
    user_id = item["id"]
    result[user_id] = {"name": item['name'], "text": item['text'], 'id': item['id'], "children": item['children']}

result[1]['name'] = '123123'

print(data_list)

```

```python
result = {
    1:{"id":1,"name":"董国鹏","text":"这个位置真不用错", 'children':[] },
    2:{"id":2,"name":"陈聪","text":"我觉得还行把", 'children':[] },
    3:{"id":3,"name":"魏志彪","text":"我特么懵逼了", 'children':[] },
}
```



```python
comment_list = [
    {"id": 1, "name": "董国鹏", "text": "这个位置真不用错", 'reply': None},  # 地址
    {"id": 2, "name": "陈聪", "text": "我觉得还行把", 'reply': None},  # 地址
    {"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'reply': 1},
    {"id": 4, "name": "王卓", "text": "你真美", 'reply': 1},
    {"id": 5, "name": "王卓", "text": "你真美", 'reply': 2},
    {"id": 6, "name": "基友", "text": "xx", 'reply': 4},
    {"id": 7, "name": "基友", "text": "fff", 'reply': 5},
    {"id": 8, "name": "基友", "text": "sdf", 'reply': 3},
    {"id": 9, "name": "基友", "text": "fff", 'reply': 1},
    {"id": 10, "name": "基友", "text": "到处ss留情", 'reply': 2},
]

"""
result = [
    {"id": 1, "name": "董国鹏", "text": "这个位置真不用错", 'reply': None,'child':[
        {"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'reply': 1,'child':[]},
        {"id": 4, "name": "王卓", "text": "你真美", 'reply': 1,'child':[
            {"id": 6, "name": "基友", "text": "xx", 'reply': 4,'child':[]},
        ]},
    ]}, # 地址
    {"id": 2, "name": "陈聪", "text": "我觉得还行把", 'reply': None,'child':[]}, # 地址
]
"""
result = []
for item in comment_list:
    if item['reply']:
        continue
    result.append(item)

"""
data_dict = {
    1:{"id": 1, "name": "董国鹏", "text": "这个位置真不用错", 'reply': None,'child':[
        {"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'reply': 1,'child':[]},
        {"id": 4, "name": "王卓", "text": "你真美", 'reply': 1,'child':[
            {"id": 6, "name": "基友", "text": "xx", 'reply': 4,'child':[]},
        ]},
    ]},  # 地址
    2:{"id": 2, "name": "陈聪", "text": "我觉得还行把", 'reply': None,'child':[
        {"id": 5, "name": "王卓", "text": "你真美", 'reply': 2,'child':[]},
    ]},  # 地址
    3:{"id": 3, "name": "魏志彪", "text": "我特么懵逼了", 'reply': 1,'child':[]},
    4:{"id": 4, "name": "王卓", "text": "你真美", 'reply': 1,'child':[
        {"id": 6, "name": "基友", "text": "xx", 'reply': 4,'child':[]},
    ]},
    5:{"id": 5, "name": "王卓", "text": "你真美", 'reply': 2,'child':[]},
    6:{"id": 6, "name": "基友", "text": "xx", 'reply': 4,'child':[]},
    7:{"id": 7, "name": "基友", "text": "fff", 'reply': 5,'child':[]},
    8:{"id": 8, "name": "基友", "text": "sdf", 'reply': 3,'child':[]},
    9:{"id": 9, "name": "基友", "text": "fff", 'reply': 1,'child':[]},
    10:{"id": 10, "name": "基友", "text": "到处ss留情", 'reply': 2,'child':[]},
}   
"""
data_dict = {}
for item in comment_list:
    cid = item['id']
    item['child'] = []
    data_dict[cid] = item

for item in data_dict.values():
    reply = item['reply']
    if not reply:
        continue
    data_dict[reply]['child'].append(item)

print(result)

import json

print(json.dumps(result, indent=2,ensure_ascii=False))
```









## 4.推导式

一行代码去生成数据。

```python
num_list = []
for i in range(1,301):
    num_list.append(i)
```

```python
user_list = []
for i in range(1,301):
    item = "用户-{}".format(i)
    user_list.append(item)
```



- 列表推导式

  ```python
  # [1,2,3,4...300]
  num_list = [ i for i in range(1,301) ]
  ```

  ```python
  num_list = [ i+100 for i in range(1,301) ]
  ```

  ```python
  num_list = [ str(i+100) for i in range(1,301) ]
  ```

  ```python
  # [ [1,123], [2,123], ...   ]
  num_list = [ [i,123] for i in range(1,301) ]
  ```

  ```python
  num_list = [ 9 for i in range(1,301) ]
  ```

  ```python
  # [100,100]
  num_list = [ 100 for i in range(100) if i > 7 and i<10 ]
  ```

  ```python
  data_list = [ "欧阳精心", "欧阳陈聪", "欧阳王卓", "董国鹏", "明宇","接电话"]
  
  result = [ item for item in data_list if len(item) >3 ]
  ```

  ```python
  data_list = [ "欧阳精心",[11,22,33],11,2, "欧阳陈聪", 1, "欧阳王卓", "董国鹏", "明宇","接电话"]
  
  
  result = [ item for item in data_list if type(item) == str or type(item) == int ]
  ```

  ```python
  data_list = ["欧阳精心", "欧阳陈聪", "欧阳王卓", "董国鹏", "明宇", "接电话"]
  
  result = [item[-2:] for item in data_list]
  
  print(result)
  ```

  ```python
  data_list = [
      '5 编译器和解释器.mp4',
      '9 Python解释器种类.mp4',
      '21 课堂笔记的创建.mp4',
      '82 Python介绍.mp4',
      '70 编程语言的分类.mp4',
      '3 常见计算机基本概念.mp4',
      '1 今日概要.mp4',
      '6 学习编程本质上的三件事.mp4',
      '4 编程语言.mp4',
  ]
  
  result = [ int(item.split(" ")[0]) for item in data_list]
  print(result)
  ```

- 字典推导式

  ```python
  info = { i:123 for i in range(10)}
  info = { i:123+100 for i in range(10)}
  
  info = { i:123+100 for i in range(10) if i > 5}
  ```

  ```python
  data_list = [
      '5 编译器和解释器.mp4',
      '9 Python解释器种类.mp4',
      '21 课堂笔记的创建.mp4',
      '82 Python介绍.mp4',
      '70 编程语言的分类.mp4',
      '3 常见计算机基本概念.mp4',
      '1 今日概要.mp4',
      '6 学习编程本质上的三件事.mp4',
      '4 编程语言.mp4',
  ]
  
  result = { item.split(" ")[0]:item.split(" ")[1] for item in data_list}
  ```

  ```python
  data = "query=fff&_asf=www.sogou.com&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index"
  
  result = {item.split('=')[0]: item.split('=')[1] for item in data.split("&")}
  
  print(result)
  ```

  ```python
  params = {'query': 'fff', '_asf': 'www.sogou.com', 'w': '01019900', 'p': '40040100', 'ie': 'utf8',
            'from': 'index-nologin', 's_from': 'index'}
  
  # "query=fff&_asf=www.sogou.com&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index"
  str_list = []
  
  for k, v in params.items():
      str_list.append(k)
      str_list.append('=')
      str_list.append(v)
      str_list.append("&")
  
  result = "".join(str_list)[:-1]
  print(result)
  
  ```

  ```python
  params = {'query': 'fff', '_asf': 'www.sogou.com', 'w': '01019900', 'p': '40040100', 'ie': 'utf8',
            'from': 'index-nologin', 's_from': 'index'}
  
  # "query=fff&_asf=www.sogou.com&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index"
  str_list = []
  
  for k, v in params.items():
      ele = k + "=" + v  # query=fff
      str_list.append(ele)
  
  res = "&".join(str_list)
  print(res)
  ```

  ```python
  params = {'query': 'fff', '_asf': 'www.sogou.com', 'w': '01019900', 'p': '40040100', 'ie': 'utf8',
            'from': 'index-nologin', 's_from': 'index'}
  
  # "query=fff&_asf=www.sogou.com&w=01019900&p=40040100&ie=utf8&from=index-nologin&s_from=index"
  str_list = []
  
  for k, v in params.items():
      ele = "{}={}".format(k, v)
      str_list.append(ele)
  
  res = "&".join(str_list)
  print(res)
  ```

  ```python
  params = {'query': 'fff', '_asf': 'www.sogou.com', 'w': '01019900', 'p': '40040100', 'ie': 'utf8',
            'from': 'index-nologin', 's_from': 'index'}
  
  res = "&".join(["{}={}".format(k, v) for k, v in params.items()])
  print(res)
  ```

- 集合推导式

  ```python
  data = {i for i in range(10)}
  print(data)
  ```

- 生成器

  ```python
  data = (i for i in range(1000000000))
  
  for item in data:
      print(item)
  ```

  

## 5.第一阶段考试题

- 入门
- 数据类型









































































