# 第三模块考核，范围：面向对象、异常、网络编程


# -- 如何查看类和对象的名称空间
# class Foo(object):
#     def show_course(self):
#         print('show course')
#
# obj1 = Foo()
# print(dir(obj1))        #返回一个包含所有属性名和方法名的有序列表
# print(dir(Foo))         #返回一个包含所有属性名和方法名的有序列表
# print(obj1.__dict__)    #返回对象属性组成的字典
# print(Foo.__dict__)     #返回类属性组成的字典

# -- 什么是反射？反射相关的方法是什么？请用反射执行下面类中的 show_course 方法
'''
反射： 通过字符串调用对象成员
相关方法
    getattr
    setattr
    hasattr
    delattr
'''

# class Foo(object):
#     def show_course(self):
#         print('show course')
#         return '1'
# obj1 = Foo()
# obj1.show_course()
# getattr(obj1,"show_course")()


# -- 列举常用的内置方法
'''
__init__
__new__
__iter__
__next__
__enter__
__exit__
__add__
__call__
__getitem__
__dict__
__dir__
'''


# -- 编写一个学生类，并且实现一个计数器功能，统计这个类一共实例化了多少个实例对象
# class Student:
#     num = 0
#     def __init__(self,name):
#         self.name = name
#     def __new__(cls, *args, **kwargs):
#         cls.num += 1
#         return object.__new__(cls)
#
# s1 = Student('alex')
# s2 = Student('kaikai')
# print(Student.num)



"""
-- 基于tcp协议,实现一个注册登录功能
    - 文件构成
        D:\demo
            - server.py
            - client.py
            - userinfo.json   # 你也可以选择其他类型的文件
    - 需求：
        - 客户端运行程序后，有登录和注册、退出三个功能
        - 当用户选择注册，让用户输入用户名和密码，并对密码进行md5加密，然后将数据传给 sever 端，server校验用户名是否存在
            - 存在则返回用户已存在，让客户端重新注册
            - 如果不存在，则保存注册信息，并返回注册成功
        - 如果用户选择登录，将用户输入的信息发送到server端进行校验
            - 成功提示登录成功
            - 否则提示登录失败
            - 重复登录时，能自动登录
        - 如果用户选择退出，结束客户端程序并断开连接
        - 运行示例
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 1
            user: root
            pwd: 123
            register successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 1
            user: root
            pwd: 123
            register error, user exists！
            user: admin
            pwd: 123
            register successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 2
            user: root
            pwd: 123
            login successful
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 2
            自动登录成功.....
            1 注册
            2 登录
            3 退出
            根据序号选择操作: 3
            client exit.......
"""
