'''
对于基础整体掌握程度还行。
对于变量和内存这块理解的也可以。
对于默写列表、字符串、元组、字典的常用方法：str.startswith    str.endswith
对于列表的切片方面，基本操作还行，但对于步长和从右往左切片掌握的不是很好，对于步长理解稍差。
通过for循环配合range打印1-100时，同样对于从右往左打印有点迷糊，不清楚 1，2这种步长的用法。
但整体上，对于基础掌握的还行，遇到问题没有出现明显的无法下手的情况。
后续通过多做复习和练习这些问题都会逐步得到解决。
if
if/else
if/elif
if/elif....else
if/if
if嵌套
'''

"""
1. 在多行注释中(既不能使用pycharm的智能提示)，列举 str list dict set tuple 这几种数据类型的常用方法


2. 列表li = ['alex','egon','yuan','wusir','666']
    把666替换成999   
    获取"yuan"索引
    假设不知道前面有几个元素，分片得到最后的三个元素

3. 将字符串s = "www.luffycity.com"给拆分成列表：li=['www','luffycity','com'] 

4. 对字典进行增删改查
    d = {
        "Development":"开发小哥",
        "OP":"运维小哥",
        "Operate":"运营小仙女",
        "UI":"UI小仙女"
    }
    - 增加： name : alex
    - 修改： alex 改为 wusir
    - 删除： 删除 name 为 wusir
    - 两种方式查询： "UI":"UI小仙女"

5. 使用两种循环打印1-100
6. 循环打印1-100中的偶数
9. 计算1-100，偶数的和
12. 列举Python中布尔值为False的对象
13. 接收用户输入，一百分制成绩（0~100），要求输出其对应的成绩等级A~E。其中，90分以上为'A'，
    80~89分为'B'，70~79分为'C'，60~69分为'D'，60分以下为'E'
14. 请将各个数据类型按照有序和无序进行分类？ set list dict str tuple

16. 猜数游戏。预设一个0~9之间的整数，让用户猜一猜并输入所猜的数，如果大于预设的数，显示“太
    大”；小于预设的数，显示“太小”，如此循环，直至猜中该数，显示“恭喜！你猜中了！
17. 将上一题进行升级，给用户三次猜测机会，如果三次之内猜测对了，则显示猜测正确，退出循环，如果三次之内没有猜测正确，则自动退出循环，并显示‘太笨了你....’
18. 下列结果是什么？
     6 or 2 > 1
     3 or 2 > 1
     0 or 5 < 4
     2 > 1 or 6
19. 使用for循环对s="321"进行循环，打印的内容依次是："倒计时3秒"，"倒计时2秒"，"倒计时1秒"，"出发！"
20. 实现一个整数加法计算器(两个数相加)：
    - 如：content = input("请输入内容:") 用户输入：5+9或5+ 9或5 + 9，然后进行分割再进行计算。
    - 升级，实现多个数相加，如 3+2+3+5
"""

# ---------------------------------------------------------------------------------------


"""
1. 列举 str list dict set tuple 这几种数据类型的常用方法

str.strip

"""
# str.startswith
# str.endswith
# str.split
# str.replace
# str.strip
# str.index
# str.format
# str.find   #和index 方法一样 返回查找字符所在索引位置， 区别是找不到return -1
# str.isdigit

# list.append
# list.insert
# list.index
# list.extend  # 后面拼接一个数组
# list.pop
# list.remove
# list.count #统计参数在列表的次数

# dict.get
# dict.fromkeys
# dict.setdefault
# dict.clear
# dict.keys
# dict.values
# dict.items
# dict.pop
# dict.popitem
# dict.setdefault


# tuple.index
# tuple.count

# set.add
# set.remove
# set.pop
# set.discard
# set.remove
# set.union
# set.difference
# set.symmetric_difference


"""
2. 列表li = ['alex','egon','yuan','wusir','666']
    把666替换成999   
    获取"yuan"索引
    假设不知道前面有几个元素，分片得到最后的三个元素
"""
li = ['alex', 'egon', 'yuan', 'wusir', '666']

# li[-1] = 999
# print(li)


# print(li.index("yuan"))


# print(li[-3:])


"""
3. 将字符串s = "www.luffycity.com"给拆分成列表：li=['www','luffycity','com'] 
"""
# s = "www.luffycity.com"
# li = s.split(".")
# print(li)


"""
4. 对字典进行增删改查
    d = {
        "Development":"开发小哥",
        "OP":"运维小哥",
        "Operate":"运营小仙女",
        "UI":"UI小仙女"
    }
    - 增加： name : alex
    - 修改： alex 改为 wusir
    - 删除： 删除 name 为 wusir
    - 查询： "UI":"UI小仙女"
"""
# d = {
#     "Development": "开发小哥",
#     "OP": "运维小哥",
#     "Operate": "运营小仙女",
#     "UI": "UI小仙女"
# }

# d['name'] = 'alex'
# print(d)

# d['name'] = "wusir"
# print(d)


# d.pop("name")
# print(d)

# print(d['UI'])
# print(d.get("UI"))


"""
5. 使用两种循环打印1-100
"""
# for i in range(1, 101):
#     print(i)

# count = 1
# while count <= 100:
#     print(count)
#     count += 1


"""
6. 循环打印1-100中的偶数
"""
# for i in range(1, 101):
#     if i % 2 == 0:
#         print(i)

"""
7. 循环打印1-100中的奇数
"""

# for i in range(1, 101):
#     if i % 2 != 0:
#         print(i)

"""
8. 计算1-100的和
"""
# count = 0
# for i in range(1, 101):
#     count += i
# print(count)


"""
9. 计算1-100，偶数的和
"""
# count = 0
# for i in range(1, 101):
#     if i % 2 != 0:
#         count += i
# print(count)


"""
10. 计算-1+2-3+4-5...100的和
"""
# 法1
count = 0
for i in range(1, 101):
    if i % 2 == 0:
        count += i
    else:
        count -= i
print(count)


# 法2
# total = 0
# for i in range(1, 101):
#     total += (-1) ** i * i
# print(total)

"""
11. 制作趣味模板程序，(最少使用两种方式进行字符串格式化)
    需求：等待用户输入名字、地点、爱好，根据用户的名字和爱好进行任意现实
    如：敬爱可爱的xxx，最喜欢在xxx地方干xxx

"""
# name = input("请输入名字")
# a = input("爱好")
# b = input("地点")
# print("敬爱可亲的%s,最喜欢在%s地方干%s" % (name, b, a))
# print("敬爱可亲的{},最喜欢在{}地方干{}".format(name, b, a))

"""
12. 列举Python中布尔值为False的对象
"""
# 0 None ''  [] {}


"""
13. 接收用户输入，一百分制成绩（0~100），要求输出其对应的成绩等级A~E。其中，90分以上为'A'，
    80~89分为'B'，70~79分为'C'，60~69分为'D'，60分以下为'E'
"""
while True:
    score = input('输入成绩: ').strip()
    if score.upper() == "Q":
        break
    if score.isdigit():
        score = int(score)
        if 0 <= score <= 100:
            if 90 <= score <= 100:
                print('A')
            elif 80 <= score <= 89:
                print('B')
            elif 70 <= score <= 79:
                print('C')
            elif 60 <= score <= 69:
                print('D')
            else:
                print('E')

        else:
            print('输入的成绩不合法，合法范围的成绩是 1~100， 你输入的是 {}'.format(score))
    else:
        print('请输入整数类型')


"""

14. 请将各个数据类型按照有序和无序进行分类？ set list dict str tuple
"""
# 有序的数据类型： str list dict tuple
# 无序的数据类型：set
"""
15. 求100以内不能被3整除的所有数，并把这些数字放在一个新的列表中
"""
# tmp_list = []
# for i in range(1, 101):
#     if i % 3 != 0:
#         tmp_list.append(i)

# print(tmp_list)


"""
16. 猜数游戏。预设一个0~9之间的整数，让用户猜一猜并输入所猜的数，如果大于预设的数，显示“太
    大”；小于预设的数，显示“太小”，如此循环，直至猜中该数，显示 恭喜！你猜中了！并结束程序
"""
# e = 6  # 预期值
# while True:
#     num = input('输入一个0~9之间的整数: ').strip()
#     if num.upper() == "Q":
#         break
#     if num.isdigit():
#         num = int(num)
#         if 0 <= num <= 9:
#             if num > e:
#                 print('太大')
#             elif num < e:
#                 print('太小')
#             else:
#                 print('恭喜！你猜中了！')
#                 break
#         else:
#             print('输入范围不合法')
#     else:
#         print('输入不合法')




"""
17. 将上一题进行升级，给用户三次猜测机会，如果三次之内猜测对了，则显示猜测正确，退出循环，如果三次之内没有猜测正确，则自动退出循环，并显示‘太笨了你....’
"""

# e = 6  # 预期值
n = 0
while n < 3:
    num = input('输入一个0~9之间的整数: ').strip()
    if num.upper() == "Q":
        break
    if num.isdecimal():
        num = int(num)
        if 0 <= num <= 9:
            if num > e:
                print('太大')
            elif num < e:
                print('太小')
            else:
                print('恭喜！你猜中了！')
                break
        else:
            print('输入范围不合法')
    else:
        print('输入不合法')
    n += 1
    if n == 3:
        print('太笨了你.....')



"""
18. 下列结果是什么？
    - 6 or 2 > 1    --> 6
    - 3 or 2 > 1    --> 3
    - 0 or 5 < 4    --> False
    - 2 > 1 or 6    --> True
"""

"""
19. 使用for循环对s="321"进行循环，打印的内容依次是："倒计时3秒"，"倒计时2秒"，"倒计时1秒"，"出发！"
"""
# s = "321"
# for i in s:
#     print('倒计时{}秒'.format(i))
# print("出发！")



"""
20. 实现一个整数加法计算器(两个数相加)：
    - 如：content = input("请输入内容:") 用户输入：5+9或5+ 9或5 + 9，然后进行分割再进行计算。
    - 升级，实现多个数相加，如 3+2+3+5
"""
# while True:
#     count = 0
#     n1 = input('输入加法算式: ').strip()
#     if n1.upper() == 'Q':
#         break
#     tmp_list = n1.split('+')
#     for i in tmp_list:
#         count += int(i)
#     print("{} = {}".format(n1, count))
