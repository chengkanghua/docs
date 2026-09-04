
# 1. 在多行注释中(既不能使用pycharm的智能提示)，列举 str list dict set tuple 这几种数据类型的常用方法
# str.strip
# str.split
# str.upper
# str.lower
# str.isdecimal
# str.disgit
# ''.format
# '{}'%{}


# l = [1, 2]
# l.remove(1)
# print(l)

# list.update
# list[][].remove
# del list[]
# list[][] = xx
# list.index
#
# dict.remove
# dict[][] = xx

# set().add
# set().remove
# del set()

# del tuple[]
#
# """


# 2. 列表li = ['alex','egon','yuan','wusir','666']
#     把666替换成999
#     获取"yuan"索引
#     假设不知道前面有几个元素，分片得到最后的三个元素

# li = ['alex', 'egon', 'yuan', 'wusir', '666']
# li[4] = '999'
# re = li.index('yuan')
# print(li[-3:])
# print(re)

# 3. 将字符串s = "www.luffycity.com"给拆分成列表：li=['www','luffycity','com']
# s = "www.luffycity.com"
# list2 = s.split('.')
# # print(list2)

# 4. 对字典进行增删改查
# d = {
#     "Development": "开发小哥",
#     "OP": "运维小哥",
#     "Operate": "运营小仙女",
#     "UI": "UI小仙女"
# }
#     - 增加： name : alex
#     - 修改： alex 改为 wusir
#     - 删除： 删除 name 为 wusir
#     - 两种方式查询： "UI":"UI小仙女"
# d.update({'name':'alex'})
# d['name'] = 'alex'
# d.update({'name': 'wusir'})
# dict2 = d.get('UI')
# dict3 = d['UI']
# print(dict3)
# print(dict2)
# print(d)

# 5. 使用两种循环打印1-100
# for i in range(1,101):
#     print(i)

# i = 1
# while i < 101:
#     print(i)
#     i +=1

# 6. 循环打印1-100中的偶数
# for i in range(2, 101):
#     if i % 2 == 0:
#         print(i, end=' ')
# for i in range(2, 101, 2):
#     print(i)


# 9. 计算1-100，偶数的和
# count = 0
# for i in range(2,101):
#     if i % 2 == 0:
#         count += i
# print(count)
# 12. 列举Python中布尔值为False的对象
# False
# 0
# []
# ()
# set()
# dict()
# 1>2
# ''
# not 2

# 13. 接收用户输入，一百分制成绩（0~100），要求输出其对应的成绩等级A~E。其中，90分以上为'A'，
#     80~89分为'B'，70~79分为'C'，60~69分为'D'，60分以下为'E'

# while True:
#     sum = input('请输入对应分数进行评等级 Q/q退出： ')
#     if sum.upper() == 'Q':
#         break
#     if not sum.isdecimal():
#         print('error 只能输入数字：')
#         continue
#     sum = int(sum)
#     if sum >100 or sum < 0:
#         print('只能输入0~100 的分数')
#         continue
#     if sum > 90:
#         print('A')
#     elif sum >79 and sum < 90:
#         print('B')
#     elif sum > 69 and sum < 80:
#         print('C')
#     elif sum >59 and sum < 70:
#         print('D')
#     else:
#         print("E")
#
#


# 14. 请将各个数据类型按照有序和无序进行分类？ set list dict str tuple
# 有序 list dict（python3.6之后） str tuple
# 无序 set

# 16. 猜数游戏。预设一个0~9之间的整数，让用户猜一猜并输入所猜的数，如果大于预设的数，显示“太
#     大”；小于预设的数，显示“太小”，如此循环，直至猜中该数，显示“恭喜！你猜中了！
# number = 6
# while True:
#    inp = input('guess number: ')
#    inp = int(inp)
#    if inp >number:
#        print('大了')
#    elif inp < number:
#        print('小了')
#    else:
#        print('恭喜 猜中了')
#        break


# 17. 将上一题进行升级，给用户三次猜测机会，如果三次之内猜测对了，则显示猜测正确，退出循环，如果三次之内没有猜测正确，则自动退出循环，并显示‘太笨了你....’

# number = 6
# i = 1
# while i < 4:
#     inp = input('guess number: ')
#     inp = int(inp)
#     if inp >number:
#        print(f'第{i}次 提示：大了')
#        # i += 1
#     elif inp < number:
#        print(f'第{i}次 提示：小了')
#        # i +=1
#     else:
#        print('恭喜 猜中了')
#        break
#     i += 1
# else:
#     print('太笨了你。。。。')

# 18. 下列结果是什么？
#      6 or 2 > 1  #6
#      3 or 2 > 1  #3
#      0 or 5 < 4  #True
#      2 > 1 or 6  #True

# 19. 使用for循环对s="321"进行循环，打印的内容依次是："倒计时3秒"，"倒计时2秒"，"倒计时1秒"，"出发！"
# s="321"
# for i in s:
#     print(f'倒计时{i}秒，')
# print("出发！")

# 20. 实现一个整数加法计算器(两个数相加)：
#     - 如：content = input("请输入内容:") 用户输入：5+9或5+ 9或5 + 9，然后进行分割再进行计算。
#     - 升级，实现多个数相加，如 3+2+3+5
#
# content = input("请输入内容:")
# li2 = content.strip().split('+')
# print(li2)
# count = 0
# for i in li2:
#     i = int(i)
#     count += i
# print(count)
#
# li2 = ['3', '4', '1']
# print(sum([int(i) for i in li2]))

# def func(x):
#     return int(x)
# print(sum(map(func, li2)))
# print(sum(map(int, li2)))



#导师点评
'''
多print
整体来说，掌握的还不错，就是你要把基础再复习复习
把练习题多做做
列表解析式的应用
li2 = ['3', '4', '1']
print(sum([int(i) for i in li2]))
def func(x):
    return int(x)

print(sum(map(func, li2)))
print(sum(map(int, li2)))
列表的更新是用的
list.extend
列表和字典还需要复习
tuple.index
tuple.count
'''