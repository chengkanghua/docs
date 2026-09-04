# 第一章 Python基础
1. 公司线上和开发环境使用的什么系统？

   ```
   Linux
   	centos
   	ubuntu
   ```

5. 简述解释型和编译型编程语言？

7. 位和字节的关系？

8. b、B、KB、MB、GB 的关系？

5. 请至少列举5个 PEP8 规范（越多越好）

   ```
   name = "alex"
   
   """
   休息休息
   """
   def func():
       pass
   ....
   ```

6. 求结果：or and

   ```python
   v1 = 1 or 3
   v2 = 1 and 3
   v3 = 0 and 2 and 1
   v4 = 0 and 2 or 1
   v5 = 0 and 2 or 1 or 4
   v6 = 0 or Flase and 1
   ```

11. ascii、unicode、utf-8、gbk 区别？

12. 字节码 和 机器码 的区别？

9. 三元运算编写格式。

   ```
   v = 99 if 1>2 else 666
   ```

10. 列举你了解的所有Python2和Python3的区别？

    ```
    - print写法不一样
    - 解释器编码
    - int（地板除）
    - 字典有序（py3.6+）
    - range
    	py2:range   xrange
    	py3:range
    - 经典类&新式类
    - 字符串的底层存储
    	py2: unicode     str
    	py3:   str      bytes
    - 字典
    	py2: info.keys() --> 立即把自己所有的key都获取到列表。
    	py3: info.keys() 迭代器
    ```

11. 用一行代码实现数值交换：

     ```python
     a = 1
     b = 2
    
    a, b=b, a
     ```

18. Python3和Python2中 int 和 long的区别？

19. xrange和range的区别？

20. 如何实现字符串的反转？如： name = "wupeiqi" 请反转为 name = "iqiepuw" 。

15. 文件操作时：xreadlines和readlines的区别？

    ```python
    f = open('xx')
    data = f.readlines()
    f.close()
    
    f = open('xx')
    for line in f.xreadlines():
        print(line)
    f.close()
    ```

    ```python
    f = open('xx')
    for line in f:
        print(line)
    f.close()
    ```

22. 列举布尔值为False的常见值？

23. 列举字符串、列表、元组、字典每个常用的5个方法？

24. is和==的区别?

25. 1、2、3、4、5 能组成多少个互不相同且无重复的三位数

26. 什么是反射？以及应用场景？

27. 简述Python的深浅拷贝？

28. Python垃圾回收机制？

29. Python的可变类型和不可变类型的区别？

30. 求结果

    ```python
    v = dict.fromkeys(['k1','k2'],[])
    v['k1'].append(666)
    print(v)
    v['k1'] = 777
    print(v)
    ```

31. 一行代码实现删除列表中重复的值 ?

32. 如何实现 “1,2,3” 变成 [‘1’,’2’,’3’] 

33. 如何实现[‘1’,’2’,’3’]变成[1,2,3] 

34. 比较： a = [1,2,3] 和 b = [(1),(2),(3) ] 以及 c = [(1,),(2,),(3,) ] 的区别？

35. 如何用一行代码生成[1,4,9,16,25,36,49,64,81,100] ?

36. 常用字符串格式化哪几种？

37. 什么是断言（assert）？应用场景？

38. 有两个字符串列表a和b，每个字符串是由逗号分隔的一些字符：

    ```python
    a= [ 'a,1',
        'b,3,22',
        'c,3,4',
    ]
    
    b = [
        'a,2',
        'b,1',
        'd,2',
    ]
    按每个字符串的第一个值，合并a和b到c
    
    c = [
        'a,1,2',
        'b,3,22,1',
        'c,3,4',
        'd,2'
    ]
    ```

39. 有一个多层嵌套的列表A=[1,2,[3,4,["434",...]]], 请写一段代码遍历A中的每一个元素并打印出来【跳过】

40. a = range(10),a[::-3] 的结果是 \____________

41. 下面那个命令可以从虚拟环境中退出

    ```
    A.  deactivate
    B.  exit
    C.  quit
    D.  以上均可
    ```

42. 将列表内的元素,根据位数合并成字典

    ```python
    lst = [1,2,4,8,16,32,64,128,256,512,1024,32769,65536,4294967296]
    
    # 输出
    {
        1:[1,2,3,8],
        2:[16,32,64],
        3:[128,256,512],
        4:[1024,],
        5:[32769,65536],
        6:[4294967296]
    }
    ```

37. 请尽量用简洁的方法将二维数组转换成一维数组

    ```
    例: 
    	转换前 lst=[ [1,2,3], [4,5,6], [7,8,9] ]
    
    	转换后 lst = [1,2,3,4,5,6,7,8,9]
    	
    
    import itertools
    lst = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    val = list(itertools.chain(*lst))
    print(val)
    ```

38. 以下代码输出是什么?list=['a','b','c','d','e']   list[10:]

    ```
    list=['a','b','c','d','e'] 
    print( list[10:] ) # 1
    print( list[10] )  # 2
    ```

    ```
    A.  []
    B.  程序异常
    C.  ['a','b','c','d','e']
    D.  输出空
    ```

48. Python语言什么那些类型的数据才能做为字典的key?

    ```
    A.  没有限制
    B.  字母数字下划线
    C.  字母
    D.  可被hash的类型
    ```

49. 以下两段代码的输出一样吗, 占用系统资源一样吗, 什么时候要用xrange代替range

    ```python
    for i  in range(1): print i
    
    for i in xrange(1): print i
    ```

41. 如下代码段

    ```
    a = [1,2,3,[4,5],6]
    b = a 
    c = copy.copy(a)
    d = copy.deepcopy(a)
    b.append(10)
    print(a,b,c,d)
    
    c[3].append(11)
    print(a,b,c,d) 
    d[3].append(12)
    print(a,b,c,d) 
    请问a,b,c,d的值为;
    ```

42. 现有字典d={"a":26,"g":20,"e":20,"c":24,"d":23,"f":21,"b":25} 请按照字段中的value字段进行排序。

    ```python
    sorted(d.items(),key=lambda x:x[1])
    ```

52. 给定两个listA,B,请用Python找出A,B中相同的元素,A,B中不同的元素

60. 描述下dict的items()方法与iteritems()的不同

62. 介绍一下try except的用法和作用?

63. 输入一个字符串, 返回倒序排列的结果 如: abcdef, 返回 fedcba

47. 阅读以下代码, 并写出程序的输出结果

    ```python
    alist = [2,4,5,6,7]
    for var in alist:
        if var % 2 ==0:
            alist.remove(var)
    
    print(alist) # [4, 5, 7]
    ```

48. 现有列表alist=[3,1,-4,-2],按期元素的绝对值大小进行排序?

    ```python
    sorted(d.items(),key=lambda x:abs(x))
    ```

49. 那些情况下,  y != x - (x-y)  会成立?

    ```
    x和y是集合
    ```

50. 用Python实现99乘法表(用两种不同的方法实现)

51. 获取list中的元素个数,和向末尾追加元素所用的方法分别是什么？

52. 判断dict中有没有某个key用的方法是什么？

53. 现有一列表alist, 请写出两种去除alist中重复元素的方法, 其中：

    - 要求保持原有列表中元素的排列顺序。
    - 无需考虑原有列表中元素的排列顺序。

54. 请描述Unicode,utf-8, gbk等编码之间的区别?

55. 填空

    ```python
    l=range(100)
    
    1. 如何取第一到第三个元素用的是
    2. 如何取倒数第二个元素
    3. 如何取后十个
    ```

56. 如何判断一个变量是否是字符串？

57. list和tuple有什么不同？

58. a = dict(zip(("a","b","c","d","e"),(1,2,3,4,5)))   请问a是什么？

59. 一行代码生成列表 [1,4,9,16,25,36,49,64,81,100]。

60. 以下叙述正确的是

    ```
    A.  continue语句的作用是结束整个循环的执行
    B.  只能在循环体和switch语句体内使用break语句
    C.  在循环体内使用break语句或者continue语句的作用相同
    D.  从多层循环嵌套中退出时, 只能使用goto语句
    ```

61. 读代码

    ```
    for i in range(5,0,-1):
        print(i)
    请在下面写出打印结果
    ```

62. 写结果

    ```
    x= "foo"
    y = 2
    print x+y
    -------
    A.  foo
    B.  foo foo
    C.  foo 2
    D.  2
    E.  An exception is thrown
    ```

63. 求结果

    ```
    kvps = {"1":1,"2":2}
    theCopy = kvps
    kvps["1"] = 5
    sum = kvps["1"] + theCopy ["1"]
    print sum
    
    A.  1
    B.  2
    C.  7
    D.  10
    ```

64. python里如何实现tuple和list的转化

65. type(1+2L*3.14)的结果是

    ```
    A.  int
    B.  long
    C.  float
    D.  str
    ```

66. 若k为整型, 下列while循环执行的次数为

    ```
    k = 1000
    while k>1:
        print k
        k = k/2
    ```

67. 以下何者是不合法的布尔表达式

    ```
    A.  x in range(6)
    B.  3 = a
    C.  e>5 and 4==f
    D.  (x-6)>5
    ```

68. python不支持的数据类型有

    ```
    A.  char
    B.  int
    C.  float
    D.  list
    ```

69. 如何在Python中拷贝一个对象, 并说明他们之间的区别？

70. 99(10进制)的八进制表示是什么？

71. 下列Python语句正确的是

    ```
    1.  min = x is x<y=y
    2.  max = x>y?x:y
    3.  if(x>y) print x
    4.  while True:pass
    ```

72. list对象 alist = [{'name':'a','age':20},{'name':'b','age':30},{'name':'v','age':25},]按alist中元素的age由大到小排序。

73. Python是如何进行内存管理的? Python的程序会内存泄漏吗?说说有没有什么方面阻止或检测内存泄漏

74. 详细说说tuple,list,dict的用法, 他们的特点

75. 一个大小为100G的文件etl_log.txt, 要读取文件中的内容, 写出具体过程代码？

76. 已知Alist=[1,2,3,1,2,1,3],如何根据Alist得到[1,2,3]

77. 已知stra = 'wqedsfsdrfweedqwedqw'

    ```
    1.  如何获取最后两个字符
    2.  如何获取第二个和第三个字符
    ```

78. 已知Alist = ["a","b","'c'],将Alist转化为'a,b,c'的实现过程

79. 已知ip='192.168.0.100' 代码实现提取各部分并写入列表。

80. python代码如何获取命令行参数？

81. 写代码

    ```
    tupleA = ("a","b","c","d","e")
    tupleB = (1,2,3,4,5)
    RES = {"a":1,"b":2,"c":3,"d":4,"e":5}
    
    写出由tupleA和tupleB得到res的及具体实现过程
    ```

82. 选出一下表达式表述正确的选项

    ```
    A.  {1:0,2:0,3:0}
    B.  {'1':0,'2':0,'3':0}
    C.  {(1,2):0,(4,3):0}
    D.  {[1,2]:0,[4,3]:0}
    E.  {{1,2}:0,{4,3}:0}
    ```

83. what gets printde() ?

    ```
    kvps = {"1":1,'2':2}
    theCopy = kvps.copy()
    kvps["1"] = 5
    sum = kvps["1"] + theCopy["1"]
    print sum
    
    A.  1
    B.  2
    C.  6
    D.  10
    E.  An execption is thrown
    ```

84. what gets printde() ?

    ```
    numbers = [1,2,3,4]
    numbers.append([5,6,7,8])
    print len(numbers)
    
    A.  4
    B.  5
    C.  8
    D.  12
    E.  An exception is thrown
    ```

85. what getsprintde() ?

    ```
    names1 = ["Amir","Barry","Chaies","Dao"]
    if "amir" in names1:
       print 1
    else:
       print 2
    
    A.  1
    B.  2
    C.  An exception is thrown
    ```

86. what getsprintde() ? Assuming ptrhon version2.x()

    ```
    print(type(1/2))
    
    A.  int
    B.  float
    C.  0
    D.  1
    E.  0.5
    ```

87. 以下用来管理Python库管理工具的是

    ```
    A.  APT
    B.  PIP
    C.  YUM
    D.  MAVEN
    ```

88. which numbers are printed ()?

    ```
    for i in range(2):
        print i
    
    for i in range(4,6):
        print i
    
    A.  2,4,6
    B.  0,1,2,4,5,6
    C.  0,1,4,5
    D.  0,1,4,5,6,7,8,9
    E.  1,2,4,5,6
    ```

89. 求结果

    ```
    import math
    print (math.floor(5.5))
    
    A.  5
    B.  5.0
    C.  5.5
    D.  6
    E.  6.0
    ```

90. 关于Python的内存管理, 下列说法错误的是

    ```
    A.  变量不必事先声明
    B.  变量无需先创建和赋值而直接使用
    C.  变量无需指定类型
    D.  可以使用del释放资源
    ```

91. 下面那个不是Python合法的标识符

    ```
    A.  int32
    B.  40xl
    C.  self
    D.  name
    ```

92. 下列哪种说法是错误的

    ```
    A.  除字典类型外, 所有标准对象均可用于布尔测试
    B.  空字符串的布尔值是False
    C.  空列表对象的布尔值是False
    D.  值为0的任何数字对象的布尔值是False
    ```

93. 下列表达是的值为True的是

    ```
    A.  5+4j >2-3j
    B.  3>2>2
    C.  (3,2)<("a","b")
    D.  " abc" > 'xyz'
    ```

94. 关于Python的复数, 下列说法错误的是

    ```
    A.  表示复数的语法是 real+imagej
    B.  实部和虚部都是浮点数
    C.  虚部后缀必须是j, 且必须小写
    D.  方法conjugate返回复数的共轭复数
    ```

95. 关于字符串下列说法错误的是

    ```
    A.  字符应视为长度为1的字符串
    B.  字符串以\0标志字符串的结束
    C.  既可以用单引号, 也可以用双引号创建字符串
    D.  在三引号字符串中可以包含换行回车等特殊字符
    ```

96. 以下不能创建一个字典的语句是

    ```
    A.  dic1 = {}
    B.  dic2 = {3:5}
    C.  dic3 = {[1,2,3]:"usetc"}
    D.  dic4 = {(1,2,3):"usetc"}
    ```

97. python里面如何拷贝一个对象?(赋值,浅拷贝,深拷贝的区别)

98. 描述在python中的元祖,列表,字典的区别,并且分别写一段定义,添加,删除操作的代码片段。

99. 选择结果

    ```
    names1 = ["Amir","Barry","Chales","Dao"]
    names2 = names1
    names3 = names1[:]
    name2[0] = "Alice"
    names3[1] =  "Bob"
    sum = 0
    for ls in (names1,names2,names3):
        if ls[0] == "Alice":
            sum+=1
        if ls[1]=="Bob":
            sum+=10
    
    print sum
    
    
    A.  11
    B.  12
    C.  21
    D.  22
    E.  23
    ```

100. 下面程序的输出结果是

     ```
     x = True
     y = False
     z = False
     
     if x or y and z:
         print 'yes'
     else:
         print 'no'
     ```

101. 1 or 2 和1 and 2输出分别是什么? 为什么

102. 1 <(2==2)和1 <2==2的结果分别是什么, 为什么

103. 如何打乱一个排好序的list对象alist

104. 如何查找一个字符串中特定的字符?find和index的差异？

105. 把aaabbcccd这种形式的字符串压缩成a3b2c3d1这种形式。

106. Python 一个数如果恰好等于它的因子之和，这个数就称为"完数"。例如6=1＋2＋3.编程找出1000以内的所有完数。 

107. 输入一个字符串, 输出该字符串中字符的所有组合. 

     ```
     例如: 输入字符串"1,2,3", 则输出为1,2,3,12,13,23,123(组合数, 不考虑顺序, 所以12和21是等价的)
     ```

108. 执行以下代码后, i和n的值为

     ```
     int i=10;
     int n=i++%5
     
     
     A.  10, 0
     B.  10, 1
     C.  11, 0
     B.  11, 1
     ```

109. 执行以下代码段后,x的值为

     ```
     int x=10;
     x+=x-=x-x;
     
     
     A.  10
     B.  20
     C.  30
     D.  40
     ```

110. 对于一个非空字符串,判断其是否可以有一个子字符串重复多次组成,字符串只包含小写字母且长度不超过10000

     ```
     示例1:
     
     1.  输入"abab"
     2.  输出True
     3.  样例解释: 输入可由"ab"重复两次组成
     
     示例2:
     
     1.  输入"abcabcabc"
     2.  输出True
     3.  样例解释: 输入可由"abc"重复三次组成
     
     示例3:
     
     1.  输入"aba"
     2.  输出False
     ```



