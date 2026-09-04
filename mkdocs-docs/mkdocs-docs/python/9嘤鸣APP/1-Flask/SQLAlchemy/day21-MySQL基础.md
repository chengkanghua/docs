



## 前言

假设现在你已经是某大型互联网公司的高级程序员，让你写一个火车票购票系统，来hold住十一期间全国的购票需求，你怎么写？

在同一时段抢票的人数如果太多，那么你的程序不可能运行在一台机器上，应该是多台机器一起分担用户的购票请求。

![image-20220527045229569](assets/image-20220527045229569-1654057010759.png)

那么问题就来了，票务信息的数据存在哪里？存在文件里么？

如果存储在文件里，那么存储在哪一台机器上呢？是每台机器上都存储一份么？

首先，如果其中一台机器上卖出的票另外两台机器是感知不到的，其次，如果我们将数据和程序放在同一个机器上，如果程序和数据有一个出了问题都会导致整个服务不可用。最后，操作或修改文件中的内容对python代码来说是一件很麻烦的事。

基于上面这些问题，单纯的将数据存储在和程序同一台机器上的文件中是非常不明智的。

## 数据库

根据上面的例子，我们可以知道，将文件和程序存在一台机器上是很不合理的，同时，操作文件是一件很麻烦的事，所以我们可以使用数据库来存储数据。

### 基本概念

#### 数据

所谓的数据（Data），就是描述主观或客观存在的人、事、物特征的符号记录（Record），描述事物的符号既可以是数字，也可以是文字、图片，图像、声音、语言等，数据由多种表现形式，它们都可以经过数字化后存入计算机。如：

```python
name = "moluo"
age = 18
gender = True
```

#### 记录

所谓的记录（Record），就是指代描述事物的一系列特征而组成的相关信息集合，在计算机中描述一个事物的记录，就相当于文件里的一行内容。

```bash
moluo, True, 18, 2000, 广东, 计算机科学与技术, python开发
```

当然单纯的一行记录如果没有任何的组织结构或没有任何的说明，实际上是没有任何意义，如果我们按逗号作为分隔，依次定义各个信息代表的具体意义，相当于定义一张表格一样，如：

| name  | sex  | age  | birthday | province | major            | job        |
| :---- | :--- | :--- | :------- | :------- | :--------------- | :--------- |
| moluo | True | 18   | 2000     | 广东     | 计算机科学与技术 | python开发 |

这样我们就可以了解moluo，性别为男，年龄18岁，出生于2000年，来自于广东，计算机专业等相关信息。

#### 数据表

数据表（Data Table，或者Table）就如同上面的表格一样，在第二行以后还可以继续写入其他人的相关信息记录。最终保存为一个文件的形式。我们可以通俗的理解这个文件就是一个数据表。 

| name     | sex   | age  | birthday | province | major            | job        |
| :------- | :---- | :--- | :------- | :------- | :--------------- | :--------- |
| moluo    | True  | 18   | 2000     | 广东     | 计算机科学与技术 | python开发 |
| xiaohong | False | 17   | 2000     | 广西     | 舞蹈学           | 音乐老师   |

当然，开发中我们有时候一个程序或项目，要保存的数据会非常多，相关的数据会保存成一个数据表，那么当数据表文件特别多时，我们又要怎么管理呢？ 是不是得建一个文件夹保存这些文件啊？

#### 数据库

数据库（Database） 就是一种按照特定数据结构来组织、存储和管理数据的仓库。通俗地理解，数据库就是一个存储数据表的特殊文件夹，只不过这个仓库可以将数据按照特定的数据结构进行高效压缩存储在磁盘上，同时为了方便用户组织和管理数据，数据库还会专门配套了数据库管理系统（Database Management System 简称DBMS）。用户通过操作数据库管理系统提供的功能，就可以有效的组织和管理存储在数据库中的数据。

![image-20220527045656721](assets/image-20220527045656721-1654057010760.png)

##### 数据库管理系统

在了解了Data与Database的概念后，如何科学地组织和存储数据，如何高效获取和维护数据成了关键，这就需要用到了一个系统软件---数据库管理系统。

所谓的数据库管理系统（DataBase Management System，简称DBMS），就是操纵和管理数据库的软件，基于这个软件，用户可以对数据库进行科学地组织和存储数据，它对数据库进行统一的管理和控制，可以保证数据库的数据的安全性和完整性。



##### 数据库服务器

数据库管理系统本质上就是一套基于socket通信实现的Client/Server架构的软件，所以我们肯定需要一台计算机来安装并运行起来，而安装了数据库管理系统的服务端程序的计算机，我们一般就称之为数据库服务器。用户通过安装数据库管理系统客户端的计算机，我们就称之为数据库客户端。

一般而言，数据库服务器，我们都会选择安装在linux、unix或window server等系统服务器上，而数据库客户端则可以是如下三种：

+ 界面化管理工具，如Navicat，pycharm，Induction
+ 代码程序，java、python、php等编程语言基于socket通讯实现的，往往作为一个工具类或者模块被程序直接调用。
+ 终端命令行工具，cmd/bash

![img](assets/e7cd7b899e510fb344c87acec9899b9cd3430cdc-1654057010760.png)

##### 数据库类型

数据库类型，也就是数据库管理系统的类型，一般基于不同的操作方式或不同的底层实现，会分2大类：

- 关系型数据库（RMDBS）：是建立在关系模型基础上的数据库，即数据库中表与表的数据之间存在某种关联的内在关系，因为这种内在关系，所以我们称这种数据库为关系型数据库。

  常见的关系型数据库管理系统：

  ​     中小型数据库：**Mysql/MariaDB**、postgreSQL。（一张表可以保存千万级，勉强亿级）

  ​     重量级数据库：Oracle、SQLServer、DB2（一张表保存亿级，轻轻松松）

  ​     微型数据库：    Access、SQLlite3（一张表保存几十万的数据就已经超常发挥了）

  ![image-20220527113414332](assets/image-20220527113414332-1654057010760.png)

  

- 非关系型数据库（NO SQL，Not Only SQL）：

  泛指除了关系型数据库以外的所有数据库。

  例如：**Redis**、**MongoDB**、hbase、 Hadoop、**elasticsearch**、图数据库。

因为关系型数据库全部是通过SQL（结构化查询语言）来完成数据管理操作的，所以我们会经常把这一类的数据库称之为SQL数据库，而同样的，非关系型数据库并不使用SQL来完成数据库的操作，所以非关系型数据这一类型，叫NO SQL数据库。



#### SQL

SQL（Structured Query Language，结构化查询语言），是1974年IBM（蓝色巨人）的开发人员Boyce和Chamberlin提出的一套专为关系型数据库而建立的操作命令集，是一种用于对数据库进行数据操作的特殊编程语言。因为它功能齐全，效率高，简单易学易维护，所以被所有的关系型数据库系统所使用的。SQL与Python这种编程语言不一样，SQL依赖于数据库管理系统而存在，也就是说一般情况下，只有数据库管理系统才能识别SQL代码，并根据SQL代码完成对数据库的操作。

```sql
SELECT name,sex,age FROM `student`;
```

上面的代码就是SQL语句的查询语句，其中大写的单词，就是SQL语句的操作关键代码，也可以叫语句或命令或关键字。它本质上就是一个底层封装了如何操作数据的数学公式的函数名，而跟着在后面的内容，则是函数的参数。



## MySQL

MySQL是一个开源免费的关系型数据库管理系统，由瑞典MySQL AB 公司开发，目前属于 Oracle 旗下公司。MySQL 最流行的关系型数据库管理系统，在 WEB 应用方面MySQL是最好的 RDBMS (Relational Database Management System，关系数据库管理系统) 应用软件之一，具有成本低、速度快、体积小且开放源代码等优点。

![image-20220527060859153](assets/image-20220527060859153-1654057010760.png)

上图来源：https://db-engines.com/en/ranking



### 基本安装

此处我们演示的是windows下安装mysql。linux的安装过程在ubuntu封装笔记里面有。

#### 下载

打开网址，https://www.mysql.com，点击导航[DOWNLOADS](https://www.mysql.com/downloads/)

![image-20220527062226584](assets/image-20220527062226584-1654057010760.png)

mysql分2个主版本：Enterprise（企业版，收费闭源）和 Community（社区版，免费开源）。此处我们使用免费的社区版。

点击[MySQL Community (GPL) Downloads »](https://dev.mysql.com/downloads/)。

![image-20220527062138796](assets/image-20220527062138796-1654057010760.png)

点击 [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)

![image-20220527062437462](assets/image-20220527062437462-1654057010761.png)

windows选择zip压缩包格式，mac OS选择dmg格式。

![image-20220527062602586](assets/image-20220527062602586-1654057010761.png)

不需要注册登陆网站，直接谢谢，继续下载即可。

![image-20220527123500178](assets/image-20220527123500178-1654057010761.png)



#### 解压

把下载到本地的zip文件手动解压，将解压之后的文件夹放到专门保存开发软件的目录下，这个目录就是mysql的安装目录。

例如，此处我放在了C:/tool/目录下。

注意，目录路径不能出现中文，不能出现空格等特殊符号，否则会出错的！！！

![image-20220527123652517](assets/image-20220527123652517-1654057010761.png)

#### 配置

什么是配置？主要是为了让软件能适应当前安装的环境（网络环境、使用环境、操作系统等）而进行变量配置或者参数的修改。

##### 配置环境变量

【此电脑】- 【右键】-【属性】-【高级系统设置】-【环境变量】- 【找到系统变量中的path】-【选中】-【编辑】- 【新建】-【将刚刚mysql压缩包点进去bin目录路径复制并粘贴进来】-【确定】

![image-20220527063226145](assets/image-20220527063226145-1654057010761.png)

![image-20220527063446999](assets/image-20220527063446999-1654057010761.png)

##### 创建data目录

主要用于存放mysql数据库以及数据的。

> 注意：是mysql的安装目录！！！！

![image-20220527063639349](assets/image-20220527063639349-1654057010761.png)

##### 创建配置文件

mysql在windows下的配置文件，叫 mysql.ini，默认是没有的，我们需要手动创建。

![image-20220527063910153](assets/image-20220527063910153-1654057010762.png)

mysql.ini的配置内容，注意，basedir和datadir的路径要根据自己的路径如实填写，如下：

```ini
[mysqld]
; 设置3306端口，如果当前电脑安装了多个mysql时，需要错开端口。
port=3306
; 设置mysql的安装目录
basedir="C:/tool/mysql-8.0.28-winx64"
; 设置mysql数据库的数据的存放目录，就是前面手动创建的data目录
datadir="C:/tool/mysql-8.0.28-winx64/data"
; 允许最大连接数
max_connections=200
; 允许连接失败的次数。
max_connect_errors=10
; 服务端使用的字符集默认为utf8mb4
character-set-server=utf8mb4
; 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
; 默认使用“mysql_native_password”插件认证, mysql_native_password
default_authentication_plugin=mysql_native_password
[mysql]
; 设置mysql网络通信的默认字符集
default-character-set=utf8mb4
[client]
; 设置mysql客户端连接服务端时默认使用的端口
port=3306
; 设置mysql客户端的默认字符集
default-character-set=utf8mb4
```

##### 初始化数据库

重新打开一个cmd黑窗口，输入以下命令，让数据库完成初始化操作。

```bash
mysqld --initialize --console
```

![image-20220527064324111](assets/image-20220527064324111-1654057010762.png)

##### 注册系统服务

把mysql注册到操作系统作为系统服务，保证将来电脑重启了就可以开机自启了。

![image-20220530090559079](assets/image-20220530090559079-1654057010762.png)

在上面打开的黑窗口中如下以下命令：

```bash
mysqld --install mysql80

# 注销服务，用于卸载mysql的，别乱用。
# mysqld --remove mysql80
```

mysql80就是自己取的服务名（服务器是唯一的），只要符合python的变量规则，不要使用中文，可以自己发挥。

确认是否安装到了系统服务，可以通过【此电脑】- 【右键】-【管理】- 【服务与应用程序】 - 【服务】- 【右边窗口】

![image-20220527125007164](assets/image-20220527125007164-1654057010762.png)



#### 启动

windows下安装的mysql默认是没有启动服务的。

```bash
net start mysql80

# 关闭mysql的命令:
# net stop mysql80
# 重启mysql的命令：
# net start mysql80
```

![image-20220527064950514](assets/image-20220527064950514-1654057010762.png)

#### 登录

通过以下命令按回车键，接着输入上面初始化的登陆密码，就可以登陆MySQL交互终端了。

```bash
mysql -uroot -p


# 退出终端
# exit
```

![image-20220527065115515](assets/image-20220527065115515-1654057010762.png)

注意：mysql与linux一样，在安装成功以后默认就存在了一个上帝一般的用户，叫root。

##### 修改root登陆密码

接下来的操作是在登陆了mysql终端以后的操作。

```bash
alter user 'root'@'localhost' identified by '123';
# 'root' 就是要修改密码的用户名
# 'localhost' 表示允许用户在什么地址下可以使用密码登陆到数据库服务器，localhost表示本地登陆
# '123'  就是新的密码了，注意，不要设置空密码！以后公司里面的密码一定要非常难记的才最好。
```

![image-20220527065438994](assets/image-20220527065438994-1654057010762.png)

完成了上面的操作以后，mysql就安装完成了。



### 基本概念

前面的学习中我们提到，mysql是关系型数据库，所以我们要操作mysql就需要使用SQL（结构化查询语言）。

#### sql规范

```tex
1. 在数据库管理系统中，SQL语句关键字不区分大小写(但官方建议用大写) ，参数区分大小写。数据库名、数据表名、字段名统一小写，如数据库名、数据表名、字段名与SQL关键字同名，使用反引号` ` 圈起来，避免冲突。

2. SQL语句可单行或多行书写，默认以英文分号（;）结尾，关键词不能跨多行或简写。主要关键字的前后必须使用英文空格！！

3. 字符串跟日期类型的值都要以（单|双）引号括起来，单词之间需要使用半角的空格隔开。

4. 用空格和缩进来提高SQL语句的可读性。

```

```sql
select * FROM `table_name`
    WHERE name = "moluo";
```



##### 注释

SQL语句中支持2种不同的注释，注释的作用是写给开发人员的，数据库管理系统是不识别的。

```sql
第一种：单行注释以2个英文横杠开头
-- 单行注释

第二种：以/* 开头，以*/ 结尾 
/*
   多行注释
*/

第三种：与python的单行注释一模一样。 
# mysql单独支持单行注释
```



#### SQL类型

因为SQL语句的底层本质就是对操作数据的数学公式进行封装而得到的函数关键字，那么根据不同底层不同函数的用途，SQL语句通常分3大类型：

1. **数据定义语言**（Data Definition Language，DDL）

   用于创建或删除数据库、数据表、字段的SQL语句，包含以下几种指令：

   | SQL关键字 | 描述                       |
   | --------- | -------------------------- |
   | create    | 创建数据库和数据表等       |
   | drop      | 删除数据库和数据表等       |
   | alter     | 修改数据库和表等对象的结构 |

2. **数据操作语言**（Data Manipulation Language，DML）

   用于对数据表中的数据进行增删查改的。

   | SQL关键字 | 描述             |
   | --------- | ---------------- |
   | SELECT    | 查询表中的数据   |
   | INSERT    | 向表中插入新数据 |
   | UPDATE    | 变更表中的数据   |
   | DELETE    | 删除表中的数据   |

3. **数据控制语言**（Data Control Language，DCL）

   用于对控制数据库的操作权限的，包括用户权限以及数据操作权限。

   | SQL关键字 | 描述                           |      |
   | --------- | ------------------------------ | ---- |
   | COMMIT    | 确认对数据库中的数据进行的变更 |      |
   | ROLLBACK  | 取消对数据库中的数据进行的变更 |      |
   | GRANT     | 赋予用户操作权限               |      |
   | REMOVE    | 取消用户的操作权限             |      |

扩展：有些人也会把SQL语句主要分为6种：

```bash
DDL：数据定义语言，进行数据库、表的管理等，如create、drop

DQL：数据查询语言，用于对数据进行查询，如select
DML：数据操作语言，对数据进行增加、修改、删除，如insert、udpate、delete

TPL：事务处理语言，对事务进行处理，包括begin transaction、commit、rollback
DCL：数据控制语言，进行授权与权限回收，如grant、revoke
CCL：指针控制语言，通过控制指针完成表的操作，如declare cursor
```



#### 常用命令

mysql的学习官方文档：http://dev.mysql.com/

mysql8.0的中文翻译文档：http://www.deituicms.com/mysql8cn/cn/web.html

mysql 5.1的中文翻译文档：https://www.mysqlzh.com/

| 命令   | 描述                                                     |
| ------ | -------------------------------------------------------- |
| help   | 查看系统帮助                                             |
| status | 查看数据库管理系统的状态信息                             |
| exit   | 退出数据库终端连接，也可以使用quit                       |
| \c     | 当打错命令了，想换行重新写时可以在错误命令后面跟着\c回车 |

status命令查看mysql运行状态

```bash
mysql> status
--------------
mysql  Ver 8.0.28 for Win64 on x86_64 (MySQL Community Server - GPL)

Connection id:          15             # mysql是一个单进程多线程的软件，连接ID 是 20
Current database:                      #当前操作或使用的数据库名，空表示刚登陆mysql终端 
Current user:           root@localhost           # 当前用户账户信息，格式： 用户名@用户登录地址
SSL:                    Cipher in use is TLS_AES_256_GCM_SHA384      # SSL: 是否开启安全加密的端口连接MySQL，No就是没有加密
Using delimiter:        ;                                 # 当前MySQL的断句符号[定界符]，就是要求我们写完一条SQL语句以后，必须以这个符号结尾。
Server version:         8.0.28 MySQL Community Server - GPL    #  mysql属于基于socket通信实现的C/S架构的系统软件，当前数据库版本
Protocol version:       10                              # 端口号版本
Connection:             localhost via TCP/IP    # socekt连接
Server characterset:    utf8mb4                   # 数据库管理系统的字符集
Db     characterset:    utf8mb4                    # 数据库的字符集
Client characterset:    gbk                           # 客户端的字符集，windows下使用cmd连接默认会以gbk编码方式
Conn.  characterset:    gbk                          # socket通信连接的字符集
TCP port:               3306                              # 当前数据库使用的端口号（mysql的默认端口就是3306）
Binary data as:         Hexadecimal               # 二进制数据查询显示的转换进制（Hexadecimal表示十六进制显示二进制呢绒）
Uptime:                 2 days 15 hours 40 min 26 sec    # 当前系统已经启动的时间

Threads: 2  Questions: 14  Slow queries: 0  Opens: 130  Flush tables: 3  Open tables: 46  Queries per second avg: 0.000
# Threads: 2 表示当前mysql进程中一共维护了多少个线程
# Questions: 14 mysql数据库启动以来， 一共执行了多少条SQL语句
# Slow queries: 0  在mysql执行所有的SQL语句中是否有慢查询SQL的出现，所谓的满查询SQL指代的就是执行时间耗时很长的性能很低的SQL语句。
# Opens: 130  mysql被打开链接了多少次
# Flush tables: 3  表示mysql启动以来，里面的所有数据表一共被修改的次数多少次
#  Open tables: 46   表示mysql启动以来，里面的所有数据表一共被打开查询了多少次
# Queries per second avg: 0.000   平均每秒mysql完成多少次SQL执行，是一个负载参数，是一个很重要的性能指标，接近于0是性能最好的时候，数值越大，性能越差。
--------------
```



## 基本操作

MySQL中针对数据的操作划分为3个等级：数据库>数据表>数据记录，而在postgreSQL等数据库中，则划分为数据库>模式>数据表>数据记录。

### 数据库操作

#### 创建数据库

在磁盘上创建一个存储数据表的文件夹。开发中，一个软件项目往往就使用一个或多个数据库来保存数据。

```sql
create database [if not exists] 数据库名 [character set 编码字符集];
```

注意：mysql中的编码字符集中utf-8，要换成utf8mb4。SQL语句中的中括号部分表示可选。

终端操作，创建一个名为base数据库。

```sql
create database base;
```

执行效果：

```sql
mysql> create database base;
Query OK, 1 row affected (0.01 sec) 
-- 在mysql中，每一次执行SQL语句，不管这条SQL语句用于干什么的，对于ymsql而言，都是一次查询（query）
-- Query OK, 表示语句执行过程中，没有任何语法错误，但是并不保证执行结果就是我们所要的。
-- 1 row affected 有一个数据发生了变化、
--  (0.01 sec) 表示mysql执行本次的SQL语句一共耗费了多长时间，单位：秒（sec，second）
```

SQL语句的执行错误效果：

```sql
mysql> create databases base;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'databases base' at line 1
-- 上面就是SQL语句的语法错误提示，主要关注的就是 the right syntax to use near 后面单引号部分的内容，里面就是mysql识别到的错误代码部分。
```

注意：数据库相当于存储数据的一个特殊目录，所以数据名必须是唯一的。不能重复，否则报错！！！

![image-20220530102657093](assets/image-20220530102657093-1654057010762.png)

重复数据库名会报错如下：

```sql
mysql> create database base;
ERROR 1007 (HY000): Can not create database 'base'; database exists

-- database exists表示数据库已经存在了。
```

因此，在不确定数据库是否存在的情况下，可以采用if not exists来判断，如果没有创建。

```sql
mysql> create database if not exists base;
Query OK, 1 row affected, 1 warning (0.00 sec)

-- Query OK， 就是SQL语句成功执行了，
-- 1 row affected，有一行数据被影响了。明明数据库没有被添加，为什么还有会1行数据记录产生？原因是mysql会在SQL语句执行过程中，记录运行日志的。所以这里是多了一行错误日志。
-- 1 warning，SQL执行过程中，mysql发现了一个运行级别的错误
```



#### 查看数据库

```sql
-- 查看所有数据库
show databases;

-- 查看名字中包含base的数据库
show databases like '%base%';

-- 查看指定数据库的建库sql语句
show create database 数据库名;
```

终端操作：

```sql
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| base               |
| information_schema |
| mysql              |
| performance_schema |
| school             |
| sys                |
+--------------------+
6 rows in set (0.00 sec)
```



#### 修改数据库

针对数据库的修改操作，mysql提供了修改字符集的操作，该操作一般不使用。所以仅作了解即可。

```bash
alter database 数据库名 [character set 编码字符集];
```

终端操作

```sql
mysql> alter database base character set utf8;   -- 设置数据库的编码为utf8，mysql中编码utf-8必须改成utf8
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> show create database base;   -- 显示base数据库的建库语句
+----------+--------------------------------------------------------------------------------------------------+
| Database | Create Database
                    |
+----------+--------------------------------------------------------------------------------------------------+
| base     | CREATE DATABASE `base` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */ |
+----------+--------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> alter database base character set utf8mb4;  -- 设置数据库编码为utf8mb4
Query OK, 1 row affected (0.00 sec)

mysql> show create database base;   -- 显示base数据库的建库语句
+----------+--------------------------------------------------------------------------------------------------------------------------------+
| Database | Create Database
                                                  |
+----------+--------------------------------------------------------------------------------------------------------------------------------+
| base     | CREATE DATABASE `base` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */ |
+----------+--------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```



#### 删除数据库

删除数据库，会把库中所有数据表与表中数据一并删除，使用需谨慎，建议备份数据库内容之后再进行删除。

```sql
drop database [if exists] 数据库名;
```

终端操作：

```sql
mysql> drop database base;   -- 删除数据库语句
Query OK, 0 rows affected (0.00 sec)

mysql> drop database if exists base;   -- 删除时先判断当前数据库是否存在
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> drop database base;   -- 删除一个不存在的数据会报错
ERROR 1008 (HY000): Can not drop database 'base'; database does not exist
```



#### 使用数据库

在开发中，我们创建数据库的目录就是为了保存数据，而保存数据的话，则必须在数据库中对数据表进行操作，因为不同的目录是可以保存同名的文件，同样道理，不同的数据库可以拥有同样表名的文件，那么要对哪一个数据库中的数据表进行操作呢？就需要告诉数据库管理系统，我们要使用哪一个数据库。

```sql
use 数据库名;        -- 使用数据库/切换数据库 
select database();  --  查看当前使用的数据库
```

终端操作：

```sql
-- 因为上面的操作中，我们已经没有新建的数据库了，而剩下的几个数据库是mysql内置的，没有特殊原因，千万不要碰！！！
-- 为了接下来的学习，我们再次创建一个school数据库。也就是，被删除的数据库，可以在后面再次创建一个同名的数据库，但是并非原来的数据库了。
create database school;
use school;
```

执行效果：

```sql
mysql> create database school;
Query OK, 1 row affected (0.00 sec)

mysql> use school;   -- 高数mysql，我们要使用school数据库
Database changed
mysql> status    -- 可以通过status查看，我们当前使用了是哪一个数据库
--------------
C:\tool\mysql-8.0.28-winx64\bin\mysql.exe  Ver 8.0.28 for Win64 on x86_64 (MySQL Community Server - GPL)

Connection id:          20
Current database:       school
Current user:           root@localhost
```

注意：使用 drop database 命令时要非常谨慎，在执行该命令后，MySQL 不会给出任何提示确认信息。删除数据库后，数据库中存储的所有数据表和数据也将一同被删除，而且不能恢复。因此最好在删除数据库之前先将数据库进行备份。



### 数据表操作

数据表就相当于存储数据的特殊文件，数据表中的一条记录就相当于普通文件的一行内容。

```text
moluo, True, 18, 2000, 广东, 计算机科学与技术, python开发
xiaohong, False, 17, 2001, 广西, 舞蹈学, 音乐老师
```

与普通文件不同的是，数据表是二维的表格结构。

![image-20220530105512983](assets/image-20220530105512983-1654057010762.png)

#### 创建数据表

数据表就相当于文件，文件有文件名，自然地，数据表也要有表名。同样道理，数据表中的一条记录就相当于文件的一行内容。只是不同的是，数据表需要定义表头（上图中的首行），称为表的字段名。而且因为数据库的存储数据更加科学、严谨，所以需要创建表时要给每一个字段设置数据类型以及字段约束（完整性约束条件）。

```sql
create table  [if not exists]  表名 (
    字段名1    数据类型[ ( 存储空间 )    字段约束 ],
    字段名2    数据类型[ ( 存储空间 )    字段约束 ],
    字段名3    数据类型[ ( 存储空间 )    字段约束 ],
    .....
    字段名n   数据类型[ ( 存储空间 )    字段约束 ],
    primary key(一个 或 多个 字段名)    -- 注意，最后一段定义语句，不能有英文逗号的出现，否则报错。
) [engine = 存储引擎 character set 字符集];
```

注意：

>1. 上面SQL语句中，小括号中的定义字段语句后面必须以英文逗号结尾，而最后一个字段的定义语句不能有英文逗号出现，否则报错。
>2. 在同一张数据表中，字段名是不能相同，否则报错！
>3. 创建数据表的SQL语句中，存储空间和字段约束是选填的，而字段名和数据类型则是必须填写的。

创建班级表

```sql
-- mysql中创建数据表要以 create table `表名`
-- 表的字段信息必须写在 (  )  小括号里面
create table classes (
    -- 建议一行一个字段，id 就是字段名
    -- int 表示设置字段值要以整数的格式保存到硬盘中，
    -- auto_increment表示当前字段值在每次新增数据时自动+1作为值保存
    -- primary key，mysql中叫主键，表示用于区分一个数据表中不同行的数据的唯一性，同时还具备加快查询速度的作用
    -- 注意：auto_increment与primary key 一般是配合使用的，对应的字段名一般也叫id，而且在一个数据表中只有一个字段能使用auto_increment primary key进行设置。
    id int auto_increment primary key,
    -- 字段名：name
    -- varchar(10) 表示当前name这一列可以存储的数据是字符串格式，并且最多只能存10个字符
    name varchar(10),
    -- 字段名：address
    -- varchar(100) 表示adderss这一列可以存储的数据是字符串格式，并且最多只能存100个字符
    address varchar(100),
    -- 字段名：total
    -- int 表示当前total这一列的数据只能是整数，而且一个数据表中，整数的最大范围只能是42亿
    total int
);
```

上面的SQL语句就相当于创建了一个表格。

| id   | name | address | total |
| ---- | ---- | ------- | ----- |
|      |      |         |       |
|      |      |         |       |

终端操作：

```sql
mysql> create table classes (
    ->     id int auto_increment primary key,
    ->     name varchar(10),
    ->     address varchar(100),
    ->     total int
    -> );
Query OK, 0 rows affected (0.03 sec)

mysql> show tables;  -- 显示当前数据库school中所有的数据表
+------------------+
| Tables_in_school |
+------------------+
| classes          |
+------------------+
1 row in set (0.00 sec)
```



创建学生表

```sql
create table student(
id int auto_increment,   -- 字段名：id，数据类型：int整型，auto_increment整数自动增长+1
name varchar(10),   -- 字段名：name， 数据类型：varchar字符串（长度限制最多10个字符）
sex int default 1,  -- 字段名：sex，数据类型：int整型，默认值（default）：1 相当于True 
classes int,         -- 字段名：classes， 数据类型：int整型，
age int,             -- 字段名：age，数据类型：int整数,
description text,  -- 字段名：description，数据类型：text文本
primary key (id)  -- 设置主键(id) 每个表必须都有主键，用以区分不同行的数据
);
```

终端操作：

```sql
mysql> create table student (  -- 建表语句
    -> id int auto_increment,   -- 字段名：id，数据类型：int整型，auto_increment整数自动增长+1
    -> name varchar(10),   -- 字段名：name， 数据类型：varchar字符串（长度限制最多10个字符）
    -> sex int default 1,  -- 字段名：sex，数据类型：int整型，默认值（default）：1 相当于True
    -> classes int,         -- 字段名：classes， 数据类型：int整型，
    -> age int,             -- 字段名：age，数据类型：int整数,
    -> description text,  -- 字段名：description，数据类型：text文本
    -> primary key (id)  -- 设置主键(id) 每个表必须都有主键，用以区分不同行的数据
    -> );
Query OK, 0 rows affected (0.02 sec)



mysql> show tables;  -- 显示当前数据库下所有的数据表
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| student          |
+------------------+
2 rows in set (0.00 sec)  -- 出现这句话，表示创建表成功



mysql> desc student;   -- 查看表结构
+-------------+-------------+------+-----+---------+----------------------------------------+
| Field            |  Type                     | Null                    |     Key    | Default |      Extra               |
| 字段名          |  数据类型               | 是否能填None值 |     键      | 默认值   |      额外选项         |
+-------------+-------------+------+-----+---------+-----------------------------------------+
| id                 | int                           | NO                  |      PRI     | NULL    |   auto_increment |
| name           | varchar(10)             | YES                  |                | NULL    |                             |
| sex              | int                            | YES                  |                | 1          |                              |
| classes        | int                            | YES                  |                | NULL    |                             |
| age             | int                            | YES                  |                | NULL    |                             |
| description | text                          | YES                  |                | NULL    |                             |
+-------------+-------------+------+-----+---------+---------------------------+
6 rows in set (0.00 sec)



mysql> show create table student;   -- 显示当前数据库中的student数据表的建表语句
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table   | Create Table


                             |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| student | CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL,
  `sex` int DEFAULT '1',
  `classes` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

```

练习：假设现在我们有一个课程表(courses)，里面需要保存课程编号（id），课程名（cource），授课老师（lecturer），教室（address）。

![image-20220530113752339](assets/image-20220530113752339-1654057010762.png)

```sql
create table courses (
id int auto_increment primary key comment "课程编号",
course varchar(50) comment "课程名称",
lecturer int comment "讲师编号",
address int comment "教室编号"
);
```

终端操作：

```sql
mysql> create table courses (
    -> id int auto_increment primary key comment "课程编号",
    -> course varchar(50) comment "课程名称",
    -> lecturer int comment "讲师编号",
    -> address int comment "教室编号"
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> desc courses;  -- 显示表结构
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int         | NO   | PRI | NULL    | auto_increment |
| course   | varchar(50) | YES  |     | NULL    |                |
| lecturer | int         | YES  |     | NULL    |                |
| address  | int         | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
4 rows in set (0.00 sec)

mysql> show create table courses;   -- 显示建表语句
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table   | Create Table


                                                                 |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| courses | CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '课程编号',
  `course` varchar(50) DEFAULT NULL COMMENT '课程名称',
  `lecturer` int DEFAULT NULL COMMENT '讲师编号',
  `address` int DEFAULT NULL COMMENT '教室编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+---------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```





#### 命名规范

定义字段名，与mysql中数据表名、数据库名，规范基本一样，如下：

>1. 在64个字符以内，建议简短，如果不够清晰，可以使用下划线前缀_来划分，例如：user_info，user_address，user_course，teacher_info，等等， 
>2. 不能是SQL语句的关键字或者保留字，如果不确定名称是否是关键字或保留字，则可以使用反引号来圈住，例如：`age`，`info`
>3. 采用变量命名方式[ 由字母、数字、下划线组成，不能以数字开头 ]



#### 数据类型

数据库里面的数据在保存时也要通过指定数据的类型来告诉数据库管理系统，这些数据有什么用途，所以也会有对应的数据类型。**数据类型是为了节约内存,提高计算速度，尽量使用存储空间少的类型**。常用数据类型有数值类型、字符串类型、时间日期类型、枚举类型。mysql的单表数据表可以支持最多亿级（2000W-5000W是比较合适的）

##### 数值类型

MySQL中的数值类型提供了整型、浮点型、定点数，与python类似。

对于小数的表示，MYSQL分为两种方式：浮点数（float）和定点数（Decimal）。浮点数包括float(单精度)和double(双精度), 而定点数只有decimal一种，在mysql中底层以字符串的形式存放，比浮点数更精确，适合用来表示货币等精度要求高的数据。

| 分类     | 数据类型         | 存储大小          | 有符号范围（signed）                                         | 无符号范围(unsigned)                                         | 使用场景                         |
| -------- | ---------------- | ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------- |
| 整型     | **tinyint(m)**   | 1个字节           | (-128，127)                                                  | (0，255)                                                     | 年龄，分类的变好                 |
| 整型     | **smallint(m)**  | 2个字节           | (-32 768，32 767)                                            | (0，65 535)                                                  | 商品分类编号，员工编号，         |
| 整型     | mediumint(m)     | 3个字节           | (-8388608~8388607)                                           | (0，16 777 215)                                              | 小的数据表的主键id               |
| 整型     | **int(m)**       | 4个字节           | (-2147483648~2147483647)                                     | (0，4 294 967 295)                                           | 一般数据表的主键id               |
| 整型     | bigint(m)        | 8个字节           | (-9 233 372 036 854 775 808，9 223 372 036 854 775 807)      | (0，18 446 744 073 709 551 615)                              | 超大表的主键id                   |
| 浮点型   | **float(m,d)**   | 8位精度，4个字节  | 单精度，近似值的小数 m总个数，d小数位<br>(-3.402 823 466 E+38，-1.175 494 351 E-38)，0，(1.175 494 351 E-38，3.402 823 466 351 E+38) | 0，(1.175 494 351 E-38，3.402 823 466 E+38)                  | 数值类型的时间戳，带小数的经纬度 |
| 浮点型   | double(m,d)      | 16位精度，8个字节 | 双精度，近似值的小数  m总个数，d小数位<br>(-1.797 693 134 862 315 7 E+308，-2.225 073 858 507 201 4 E-308)，0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) | 0，(2.225 073 858 507 201 4 E-308，1.797 693 134 862 315 7 E+308) |                                  |
| 定点数   | **decimal(m,d)** |                   | 精确值，精确值的小数  m总个数，d小数位<br>依赖于m和d的值     | 依赖于m和d的值                                               | 货币，积分                       |
| 二进制位 | bit(m)           | 1个字节           | 依赖于m的值<br>                                              | 依赖于m的值                                                  | 签到二进制记录，布隆过滤器。     |

整型：

```sql
-- 说明：在数据表中，建议加上主键id，但是如果有特殊要求，也可以不加
-- tinyint类型
drop table if exists test1;
create table test1 (
id int auto_increment primary key,
age tinyint unsigned,
score tinyint,
number smallint,
chinese_achievement float(4,1),  -- 当前小数中所有数字的数量最多是3个数字，其中小数位最多1个数字
math_achievement double(4,1),  --  
english_achievement decimal(4,1)
);


-- 以下是测试代码，后面学习到
insert into test1 (age, score, number, chinese_achievement, math_achievement, english_achievement)
values (20, 100, 30000, 60.5, 93.5, 100);
```

终端操作：

```sql
mysql> drop table if exists test1;   -- 删除表，如果表存在的话
Query OK, 0 rows affected (0.01 sec)

mysql> create table test1 (    -- 建表语句
    -> id int auto_increment primary key,
    -> age tinyint unsigned,
    -> score tinyint,
    -> number smallint,
    -> chinese_achievement float(4,1),  -- 当前小数中所有数字的数量最多是3个数字，其中小数位最多1个数字
    -> math_achievement double(4,1),  --
    -> english_achievement decimal(4,1)
    -> );
Query OK, 0 rows affected, 2 warnings (0.02 sec)

-- 添加一条数据到数据表test1中
mysql> insert into test1 (age, score, number, chinese_achievement, math_achievement, english_achievement)
    -> values (20, 100, 30000, 60.5, 93.5, 100);
Query OK, 1 row affected (0.01 sec)

-- 查看数据表test1中的所有数据
mysql> select * from test1;
+----+------+-------+--------+---------------------+------------------+---------------------+
| id | age  | score | number | chinese_achievement | math_achievement | english_achievement |
+----+------+-------+--------+---------------------+------------------+---------------------+
|  1 |   20 |   100 |  30000 |                60.5 |             93.5 |               100.0 |
+----+------+-------+--------+---------------------+------------------+---------------------+
```



##### 字符串类型

MySQL中针对文本内容的存储类型提供了字符串与文本两种格式，其中按存储方式不同，又分为固定长度（定长）与可变长度（变长）两种，按存储格式不同，又分为普通字符格式与二进制格式两种。

SQL 语句中（单|双）引号都能表示字符串或文本。

| 数据类型(n指定存储的长度上限) | 大小                | 描述                                       | 应用场景                       |
| ----------------------------- | ------------------- | ------------------------------------------ | ------------------------------ |
| **char(n)**                   | 0-255字符           | 定长字符串                                 | 姓名，验证码                   |
| **varchar(n)**                | 0-65535字符         | 变长字符串                                 | 账号，密码，文章标题，商品标题 |
| binary(n)                     | 0-255字符           | 定长二进制字符串                           |                                |
| varbinary(n)                  | 0-65535字符         | 变长二进制字符串                           |                                |
| tinytext                      | 0-255字符           | 可变长度文本                               |                                |
| **text**                      | 0-65 535字符        | 可变长度文本                               | 文章内容，                     |
| mediumtext                    | 0-16 777 215字符    | 可变长度文本                               |                                |
| longtext                      | 0-4 294 967 295字符 | 可变长度文本                               |                                |
| tinyblob                      | 0-255字符           | 可变二进制文本                             |                                |
| **blob**                      | 0-65 535字符        | 可变二进制文本                             | 小图标、二进制的认证信息       |
| mediumblob                    | 0-16 777 215字符    | 可变二进制文本                             |                                |
| longblob                      | 0-4 294 967 295字符 | 可变二进制文本                             |                                |
| **json**                      | 0-4 294 967 295字符 | 可变二进制json文本 (也叫bson: binary json) | 主要实现一些NoSQL数据的存储    |

char与varchar的区别：

> 1.char(n) 若存入字符数小于n，则以空格补于其后，SQL语句查询时再将空格去掉。所以char类型存储的字符串末尾不能有空格，varchar不限于此。 
> 2.char(4)不管是存入几个字符，都将占用4个字符空间，varchar是存入的实际字符数+1个结束符号（n<=255）或2个字节(n>255)，所以varchar(4), 存入3个字符将占用4个字符空间。 
> 3.因为char类型是固定长度存储空间的，所以在数据库查询速度要比varchar类型的快，因为varchar是动态空间分配，所以每次查找的是否要判断结束符的位置。

varchar字符串和text文本的区别：

> 1. varchar可指定n，text不能指定，内部存储varchar是存入的实际字符数+1个结束符号（n<=255）或2个字节(n>255)，text是实际字符数+2个字节。 
> 2. text类型不能有默认值，注意json也不能有默认值。
> 3. varchar可直接创建索引，text创建索引要指定前多少个字符。varchar查询速度快于text。
>
> 索引：index，主要为了加快查询数据的数据的一种技术，类似书籍的目录。

```sql
create table test2 (
id int auto_increment primary key,
name char(15),
username varchar(15),
password varchar(250),
description text,
avatar blob,
info json
);
```

 

终端操作：

```sql
-- 创建表语句
mysql> create table test2 (
    -> id int auto_increment primary key,
    -> name char(15),
    -> username varchar(15),
    -> password varchar(250),
    -> description text,
    -> avatar blob,
    -> info json
    -> );
Query OK, 0 rows affected (0.02 sec)

-- 添加数据
insert into test2 (name ,username, password, description, avatar, info) 
values 
("李磊", "lilei202209", sha1("123456"),  "很长的一段自我介绍....", "abc", '{"address": "北京市"}');


-- 查看数据
mysql> select * from test2;
+----+------+-------------+------------------------------------------+------------------------+----------------+-----------------------+
| id | name | username    | password                                 | description            | avatar         | info                  |
+----+------+-------------+------------------------------------------+------------------------+----------------+-----------------------+
|  1 | 李磊 | lilei202209 | 7c4a8d09ca3762af61e59520943dc26494f8941b | 很长的一段自我介绍.... | 0x616263       | {"address": "北京市"} |
+----+------+-------------+------------------------------------------+------------------------+----------------+-----------------------+
1 row in set (0.00 sec)
```



##### 日期类型

表示时间值的日期和时间类型为 DATETIME、DATE、TIMESTAMP、TIME 和 YEAR。

每个时间类型有一个有效值范围和一个"零"值，当指定不合法的 MySQL 不能表示的值时使用"零"值。

| 数据类型      | 取值范围                                | 日期格式            | 零值                | 使用场景                               |
| :------------ | :-------------------------------------- | :------------------ | :------------------ | -------------------------------------- |
| **year**      | 1901~2155                               | YYYY                | 0000                | 电影年份，图书年份                     |
| **date**      | 1000-01-01~9999-12-31                   | YYYY-MM-DD          | 0000-00-00          | 生日                                   |
| time          | -838:59:59~838:59:59                    | HH:MM:SS            | 00:00:00            | 餐牌时间，会议时间                     |
| **datetime**  | 1000-01-01 00:00:00~9999-12-31 23:59:59 | YYYY-MM-DD HH:MM:SS | 0000-00-00 00:00:00 | 添加时间，更新时间，删除时间，登陆时间 |
| **timestamp** | 1970-01-01 00:00:01~2038-01-19 03:14:07 | YYYY-MM-DD HH:MM:SS | 0000-00-00 00:00:00 | 添加时间，更新时间，删除时间，登陆时间 |

```sql
create table user_info (
id int auto_increment primary key comment "主键ID",
nickname varchar(50) comment "昵称",
username varchar(32) comment "登陆账户",
password varchar(500) comment "登录密码",
birthday date comment "出生日期",
created_time timestamp default current_timestamp() comment "创建时间",
updated_time timestamp comment "更新时间",
deleted_time timestamp default null comment "虚拟删除时间"
);

-- 添加数据给数据表
insert into user_info (nickname, username, password, birthday) 
values
("小灰灰", "root", sha1("123456"), "2000-10-21"); 

-- 查询数据
select * from user_info;

-- 更新数据
update user_info set nickname="大灰狼", updated_time=current_timestamp() where id = 1;

-- 删除数据[虚拟删除]
update user_info set deleted_time=current_timestamp() where id = 1;

-- 查看数据[加上一个查询条件，通过where指定不要查询deleted_time有值的]
select * from  user_info where deleted_time = null;
```

mysql的空叫null，python的空叫None。

终端操作：

```sql
mysql> use school  -- 使用school数据库
Database changed
mysql> show tables; -- 显示数据库下所有的数据表
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| student          |
| test1            |
| test2            |
+------------------+
5 rows in set (0.05 sec)

-- 建表语句
mysql> create table user_info (
    -> id int auto_increment primary key comment "主键ID",
    -> nickname varchar(50) comment "昵称",
    -> username varchar(32) comment "登陆账户",
    -> password varchar(500) comment "登录密码",
    -> birthday date comment "出生日期",
    -> created_time timestamp default current_timestamp() comment "创建时间",
    -> updated_time timestamp comment "更新时间",
    -> deleted_time timestamp default null comment "虚拟删除时间"
    -> );
Query OK, 0 rows affected (0.06 sec)

mysql> desc user_info; -- 显示表结构
+--------------+--------------+------+-----+-------------------+-------------------+
| Field        | Type         | Null | Key | Default           | Extra             |
+--------------+--------------+------+-----+-------------------+-------------------+
| id           | int          | NO   | PRI | NULL              | auto_increment    |
| nickname     | varchar(50)  | YES  |     | NULL              |                   |
| username     | varchar(32)  | YES  |     | NULL              |                   |
| password     | varchar(500) | YES  |     | NULL              |                   |
| birthday     | date         | YES  |     | NULL              |                   |
| created_time | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| updated_time | timestamp    | YES  |     | NULL              |                   |
| deleted_time | timestamp    | YES  |     | NULL              |                   |
+--------------+--------------+------+-----+-------------------+-------------------+
8 rows in set (0.02 sec)

-- 添加数据给数据表
mysql> insert into user_info (nickname, username, password, birthday)
    -> values
    -> ("小灰灰", "root", sha1("123456"), "2000-10-21");
Query OK, 1 row affected (0.01 sec)

-- 查看表中所有的数据内容
mysql> select * from user_info;
+----+----------+----------+------------------------------------------+------------+---------------------+--------------+--------------+
| id | nickname | username | password                                 | birthday   | created_time        | updated_time | deleted_time |
+----+----------+----------+------------------------------------------+------------+---------------------+--------------+--------------+
|  1 | 小灰灰   | root     | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2000-10-21 | 2022-05-31 08:56:31 | NULL
| NULL         |
+----+----------+----------+------------------------------------------+------------+---------------------+--------------+--------------+
1 row in set (0.00 sec)

-- 更新数据的时候，顺便更新下更新时间
mysql> update user_info set nickname="大灰狼", updated_time=current_timestamp() where id = 1;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

-- 查询更新数据后的信息
mysql> select * from user_info;
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+--------------+
| id | nickname | username | password                                 | birthday   | created_time        | updated_time        | deleted_time |
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+--------------+
|  1 | 大灰狼   | root     | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2000-10-21 | 2022-05-31 08:56:31 | 2022-05-31 08:58:57 | NULL         |
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+--------------+
1 row in set (0.00 sec)

-- 删除数据[逻辑删除, 虚拟删除]
mysql> update user_info set deleted_time=current_timestamp() where id = 1;
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from user_info;
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+---------------------+
| id | nickname | username | password                                 | birthday   | created_time        | updated_time        | deleted_time        |
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+---------------------+
|  1 | 大灰狼   | root     | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2000-10-21 | 2022-05-31 08:56:31 | 2022-05-31 08:58:57 | 2022-05-31 09:00:08 |
+----+----------+----------+------------------------------------------+------------+---------------------+---------------------+---------------------+
1 row in set (0.00 sec)

-- 查询数据时，使用where指定不要查询哪些已经被虚拟删除的数据
mysql> select * from  user_info where deleted_time = null;
Empty set (0.00 sec)
```



##### 枚举与集合

enum中文名称叫枚举类型，它的值范围需要在创建表时通过枚举方式显示。ENUM**只允许从值集合中选取单个值，而不能一次取多个值**。SET和ENUM非常相似，也是一个字符串对象，里面可以包含0-64个成员。根据成员的不同，存储上也有所不同。set类型可以**允许值集合中任意选择1或多个元素进行组合**。对超出范围的内容将不允许注入，而对重复的值将进行自动去重。

| 类型     | 大小 (字节)                                                  | 用途                       |
| -------- | ------------------------------------------------------------ | -------------------------- |
| **enum** | 对1-255个成员的枚举需要1个字节存储;<br>对于255-65535个成员，需要2个字节存储;<br>最多允许65535个成员。 | 单选：选择性别，现居地城市 |
| **set**  | 1-8个成员的集合，占1个字节<br>9-16个成员的集合，占2个字节<br>17-24个成员的集合，占3个字节<br>25-32个成员的集合，占4个字节<br>33-64个成员的集合，占8个字节 | 多选：兴趣、爱好、标签     |

```sql
create table users (
id int auto_increment primary key comment "主键ID",
nickname varchar(50) comment "昵称",
username varchar(32) comment "登陆账户",
password varchar(500) comment "登录密码",
birthday date comment "出生日期",
education enum("小学","初中", "高中", "中专", "大专", "本科") comment "学历",
hobby set("game", "code", "shopping", "swim", "play ball"),
created_time timestamp default current_timestamp() comment "创建时间",
updated_time timestamp comment "更新时间",
deleted_time timestamp default null comment "虚拟删除时间"
);

desc users;

-- 添加数据
insert into users (nickname, username, password, birthday, education, hobby) 
values
("小灰灰", "root", sha1("123456"), "2000-10-21", "小学", "game"); 

insert into users (nickname, username, password, birthday, education, hobby) 
values
("墨落", "moluo", sha1("123456"), "2018-01-21", "初中",  'game,code,shopping'); 


-- 查看数据
select * from users;
```

终端操作：

```sql
-- 创建表
mysql> create table users (
    -> id int auto_increment primary key comment "主键ID",
    -> nickname varchar(50) comment "昵称",
    -> username varchar(32) comment "登陆账户",
    -> password varchar(500) comment "登录密码",
    -> birthday date comment "出生日期",
    -> education enum("小学","初中", "高中", "中专", "大专", "本科") comment "学历",
    -> hobby set("game", "code", "shopping", "swim", "play ball"),
    -> created_time timestamp default current_timestamp() comment "创建时间",
    -> updated_time timestamp comment "更新时间",
    -> deleted_time timestamp default null comment "虚拟删除时间"
    -> );
Query OK, 0 rows affected (0.03 sec)

-- 查看表结构
mysql> desc users;
+--------------+--------------------------------------------------+------+-----+-------------------+-------------------+
| Field        | Type                                             | Null | Key | Default           | Extra             |
+--------------+--------------------------------------------------+------+-----+-------------------+-------------------+
| id           | int                                              | NO   | PRI | NULL              | auto_increment    |
| nickname     | varchar(50)                                      | YES  |     | NULL              |                   |
| username     | varchar(32)                                      | YES  |     | NULL              |                   |
| password     | varchar(500)                                     | YES  |     | NULL              |                   |
| birthday     | date                                             | YES  |     | NULL              |                   |
| education    | enum('小学','初中','高中','中专','大专','本科')  | YES  |     | NULL              |                   |
| hobby        | set('game','code','shopping','swim','play ball') | YES  |     | NULL              |                   |
| created_time | timestamp                                        | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| updated_time | timestamp                                        | YES  |     | NULL              |                   |
| deleted_time | timestamp                                        | YES  |     | NULL              |                   |
+--------------+--------------------------------------------------+------+-----+-------------------+-------------------+
10 rows in set (0.00 sec)


-- 添加数据
mysql> insert into users (nickname, username, password, birthday, education, hobby)
    -> values
    -> ("小灰灰", "root", sha1("123456"), "2000-10-21", "小学", "game");
Query OK, 1 row affected (0.00 sec)


-- 查看数据
mysql> select * from users;
+----+----------+----------+------------------------------------------+------------+-----------+-------+---------------------+--------------+--------------+
| id | nickname | username | password                                 | birthday   | education | hobby | created_time        | updated_time | deleted_time |
+----+----------+----------+------------------------------------------+------------+-----------+-------+---------------------+--------------+--------------+
|  1 | 小灰灰   | root     | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2000-10-21 | 小学      | game  | 2022-05-31 09:18:05 | NULL         | NULL         |
+----+----------+----------+------------------------------------------+------------+-----------+-------+---------------------+--------------+--------------+
1 row in set (0.00 sec)


-- 再次添加数据
mysql> insert into users (nickname, username, password, birthday, education, hobby)
    -> values
    -> ("墨落", "moluo", sha1("123456"), "2018-01-21", "初中",  'game,code,shopping');
Query OK, 1 row affected (0.00 sec)

-- 再次查看数据
mysql> select * from users;
+----+----------+----------+------------------------------------------+------------+-----------+--------------------+---------------------+--------------+--------------+
| id | nickname | username | password                                 | birthday   | education | hobby              | created_time        | updated_time | deleted_time |
+----+----------+----------+------------------------------------------+------------+-----------+--------------------+---------------------+--------------+--------------+
|  1 | 小灰灰   | root     | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2000-10-21 | 小学      | game               | 2022-05-31 09:18:05 | NULL
| NULL         |
|  2 | 墨落     | moluo    | 7c4a8d09ca3762af61e59520943dc26494f8941b | 2018-01-21 | 初中      | game,code,shopping | 2022-05-31 09:24:19 | NULL
| NULL         |
+----+----------+----------+------------------------------------------+------------+-----------+--------------------+---------------------+--------------+--------------+
2 rows in set (0.00 sec)
```



#### 字段约束

也叫完整性约束条件，主要是为了防止不符合规范的数据进入数据库，在用户对数据进行插入、修改、删除等操作时，DBMS自动按照一定的约束条件对数据进行监测，使不符合规范的数据不能进入数据库，以确保数据库中存储的数据正确、有效、相容。 

| 约束类型 | SQL关键字          | 语法                                                         | 描述                                                         |
| -------- | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 填充     | zerofill           | 字段名 整型 zerofill                                         | 为数据表中的整型字段设置数值左边补0                          |
| 无符号   | **unsigned**       | 字段名 数据类型 unsigned                                     | 为数据表中的数值类型字段设置数值指定不能小于0，可以让字段值的取值范围，在正数范围内增加1倍。 |
| 默认值   | **default**        | 字段名 数据类型 default 默认值                               | 为数据表中的字段指定默认值。但blob、text与json类型不支持default。 |
| 非空     | **not null**       | 字段名 数据类型 not null                                     | 非空字段指字段的值不能为NULL。                               |
| 唯一索引 | **unique**         | 列级约束<br>字段名 数据类型 unique<br>表级约束<br>unique (字段名 1，字段名 2…) | 用于保证数据表中字段的不同行的值唯一性，即表中字段的值不能重复出现在多行。<br>列级约束定义在一个列上，只对该列起约束作用； <br>表级约束是独立于列的定义，可以应用在一个表的多个列上。 |
| 主键索引 | **primary key**    | 列级约束<br> 字段名 数据类型 primary key <br>表级约束<br>primary key(字段名 1,字段名2…) | 一个表中只能有一个主键。可以指定单个字段为单列主键，也可以指定多个字段为联合主键。 |
| 自动增长 | **auto_increment** | 字段名 数据类型 auto_increment                               | 一个表中只能有一个自动增长的字段，该字段类型是整数类型，一般用于设置主键。<br>自动增长值从1开始自增，每次加1。 |
| 索引     | **index / key**    | index / key (字段名)                                         | 给对应的字段的值设置添加索引（目的让当前字段的值在被删除，修改，查询时，加快执行速度） |
| 外键索引 | **foreign key**    | constraint 外键名 foreign key 字段名 [，字段名2，…] references <主表名> 主键列1 [，主键列2，…] | 用来建立主表与从表的关联关系，为两个表的数据建立连接，约束两个表中数据的一致性和完整性。 |

练习，动手创建一个商品表。 

```sql
create table goods_info(
    id int unsigned not null auto_increment comment "主键ID",
    goods_number int zerofill unsigned not null comment "商品进货号",
    title varchar(100) not null comment "商品标题",
    company varchar(100) not null comment "商品厂商",
    description text null comment "商品描述",
    country varchar(50) default "中国" comment "产地",
    unique (title, company),
    index (title),
    index (country),
    primary key (id, goods_number) 
);


-- 添加一条数据
insert into goods_info (goods_number, title, company, description) 
values 
(1, "小羊牌沐浴露", "小羊生活科技", "很好用的沐浴露~~~");

-- 一次性添加多条数据
insert into goods_info (goods_number, title, company, description) 
values 
(2, "小羊牌洗发水", "小羊生活科技", "很好用的洗发水~~~"),
(3, "小羊牌洗面奶", "小羊生活科技", "很好用的洗面奶~~~"),
(4, "大羊牌沐浴露", "大羊生活科技", "很好用的沐浴露~~~"),
(5, "大羊牌洗面奶", "大羊生活科技", "很好用的洗面奶~~~");

-- 查看数据
select * from goods_info;
```

终端操作：

```sql
-- 建表语句
mysql> create table `goods_info`(
    ->     id int unsigned not null auto_increment comment "主键ID",
    ->     goods_number int zerofill unsigned not null comment "商品进货号",
    ->     title varchar(100) not null comment "商品标题",
    ->     company varchar(100) not null comment "商品厂商",
    ->     description text null comment "商品描述",
    ->     country varchar(50) default "中国" comment "产地",
    ->     unique (title, company),
    ->     index (title),
    ->     index (country),
    ->     primary key (id, goods_number)
    -> );
Query OK, 0 rows affected, 1 warning (0.05 sec)

mysql> desc goods_info;
+--------------+---------------------------+------+-----+---------+----------------+
| Field        | Type                      | Null | Key | Default | Extra          |
+--------------+---------------------------+------+-----+---------+----------------+
| id           | int unsigned              | NO   | PRI | NULL    | auto_increment |
| goods_number | int(10) unsigned zerofill | NO   | PRI | NULL    |                |
| title        | varchar(100)              | NO   | MUL | NULL    |                |
| company      | varchar(100)              | NO   |     | NULL    |                |
| description  | text                      | YES  |     | NULL    |                |
| country      | varchar(50)               | YES  | MUL | 中国    |                |
+--------------+---------------------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)


-- 添加一条数据
mysql> insert into goods_info (goods_number, title, company, description)
    -> values
    -> (1, "小羊牌沐浴露", "小羊生活科技", "很好用的沐浴露~~~");
Query OK, 1 row affected (0.00 sec)


-- 一次性添加多条数据
mysql> insert into goods_info (goods_number, title, company, description)
    -> values
    -> (2, "小羊牌洗发水", "小羊生活科技", "很好用的洗发水~~~"),
    -> (3, "小羊牌洗面奶", "小羊生活科技", "很好用的洗面奶~~~"),
    -> (4, "大羊牌沐浴露", "大羊生活科技", "很好用的沐浴露~~~"),
    -> (5, "大羊牌洗面奶", "大羊生活科技", "很好用的洗面奶~~~");
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

-- 查看数据
mysql> select * from goods_info;
+----+--------------+--------------+--------------+-------------------+---------+
| id | goods_number | title        | company      | description       | country |
+----+--------------+--------------+--------------+-------------------+---------+
|  1 |   0000000001 | 小羊牌沐浴露 | 小羊生活科技 | 很好用的沐浴露~~~ | 中国    |
|  2 |   0000000002 | 小羊牌洗发水 | 小羊生活科技 | 很好用的洗发水~~~ | 中国    |
|  3 |   0000000003 | 小羊牌洗面奶 | 小羊生活科技 | 很好用的洗面奶~~~ | 中国    |
|  4 |   0000000004 | 大羊牌沐浴露 | 大羊生活科技 | 很好用的沐浴露~~~ | 中国    |
|  5 |   0000000005 | 大羊牌洗面奶 | 大羊生活科技 | 很好用的洗面奶~~~ | 中国    |
+----+--------------+--------------+--------------+-------------------+---------+
5 rows in set (0.00 sec)
```



#### 查看数据表

##### 查看所有数据表

列出当前数据库中所有的数据表,语法：

```sql
show tables;
```

终端操作：

```sql
mysql> show tables;
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| goods_info       |
| student          |
| test1            |
| test2            |
| user_info        |
| users            |
+------------------+
8 rows in set (0.00 sec)
```



##### 查看表结构

以表格形式列出当前数据表的字段结构信息。常用的是`desc`，语法：

```sql
-- 方式1：简单查看
describe 表名;
desc 表名;   -- desc是describe的缩写

-- 方式2：查看信息
describe table 表名;
desc table 表名;
```



##### 查看建表语句

```sql
show create table 表名 \G;
```

效果：

```sql
mysql> show create table goods_info;
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table      | Create Table


                                                                                                                           |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| goods_info | CREATE TABLE `goods_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `goods_number` int(10) unsigned zerofill NOT NULL COMMENT '商品进货号',
  `title` varchar(100) NOT NULL COMMENT '商品标题',
  `company` varchar(100) NOT NULL COMMENT '商品厂商',
  `description` text COMMENT '商品描述',
  `country` varchar(50) DEFAULT '中国' COMMENT '产地',
  PRIMARY KEY (`id`,`goods_number`),
  UNIQUE KEY `title` (`title`,`company`),
  KEY `title_2` (`title`),
  KEY `country` (`country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```



#### 删除数据表

删除表结构，并把数据一并删除，因为删除表操作没有确认么，所以使用需谨慎，强烈建议先备份后删除，或者直接改表名来代替删除操作。

```sql
-- 直接删除
drop table 表名;

-- 判断删除，判断表存在了，再删除，防止删除不存在的表导致错误出现
drop table if exists 表名;
```

终端操作：

```sql
-- 显示当前数据库下所有的数据表
mysql> show tables;
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| goods_info       |
| student          |
| user_info        |
| users            |
+------------------+
6 rows in set (0.00 sec)

-- 删除usres数据表
mysql> drop table users;
Query OK, 0 rows affected (0.02 sec)

-- 显示所有数据表
mysql> show tables;
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| goods_info       |
| student          |
| user_info        |
+------------------+
5 rows in set (0.00 sec)

-- 判断表存在了，再删除
mysql> drop table if exists test2;
Query OK, 0 rows affected, 1 warning (0.00 sec)
```



##### 重置表信息

保留数据表结构，但是把数据表存储的数据清空以及数据表的状态清零，相当于删除原表，并新建一张一模一样的空数据表。

```sql
truncate table 表名;
```

终端操作：

```sql
-- 一次性添加多条数据
insert into goods_info (goods_number, title, company, description) 
values 
(1, "小羊牌沐浴露", "小羊生活科技", "很好用的沐浴露~~~"),
(2, "小羊牌洗发水", "小羊生活科技", "很好用的洗发水~~~"),
(3, "小羊牌洗面奶", "小羊生活科技", "很好用的洗面奶~~~"),
(4, "大羊牌沐浴露", "大羊生活科技", "很好用的沐浴露~~~"),
(5, "大羊牌洗面奶", "大羊生活科技", "很好用的洗面奶~~~");

-- 查看数据
select * from goods_info;

-- 添加了数据以后的建表信息中，会附带一个AUTO_INCREMENT状态，记录自动增加的计算值
show create table goods_info;

-- 如果直接通过delete删除数据表所有数据的方式，实际上不能让表中的状态清零的
delete from goods_info;

-- 查看数据
select * from goods_info;

-- 查看表的建表语句
show create table goods_info;

-- 重置表所有信息
truncate table goods_info;

-- 查看数据
select * from goods_info;

-- 查看表的建表语句
show create table goods_info;
```

终端操作：

```sql
-- 一次性添加多条数据
mysql> insert into goods_info (goods_number, title, company, description)
    -> values
    -> (1, "小羊牌沐浴露", "小羊生活科技", "很好用的沐浴露~~~"),
    -> (2, "小羊牌洗发水", "小羊生活科技", "很好用的洗发水~~~"),
    -> (3, "小羊牌洗面奶", "小羊生活科技", "很好用的洗面奶~~~"),
    -> (4, "大羊牌沐浴露", "大羊生活科技", "很好用的沐浴露~~~"),
    -> (5, "大羊牌洗面奶", "大羊生活科技", "很好用的洗面奶~~~");
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

-- 查看数据
mysql> select * from goods_info;
+----+--------------+--------------+--------------+-------------------+---------+
| id | goods_number | title        | company      | description       | country |
+----+--------------+--------------+--------------+-------------------+---------+
|  1 |   0000000001 | 小羊牌沐浴露 | 小羊生活科技 | 很好用的沐浴露~~~ | 中国    |
|  2 |   0000000002 | 小羊牌洗发水 | 小羊生活科技 | 很好用的洗发水~~~ | 中国    |
|  3 |   0000000003 | 小羊牌洗面奶 | 小羊生活科技 | 很好用的洗面奶~~~ | 中国    |
|  4 |   0000000004 | 大羊牌沐浴露 | 大羊生活科技 | 很好用的沐浴露~~~ | 中国    |
|  5 |   0000000005 | 大羊牌洗面奶 | 大羊生活科技 | 很好用的洗面奶~~~ | 中国    |
+----+--------------+--------------+--------------+-------------------+---------+
5 rows in set (0.00 sec)


-- 添加了数据以后的建表信息中，会附带一个AUTO_INCREMENT状态，记录自动增加的计算值
mysql> show create table goods_info;
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table      | Create Table


                                                                                                                                            |
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| goods_info | CREATE TABLE `goods_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `goods_number` int(10) unsigned zerofill NOT NULL COMMENT '商品进货号',
  `title` varchar(100) NOT NULL COMMENT '商品标题',
  `company` varchar(100) NOT NULL COMMENT '商品厂商',
  `description` text COMMENT '商品描述',
  `country` varchar(50) DEFAULT '中国' COMMENT '产地',
  PRIMARY KEY (`id`,`goods_number`),
  UNIQUE KEY `title` (`title`,`company`),
  KEY `title_2` (`title`),
  KEY `country` (`country`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

-- 如果直接通过delete删除数据表所有数据的方式，实际上不能让表中的状态清零的
mysql> delete from goods_info;
Query OK, 5 rows affected (0.00 sec)

mysql>
mysql> -- 查看数据
mysql> select * from goods_info;
Empty set (0.00 sec)

mysql>
mysql> -- 查看表的建表语句
mysql> show create table goods_info;
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table      | Create Table


                                                                                                                                            |
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| goods_info | CREATE TABLE `goods_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `goods_number` int(10) unsigned zerofill NOT NULL COMMENT '商品进货号',
  `title` varchar(100) NOT NULL COMMENT '商品标题',
  `company` varchar(100) NOT NULL COMMENT '商品厂商',
  `description` text COMMENT '商品描述',
  `country` varchar(50) DEFAULT '中国' COMMENT '产地',
  PRIMARY KEY (`id`,`goods_number`),
  UNIQUE KEY `title` (`title`,`company`),
  KEY `title_2` (`title`),
  KEY `country` (`country`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)


-- 重置表所有信息
mysql> truncate table goods_info;
Query OK, 0 rows affected (0.05 sec)

mysql>
mysql> -- 查看数据
mysql> select * from goods_info;
Empty set (0.00 sec)

mysql>
mysql> -- 查看表的建表语句
mysql> show create table goods_info;
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table      | Create Table


                                                                                                                           |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| goods_info | CREATE TABLE `goods_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `goods_number` int(10) unsigned zerofill NOT NULL COMMENT '商品进货号',
  `title` varchar(100) NOT NULL COMMENT '商品标题',
  `company` varchar(100) NOT NULL COMMENT '商品厂商',
  `description` text COMMENT '商品描述',
  `country` varchar(50) DEFAULT '中国' COMMENT '产地',
  PRIMARY KEY (`id`,`goods_number`),
  UNIQUE KEY `title` (`title`,`company`),
  KEY `title_2` (`title`),
  KEY `country` (`country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

delete与truncate的区别：

> 两个命令都会把数据清空，但是delete会删除数据，保留表的历史状态，而truncate会清空数据并清楚表的历史状态。



#### 修改数据表

针对数据表的修改操作，MySQL提供了数据表重命名，增加字段，删除字段，修改字段信息等操作。

##### 数据表重命名

```sql
alter table 表名  rename 新表名;
```

终端操作：

```sql
mysql> show tables;
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| goods_info       |
| student          |
| user_info        |
+------------------+
5 rows in set (0.00 sec)

mysql> alter table student rename student_info;
Query OK, 0 rows affected (0.03 sec)

mysql> show tables;
+------------------+
| Tables_in_school |
+------------------+
| classes          |
| courses          |
| goods_info       |
| student_info     |
| user_info        |
+------------------+
5 rows in set (0.00 sec)
```



##### 增加字段

开发中，根据一开始的需求，设计的数据表，有可能随着业务的发展，时空的变化，可能会对数据表中的字段进行增加。

```sql
-- 添加一个字段
alter table 表名
add 字段名1  数据类型 [完整性约束条件…];

-- 一次性添加多个字段
alter table 表名
add 字段名1  数据类型 [完整性约束条件…],
add 字段名2 数据类型 [完整性约束条件…],
...
add 字段名n  数据类型 [完整性约束条件…];

-- 在指定位置添加字段
ALTER TABLE 表名
ADD 字段名  数据类型 [完整性约束条件…]  FIRST;  -- 在第一个字段之前，新增字段（新的字段就变成了表的第一个字段）

ALTER TABLE 表名
ADD 字段名  数据类型 [完整性约束条件…]  AFTER 字段名;  -- 在指定字段之后新增字段
```



```sql
create table test1 (
 id int unsigned NOT NULL AUTO_INCREMENT primary key COMMENT '主键ID'
);

desc test1;

-- 新增字段
alter table test1 add title varchar(100) NOT NULL COMMENT '商品标题';

desc test1;

-- 新增多个字段
alter table test1 
add  company varchar(100) NOT NULL COMMENT '商品厂商',
add  description text COMMENT '商品描述';

-- 新增字段作为表的第一个字段存在
alter table test1 add number int(10) unsigned zerofill NOT NULL COMMENT '商品进货号' first;

-- 在指定位置之后添加字段
alter table test1 add country varchar(50) DEFAULT '中国' COMMENT '产地' after company;
```

终端操作：

```sql
-- 新建数据表
mysql> create table test1 (
    ->  id int unsigned NOT NULL AUTO_INCREMENT primary key COMMENT '主键ID'
    -> );
Query OK, 0 rows affected (0.03 sec)

-- 查看表结构
mysql> desc test1;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int unsigned | NO   | PRI | NULL    | auto_increment |
+-------+--------------+------+-----+---------+----------------+
1 row in set (0.00 sec)

-- 新增一个字段
mysql> alter table test1 add title varchar(100) NOT NULL COMMENT '商品标题';
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test1;
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int unsigned | NO   | PRI | NULL    | auto_increment |
| title | varchar(100) | NO   |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

-- 新增多个字段
mysql> alter table test1
    -> add  company varchar(100) NOT NULL COMMENT '商品厂商',
    -> add  description text COMMENT '商品描述';
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 新增字段作为表的第一个字段
mysql> alter table test1 add number int(10) unsigned zerofill NOT NULL COMMENT '商品进货号' first;
Query OK, 0 rows affected, 2 warnings (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 2

-- 查看表结构
mysql> desc test1;
+-------------+---------------------------+------+-----+---------+----------------+
| Field       | Type                      | Null | Key | Default | Extra          |
+-------------+---------------------------+------+-----+---------+----------------+
| number      | int(10) unsigned zerofill | NO   |     | NULL    |                |
| id          | int unsigned              | NO   | PRI | NULL    | auto_increment |
| title       | varchar(100)              | NO   |     | NULL    |                |
| company     | varchar(100)              | NO   |     | NULL    |                |
| description | text                      | YES  |     | NULL    |                |
+-------------+---------------------------+------+-----+---------+----------------+
5 rows in set (0.00 sec)

-- 在指定字段的后面新增字段
mysql> alter table test1 add country varchar(50) DEFAULT '中国' COMMENT '产地' after company;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test1;
+-------------+---------------------------+------+-----+---------+----------------+
| Field       | Type                      | Null | Key | Default | Extra          |
+-------------+---------------------------+------+-----+---------+----------------+
| number      | int(10) unsigned zerofill | NO   |     | NULL    |                |
| id          | int unsigned              | NO   | PRI | NULL    | auto_increment |
| title       | varchar(100)              | NO   |     | NULL    |                |
| company     | varchar(100)              | NO   |     | NULL    |                |
| country     | varchar(50)               | YES  |     | 中国    |                |
| description | text                      | YES  |     | NULL    |                |
+-------------+---------------------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)
```



##### 删除字段

在开发中，如果表中有数据了，一般我们强烈反对删除字段的！！！因为这个操作会导致对应字段的值也被删除，因此如果非要删除字段，则务必保证已经备份了数据表。

```sql
alter table 表名 
drop 字段名;
```

终端操作：

```sql
create table test2(
id int unsigned NOT NULL AUTO_INCREMENT primary key COMMENT '主键ID',
name varchar(50) comment "用户名",
age tinyint comment "年龄",
sex enum("男", "女", "保密")
);

insert into test2 (name, age, sex) values ("小明",  17, "男"), ("小白", 18, "女");

select * from test2;

alter table test2 drop sex;

select * from test2;
```

操作效果：

```sql
-- 新建表
mysql> create table test2(
    -> id int unsigned NOT NULL AUTO_INCREMENT primary key COMMENT '主键ID',
    -> name varchar(50) comment "用户名",
    -> age tinyint comment "年龄",
    -> sex enum("男", "女", "保密")
    -> );
Query OK, 0 rows affected (0.02 sec)


-- 添加多条数据
mysql> insert into test2 (name, age, sex) values ("小明",  17, "男"), ("小白", 18, "女");
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

-- 查看表数据
mysql> select * from test2;
+----+------+------+------+
| id | name | age  | sex  |
+----+------+------+------+
|  1 | 小明 |   17 | 男   |
|  2 | 小白 |   18 | 女   |
+----+------+------+------+
2 rows in set (0.00 sec)

-- 删除sex字段
mysql> alter table test2 drop sex;
Query OK, 0 rows affected (0.07 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看数据
mysql> select * from test2;
+----+------+------+
| id | name | age  |
+----+------+------+
|  1 | 小明 |   17 |
|  2 | 小白 |   18 |
+----+------+------+
2 rows in set (0.00 sec)
```



##### 修改字段

```sql
-- 方式1: 不提供的字段名修改(针对原字段直接覆盖性修改)
alter table 表名 
modify  字段名 数据类型 [完整性约束条件…];

-- 方式2: 提供字段名的修改(相当于删除原字段， 新增一个字段进行修改，保留原字段的数据类型)
alter table 表名 
change 旧字段名 新字段名 旧数据类型 [完整性约束条件…];

-- 方式3：提供字段名的修改(相当于删除原字段，不保留源字段的数据类型)
alter table 表名 
change 旧字段名 新字段名 新数据类型 [完整性约束条件…];

-- 方式4：修改字段排列顺序/在增加的时候指定字段位置
ALTER TABLE 表名
CHANGE 字段名  旧字段名 新字段名 新数据类型 [完整性约束条件…]  FIRST;

ALTER TABLE 表名
MODIFY 字段名  数据类型 [完整性约束条件…]  AFTER 字段名;
```

演示操作，SQL语句：

```sql
-- 新建表
create table test3 (
    id int unique, 
    name char(10) not null
);

-- 去掉name字段的 no null约束，改成null
alter table test3 modify name char(10) null;

-- 添加null约束
alter table test3 modify name char(10) not null;

-- 去掉字段id的unique约束
-- 注意：删除唯一索引unique或者普通索引index，都需要使用drop index 字段来删除
alter table test3 drop index id;
-- 添加unique约束
alter table test3 modify id int unique;

-- 给数据添加联合唯一约束
alter table test3 add unique index(id, name);
```

操作效果：

```sql
-- 创建表
mysql> create table test3 (id int unique, name char(10) not null);
Query OK, 0 rows affected (0.03 sec)

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  | UNI | NULL    |       |
| name  | char(10) | NO   |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)

-- 修改name字段的no null 为 null
mysql> alter table test3 modify name char(10) null;
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  | UNI | NULL    |       |
| name  | char(10) | YES  |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)

-- 把name字段的nul 改成 no null
mysql> alter table test3 modify name char(10) not null;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  | UNI | NULL    |       |
| name  | char(10) | NO   |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)

-- 删除id的unique索引
mysql> alter table test3 drop index id;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  |     | NULL    |       |
| name  | char(10) | NO   |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)

-- 给id添加unique 唯一索引
mysql> alter table test3 modify id int unique;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  | UNI | NULL    |       |
| name  | char(10) | NO   |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)


--再次删除id的索引
mysql> alter table test3 drop index id;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 给id 与 name 添加联合唯一的索引（就是在数据表中多行的情况，id+name 的结果不能重现两个一样的）
mysql> alter table test3 add unique index(id, name);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

-- 查看表结构
mysql> desc test3;
+-------+----------+------+-----+---------+-------+
| Field | Type     | Null | Key | Default | Extra |
+-------+----------+------+-----+---------+-------+
| id    | int      | YES  | UNI | NULL    |       |
| name  | char(10) | NO   |     | NULL    |       |
+-------+----------+------+-----+---------+-------+
2 rows in set (0.00 sec)


-- 添加数据
mysql> insert into test3 (id, name ) values (1, "小明");
Query OK, 1 row affected (0.00 sec)

-- 查看数据
mysql> select * from test3;
+------+------+
| id   | name |
+------+------+
|    1 | 小明 |
+------+------+
1 row in set (0.00 sec)


-- 添加数据
mysql> insert into test3 (id, name ) values (2, "小明");
Query OK, 1 row affected (0.00 sec)

-- 查看数据
mysql> select * from test3;
+------+------+
| id   | name |
+------+------+
|    1 | 小明 |
|    2 | 小明 |
+------+------+
2 rows in set (0.00 sec)

-- 添加数据
mysql> insert into test3 (id, name ) values (2, "小红");
Query OK, 1 row affected (0.00 sec)

-- 查看数据
mysql> select * from test3;
+------+------+
| id   | name |
+------+------+
|    1 | 小明 |
|    2 | 小明 |
|    2 | 小红 |
+------+------+
3 rows in set (0.00 sec)

-- 如果出现id=1，name=小明，这种情况则会因为联合唯一索引的原因，会报错。
mysql> insert into test3 (id, name ) values (1, "小明");
ERROR 1062 (23000): Duplicate entry '1-小明' for key 'test3.id_2'
```

在实际开发中，很多时候，开发人员实际上是没有权限去操作数据库或者数据表的，因为开发人员只负责代码的编写与数据的操作，在很多中大型IT企业中，数据库的创建和数据表的设计，实际上很多时候都是技术总监、项目主管、DBA（数据库管理员）来完成的。因此针对数据表的操作，往往都是在开发人员参与项目进来之前就已经完成的了。当然在国内相对来说说，大部分的公司都是中小型IT企业，甚至有草台班子的情况，所以数据库的创建或者数据表的设计，也会有时候落实到开发人员的手上。



### 数据操作

数据操作是开发人员开发中对数据库进行最多最频繁的操作，主要有增加（insert）、查询（select）、修改（update）与删除（delete）四大语句。

>对数据的增删查改操作有时候也被统称为CURD。
>
>Create 增加数据
>
>Update 修改数据
>
>Read  查询数据
>
>Delete 删除数据



#### 添加数据

添加数据时，主键字段和有默认值的字段可以不写值，当然有需要的话，也可以填写上。

添加数据使用`insert into 表名` 语句来添加数据，其中`into`可以省略不写。

```sql
-- 指定字段添加数据（可以打乱顺序）
INSERT INTO 表名 (字段1,字段2,字段3,....) VALUES (字段1的值,字段2的值,字段3的值,....);

-- 也可以省略不写字段名，但是values后面字段值必须和表结构中的字段的排序位置与数量都保持一致（除了主键）。
INSERT INTO 表名 VALUES (字段值1,字段值2,字段值3,....);


-- 一次性添加多条记录(指定要添加数据的字段名，可以打乱顺序)
INSERT INTO 表名 (字段1,字段2,字段3,....) 
VALUES 
(字段值1,字段值2,字段值3,....),
(字段值1,字段值2,字段值3,....),
(字段值1,字段值2,字段值3,....)
...
(字段值1,字段值2,字段值3,....);   -- 末行一定不要忘了结束符号

-- 一次性添加多条记录(不指定要添加数据的字段名，不可以打乱顺序，一定是按照表结构的字段排列顺序一一填写，除了主键ID以外)
INSERT INTO 表名 
VALUES 
(字段值1,字段值2,字段值3,....),
(字段值1,字段值2,字段值3,....),
(字段值1,字段值2,字段值3,....)
...
(字段值1,字段值2,字段值3,....);   -- 末行一定不要忘了结束符号


-- 表数据的添加还支持表复制操作[这实际上是一种叫子查询的写法]
insert into 表名 (字段1, 字段2, 字段3, ...) select (字段1, 字段2, 字段3, ...) from 表名
```

操作演示：

```sql
-- 删除原来的student_info;
drop table if exists student_info;

-- 新建数据表
CREATE TABLE `student_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL,
  `sex` int DEFAULT '1',
  `classes` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
);

-- 新增一条数据[可以选择指定ID]
insert into student_info (id,name,sex,classes,age, description) values (101,'刘德华',1,508,17,'给我一杯忘情水~');

-- 新增一条数据[更多时候，我们是不指定主键ID，让其自动增长，同时，具有默认值的字段也可以不填写，mysql会自动采用默认值替换]
insert into student_info (name, classes, age, description) values ('周华健', 501,17,'来也匆匆去也冲冲~恨不能相逢');

-- 上面的字段，如果是全部字段，那么字段这一块内容可以省略不写。
-- 例如，我们再次添加一个学生，如果省略了字段名，那么填写数据的数据项必须和表结构的字段数量保持一致。id字段，采用null来代替
insert into student_info values (null, '张学友', 1, 508, 17, '爱就像头饿狼~');


-- 添加多名学生
INSERT INTO student_info (name,sex,classes,age,description) 
VALUES 
('周润发',1,508,17,'5个A~'),
('周杰伦',1,508,17,'给我一首歌的时间~');


-- 复制表数据[可以复制来自当前表数据，也可以复制来自其他表的数据，只要字段值符合数据类型即可]
insert into student_info (name,sex,classes,age,description)  select name,sex,classes,age,description from student_info;
```

操作效果：

```sql
-- 删除数据表
mysql> drop table if exists student_info;
Query OK, 0 rows affected (0.02 sec)

-- 新增一张数据表
mysql> CREATE TABLE `student_info` (
    ->   `id` int NOT NULL AUTO_INCREMENT,
    ->   `name` varchar(10) DEFAULT NULL,
    ->   `sex` int DEFAULT '1',
    ->   `classes` int DEFAULT NULL,
    ->   `age` int DEFAULT NULL,
    ->   `description` text,
    ->   PRIMARY KEY (`id`)
    -> );
Query OK, 0 rows affected (0.02 sec)

-- 查看表结构
mysql> desc student_info;
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int         | NO   | PRI | NULL    | auto_increment |
| name        | varchar(10) | YES  |     | NULL    |                |
| sex         | int         | YES  |     | 1       |                |
| classes     | int         | YES  |     | NULL    |                |
| age         | int         | YES  |     | NULL    |                |
| description | text        | YES  |     | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+
6 rows in set (0.00 sec)

-- 添加一条数据（指定所有字段，包括ID字段）
mysql> insert into student_info (id,name,sex,classes,age, description) values (101,'刘德华',1,508,17,'给我一杯忘情水~');
Query OK, 1 row affected (0.01 sec)

-- 查看数据
mysql> select * from student_info;
+-----+--------+------+---------+------+-----------------+
| id  | name   | sex  | classes | age  | description     |
+-----+--------+------+---------+------+-----------------+
| 101 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~ |
+-----+--------+------+---------+------+-----------------+
1 row in set (0.00 sec)

-- 显示建表语句，可以发现当前ID计数器已经到了102了
mysql> show create table student_info;
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table        | Create Table

                      |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| student_info | CREATE TABLE `student_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) DEFAULT NULL,
  `sex` int DEFAULT '1',
  `classes` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+--------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

-- 添加一条数据（指定字段，不指定ID主键与有默认值的字段）
mysql> insert into student_info (name, classes, age, description) values ('周华健', 501,17,'来也匆匆去也冲冲~恨不能相逢');
Query OK, 1 row affected (0.00 sec)

-- 查看数据
mysql> select * from student_info;
+-----+--------+------+---------+------+-----------------------------+
| id  | name   | sex  | classes | age  | description                 |
+-----+--------+------+---------+------+-----------------------------+
| 101 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~             |
| 102 | 周华健 |    1 |     501 |   17 | 来也匆匆去也冲冲~恨不能相逢 |
+-----+--------+------+---------+------+-----------------------------+
2 rows in set (0.00 sec)

--  添加一条数据，不指定字段则必须一个个全部按顺序添加，其中id使用null来代替，作用是保证后续的字段的位置与表结构中的一致。
mysql> insert into student_info values (null, '张学友', 1, 508, 17, '爱就像头饿狼~');
Query OK, 1 row affected (0.00 sec)

-- 查看数据
mysql> select * from student_info;
+-----+--------+------+---------+------+-----------------------------+
| id  | name   | sex  | classes | age  | description                 |
+-----+--------+------+---------+------+-----------------------------+
| 101 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~             |
| 102 | 周华健 |    1 |     501 |   17 | 来也匆匆去也冲冲~恨不能相逢 |
| 103 | 张学友 |    1 |     508 |   17 | 爱就像头饿狼~               |
+-----+--------+------+---------+------+-----------------------------+
3 rows in set (0.00 sec)

-- 一次性添加多条数据
mysql> INSERT INTO student_info (name,sex,classes,age,description)
    -> VALUES
    -> ('周润发',1,508,17,'5个A~'),
    -> ('周杰伦',1,508,17,'给我一首歌的时间~');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

-- 查看数据
mysql> select * from student_info;
+-----+--------+------+---------+------+-----------------------------+
| id  | name   | sex  | classes | age  | description                 |
+-----+--------+------+---------+------+-----------------------------+
| 101 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~             |
| 102 | 周华健 |    1 |     501 |   17 | 来也匆匆去也冲冲~恨不能相逢 |
| 103 | 张学友 |    1 |     508 |   17 | 爱就像头饿狼~               |
| 104 | 周润发 |    1 |     508 |   17 | 5个A~                       |
| 105 | 周杰伦 |    1 |     508 |   17 | 给我一首歌的时间~           |
+-----+--------+------+---------+------+-----------------------------+
5 rows in set (0.00 sec)


-- 复制指定表中的数据并添加到当前表中
mysql> insert into student_info (name,sex,classes,age,description)  select name,sex,classes,age,description from student_info;
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0

-- 复制指定表中的数据并添加到另一张表中
mysql> insert into student_info (name) select name from test3;
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

-- 查看表数据
mysql> select * from student_info;
+-----+--------+------+---------+------+-----------------------------+
| id  | name   | sex  | classes | age  | description                 |
+-----+--------+------+---------+------+-----------------------------+
| 101 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~             |
| 102 | 周华健 |    1 |     501 |   17 | 来也匆匆去也冲冲~恨不能相逢 |
| 103 | 张学友 |    1 |     508 |   17 | 爱就像头饿狼~               |
| 104 | 周润发 |    1 |     508 |   17 | 5个A~                       |
| 105 | 周杰伦 |    1 |     508 |   17 | 给我一首歌的时间~           |
| 106 | 刘德华 |    1 |     508 |   17 | 给我一杯忘情水~             |
| 107 | 周华健 |    1 |     501 |   17 | 来也匆匆去也冲冲~恨不能相逢 |
| 108 | 张学友 |    1 |     508 |   17 | 爱就像头饿狼~               |
| 109 | 周润发 |    1 |     508 |   17 | 5个A~                       |
| 110 | 周杰伦 |    1 |     508 |   17 | 给我一首歌的时间~           |
| 113 | 小明   |    1 |    NULL | NULL | NULL                        |
| 114 | 小明   |    1 |    NULL | NULL | NULL                        |
| 115 | 小红   |    1 |    NULL | NULL | NULL                        |
+-----+--------+------+---------+------+-----------------------------+
13 rows in set (0.00 sec)
```

添加数据的SQL语句使用中，一次性插入多个记录，效率要比多次添加一条记录的性能要更好。因为mysql是基于socket通信的单进程多线程的系统软件，所以每次执行SQL语句的，每次都会打开一个客户端与服务端的通信线程。所以同样的添加10条记录，一次添加一条记录，则会打开10个线程，而一次性添加10个记录，那么只需要打开1个线程。

![img](assets/2022124155532318-1654057010762.png)

#### 界面化工具

使用界面化工具来管理数据库会更加清晰高效。常用的界面化工具：pycharm、navicat、dbeaver、phpstudy+phpmyadmin、syslog、mysql workbench（官方开发）。其中，pycharm的免费版本的数据库管理工具比较难用，navicat属于收费的。其他都是免费。

##### pycharm

使用database数据库管理工具

![image-20220601085453979.png](./assets/image-20220601085453979.png)

创建数据库连接

![image-20220601085549706.png](./assets/image-20220601085549706.png)

![image-20220601122856363](assets/image-20220601122856363.png)

管理数据

![image-20220601091402961.png](./assets/image-20220601091402961.png)

创建数据表

![image-20220601092208741.png](./assets/image-20220601092208741.png)

![image-20220601092303529.png](./assets/image-20220601092303529.png)

![image-20220601092327767.png](./assets/image-20220601092327767.png)

使用database提供的console终端执行SQL语句

![image-20220601095916069.png](./assets/image-20220601095916069.png)



##### navicat

左上角可以创建数据库连接。

![image-20220601091715464.png](./assets/image-20220601091715464.png)

![image-20220601091821182.png](./assets/image-20220601091821182.png)

创建数据表

![image-20220601092611774.png](./assets/image-20220601092611774.png)

![image-20220601092640013.png](./assets/image-20220601092640013.png)

![image-20220601092651780.png](./assets/image-20220601092651780.png)

![image-20220601092706026.png](./assets/image-20220601092706026.png)

如果要创建主键以外的其他索引，则操作如下。

![image-20220601092749316.png](./assets/image-20220601092749316.png)

完成了字段设置操作以后，点击保存，设置表名即可。

![image-20220601092825701.png](./assets/image-20220601092825701.png)



#### 导入csv数据到数据库中

点选数据库连接，选择Import Data from files...

![image-20220601101205225.png](./assets/image-20220601101205225.png)

在弹出的新窗口中选择csv文件所在路径。

![image-20220601101246753.png](./assets/image-20220601101246753.png)

设置导入数据选项。因为我们使用的是windows，所以一般在windows下生成的csv数据都是gbk编码的。

![image-20220601101408577.png](./assets/image-20220601101408577.png)

完成以后的效果如下：

![image-20220601101706211.png](./assets/image-20220601101706211.png)



#### 查询数据

查询操作是开发中四大操作中最常用（100个数据操作，其中可能存在90个操作是查询数据），也是最复杂的操作，复杂的原因是因为查询的过程中，需要通过不同的条件来查询，有时候查询会涉及到1张表，有时候多张表。

##### 全列查询

在生产环境中，谨慎使用上述语句，因为返回的数据可能超大的。如果数据很大的话，就可能把服务器的网络带宽吃满，从而导致服务器无法正常工作。所以全列查询仅用于测试与学习。

```sql
select * from 表名;
```

操作：

```sql
-- 查找学生表中所有学生的所有信息
SELET * FROM student;
```



##### 指定列查询

指定列的顺序不需要按照定义表时的顺序查询，在查询SQL语句中，除了from关键字以外，其他关键字后面跟着的字段名，通常可以当做变量名看待。

```sql
-- 查询指定单个字段
select 字段 from 表名;

-- 查询指定多个字段
select 字段1,字段2,... from 表名;
```

操作：

```sql
-- 查找学生表的姓名跟年龄
SELECT name,age FROM student;


--查找课程表中的id,课程名称和教室编号
select id, cource,address from course;
```



##### 表达式查询

SQL语句的关键字除了from等少部分关键以外，大部分关键字后面通常都可以跟着1个或多个表达式，MySQL中的表达式与Python中的表达式类似，可以是一个常量数值，也可以一个是字段名，也可以是基于运算符的表达式或基于函数调用的表达式。

```sql
-- 单个表达式
select 表达式 from 表名;
-- select 字段名 from 表名;
-- select 字段名+10 from 表名;         -- 注意：此处的字段名的数据类型必须支持+号运算。
-- select 函数名(字段名) from 表名;    -- 注意：此处的函数必须是MySQl内置的函数或者开发者基于MySQl语法声明的自定义函数

-- 多个表达式
select 表达式1,表达式2... from 表名;
```

操作：

```sql
select 1, name, age, 2022-age from student;  -- 查询学生年龄
select name, if(sex=1, '男', '女') from student;
-- if在mysql中既是一个语句关键字，也是一个函数，参数1：表达式，参数2：表示结果为True的值内容，参数3：表示结果为False的值内容，
```

![image-20220601102443600.png](./assets/image-20220601102443600.png)



##### 指定别名

SQL语句中提供了`as`关键字，可以给表达式、表名、字段名设置别名，在查看结果中表达式的字段名会被替换成别名。

```sql
-- 单个表达式
select 表达式 as 别名 from 表名  as 别名;

-- 多个表达式
select 表达式1 as 别名, 表达式2  as 别名 ... from 表名  as 别名;
```

操作：

```sql
select 1, name, age, 2022-age as born from student;
select name, if(sex=1, '男', '女') as sex, description as des from student;
```



##### 去重查询

使用关键字 `distinct`可以把某列在不同行上相同的值的记录给去重。`distinct`必须写在所有字段名（字段列）或表达式前面。

```sql
-- 查询指定单个字段
select distinct 字段 from 表名;

-- 查询指定多个字段
select distinct 字段1, 字段2,... from 表名;  -- 反正distinct必须跟在select后面，否则报错。而且只能出现一个distinct
```

操作：

```sql
-- 查询当前所有学生的年龄值
select distinct age from student;
```

效果：

![image-20220601103141531.png](./assets/image-20220601103141531.png)



##### 结果排序

如果我们的SQL查询语句没有加上 `order by`，此时查询出来的结果顺序是未定的（MySQl数据库中并不会按人类的想法进行排序）。

> 可以在查询语句的表名后面加上 order by 要排序的列名/表达式 [asc | desc] 来进行排序
>
> - `asc`：表示升序（由小到大），不加具体要排序的方式，默认是 asc
> - `desc`：表示降序（由大到小），是 `descending `的缩写
>
> 排序过程中，是字符编码的位置来排序的。

```sql
-- 单列排序
select 字段 from 表名 order by 字段 desc;

select 字段1, 字段2.... from 表名 order by 字段名 asc | desc;

-- 多列排序
select 字段1, 字段2.... from 表名 order by 字段1 asc | desc, 字段2 asc | desc ....;
```

操作：

```sql
-- 结果排序
-- 单个字段排序
select * from student order by age desc;

-- 多个字段排序
select * from student order by classes asc, age asc;  -- 每一个班最小的都在第一个位置。

select * from student order by classes asc, age desc;  -- 每一个班最大的都在第一个位置。
```



##### 结果限制

因为服务器的内存是有限的，而我们在查询一些大量数据的表时，如果一次性全部把数据读取出来，这些数据放在内存中有可能导致服务器的内存不足，严重的话还会导致程序崩溃，因此 往往我们不想一次取出所有的数据，可以对查询出的结果使用`limit`进行数量限制。limit 主要用于在项目开发中的分页功能实现。

limit有三种使用方式：

```sql
-- 方式1：limit后面跟着 一个参数  表示限制结果的数量
select 字段列表 from 表名 limit 结果数量;

-- 方式2： limit后面跟诊 两个参数，第一个参数表示取数据的开始下标[在表中下标从0开始]，第二个参数表示限制结果的数量。
select 字段列表 from 表名 limit 开始下标, 结果数量;

--方式3：也可以通过offset指定显示结果的开始下标
select 字段列表 from 表名 limit 结果数量 offset 开始下标;
```

操作：

```sql
-- 结果限制
SELECT * FROM student LIMIT 3;   -- 从下标=0开始查询3条数据，相当远 limit 0,3
select * from student limit 3,3; -- 从下标=3开始查询3条数据
select * from student limit 6,3; -- 从下标=6开始查询3条数据

select * from student limit 3 offset 0;  -- 从下标=0开始查询3条数据，相当远 limit 0,3
select * from student limit 3 offset 3;  -- 从下标=3开始查询3条数据
select * from student limit 3 offset 6;  -- 从下标=6开始查询3条数据
```

```sql
-- 结合排序就可以实现基本的查询
-- 成绩最好的5个学生
select sid from student_course order by achievement desc limit 5;

-- 查询年龄最大的10个学生[0-9]
select id, name,age from student order by age desc limit 0,10;

-- 从所有学生中，查询年级最大的下标从10-19的学生出来。[10-19]
select id,name,age from student order by age desc limit 10,10;
```



##### 条件查询

条件查询需要使用条件语句，而条件语句适用很广，我们上面所学的几种查询语句的后面都可以使用，除此之外，后面所学的 `update`、`delete ` 等语句也可以使用条件语句。条件语句是通过 `where 条件表达式`的形式，去进行数据筛选，相当于遍历数据表，针对每一个记录带入到条件中，将符合条件的记录保留下来，不符合的则淘汰。

```sql
select 字段 from 表名 where 条件表达式;
```

操作：

```sql
-- 查询id为13的学生
select * from student where id=13;

-- 查询名为“吴杰”的学生
select * from student where name = '吴杰';

-- 多条件查询，查出301班的女生
select * from student where classes = 301 and sex=2;

-- 查询年龄最大的男生？
select * from student where sex=1 order by age desc limit 1;

-- 查询301班年龄最小的男生？
select * from student where classes=301 and sex = 1 order by age limit 1;

 -- 以下条件等于不写条件，因为1相当于Ture
select * from student where 1;
select * from student where id = 3 or 1;
```

> MySQL针对一条SQL查询语句的执行，内部会使用查询优化器使用“选取-投影-连接”策略进行查询。例如 `SELECT id, name FROM student WHERE sex = "女";`中，SELECT查询先根据WHERE条件子句在数据表中选取符合条件，而不是将表全部查询出来以后再进行 sex 过滤。SELECT 查询先根据 id 和 name 进行属性投影，而不是将属性全部取出以后再进行过滤，将这两个查询条件连接起来生成最终查询结果。

##### 运算符

MySQL中提供的运算符主要有：算术运算符、比较运算符、逻辑运算符与位运算符等。其中，常用的运算符有算术运算符、比较运算符、逻辑运算符。

###### 算术运算符

| 运算符   | 描述 |
| :------- | :--- |
| +        | 加法 |
| -        | 减法 |
| *        | 乘法 |
| / 或 DIV | 除法 |
| % 或 MOD | 取余 |

操作：

```sql
select 1, name, age, 2022-age as born from student;

-- 在成绩中查询中所有学生被扣的分数
select sid, cid, achievement, 100-achievement from student_course;

-- id为偶数的学生，在mysql中判断两边的值是否相等，使用一个=来完成.
select id,name from student where id % 2 = 0;
```



###### 比较运算符

比较结果为真，则返回 1，为假则返回 0，比较结果不确定则返回 NULL。

| 符号            | 描述                                                         |
| :-------------- | :----------------------------------------------------------- |
| =               | 等于                                                         |
| <>, !=          | 不等于                                                       |
| >               | 大于                                                         |
| <               | 小于                                                         |
| <=              | 小于等于                                                     |
| >=              | 大于等于                                                     |
| BETWEEN         | 叫范围运算符，在两值之间，相当于    >=min &&<=max            |
| NOT BETWEEN     | 不在两值之间                                                 |
| IN              | 叫成员运算符，判断字段值是否在集合中                         |
| NOT IN          | 判断字段值是否不在集合中                                     |
| <=>             | 严格比较两个NULL值是否相等，两个操作码均为NULL时，其所得值为1；而当一个操作码为NULL时，其所得值为0 |
| LIKE            | 模糊匹配                                                     |
| REGEXP 或 RLIKE | 正则式匹配                                                   |
| IS NULL         | 为空                                                         |
| IS NOT NULL     | 不为空                                                       |

```sql
-- 运算符
select 1, name, age, 2022-age as born from student;

-- 在成绩中查询中所有学生被扣的分数
select sid, cid, achievement, 100-achievement from student_course;

-- id为偶数的学生
select id,name from student where id % 2 = 0;

-- 比较运算符
-- 查询出所有年龄大于20岁的学生
select id, name, age from student where age > 20;

-- 查询出所有年龄大于20岁的女生
select id, name, age from student where age > 20 and sex=2;

-- 查询出除了301班以外的其他学生信息
select id, name, classes from student where classes != 301;

-- 范围比较查询，也叫范围查询
-- BETWEEN ... AND 查询出班级编号在301-305之间的学生
select id,name,classes from student where classes >=301 and classes <= 305;
select id,name,classes from student where classes between 301 and 305; -- 等价于上面的语句

-- NOT BETWEEN ... AND
-- 查出年齡段不在20-22之间的学生
select id,name,age from student where age < 20 or age > 22;
select id,name,age from student where age not between 20 and 22; -- 等价于上面的语句

-- IN 成员查询
-- 查询ID为1, 11, 21, 31, 41,的学生信息
select * from student where id = 1 or id = 11 or id = 21 or id = 31 or id = 41;
select * from student where id in (1, 11, 21, 31, 41); -- 等价于上面的语句

-- NOT IN 非成员查询
-- 查询出301，401，501以外的其他班级学生信息
select * from student where classes != 301 and classes != 401 and classes != 501;
select * from student where classes not in (301, 401, 501); -- 等价于上面的语句

-- 飞船运算符[主要是识别null]
-- 查询没有填写个性签名的学生信息
select * from student where description <=> null;

-- is null 与 is not null 判断值是否为空或不为空
select * from student where description is null;
select * from student where description is not null;

-- LIKE 模糊查询
-- 找出姓李的学生
select * from student where name like '李%';

-- 找出名字格式：李x的学生
select * from student where name like '李_';
-- 找出名字格式：李xx的学生
select * from student where name like '李__';

-- 找出名字是4个字的学生
select * from student where name like '____';

-- 名字包含"白"字的学生
select * from student where name like '%白%';

-- 名字以"杰"结尾的
select * from student where name like '%杰';

-- REGEXP 正则匹配
-- 找出个性签名子里面包含英文的
select * from student where student.description regexp '[a-zA-Z]+';
```



###### 逻辑运算符

用于组合判断多个子条件形成一个整体的表达式，如果表达式是真，结果返回 1。如果表达式是假，结果返回 0。

| 运算符写法1 | 运算符号写法2 | 作用                                            |
| ----------- | :------------ | :---------------------------------------------- |
| !           | NOT           | 逻辑非，并列，如果组合的条件都是TRUE,返回TRUE   |
| &&          | AND           | 逻辑与，或者，如果组合的条件其一是TRUE,返回TRUE |
| \|\|        | OR            | 逻辑或，取反，如果条件是FALSE,返回TRUE          |

操作：

```sql
-- 逻辑运算符
-- 查询年龄大于20岁小于22岁的学生
select  * from student where age > 20 and age < 22;

-- 查询年龄小于20岁或者大于22岁的学生
select  * from student where age < 20 or age > 22;


-- 查询年龄小于18岁 或者性别是女的学生
select * from student where age < 18 or sex = 2;

-- 查询年龄在18-22之间的女生信息(班级、姓名、年龄和性别)
select * from student where age >= 18 and age <= 22 and sex = 2;
select * from student where age between 18 and 22 and sex = 2;

-- 查询309班的所有男生信息(姓名、年龄、个性签名)
select * from student where classes = 309 and sex = 1;

-- 查询306班、305班、304班的男生信息(姓名、年龄、个性签名)
select  * from student where (classes = 304 or classes = 305 or classes = 306) and sex = 1;
select  * from student where classes in (304, 305, 306) and sex = 1;

-- 另一种写法的逻辑运算符
select  * from student where (classes = 304 || classes = 305 || classes = 306) && sex = 1;
select  * from student where classes in (304, 305, 306) && sex = 1;
```



###### 优先级

- 优先级由高到低的顺序为：小括号 > not > 算术运算符 > 比较运算符 > and > or
- 使用过程中， 如果不清晰运算符之间的优先级，可以使用小括号`( )`提升优先级。



##### 聚合查询

聚合的意思是把多个数据放在一起计算，最终得到一个结果。聚合运算都是写在select关键字后面。

| 聚合函数 | 说明                                                |
| -------- | --------------------------------------------------- |
| count    | 返回查询到的数据的行的**数量**                      |
| sum      | 返回查询到的数据的值的**总和**，不是数字没有意义    |
| avg      | 返回查询到的数据的值的 **平均值**，不是数字没有意义 |
| max      | 返回查询到的数据的值的 **最大值**，不是数字没有意义 |
| min      | 返回查询到的数据的值的 **最小值**，不是数字没有意义 |

```sql
SELECT 聚合函数("字段") FROM 表名 WHERE 条件;
SELECT 聚合函数("字段"),其他字段列表 FROM 表名 WHERE 条件;
```

操作：

```sql
-- 查询305班所有的学生数量
select count(1) from student where classes=305;
select count(id) as c from student where classes=305;

-- 所有学生的最小年龄
SELECT MIN(age) FROM student;
-- 所有学生的最大年龄
SELECT max(age) FROM student;

-- 查询302班中所有学生的平均年龄。
select AVG(age) from student where classes=302;

-- 查询305、304、302、301的男生平均年龄
select avg(age) from student where classes in (301, 302, 304, 305) and sex =1;
```



##### 分组查询

GROUP BY子句， 可以对表的查询结果中的指定字段进行分组，常常与聚合函数一起使用。格式：`GROUP BY 字段名`语句不能写在`where 条件表达式`之前。

```sql
-- 方式1：按单个字段的不同行的值进行分组
group by 字段

-- 方式2：按多个字段的值的组合进行分组
group by 字段1, 字段2...


-- 不管是单个字段或多个字段分组，实际上都是在数据表中查看出现的多少个不同的字段值或字段值的组合，那么查询结果就会有多少个组。
```

操作：

```sql
-- 查询student表中有男女学生的数量分别是多少？
select if(sex=1,'男', '女') as sex, count(id) as total from student group by sex;

-- 查询学生表中各个年龄段的学生数量
select age, count(id) as total from student group by age;

-- 查询各个班级的人数各是多少
select classes, count(id) from student group by classes order by classes;

-- 多个分组
-- 计算每一个班中男生女生的数量
select classes, sex, count(id) from student group by classes, sex order by classes;
```



##### 结果过滤

where条件语句的作用是针对当前数据表中的原始数据（聚合前的数据）进行筛选，而如果我们希望对聚合后的数据进行筛选，则需要使用`having`关键字才可以，`having`只能跟在`group by `之后使用，也叫分组结果过滤。

```sql
group by 字段 having 条件表达式;
```

操作，查询301班级大于班上平均成绩的学生成绩信息(name，平均分，班级)。

```sql
-- 获取人数超过5个人的班级
select classes, count(id) as c from student group by classes having c >= 5;
```



##### 连表查询

在前面的学习中，我们对数据查询操作全部都基于单张数据表进行操作的，但是在工作中，因为数据的存储需求不同或者用途不同，有时候并不能一张表把所有的数据都保存起来，因此一个真正项目，一般都是一个或多个数据库组成，而一个数据库下往往也会存在多张数据表。50张表以下基本都是小项目，200张表以下的基本都是属于中性项目，200张以上的基本就是大型项目。

当然，我们对于数据的查询操作，有时候单纯依靠对一张表进行查询，得到的数据可能并不完整，此时我们就需要采用连表查询了，也叫关联查询。主要是依靠关系型数据库中表与表之间在设计时存在的内在关联关系来进行联合查询的。

mysql中针对连表的方式有3种：**左连（left join）**、**内连（inner join）**与 右连（right join），在一些其他的重量级数据库管理系统中，如Oracle，实际上还支持外连（outer join）。

| 连表方式 | 描述                                          | 举例 |
| -------- | --------------------------------------------- | ---- |
| 左连     | `from 主表 left join 从表 on 连表条件表达式`  |      |
| 内连     | `from 主表 inner join 从表 on 连表条件表达式` |      |
| 右连     | `from 主表 right join 从表 on 连表条件表达式` |      |

![image-20220601154717382](assets/image-20220601154717382.png)![image-20220601153841702](assets/image-20220601153841702.png)![image-20220601153953223](assets/image-20220601153953223.png)

在开发中，一般连表的前提时两张表或多张表之间存在字段的值是有映射关联的，而且一般不建议关联查询的表数量太多，建议在7张以内，太多的数据表进行关连查询，容易导致字段名重复引起冲突，此时如果冲突需要使用`as` 给字段起别名来避免。格式：

```sql
-- 2张表进行左连查询
select 字段列表 from 主表名 left join 从表名 on 主表名.主键名 = 从表名.外键名
-- 2张表进行右连查询
select 字段列表 from 主表名 right join 从表名 on 主表名.主键名 = 从表名.外键名
-- 2张表进行内连查询
select 字段列表 from 从表名 inner join 从表名 on 主表名.主键名 = 从表名.外键名

-- 3张表以上，连表条件表达式，只要写出来的任意一张表与当前表有关联，都可以参与连表操作，并非一定要主表的主键名
-- 下面的left join 仅仅是举例，多张表的连表查询，可以是left join，也可以right join，或者inter join
select 字段列表 from 主表名 
left join 从表名1 on 任意表.主键名 = 从表名1.外键名
left join 从表名2 on 任意表.主键名 = 从表名2.外键名 -- 此处的任意表可以是 主表名，也可以是从表名1或者从表名n
... 
left join 从表名n on 任意表.主键名 = 从表名n.外键名
```

操作：

```sql
-- 查询学生id为1的用户，成绩信息
select * from student
left join student_course on student.id = student_course.sid
where id = 1;


-- 关联三张表
select student.id, name, cid, achievement, cource from student
left join student_course on student.id = student_course.sid
left join course on student_course.cid = course.id
where student.id = 1;


-- 关联四张表
select student.id, name, cid, achievement, cource, lecturer.lecturer from student
left join student_course on student.id = student_course.sid
left join course on course.id = student_course.cid
left join lecturer on lecturer.id = course.lecturer
where student.id = 1;
```



##### 查询语句的完整格式

```sql
select [distinct] 字段1 as A,字段2 as B....
from 表名1 as 表别名2, 表名2 as 表别名2
left join 从表1 on 表名.主键=从表1.外键
left join ....
where ....
group by ... having ...
order by ...
limit start,count
```

> - 执行顺序为：
>   - from 表名[包括连表]
>   - where ....
>   - group by ...
>   - select distinct *
>   - having ...
>   - order by ...
>   - limit start,count
> - 实际使用中，只是语句中某些部分的组合，而不是全部

from后面实际上可以跟着多个表名。

```sql
select * from student, course; -- 笛卡尔积的组合显示方式
select * from student, course where student.id < 3 and course.id <5; -- 笛卡尔积的组合显示方式

A表   B表
1       A
2       B
------------------------------------
最终显示结果：笛卡尔积
1   A
1   B
2   A
2   B
```



#### 更新数据

更新操作会对数据造成不可逆的操作，所以更新数据时一定要注意添加`where`条件子句。如果没有条件或条件的判断结果一直是True，则整个表所有的记录都会被更新。

```sql
update 表名 set 字段1=字段值1,字段2=字段值2 where 条件表达式;
```

演示：

```sql
-- 修改学生的年龄
UPDATE student set age=18 where name='刘福荣';

-- 修改学生的名字与年龄
UPDATE student set name="吴小杰", age=20 where id = 65;
```



#### 删除数据

删除操作也会对数据造成不可逆的操作，所以删除数据时一定要注意添加where条件子句。如果没有条件或条件的判断结果一直是True，则整个表所有的记录都会被删除。

```sql
DELETE FROM 表名 WHERE 条件表达式;
```

演示：

```sql
-- 删除信息
DELETE FROM student WHERE id=104;

-- 可以删除一条，也可以删除多条
delete from student_1 where id < 10;
```



### 数据备份与恢复

#### 备份数据

备份数据就是把数据库中的数据保存到指定格式文件中。公司中为了保证数据安全，往往都会进行周期性的数据备份。

在cmd终端下运行mysqldump命令可以完成数据备份（注意：不需要进入MySQL的交互终端）：

```sql
mysqldump –uroot –p 数据库名 > python.sql;

-- 按提示输入mysql的密码
```

#### 数据恢复

- 连接mysql，创建新的数据库
- 退出连接，执行如下命令

```sql
-- 方式1：不登陆进入mysql交互终端的情况下导入数据
mysql -uroot –p 新数据库名 < python.sql
-- 根据提示输入mysql密码


-- 方式2：登陆进入mysql交互终端的情况下导入数据
mysql -uroot -p
-- 根据提示输入mysql密码

use 数据库名

-- source SQL文件绝对路径[windows下的反斜杠路径要改成正斜杠]
source /student_system.sql
```



## 进阶操作

### 架构体系

作为开发人员，在日常开发过程中我们需要经常和MySQL数据库打交道。如果公司有DBA（数据库管理员）还稍微好点，但如果没有DBA的话，我们就很有必要了解下MySQL的整个架构体系了。因为开发中我们如果不了解一条SQL是怎么查询的，那可想而知我们写出来的SQL语句肯定是有可能存在很多问题的，而面试过程中关于数据库的问答是必然出现的，因此于情于理，我们就有必要学习MySQL的架构体系了。MySQL是一个单进程多线程的数据库管理系统软件，分为四层架构体系采用解耦式的方式，使得MySQL的运作及其轻便高效。如下图就是MySQL的整体架构图：

![img](assets/img2020.cnblogs-1654119567533.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto)

从上面的架构图，我们可以看出MySQL的架构自上向下大致可以分为连接层、服务层、引擎层和文件层四大部分。对外暴露的是连接层，连接层调用SQL查询接口，交给服务层。

注意：MySQL也有三层逻辑架构的说法，分别是网络连接层（连接器+连接池），核心服务层，存储引擎层（引擎层与文件层合并层一层）。

#### 连接层

连接层位于整个MySQL体系架构的最上层，主要担任客户端连接器的角色。提供与MySQL服务器建立连接的能力，几乎支持所有主流的服务端语言，例如：Java、C、C++、Python、PHP、Go等，各语言都是通过各自的API接口与MySQL的连接层建立连接。连接层包括通信协议、线程处理、用户名密码认证等。



#### 服务层

服务层是整个数据库服务器的核心，在 MySQL数据库系统处理底层数据之前的所有工作都是在这一层完成的，包括权限判断，SQL接口，解析器，查询优化器(自动优化SQL以匹配索引)， 缓存查询的处理以及部分内置函数执行(如日期,时间,数学运算,加密)等等。往下一层的各个存储引擎提供的功能都集中在这一层操作，如存储过程，触发器，视图等。

| 名称                                                  | 说明                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| 系统管理和控制工具（Management Services & Utilities） | 提供数据库系统的管理和控制功能，例如对数据库中的数据进行备份和恢复，<br>保证整个数据库的安全性，提供安全管理，对整个数据库的集群进行协调和管理等。 |
| SQL接口（SQL Interface）                              | 用来接收客户端发送的SQL命令，并将SQL命令发送到其他部分，返回用户需要查询的结果。<br>例如 SELECT、FROM 就是调用 SQL 接口。 |
| 解析器（Parser）                                      | 也叫解析树，在SQL命令传递到解析器的时候会被解析器验证和解析成一棵“解析树”，<br>然后根据MySQL中的一些语法规则对“解析树”做进一步的语法验证与识别数据结构，确认SQL命令是否合法。 |
| 查询优化器（Optimizer）                               | SQL 语句在真正的查询操作之前会使用查询优化器对SQL查询语句进行优化，<br>同时验证用户是否有权限进行查询，缓存中是否有可用的最新数据，查询优化器使用“选取-投影-连接”策略进行查询。<br>  例如 `SELECT id, name FROM student WHERE sex = "女";`中，<br>SELECT查询先根据WHERE子句进行选取，而不是将表全部查询出来以后再进行 sex 过滤。<br>SELECT 查询先根据 id 和 name 进行属性投影，而不是将属性全部取出以后再进行过滤，<br>将这两个查询条件连接起来生成最终查询结果。 |
| 缓存（Caches）                                        | 如果查询缓存有命中的查询结果，查询语句就可以直接去查询缓存中取数据。<br>这个缓存机制是由一系列小缓存组成的，比如表缓存、记录缓存、key 缓存、权限缓存等。<br>在实际开发中，我们一般不适用缓存，所以在mysql8.0以后，实际上这个部分已经逐步被移除了。当然，即便在低版本下，我们也是关闭缓存的。 |

#### 引擎层

引擎层主要提供了各种存储引擎（Storage Engine），存储引擎的主要作用是接收上层传下来的指令，负责数据的写入和读取，与底层的表文件进行交互，不同的存储引擎保存的数据格式不一样，使用场景也不一样。MySQL中的存储引擎是插件式的，服务器中的查询执行引擎通过相关的接口与存储引擎进行通信，同时接口屏蔽了不同存储引擎之间的差异。

因为在关系数据库中，数据的存储是以表的形式存储的，所以存储引擎也可以称为**表类型**（即存储和操作表的类型，除了mysql以外，很多其他数据库不叫存储引擎，而是叫表类型）。

通过以下SQL语句，可以查看MySQL中支持的存储引擎：

```sql
show engines;
```

MySQL中最常用的存储引擎就是InnoDB与MyISAM。

因为Memcached、Redis等内存缓存系统的出现，所以Momory存储引擎现今使用非常少了，MySQL5.5版本之后开始采用InnoDB为默认存储引擎，之前版本默认的存储引擎为MyISAM。



##### InnoDB

InnoDB存储引擎，是MySQL当前版本（5.5以后）的默认存储引擎，具有支持事务处理（transaction），外键约束（foreign key），行锁设计，崩溃恢复历史回滚 等特点，是mysql最重要和使用最广泛的存储引擎。innoDB保存表的数据，索引与表结构都在一个ibd文件中。

###### 事务处理

事务可以让多条写操作（添加、删除、修改）的SQL语句以一个整体的方式在mysql内部执行，保证多条SQL语句要么一起执行成功，要么一起执行失败！

![image-20220602120547032](assets/image-20220602120547032.png)

###### 外键约束

外键约束，也叫主外键关联，指代mysql中提供一个监控数据表与表之间进行级联绑定的索引。

![image-20220602121549125](assets/image-20220602121549125.png)

上面的表中，如果我们设置user_id作为id的外键，则可以设置让user表中的小明同学被删除以后，address中的对应数据会被mysql自动级联删除掉。当然，这种外键工作中，我们一般不适用mysql提供的，而是在编程语言中，进行外键的维护（虚拟外键，逻辑外观）。

###### 行锁设计

所谓的锁，就是基于锁的机制，对数据表中的数据进行锁定，保证数据在写入(添加，更新，删除)的时候，不会因为并发导致出现一致性的问题。InnoDB中提供的锁有表级锁，行级锁。

表级锁，指在同一时间内，客户端连接修改一个表数据时，会把当前表进行锁定，其他客户端连接访问操作当前表时会阻塞等待。

行级锁，指在同一时间内，客户端连接修改一个表数据时，会把当前要修改的数据所在那一行数据进行锁定，其他客户端的其他客户端连接访问操作当前表的其他行数据畅通无阻，但修改同一行数据时会阻塞等待。

不管是表级锁还是行级锁，都是针对SQL语句中的写入命令生效，读取数据没有影响。



###### 崩溃恢复

innoDB存储引擎在数据操作时，针对所执行的所有SQL语句，都会记录到一个redo日志文件中。当mysql因为意外而出现系统奔溃或宕机了，那么在mysql重启以后，mysql内部会自动通过redo日志对比丢失的数据，并进行恢复（历史回滚）。



##### MyISAM

MyISAM存储引擎，是MySQL早期版本（5.5以前）的默认存储引擎，拥有较高的插入、查询速度，表锁设计，支持全文索引的特点，但不支持事务处理和外键约束，也不支持崩溃恢复。MyISAM用3个文件来存储数据，frm文件存储表的定义、MYD文件存放数据、MYI文件存放索引。mysql8.0以后不再使用frm保存数据表的定义，而是叫sdi。



InnoDB与MyISAM的区别：

1. 锁设计，InnoDB支持表级锁（(table-level locking)）与行级锁（row-level locking），而myISAM只支持表级锁。用户在操作myISAM类型表时，select，update，delete，insert等语句都会给表自动加锁，导致其他客户端连接的数据操作都会被阻塞，因此并发访问受限。当然，InnoDB虽然提供了行级锁，但也只是在使用了索引时是有效的，如果没使用索引也会锁全表，行锁大幅度提高了多用户并发操作的性能。同时InnoDB还支持MVCC（Multi-Version Concurrency Control，多版本并发控制）机制，只需要很小的开销，就可以实现非锁定读，从而大大提高数据库系统的并发性能（MVCC 可以看作是行级锁的一个升级版本）。

   

2. 事务安全，InnoDB支持完整的事务安全机制（ACID），具有提交(commit)和回滚(rollback)事务的能力，所以在写入数据时可以有效保证数据的安全性以及一致性。

   ACID：Atomicity(原子性)、Consistency(一致性)、Isolation(隔离性)、Durability(持久性)。后面讲到事务再说。

   

3. 外键约束，MyISAM不支持，而 InnoDB 支持。但是开发中一般不在数据库使用外键，而是在应用层实现逻辑外键或虚拟外键，使用外键会造成级联更新，且级联更新是强阻塞，存在数据库更新风暴的风险；外键使用时也会影响数据库的插入速度。

   因为插入一张表的时候，mysql会自动去检查关联的外键所在表的全部数据是否一致。

   

4. 主键约束，MyISAM允许没有主键的表存在。InnoDB表必须有主键，如果没有设定主键，就会自动生成一个用户不可见的6字节隐藏列作为主键列(对于用户而言，MyISAM与InnoDB都可以创建没有外键的表)。

   

5. 崩溃恢复，MyISAM不支持，而InnoDB支持。使用 InnoDB 的数据库在异常崩溃后，数据库重新启动的时候会保证数据库恢复到崩溃前的状态。这个恢复的过程依赖于 redo log（重做日志）、undo log（回滚日志）、bin log（二进制日志）。



#### 文件层

文件层主要包括MySQL中存储数据的底层文件，与上层的存储引擎进行交互，是文件的物理存储层。其存储的文件主要有：日志文件、数据文件、配置文件、MySQL的进程ID文件pid和socket文件等。

数据文件中主要包括了：db.opt文件、frm文件、MYD文件、MYI文件、ibd文件、ibdata文件、ibdata1文件、ib_logfile0和ib_logfile1文件等。

配置文件用于存在MySQL所有的配置信息，在Unix/Linux系统中配置文件格式为xxxx.cnf，而在Windows系统下则是xxxx.ini。注意：在ubuntu下具体的配置文件路径是**`/etc/mysql/mysql.conf.d/mysqld.cnf`**。

pid文件是存放MySQL运行时的进程号的文件，主要存在于Unix/Linux环境中，文件具体位置在mysqld.cnf或my.ini中通过配置指定。

socket文件和pid文件一样，都是MySQL在Unix/Linux环境中运行才会有的文件。在Unix/Linux环境中，客户端可以直接通过socket来连接MySQL。

##### 日志文件

日志文件主要用于记录程序运行过程中的操作历史，便于对程序的运行过程进行监控与维护。MySQL中的日志主要包括：错误日志（error log）、通用查询日志（general query log）、二进制日志（binary log）、慢查询日志（slow query log）、中继日志等。

> 为了节约性能，有些MySQl的日志功能默认是关闭的，数据库日志的开启有2种方式：
> 临时开启, 通过mysql交互终端临时设置，服务器关机或mysql重启，则日志的配置信息还原。
> 永久开启, 通过mysql的配置文件进行参数设置.windows下的配置文件：mysqi.ini，Linux/Unix系统：mysqld.cnf

###### 错误日志（error log）

主要存储的是MySQL运行过程中产生的错误信息。固定开启的，可以使用下面的SQL语句来查看MySQL中的错误日志位置。

注意：如果MySQL运行过程中，SQL语句相关的错误，并不会在错误日志中出现。

```sql
-- mysql终端下执行
SHOW VARIABLES LIKE 'log_error';
```

![image-20220606091243232](assets/image-20220606091243232.png)

通过Linux系统提供的tail -f 可以监控日志，也可以通过ELBK日志分析系统进行监控。

```sql
tail -f /var/log/mysql/error.log
```



###### 通用查询日志（General query log）

任何执行的sql语句都会写入这个日志中。默认是关闭的，可以通过下面的SQL语句来查看MySQL中的通用查询日期的开启状态与日志存储路径。

```sql
SHOW VARIABLES LIKE '%general%'; -- OFF表示关闭，相当于0
```

![image-20220606091525148](assets/image-20220606091525148.png)

在mysql交互终端下设置临时开启

```sql
set global general_log = 1;  -- 开启日志， -- 1相当于'ON'，表示开启
set global general_log_file = '日志文件的绝对路径';  -- 设置日志路径，一般默认即可，不要更改路径。
```

在mysql配置文件中添加如下配置可以设置永久开启【开发中本地数据库可以开启，但是在线上的生产服务器中不能开启】

```sql
-- bash终端下，sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
general_log = 1
general_log_file = /var/lib/mysql/ubuntu.log

-- :wq 保存退出
```

![image-20220606092116202](assets/image-20220606092116202.png)

重启mysql

```bash
service mysql restart 
```

监控通用查询日志

```bash
sudo tail -f /var/lib/mysql/ubuntu.log
```



###### 二进制日志（binary log）

是 MySQL 最重要的日志，它记录了所有的 `DDL` 和 `DML` 语句（并不会记录查询语句select、show等），**以事件形式记录**，还包含语句所执行的消耗的时间。binlog 的主要目的是**复制和恢复**。默认关闭，但是**`生产环境中务必开启bin-log的`**。启用binlog虽然会使数据库服务器性能降低，但是binlog日志能恢复误删数据，能复制数据的这些用处而言，这点性能的损耗不算什么。

```sql
-- 查看二进制日志的开启情况
show variables like "%log_bin%";
```

在mysql配置文件中添加如下配置可以设置永久开启。临时打开，实际上是没有什么意义的。所以此处不提。

```bash
  # server-id 必须唯一
server-id=1
log-bin=mysql-bin
log-bin-index=mysql-bin.index 
# binglog日志的最大有效期，一般不设置
# binlog_expire_logs_seconds=2592000
```

终端基本操作

```sql
-- 查看所有二进制日志文件
-- show master logs;  
show binary logs;  -- 等价于上面一句

-- 查看mysql中最新的一个二进制日志的存储信息[常用语用于主从配置，集群配置的]
show master status;

-- 查看具体某个二进制日志中的记录内容
show binlog events in 'binlog.000003';  -- binlog.000003 仅仅是举例，具体要通过 show binary logs; 来查看具体二进制日志的文件名。

-- 删除指定日志文件【慎用！慎用！慎用！】
purge master logs to 'binlog.000003';  -- binlog.000003 仅仅是举例，具体要通过 show binary logs; 来查看具体二进制日志的文件名。
```



###### 慢查询日志（slow query log）

记录数据库中运行时长超过指定时间（long_query_time，慢查询时间）的SQL语句，用于数据库优化。默认关闭的。可以通过下面的SQL语句来查看慢查询日志的开启情况。一般建议建议，识别监控整个数据库运作过程中的所有执行比较慢的SQL，往往用于测试 与优化。

```sql
show variables like '%slow_query%';
```

在mysql交互终端下设置临时开启

```sql
set global slow_query_log=1;
set long_query_time=2;
```

在mysql配置文件中添加如下配置可以设置永久开启。

```bash
# bash终端下，sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
slow_query_log=1
slow_query_log_file=/var/lib/mysql/ubuntu-slow.log
long_query_time = 2
```

可以使用慢日志分析工具(mysqldumpslow，默认在mysql安装以后内置了的)来获取慢查询日志，选项如下：

|          |                                                              |                                                              |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 参数     | 说明                                                         | 备注                                                         |
| **`-s`** | 表示按照何种方式排序                                         | c：访问计数 <br>**`l`**：锁定时间（L的小写），被锁的时间 <br/>r：返回记录 <br/>**`t`**：查询时间，mysql执行SQL的时间 <br/>al：平均锁定时间 <br/>ar：平均返回记录数 <br/>at：平均查询时间 |
| **`-t`** | 即 top n，根据排序返回前多少条数据                           |                                                              |
| **`-g`** | 即 grep 关键字，匹配慢查询sql语句中是否包含关键字内容，<br>支持正则匹配模式，不缺分大小写 |                                                              |

操作：

```bash
# mysql终端下可以通过sleep睡眠函数模拟慢查询
select sleep(10);

# 查看所有慢查询SQL语句的记录信息
sudo mysqldumpslow /var/lib/mysql/ubuntu-slow.log

# 得到返回记录数量最多的20个：
sudo mysqldumpslow -s r -t 20 /var/lib/mysql/ubuntu-slow.log

# 得到平均访问次数最多的20条：
sudo mysqldumpslow -s ar -t 20 /var/lib/mysql/ubuntu-slow.log

# 得到平均访问次数最多,并且里面含有 xxx字符的20条
sudo mysqldumpslow -s ar -t 20 -g "xxx" /var/lib/mysql/ubuntu-slow.log
```

> 如果出现错误如：Died at /usr/bin/mysqldumpslow line 162, <> chunk 1.
>
> 在表示要分析的sql慢查询日志太大了，请拆分后再分析。
>
> 拆分的命令为：tail -100000 /var/lib/mysql/ubuntu-slow.log >  /var/lib/mysql/ubuntu-slow.log.1 
>
> 上面一条语句中，表示从/var/lib/mysql/ubuntu-slow.log读取最后10W条慢查询记录，复制到新的文件中 /var/lib/mysql/ubuntu-slow.log.1 



### 数据库设计

数据库设计就是根据业务系统的具体需求，结合我们所选用的DBMS（数据库管理系统），为这个业务系统构造出最优的数据存储模型，并建立数据库中的表结构以及表与表之间的关联关系的过程。数据库设计能有效的对项目中的数据进行存储，并可以高效的对已存储的数据进行访问。好的数据库设计可以减少数据冗余，降低数据维护成本，节约存储空间，并提供高效的访问数据能力。

好的数据库的产生，离不开理论支持，还有实际开发经验。

在实际开发中，一些中大型的IT企业中，往往会存在DBA（数据库管理员），如果存在DBA则数据库设计这块就是DBA去负责的。

#### 范式理论

范式理论（normalization，规范化理论）是在关系型数据库设计过程中，为了消除重复数据减少冗余数据，从而让数据库更好更科学地组织数据，让磁盘空间得到更有效利用的一种规范化设计理论。目前可以查找到的数据库范式有5条，分别是1NF，2NF，3NF，4NF，5NF。范式理论满足高等级的范式的先决条件是满足低等级范式，其中等级最低的是第一范式（1NF），在第一范式的基础上进一步满足更多规范要求的称为第二范式（2NF），其余范式以次类推。一般来说，数据库设计只需满足第三范式(3NF）就行了。范式理论仅仅是指导我们设计好的数据库的一种指导理论，并非语法标准，所以在实际开发中，有时候为了更合理的开发出更优秀的项目，也会存在逆范式（Denormalization）设计。



##### 1NF：不可分割

第一范式（1NF，First Normal Form），是指数据表的每一列都是不可分割的基本数据项，有原子性特点。即数据表中的某个字段列不能有多个成员值。不符合第一范式则不能称为关系数据库。

不满足1NF的表设计：

商品信息表

| 商品信息                         |
| -------------------------------- |
| 大马士革丝滑沐浴露,50,23.90,清怡 |
| 威王洁厕净,100,14.90,威王        |
| 西兰空气清新剂,100,12.90,西兰    |
| 立白洗衣液,120,36.90,立白        |
| 立白洗衣粉,100,29.90,立白        |

满足1NF的表设计：

| 商品名称           | 商品数量 | 商品单价 | 品牌 |
| ------------------ | -------- | -------- | ---- |
| 大马士丝滑革沐浴露 | 50       | 23.90    | 清怡 |
| 威王洁厕净         | 100      | 14.90    | 威王 |
| 西兰空气清新剂     | 100      | 12.90    | 西兰 |
| 立白洗衣液         | 120      | 36.90    | 立白 |
| 立白洗衣粉         | 100      | 29.90    | 立白 |



不满足1NF的表设计：

用户信息表：

| 姓名               | 年龄 | 性别 |
| ------------------ | ---- | ---- |
| 王小明,李白,刘晓宇 | 17   | 男   |
| 周艳,张蔷,江艺     | 17   | 女   |

满足1NF的表设计：

| 姓名   | 年龄 | 性别 |
| ------ | ---- | ---- |
| 王小明 | 17   | 男   |
| 李白   | 17   | 男   |
| 刘晓宇 | 17   | 男   |
| 周艳   | 17   | 女   |
| 张蔷   | 17   | 女   |
| 江艺   | 17   | 女   |



##### 2NF：不可重复

第二范式（2NF，Second Normal Form）是在满足第一范式的基础上提出了进一步的规范要求：确保表中的每个非主键列完全依赖于主键列，不能出现多行重复且与主键不完全依赖的非主键列。所谓完全依赖是指不能存在仅依赖主键列一部分的非主键列（主要针对联合主键而言）。如果存在，那么这个非主键列和主键列的这一部分应该分离出来形成一个新的数据表，新数据表与原数据表之间是一对多的关系。

不满足2NF的表设计：

```sql
create table order (
    goods_id int auto_increment,
    order_number char(32),
    primary key (goods_id, order_number),
)
```



订单表

| 订单编号(联合主键) | 商品ID(联合主键) | 商品名称           | 购买数量 | 商品单价 | 用户ID | 用户名 |
| ------------------ | ---------------- | ------------------ | -------- | -------- | ------ | ------ |
| 20220501001001     | 1                | 大马士革丝滑沐浴露 | 1        | 23.90    | 1      | 王小明 |
| 20220501001001     | 2                | 威王洁厕净         | 1        | 14.90    | 1      | 王小明 |
| 20220501001002     | 1                | 大马士革丝滑沐浴露 | 1        | 23.90    | 2      | 李白   |
| 20220501001002     | 2                | 威王洁厕净         | 1        | 14.90    | 2      | 李白   |
| 20220501001002     | 3                | 西兰空气清新剂     | 5        | 12.90    | 2      | 李白   |

满足2NF的表设计：

订单表

| 订单编号(主键) | 用户ID | 用户名 |
| -------------- | ------ | ------ |
| 20220501001001 | 1      | 王小明 |
| 20220501001002 | 2      | 李白   |

订单项目表

| 记录ID（主键） | 订单ID | 商品ID | 购买数量 |
| -------------- | ------ | ------ | -------- |
| 1              | 1      | 1      | 1        |
| 2              | 1      | 2      | 1        |
| 3              | 2      | 1      | 1        |
| 4              | 2      | 2      | 1        |
| 5              | 2      | 3      | 5        |



##### 3NF：不可冗余

第三范式（3NF，Third Normal Form）是在满足第二范式的基础上进一步提出了更好的要求：确保数据表中的每一列数据都和主键列直接相关，而不能间接相关，即**消除传递依赖，去除冗余字段**。所谓的传递依赖是指非主键列字段不依赖于主键列，而是完全依赖于另一个非主键列。而这些不依赖于主键的字段就是所谓的冗余字段，一般的处理方式就是另建一张新数据表与原数据表进行关联。由此，新数据表与原数据表之间的关系是一对多或多对多的关系。

不符合3NF的表设计：

订单表

| 订单ID（主键） | 订单编号       | 用户ID | 用户名 |
| -------------- | -------------- | ------ | ------ |
| 1              | 20220501001001 | 1      | 王小明 |
| 2              | 20220501001002 | 2      | 李白   |

符合3NF的表设计：

用户表

| 用户ID | 用户名 |
| ------ | ------ |
| 1      | 王小明 |
| 2      | 李白   |

订单表

| 订单ID | 订单编号       | 用户ID |
| ------ | -------------- | ------ |
| 1      | 20220501001001 | 1      |
| 2      | 20220501001002 | 2      |



不符合3NF的表设计

成绩表

| 成绩ID | 课程ID | 课程名 | 老师ID | 分数 | 学生ID | 学生名 |
| ------ | ------ | ------ | ------ | ---- | ------ | ------ |
| 1      | 1      | Python | 1      | 75.0 | 1      | 王小明 |
| 2      | 2      | MySQL  | 2      | 68.5 | 1      | 李白   |
| 3      | 1      | Python | 1      | 80   | 2      | 刘晓宇 |
| 4      | 1      | Python | 1      | 86   | 3      | 刘晓宇 |

符合3NF的表设计

成绩表

| 成绩ID | 课程ID | 学生ID | 分数 |
| ------ | ------ | ------ | ---- |
| 1      | 1      | 1      | 75.0 |
| 2      | 2      | 1      | 68.5 |
| 3      | 1      | 2      | 80   |
| 4      | 1      | 3      | 86   |

课程信息表

| 课程ID | 课程名 | 老师ID |
| ------ | ------ | ------ |
| 1      | Python | 1      |
| 2      | MySQL  | 2      |

同理，学生信息表也是如此

| 学生ID | 姓名   |
| ------ | ------ |
| 1      | 王小明 |
| 2      | 李白   |
| 3      | 刘晓宇 |

练习，基于范式理论，对超市构建一个超市自动化管理系统，超市下面有门店，门店有负责人，地址，门店名，楼层。超市有员工，员工属于不同的部门，一个部门有多个员工，有些员工属于门店的负责人，有些员工属于门店的普通职员。部门有部门的领导人，部门的地址，部门的人员。

```
门店
     id,  负责人(员工id)，地址，门店名，楼层
部门
     id, 领导人(员工id)，地址
员工
     姓名、部门id，门店的id
```



##### 数据表间的关系

数据表之间因为不同的数据库设计理论，表与表之间的会存在多种常见的关联关系：一对一、一对多、多对多。

###### 一对一（1:1）

A表中的1条记录对应着B表中的0~1条记录，而B表中的1条记录也对应着A表中的1条记录，则A表和B表为一对一关系。例如：文章信息表与文章详情表、商品信息表与商品详情表，用户信息表与用户详情表。

文章信息表(A表)

| ID   | 标题 | 字数 | 发布时间            | 阅读量 |
| ---- | ---- | ---- | ------------------- | ------ |
| 1    | 红菊 | 3385 | 2021-12-03 13:30:22 | 30212  |
| 2    | 秦腔 | 1930 | 2022-03-10 22:01:30 | 502202 |
| 3    | 高考 | 1990 | 2022-04-13 18:54:32 | 4016   |

文章详情表(B表)

| ID   | 文章id | 描述                                                         | 内容 |
| ---- | ------ | ------------------------------------------------------------ | ---- |
| 1    | 1      | 秋绽红腮丝蕊黄，盈枝挂露自芬芳。 淡怀脱俗轻扬意，笑对寒风不觉凉.... |      |
| 2    | 2      | 中国的传统戏曲对于Teenagers往往是遭到排斥的，所以我时常被视为异类.... |      |
| 3    | 3      | 10月14日至16日，浙江省进行了高考改革后的第三次学考和选考.... |      |



###### 一对多（1:n）

A表中的1条记录对应着B表中的0~多条记录，而B表中的1条记录只对应着A表中的1条记录，则A表和B表为一对多关系。例如：商品分类表与商品信息表、文章分类表与文章信息表、部门表与职工表、院系与课程、老师与课程等等。

商品分类表(A表)

| ID   | 分类名 |
| ---- | ------ |
| 1    | 手机   |
| 2    | 电脑   |
| 3    | 洗衣机 |

商品信息表(B表)

| ID   | 商品标题        | 分类ID |
| ---- | --------------- | ------ |
| 1    | 华为meta40      | 1      |
| 2    | 华为meta50      | 1      |
| 3    | 华为meta30      | 1      |
| 4    | 海尔Mate1洗衣机 | 3      |



###### 多对多（n:m）

A表中的1条记录对应着B表中的0~多条记录，而B表中的1条记录对应着A表中的0~多条记录，则A表和B表为多对多关系。在多对多关系中，需要创建1张关系表（中间人）来绑定映射两张数据表的关系。例如：学生表与课程表、活动表与商品表、会议表与员工表等。

课程表

| ID   | 课程名 |
| ---- | ------ |
| 1    | Python |
| 2    | Java   |

学生表

| ID   | 姓名   |
| ---- | ------ |
| 1    | 王小明 |
| 2    | 李白   |

成绩表(中间人)

| 成绩ID | 课程ID | 学生ID | 分数 |
| ------ | ------ | ------ | ---- |
| 1      | 1      | 1      | 79.5 |
| 2      | 1      | 2      | 100  |
| 3      | 2      | 2      | 88   |



##### 逆范式：以空间换时间

逆范式（Denormalization）指的是通过增加冗余或重复的数据来提高数据库的读性能，减少运行时带来的查询时间消耗。往往也可以总结为以空间换时间，所谓的空间就是硬盘空间，所谓的时间就是查询时间。因此以空间换时间，就是使用廉价的硬盘空间来换取更快的查询数据速度。

商品分类表

| 分类ID | 分类名   |
| ------ | -------- |
| 1      | 手机     |
| 2      | 日化用品 |

商品信息表

| 商品ID | 商品标题           | 所属分类 |
| ------ | ------------------ | -------- |
| 1      | 大马士革丝滑沐浴露 | 2        |
| 2      | 威王洁厕净         | 2        |
| 3      | 西兰空气清新剂     | 2        |
| 4      | 立白洗衣液         | 2        |
| 5      | 华为P50            | 1        |
| 6      | 华为meta40         | 1        |

逆范式化设计：

商品分类表

| 分类ID | 分类名   | 商品总数 |
| ------ | -------- | -------- |
| 1      | 手机     | 2        |
| 2      | 日化用品 | 4        |

虽然增加了一个字段，但是减少了连表查询，这就是典型的逆范式设计（也就是以空间换时间）。

除了上面的例子以外，类似文章表（点赞总数、收藏总数、阅读总数、评论总数）、商品表（销量，评价）都会存在逆范式的应用。



#### 设计步骤

数据库设计的步骤一般可以分成4个阶段或6个阶段，这里我们只讨论四个阶段的情况：

- 需求分析阶段（数据是什么；数据具有哪些属性；数据与数据之间是否存在关联）
- 逻辑分析阶段（使用E-R图对数据库进行逻辑建模(或抽象建模)，不需要考虑我们所选用的数据库管理系统）
- 物理设计阶段（根据数据自身的特点把逻辑设计转换为物理设计, 结合对应的数据库管理系统的特点，进行数据库设计）
- 维护设计阶段（1.对新的需求进行建表；2.索引优化；3. 架构升级；4.大表拆分）

##### 需求分析阶段

这是数据库设计的第一个阶段，在这个阶段中我们首先需要**熟悉实际业务流程**，以此分析出软件系统中需要存储的数据（实体），分析这些数据的特点（实体具有哪些属性），最后了解数据的生命周期以及数据与数据之间的联系（Relationship），也就是实体（数据表）之间的关联关系。

实体（Entity）就是需要保存到数据库中，主观或客观存在的并且能相互区分的信息主体（信息集合），实际一般都是描述事物或概念的名词，在后续的物理设计阶段，**实体就会转换成数据表**保存到数据库中。例如用户、商品、订单、厂商等。数据库的表名就可以看做一个实体对象。一个数据库是由很多个实体对象构成的，然后它们之间往往存在一定的关联关系和属性，因此，常见实体间的关系也可以归纳为3种：1对1、1对多、多对多。

而属性（Attribute）则是描述实体的特征信息，在后续的物理设计阶段，**属性就会转换成数据列**保存到数据库中。举例子：用户实体拥有属性【id、姓名、年龄、性别、手机号码】、商品实体拥有属性【id、商品名称、商品类型、商品价格、商品图片、商品描述、厂商id】、订单实体拥有属性【id、订单编号、用户id、商品id、下单日期、订单价格】、厂商实体拥有属性【id、名称、地址、联系人、联系电话】。

在需求分析阶段中，我们需要完成的工作就是：

1. 找出所有明面或者隐藏的实体。
2. 分析出实体所包含的属性都有哪些。
3. 实体对实体之间的关系（有的实体是没有关联的，有的实体是存在1对1，1对多，多对多的关联）。

举个栗子，例如我们要做一个商城。那么我们需要根据**需求分析报告、策划原型或UI设计图纸等**进行分析总结，提取要保存到数据库中的实体信息。

实体列表：

```text
商城首页：导航菜单、商品分类、商品信息、用户信息、Banner广告、文章分类、搜索历史等。
商品列表：商品分类等。
购物车页面：订单、支付方式等。
个人中心页面：足迹、积分、红包、退货记录、收藏历史、用户信息、收货地址、修改密码记录等。
```

属性列表：

```text
导航菜单：菜单名，菜单链接，是否显示，序号等
商品分类：分类名称等
商品信息：商品标题，商品价格，商品图片，商品描述，商品属性，是否显示，序号等
用户信息：账户名，登陆口令（哈希值），昵称，头像等
Banner广告：图片路径，广告链接，是否显示，序号等
文章分类：分类名称等
搜索历史：关键字，搜索时间等

产品分类：分类名称等

订单：订单编号，订单标题，订单总价格，订单实付价格，支付方式，支付状态，支付时间等
支付方式：平台名称，平台官网，支付账户，支付应用ID，支付应用秘钥，启用状态等

足迹：用户ID，访问地址，访问时间，信息类型等
积分：积分来源，积分数量，用途，产生时间，有效时间等
红包：红包来源，红包金额，使用状态等
退货记录：订单ID，商品ID，退货状态等
收藏历史：商品ID，用户ID，收藏时间等
收货地址：地址名称，所属省份，所属城市，所属地区，详细地址，收货时间，联系人，联系电话等
修改密码记录：用户ID，修改时间，旧登陆口令（哈希值）等
```

实体间的关系

```bash
不存在关联关系的实体：
    导航菜单
    Banner广告

存在关联关系实体：
    商品分类
        1:n    商品信息
    文章分类
        1:n    文章信息
    用户信息
        1:n    搜索历史
        1:n    收货地址
        1:n    修改密码记录
        1:n    积分
        n:m   红包<红包发放记录>
        n:m   商品<收藏历史, 足迹>
        1:n    订单
                    n:m    商品<订单项目>
                    n:1     支付方式
                    1:n     退货记录
```



##### 逻辑分析阶段

逻辑分析阶段就是基于上一阶段的分析结果使用E0R图对实体、实体的属性与实体间的关系进行逻辑建模。

E-R图也称实体-联系图(Entity Relationship Diagram，也叫实体关系模型)于1976年由陈品山提出用于描述数据概念关系的概念模型，E-R图提供了表示实体、属性和关系的方法。常用的E-R画图工具有：亿图、visio、processon、draw.io、mastergo等。逻辑分析阶段有时候也会构建UML图（统一建模语言）。

E-R图主要有3要素构成，要素与要素之间的从属关系以及关联关系使用**实线**来绑定。

| 名称 | 描述                                                        |
| ---- | ----------------------------------------------------------- |
| 实体 | 使用**矩形**框表示实体。框内就是实体名。                    |
| 属性 | 使用**椭圆形**框表示实体的属性。框内就是属性名              |
| 联系 | 使用**菱形**框表示实体与实体之间的1:1、1:n、n:m的关联关系。 |

![preview](assets/v2-e1800019d2d6a7f7c1e82468f6fc4391_r.jpg)

![image-20220605225001358](assets/image-20220605225001358.png)

作业：把上面的超市练习的题目，使用E-R图自己画一个出来。

![image-20220607145602637](assets/image-20220607145602637.png)

作业：把上面举例的商城例子中的所有实体、属性、联系通过E-R画出来。

![image-20220607151542676](assets/image-20220607151542676.png)



##### 物理设计阶段

就是基于上一阶段的E-R概念模型，将概念模型结构转换成特定DBMS所支持的数据模型的过程。物理模型的构建工具：navicat、workbanch、Powerdesigner等。

![image-20220606010836521](assets/image-20220606010836521.png)

作业：把上面的超市以及商城作业中的E-R图转换成物理模模型。



##### 维护设计阶段

经过了上面几个阶段设计以后，数据库应用系统经过试运行后即可投入正式运行。在数据库系统运行过程中因为时间、业务、数据量不断增长，必须不断地对其进行监控、维护、调整、优化、升级。



### 数据库操作进阶

#### 视图

视图（View）就是从一个或多个表中导出来的表，是一种只保存SQL语句的虚拟存在的表。视图就像一个窗口，通过这个窗口可以看到系统专门提供的数据，这样用户可以不看整个数据库表中的数据，而只关心对自己有用的数据。视图可以使用户的操作更方便，而且可以保障数据库系统的安全性。 注意，视图中的数据是依赖于真实表中的数据。一旦真实表中的数据发生改变，显示在视图中的数据也会发生改变。视图常用于一些权限要求比较多的系统项目中。

视图的优点：

1. 定制用户数据，聚焦特定的数据
2. 简化数据操作
3. 提高数据的安全性
4. 共享所需数据

基本操作格式：

```sql
-- 创建视图
create view 视图表名  as SQL语句;

-- 查看视图
desc 视图表名
show tables
show create table/view 视图表名

-- 视图的数据的读写操作与普通表一致。
select * from 视图表名

update 视图表名 set 字段1=字段1的值, 字段2=字段2的值... where 条件表达式;
-- 修改视图的数据，建议直接改视图对应的那个数据表中的数据，而不是直接改视图，因为视图中如果包含以下4种情况，是不能修改视图中的数据
-- 1. 视图中包含SUM()、COUNT()、MAX()和MIN()等函数；
-- 2. 视图中包含UNION、UNION ALL、DISTINCT、GROUP BY和HAVING等关键字；
-- 3. 视图对应的表存在没有默认值的列，而且该列没有包含在视图里；
-- 4. 包含子查询的视图;

-- 修改视图中代表的SQL语句
ALTER VIEW 视图表名  AS SQL语句;

-- 删除视图
DROP VIEW 视图表名 [,视图表名]；
```

课堂例子：

```sql
drop table employee;
create table employee (
    id int auto_increment primary key,
    name char(20),
    department varchar(50),
    money decimal(8,2)
);


-- 提供给财务部门的人
select * from employee;

-- 创建1个视图
create view staff as select id,name,department from employee;

-- 提供给其他部门的人
select * from staff;
```

除了视图以外，在MySQL中还有一种临时表（TEMPORARY），也是一种特殊的数据表。但是这种数据库仅存在本次客户端连接中，客户端断开了临时表就没有了。



#### 子查询

子查询是将一个查询语句嵌套在另一个查询语句中，那么被嵌入到内部的语句就是子语句，而外部包含的就是主语句。

内层的子查询语句的查询结果，可以为外层查询语句提供查询条件或数据源。

子查询中可以包含：IN、NOT IN、ANY、ALL、EXISTS 和 NOT EXISTS等关键字，还可以包含比较运算符：= 、 !=、> 、<等。

常见格式：

```sql
主语句 from (子语句) as 表别名;
主语句 where (子语句);
```

操作：

```sql
-- 查询大于平均年龄的学生信息
select name,age from student where age > (select avg(age) from student);

-- 查询指定学生（吴杰）在班的所有同学信息
select * from student where class = (select class from student where name = '吴杰') and name != '吴杰';

-- 子查询作为数据源
select id,name from (select * from student order by id desc limit 5) as t;
```

练习：查询黄老师授课的课程中，大于平均成绩的学生。

```sql
select student.name from student
left join achievement on student.id=achievement.sid
left join course on course.id=achievement.cid
left join lecturer on course.lecturer_id=lecturer.id
where lecturer.name='黄老师' and achievement.achievement > (
select avg(achievement) from achievement
left join course on course.id=achievement.cid
left join lecturer on course.lecturer_id=lecturer.id
where lecturer.name='黄老师');
```



#### 查询结果格式定义

##### 普通字段合并格式定义

```sql
select concat(id,',',name, ',',age) from student;

select concat_ws(',',id,name,age) from student;
```

#####  分组字段合并格式定义

```sql
select class, group_concat(name) from student group by class;

-- concat_ws与group_concat组合使用
select any_value(name), group_concat(concat_ws('-',id,name) order by id) from student group by class;
```



#### 自关联查询

自关联也叫自连接，是单表同时存在主键与外键情况下的单表自连接查询操作。例如：员工与领导，省份与城市与地区，一级菜单与二级菜单与三级菜单，权限，推荐人/分销，等数据，都是常见的需要运用自关联操作的场景。

行政区划表-area

| id   | name   | parent_id |
| ---- | ------ | --------- |
| 1    | 河南省 |           |
| 2    | 广东省 |           |
| 3    | 郑州市 | 1         |
| 4    | 开封市 | 1         |
| 5    | 广州市 | 2         |
| 6    | 深圳市 | 2         |
| 7    | 中原区 | 3         |
| 8    | 新郑市 | 3         |
| 9    | 荥阳市 | 3         |
| 10   | 龙亭区 | 4         |
| 11   | 鼓楼区 | 4         |
| 12   | 通许县 | 4         |

处理这种自关联设计的表结构，可以在自己的脑海中对当前表进行拆分。

province省份表

| id   | name   |
| ---- | ------ |
| 1    | 河南省 |
| 2    | 广东省 |

city 城市表

| id   | name   | parent_id |
| ---- | ------ | --------- |
| 3    | 郑州市 | 1         |
| 4    | 开封市 | 1         |
| 5    | 广州市 | 2         |
| 6    | 深圳市 | 2         |

area 地区表

| id   | name   | parent_id |
| ---- | ------ | --------- |
| 7    | 中原区 | 3         |
| 8    | 新郑市 | 3         |
| 9    | 荥阳市 | 3         |
| 10   | 龙亭区 | 4         |
| 11   | 鼓楼区 | 4         |
| 12   | 通许县 | 4         |

```sql
-- 河南省的城市
select id from area where parent_id = (select id from area where name = '河南省');

-- 河南省的所有城市的地区
select * from area where parent_id in (select id from area where parent_id = (select id from area where name = '河南省'));

-- 查询龙亭区属于哪一个省份
select name from area where id = (select parent_id from area where id = (select parent_id from area where name = '龙亭区'));
```

面试题：自关联表的寻根问题（后面再说）



#### 联合查询

联合查询（union query），也叫合并查询，主要用于把多个查询结果合并成一个结果集返回，支持单表或多表操作，有两个关键字：

+ union，合并查询结果，并对重复结果进行去重。
+ union all，合并查询结果，但不会对重复结果进行去重。

union的基本使用：

```sql
-- 查询男生中平均成绩最好的3个学生 与 女生中成绩最好的5个学生。
(select any_value(name), avg(achievement) as score from student s
left join achievement a on s.id = a.sid
where s.sex = 1
group by a.sid
order by score desc limit 3)  --  因为limit在SQL语句中属于语句的结束关键字，所以在联合查询中需要加上（）
union
(select any_value(name), avg(achievement) as score from student s
left join achievement a on s.id = a.sid
where s.sex = 2
group by a.sid
order by score desc limit 5);
```

union all的基本使用：

```sql
-- 查询男生数量最少与女生数量最少的班级5个班级
(select class, count(id) as c from student where sex = 1 group by class order by c limit 5)
union all
(select class, count(id) as c from student where sex = 2 group by class order by c limit 5);
```

作业：

```bash
1. 一个商城中，对于商品的分类，是存在多级分类的情况，需要大家设计出合理的数据表，可以保存多级商品分类。
2. 在上面一题的基础上，创建一个手机的顶级分类，并且基于手机这个顶级分类，查询出手机下面的所有子分类的子分类下的分类信息。
```

| id   | name     | pid  |
| ---- | -------- | ---- |
| 1    | 手机     |      |
| 2    | 笔记本   |      |
| 5    | 游戏手机 | 1    |
| 6    | 5G手机   | 1    |
| 7    | 拍照手机 | 1    |
| 8    | 合约机   | 5    |
| 9    | 性能机   | 5    |
| 10   | 美颜手机 | 6    |
| 11   | 音乐手机 | 6    |

```sql
create table goods_category(
    id int auto_increment primary key, 
    name varchar(50),
    pid int
)

select * from goods_category where pid in (select id from goods_category where pid in (select id from goods_category where name = '手机'));
```



#### 事务

事务（Transaction），是以功能或业务作为逻辑单位，把一条或多条SQL语句组成一个不可分割的操作序列来执行的数据库机制。事务适用于多用户同时操作的数据库系统的场景，如银行、保险公司及证券交易系统等等要求数据一致性或完整性比较高的场景。MySQL 中只有使用了 Innodb 存储引擎才支持事务操作。它可以用来维护数据库的完整性，保证成批的SQL语句要么全部执行成功，要么全部执行失败，当事务中的某条SQL语句执行失败或产生错误，整个事务内部的所有SQL语句都将会回滚，所有受到影响的数据将返回到事务开始前的状态。

##### 基本使用

###### 准备数据

```sql
drop table if exists users;
create table users(
  id int auto_increment primary key,
  name varchar(50),
  money decimal(8,2)
);

insert into users values(1, '小明',1000);
insert into users values(2,'小红',1000);
insert into users values(3,'小白',1000);
```

###### 事务提交

```sql
begin; -- 使用begin关键语句表示手动开启事务，以下所有的SQL语句，就会被MySQL视作一个不可分割的整体
update users set money=money-200 where name = '小明';
update users set money=money+200 where name = '小红';
commit;  -- 使用commit关键语句表示手动提交事务
```

###### 事务回滚

```sql
begin; -- 使用begin关键语句表示手动开启事务，以下所有的SQL语句，就会被MySQL视作一个不可分割的整体
update users set money=money-200 where name = '小明';
update users set money=money+200 where name = '小红';
rollback; -- 使用rollback关键语句表示手动回滚事务，事务中所执行的所有的SQL语句都相当于没有执行一样。
-- 当然，什么时候选择提交事务，什么时候选择回滚事务呢？这个就需要结合我们将来所编写的python功能代码进行判断了。
```

###### 多点回滚

```sql
begin;
update users set money=money-200 where name='小明';
select * from users;
SAVEPOINT s1; -- POINT就是事务的节点，savepoint可以给当前位置打个标记，将来如果不希望完全回滚事务，则可以选择回滚到某一个事务节点。p1是自定义的事务节点名称
update users set money=money+100 where name='小红';
select * from users;
SAVEPOINT p2;
update users set money=money+100 where name='小白';
select * from users;
SAVEPOINT p3;


ROLLBACK TO s1; -- 注意：这里并非回滚代码，而是恢复代码造成的影响，而且也不是退出事务，仅仅是回滚事务中指定保存点的影响效果。
select * from users;   -- 注意，这里仅仅是事务内部的回滚，并没有退出事务操作的，此时还在事务内部。
rollback;  -- 或执行commit;   此时才是真正的退出事务。

-- mysql 事务的多点回滚在开发中主要应用于嵌套事务。
```

##### 事务控制

上面对于事务的处理都是手动操作的，MySQL中还支持使用AUTOCOMMIT来控制是否自动提交事务。mysql中默认是开启开启自动提交事务的(AUTOCOMMIT=1)，也就是在打开客户端连接时，会默认把每一条SQL语句当成一个独立的事务进行处理[为了方便实现事务使用过程中的redolog（重做日志）与undolog（回滚日志）]。

```sql
-- 查看MySQL中的AUTOCOMMIT值，MySQL中默认是开启自动提交事务的。这种情况下，MySQL会把每个sql语句当成一个事务，然后自动的commit提交事务。
SHOW VARIABLES LIKE '%AUTOCOMMIT%';

-- 关闭自动提交事务，MySQL会把当前会话连接的所有DML操作当成一个会话级别的事务进行管理，直到输入rollback或commit，当前事务才算结束。
-- 而结束该会话事务前，新的MySQL连接中是无法读取到任何该会话的操作结果的。
SET AUTOCOMMIT=0;
-- 开启自动提交事务
SET AUTOCOMMIT=1;
```

注意：是否开启自动提交事务，并不影响手动操作事务的过程。



##### 四大特性-ACID

1. 原子性（Atomicity）：事务内的所有DML语句，作为一个不可分割的整体，要么都成功，要么都失败，由redo log（重做日志）来实现
2. 一致性（Consistency）：事务执行前后的数据完整性是一致的，由undo log（回滚日志）来实现。
3. 隔离性（Isolation）：事务执行过程中对其他事务可以设置不同的隔离级别，隔离性由锁来实现不同的隔离级别
4. 持久性（Durability）：事务一旦提交，其结果就是永久性更改的，由redo log（重做日志）来实现

###### 原子性

原子性在数据库中的体现就是**事务回滚**，回滚能够撤销所有已经执行的sql语句，InnoDB实现回滚靠的是**回滚日志undo log。**在mysql中，每次执行DML语句都会先往 undo log 写入一条反向的SQL并且持久化，当系统崩溃时，扫描没有 commit 的事务对应的 undo log，按照undo log中不同类型SQL语句执行回滚操作。

- insert 类型：undo log 记录了 id ，根据 id 写入反向的delete语句
- delete 类型：undo log 记录了id对应的删除的数据，写入反向的insert语句
- update 类型：undo log 记录了修改前的数据，写入反向的update语句

###### 一致性

一致性是指事务在从一个一致性状态（事务开始前）切换到另一个一致性状态（事务结束后），不管事务是提交还是回滚，数据具有完整性约束的。例如上面的转账，在事务开始前，小红与小明两人的总金额是2000，在事务结束后不管事务提交或回滚，小明与小红的总金额还是2000的。

InnoDB中事务的一致性是由undo log（回滚日志）来实现。



###### 持久性

对于一个已经提交的事务，在事务提交后即使系统崩溃或宕机了，这个事务对数据库中所做的更改也不能丢失。Mysql为了提高性能使用了 BufferPool （缓存池），事务会先修改或读取 BufferPool 中的数据，如果内存中不存在当前要操作数据，会从硬盘读取到内存的 BufferPool 中。Mysql 在 更新记录写入 BufferPool 之前会把记录先写到 redolog （重做日志），当事务提交时会先将 redolog 通过刷盘机制持久化到硬盘，如果出现宕机，mysql重启后将 redolog 中的事务重放执行。

InnoDB中基于事务实现，提供了2个事务日志，redo log(重做日志) 和 undo log（回滚日志），其中redo log 分2部分，其中逻辑日志（redo log buffer，重做日志缓冲）与 物理日志（保存在硬盘中，ib_logfile0、ib_logfile1），而undo log则属于逻辑日志，保存缓冲区的表空间。

```sql
SHOW VARIABLES like "%innodb%";
-- innodb_log_buffer_size ： 日志缓存区的内存大小是16M
-- innodb_log_files_in_group ：redo log日志组的数量，2则表示2个redolog交替使用
-- innodb_log_group_home_dir ：redo log日志组的存储目录，./表示在mysql的data目录下
-- innodb_flush_log_at_trx_commit：刷盘策略，默认1，值可以是0，1，2
--                                 0. MySQL的每次事务提交时不进行刷盘操作，由mysql自己的主县城每隔1秒进行刷盘
--                                 1. MySQL的每次事务提交时都会同步刷盘一次数据
--                                 2. MySQL的每次事务提交时只会把redolog日志缓存区数据写入文件系统缓存，而不会通过硬盘中，由操作系统决定什么时候同步到物理日志
```

![image-20220609091328150](assets/image-20220609091328150.png)



###### 隔离性

隔离性是指并发过程中不同的客户端事务应该是隔离的，并发执行的各个事务之间不能互相干扰，在没有隔离性约束下，并发事务就可能出现脏读（Dirty Read）、不可重复读（Non-Repeatable Read）、幻读（Phantom Read）的问题，为了解决这些问题，就有了“隔离级别”的概念。

innoDB存储引擎 遵循了SQL:1992标准中的四种隔离级别：

1. `读未提交（RAED UNCOMMITED，RU）`：基于行级锁（但使用查询语句不会加锁），允许事务中的查询SQL语句读取其他事务中没提交的数据，这会导致出现脏读（Dirty Read）、不可重复读（Non-Repeatable Read）、幻读（Phantom Read）等问题的出现。这种最低的隔离级别，我们不会使用到它。

   ![image-20220608110319666](assets/image-20220608110319666.png)

2. `读已提交（RAED COMMITED，RC）`：基于行级锁，只允许事务中的查询SQL语句读取其他事务中已经提交的数据，可以避免脏读，但是不可重复读、幻读等问题还是会出现。db2或oracle等数据库的默认隔离级别，不可重复读、幻读可以通过代码程序来判断避免的。

   ![image-20220608110804995](assets/image-20220608110804995.png)

3. `可重复读（REPEATABLE READ，RR）`：基于行级锁，确保事务中多次读取同一范围的数据会返回第一次查询结果的快照，不会返回不同的数据行，但是可能出现幻读。MySQL的默认数据隔离级别就是RR级别，开发中经常把MySQL的隔离级别降低为RC级别。

   ![image-20220608111904702](assets/image-20220608111904702.png)

4. `串行化（SERIALIZABLE）`：基于表级锁，将全部的查询语句加上共享锁，让事务基于串行化的方式一个个执行，解决了幻读的问题，但是影响了并发性。分布式事务（XA）中默认就是串行化。

   ![image-20220608113202888](assets/image-20220608113202888.png)

查询数据库的事务隔离级别有两种，全局事务（global ）与会话事务（session）。

全局事务级别是针对整个数据库中所有的客户端连接。

会话事务级别是针对当前客户端连接，会话事务隔离级别设置比全局事务隔离级别权重大。

```sql
-- 查询全局事务隔离级别
show global variables like '%transaction_isolation%';   -- mysql8.0版本之前，配置项名为：tx_isolation
SELECT @@global.transaction_isolation;  -- 等价于上一句

-- 查询会话事务隔离级别
show session variables like '%transaction_isolation%';
SELECT @@session.transaction_isolation;  -- 等价于上一句
SELECT @@transaction_isolation;  -- 等价于上一句
```

临时设置数据库的隔离级别

```sql
-- 设置全局事务隔离级别【注意，修改了事务隔离级别，并不会影响到当前已打开的客户端连接会话的隔离级别】
SET GLOBAL TRANSACTION ISOLATION LEVEL [READ UNCOMMITTED|READ COMMITTED|REPEATABLE READ|SERIALIZABLE]
-- 设置会话事务隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL [READ UNCOMMITTED|READ COMMITTED|REPEATABLE READ|SERIALIZABLE]
```

永久设置数据库的隔离级别

注意，修改了事务隔离级别，并不会影响到当前已打开的客户端连接会话的隔离级别

```bash
# 打开配置文件
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf

# 可选参数有：READ-UNCOMMITTED, READ-COMMITTED, REPEATABLE-READ, SERIALIZABLE.
[mysqld]
transaction-isolation = READ-COMMITTED

# 保存配置文件，并重启MySQL，最好pycharm也重启下。
service mysql restart
```

面试过程中针对事务的常见问题：

```sql
1. 什么是事务？事务有哪些特性？事务的隔离级别有哪些？

2. 什么是脏读？什么是幻读？什么是不可重复读？都在哪些隔离级别下会出现？
```



#### 函数

MySQL常用函数非常多， 常用的函数分类则包括数值型、字符串型、日期时间、聚合、加密、控制流程等函数。当然， MySQL中也支持自定义函数。最后要注意：要少用或不用函数，虽然mysql提供了非常多函数，但是使用了函数以后，肯定损耗性能的，MySQL提供给我们的使用的核心作用并非替代编程语言，而是存储数据。

##### 数值型函数

| 函数            | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| ABS             | 求绝对值                                                     |
| SQRT            | 求二次方根                                                   |
| MOD             | 求余数                                                       |
| CEIL            | 返回不小于参数的最小整数，即向上取整                         |
| FLOOR           | 向下取整，返回值转化为一个BIGINT                             |
| RAND            | 生成一个0~1之间的随机数，传入整数参数时，用来产生可重复使用的随机数 |
| ROUND           | 对所传参数进行四舍五入                                       |
| POW             | 幂运算                                                       |
| PI              | 圆周率                                                       |
| BIN(x)          | 返回x的二进制编码                                            |
| HEX(x)          | 返回x的十六进制编码                                          |
| OCT(x)          | 返回x的八进制编码                                            |
| CONV(x,f1,f2)   | 返回f1进制数变成f2进制数                                     |
| FORMAT(value,n) | 返回对数字value进行格式化后的结果数据。n表示`四舍五入`后保留到小数点后n位 |

```sql
select FORMAT(avg(achievement),2) as score from student
left join achievement on student.id = achievement.sid
where student.id = 10
group by achievement.sid;


select format(RAND()*100,0);
```



##### 字符串型函数

| 函数                                | 描述                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| LENGTH                              | 返回字符串的字节长度，和字符集有关，utf8中一个多字节字符的字节长度为3，gbk则是2个 |
| **`CHAR_LENGTH`**                   | 返回字符串的字符长度                                         |
| **`CONCAT(s1,s2,…)`**               | 合并字符串函数，返回结果为连接参数产生的字符串，参数可以使一个或多个 |
| **`CONCAT_WS(x, s1,s2,......,sn)`** | 同CONCAT(s1,s2,…)函数，但是每个字符串之间要加上x             |
| INSERT                              | 替换字符串函数                                               |
| **`LOWER`**                         | 将字符串中的字母转换为小写                                   |
| **`UPPER`**                         | 将字符串中的字母转换为大写                                   |
| LEFT                                | 从左侧字截取符串，返回字符串左边的若干个字符                 |
| RIGHT                               | 从右侧字截取符串，返回字符串右边的若干个字符                 |
| **`TRIM`**                          | 删除字符串左右两侧的空格                                     |
| REPLACE                             | 字符串替换函数，返回替换后的新字符串                         |
| SUBSTRING                           | 截取字符串，返回从指定位置开始的指定长度的字符换             |
| **`REVERSE(s)`**                    | 字符串反转（逆序）函数，返回与原始字符串顺序相反的字符串     |
| FIND_IN_SET(s1,s2)                  | 返回字符串s1在字符串s2中出现的位置。其中，字符串s2是一个以逗号分隔的字符串 |

```sql
select length('hello');
select name, CHAR_LENGTH(description) from student;

drop table address
create table address(
    id int auto_increment primary key ,
    uid int,
    name char(20),
    province char(50),
    city char(50),
    area char(100),
    address varchar(500)
);

select name, concat(province, city, area, address) as addr from address;
select name, CONCAT_WS('-',province, city, area, address) as addr from address;


select INSERT('Quadratic', 3, 4, 'What');
select INSERT('Quadratic', 3, 0, 'What');

select upper('hello'), lower('HEELO');

select left('hello', 2), right('hello', 2);

select TRIM(' 12345 '), length(TRIM(' 12345 '));


select SUBSTRING('hello world', 2, 5);

select REVERSE('hello');

select FIND_IN_SET('a', 'abc');  -- enum, set
```



##### 日期时间函数

| 函数                 | 描述                                                         | 格式                                         |
| -------------------- | ------------------------------------------------------------ | -------------------------------------------- |
| **`CURRENT_DATE`**   | 返回当前系统的日期值                                         | 2021-02-26                                   |
| **`CURRENT_TIME`**   | 返回当前系统的时间值                                         | 15:00:42                                     |
| **`NOW`**            | 返回当前系统的日期和时间值                                   | 2021-02-26 15:00:42                          |
| **`UNIX_TIMESTAMP`** | 获取UNIX时间戳函数，返回一个以 UNIX 时间戳为基础的无符号整数 | 1614322842                                   |
| FROM_UNIXTIME        | 将 UNIX 时间戳转换为时间格式，与UNIX_TIMESTAMP互为反函数     | 2021-02-26 15:00:42                          |
| MONTH                | 获取指定日期中的月份                                         | 2                                            |
| MONTHNAME            | 获取指定日期中的月份英文名称                                 | February                                     |
| DAYNAME              | 获取指定曰期对应的星期几的英文名称                           | Friday                                       |
| DAYOFWEEK            | 获取指定日期对应的一周的索引位置值                           | 6                                            |
| WEEK                 | 获取指定日期是一年中的第几周，返回值的范围是否为 0〜52 或 1〜53 | 8                                            |
| DAYOFYEAR            | 获取指定曰期是一年中的第几天，返回值范围是1~366              | 57                                           |
| DAYOFMONTH           | 获取指定日期是一个月中是第几天，返回值范围是1~31             | 26                                           |
| YEAR                 | 获取年份，返回值范围是 1970〜2069                            | 2021                                         |
| TIME_TO_SEC          | 将时间参数转换为秒数                                         | 54042                                        |
| SEC_TO_TIME          | 将秒数转换为时间，与TIME_TO_SEC 互为反函数                   | 15:00:42                                     |
| DATE_ADD             | 向日期添加指定的时间间隔                                     | DATE_ADD('2021-02-26', interval 1 day);      |
| DATE_SUB             | 向日期减去指定的时间间隔                                     | DATE_SUB('2021-02-26', interval 1 week );    |
| ADDTIME              | 时间加法运算，在原始时间上添加指定的时间                     | ADDTIME('2021-02-26 15:00:42', '00:30:00');  |
| SUBTIME              | 时间减法运算，在原始时间上减去指定的时间                     | SUBTIME('2021-02-26 15:00:42', '00:30:00');  |
| **`DATEDIFF`**       | 获取两个日期之间间隔，返回参数 1 减去参数 2 的值             | DATEDIFF('2021-02-26', '2022-01-26');        |
| **`TIMEFDIFF`**      | 获取两个时间之间间隔，返回参数 1 减去参数 2 的值             | select timediff(current_time(), '06:30:00'); |
| DATE_FORMAT          | 格式化指定的日期，根据参数返回指定格式的值                   | DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s');      |
| WEEKDAY              | 获取指定日期在一周内的对应的工作日                           | WEEKDAY('2021-02-26 15:00:42');              |

```sql
-- 获取当前日期
select CURRENT_DATE();

-- 获取当前时间
select CURRENT_TIME();

-- 获取当前日期时间
select now();

-- 获取当前时间戳[秒]
select UNIX_TIMESTAMP();

-- 把指定时间戳转换成 日期时间格式
select from_unixtime(1624589517);

-- 获取日期中的月份
select MONTH(now());

-- 获取日期中的月份单词
select MONTHNAME(now());  # June

-- 获取一个星期中的周几（单词）
select DAYNAME(now());  # Tuesday


select DATE_ADD('2022-06-07', interval 1 day);
select DATE_SUB('2022-06-07', interval 1 day);

select DATEDIFF('2021-02-26', '2022-01-26');

select timediff(current_time(), '06:30:00');

```



##### 聚合函数

| 函数        | 描述                             |
| ----------- | -------------------------------- |
| **`MAX`**   | 查询指定列的最大值               |
| **`MIN`**   | 查询指定列的最小值               |
| **`COUNT`** | 统计查询结果的行数               |
| **`SUM`**   | 求和，返回指定列的总和           |
| **`AVG`**   | 求平均值，返回指定列数据的平均值 |



##### 加密函数

针对项目中的用户密码往往我们都是直接在编程语言中进行加密处理了，不会使用mysql的加密函数，但是针对mysql系统内部实际上也要对数据库管理员进行密码加密，此时我们就会使用加密函数。

| 函数                 | 描述                                                         |
| -------------------- | ------------------------------------------------------------ |
| AES_ENCRYPT(str,key) | 用密钥key对字符串str利用AES加密算法加密后的结果，<br>是一个二进制字符串，以BLOB类型存储 |
| AES_DECRYPT(str,key) | 用密钥key对字符串str利用AES加密算法解密后的结果              |
| DECODE(str,key)      | 使用key作为密钥解密加密字符串str                             |
| ENCODE(str,key)      | 使用key作为密钥加密字符串str                                 |
| ENCRYPT(str,salt)    | 使用UNIXcrypt()函数，用关键词salt加密字符串str               |
| MD5()                | 计算字符串str的MD5校验和                                     |
| SHA1()               | 计算字符串str的安全散列算法(SHA)校验和                       |
| PASSWORD(str)        | 对字符串str进行加密，低版本MySQL默认使用password对数据库系统账号进行密码加密 |

```sql
-- 使用AES高级加密算法基于参数2秘钥对参数1数据进行加密，得到二进制数据（BOLB）
select AES_ENCRYPT('123456', 'hwkwkwk2');

-- 使用AES高级加密基于参数2秘钥对参数1进行解密，得到原数据
select AES_DECRYPT(AES_ENCRYPT('123456', 'hwkwkwk2'), 'hwkwkwk2');

-- md5或sha1加密
select md5('hello'), sha1('hello'), sha('hello');

-- 使用password也可以加密
select password('hello');
```



##### 系统信息函数

| 函数                                                  | 描述                                                     |
| ----------------------------------------------------- | -------------------------------------------------------- |
| VERSION()                                             | 返回当前MySQL的版本号                                    |
| CONNECTION_ID()                                       | 返回当前MySQL服务器的连接数                              |
| DATABASE()，SCHEMA()                                  | 返回MySQL命令行当前所在的数据库                          |
| USER()，CURRENT_USER()、SYSTEM_USER()，SESSION_USER() | 返回当前连接MySQL的用户名，返回结果格式为“主机名@用户名” |

```sql
select version(), user(), database(), CONNECTION_ID();
```



##### 流程控制函数

| 函数           | 描述           |
| -------------- | -------------- |
| if(expr,v1,v2) | 判断，流程控制 |
| ifnull(v1,v2)  | 判断是否为空   |

case  搜索语句

```sql
-- 用法1
CASE  <表达式>
   WHEN <值1> THEN <操作1>
   WHEN <值2> THEN <操作2>
   ...
   ELSE <操作>
END CASE;

-- 用法2：
CASE
    WHEN <条件1> THEN <命令1>
    WHEN <条件2> THEN <命令2>
    ...
    ELSE <其他命令>
END CASE;
```

```sql
SELECT
CASE WEEKDAY(NOW())
   WHEN 0 THEN '星期一'
   WHEN 1 THEN '星期二'
   WHEN 2 THEN '星期三'
   WHEN 3 THEN '星期四'
   WHEN 4 THEN '星期五'
   WHEN 5 THEN '星期六'
   ELSE '星期天'
END as text;


SELECT
CASE
   WHEN WEEKDAY(NOW())=0 THEN '星期一'
   WHEN WEEKDAY(NOW())=1 THEN '星期二'
   WHEN WEEKDAY(NOW())=2 THEN '星期三'
   WHEN WEEKDAY(NOW())=3 THEN '星期四'
   WHEN WEEKDAY(NOW())=4 THEN '星期五'
   WHEN WEEKDAY(NOW())=5 THEN '星期六'
   ELSE '星期天'
END as text;
```



##### 自定义函数

MySQL中支持自定义函数，但是这个功能默认是关闭的。可通过以下语句查看是否开启自定义函数功能。

```sql
show variables like '%func%';
```

临时开启自定义函数功能

```sql
SET GLOBAL log_bin_trust_function_creators = 1;
```

###### 创建函数

基本写法

```sql
DELIMITER $$  -- DELIMITER $$  定义语句结束符。MySQL默认的结束符是分号，但是函数体中可能用到分号。为了避免冲突，需要另外定义结束符。
set global log_bin_trust_function_creators=1$$  -- 开启自定义函数的权限
DROP FUNCTION IF EXISTS 自定义函数名$$  -- 如果自定义函数名已经存在了，就删除掉。
CREATE FUNCTION 自定义函数名([参数列表]) RETURNS 返回结果的数据类型
BEGIN -- 函数体放在BEGIN 与 END之间
    SQL语句;
    RETURN 返回结果的值;
END $$  -- 函数结束
set global log_bin_trust_function_creators=0$$  -- 关闭自定义函数的权限
DELIMITER ; -- 自定义函数结束以后，恢复原来的语句结束符
```

例子：

```sql
DELIMITER $$
set global log_bin_trust_function_creators=1$$

DROP FUNCTION IF EXISTS get_student_total_by_class$$

create function get_student_total_by_class(class_num int) returns int
BEGIN
    declare total int default 0; -- 声明一个变量total，类型为int，默认值为0
    select count(id) from student where class=class_num into total;  -- 把查询结果赋值(into)给total变量
    return total;  -- 返回total作为函数结果
END $$


set global log_bin_trust_function_creators=0$$
DELIMITER ;

select get_student_total_by_class(305);
select get_student_total_by_class(301);

```

```sql
-- 查询某个自定义函数的定义
show create function  get_student_total_by_class; -- 无法查询内置函数的定义语句
```

###### 删除函数

```sql
DROP FUNCTION [ IF EXISTS ] 自定义函数名;
```



#### 存储过程

存储过程和函数是事先经过编译并存储在数据库中的一段 SQL 语句的集合，调用存储过程和函数可以简化应用开发人员的很多工作，减少数据在数据库和应用服务器之间的传输，对于提高数据处理的效率是有好处的。

存储过程和函数的区别在于函数必须有返回值，而存储过程可以没有。

##### 创建存储过程

```sql
CREATE PROCEDURE 存储过程名称 (in/out/inout [proc_parameter[,...]])
begin
	-- 存储过程的函数体->SQL语句
end ;
```

举个例子：

```sql

-- 案例1：
delimiter $$
drop procedure if exists procedure_name$$
create procedure procedure_name(in n int)
begin
    declare total int default 0;
    declare num int default 0;
    SET num = 1; -- 赋值语句，如果值的结果是一个SQL语句的结果，则需要使用into
    SELECT num;  -- 打印，因为MySQL中没有提供print函数，所以我们调试就需要使用select
    while num<=n do
        set total = total + num;
        set num = num + 1;
    end while;
    select total;
end $$

delimiter ;

call procedure_name(10);



delimiter $$
drop procedure if exists procedure_name$$
create procedure procedure_name(in age int , inout content varchar(100))
-- in 表示外界传递进来的参数，叫入参
-- out 表示由内部处理后返回给外界的数据，叫出参[相当于返回值]
-- inout 表示外界传递进来的参数，并经过处理后可以在外界调用结果的进出参
begin
  if age < 18 then
    set content='未成年人';
  elseif age < 40 then
    set content ='青年';
  else
    set content ='中老年';
  end if;

end$$

delimiter ;

call procedure_name(50, @content); -- 出参必须使用@开头声明变量
select @content;
```

##### 调用存储过程

```sql
call 存储过程名称();
```

##### 查看储存过程

因为存储过程是基于数据库保存的，所以查询存储过程必须指定数据库

```sql
-- 查询指定数据库中的所有的存储过程或函数
select routine_type, routine_name  from information_schema.routines where routine_schema='students';

-- 查询存储过程的状态信息和创建信息
show procedure status;

-- 查询某个存储过程的定义
show create procedure  procedure_name;
```

##### 删除存储过程

```sql
DROP PROCEDURE  [IF EXISTS] procedure_name;
```

存储过程中往往会与函数类似，一般处理复杂的业务功能，而且往往内部都会采用事务批量执行SQL语句。



#### 触发器

触发器（trigger）就是在预设条件满足以后，自动执行的SQL语句的数据库特性，一般在编程开发中，也可以称之为钩子（Hook），中间件（Middleware）。

触发器是与表有关的数据库对象，指在 insert/update/delete 之前或之后，触发并执行触发器中预定义的SQL语句集合。触发器的这种特性可以协助应用程序在数据库端确保数据的完整性 ，常用于日志记录， 数据校验等操作。

| 触发器类型        | 触发器中new 和 old的使用                                     |
| ----------------- | ------------------------------------------------------------ |
| INSERT 类型触发器 | new 对象表示将要或者已经新增的数据                           |
| UPDATE 类型触发器 | old 对象表示修改之前的数据 , new 对象表示将要或已经修改后的数据 |
| DELETE 类型触发器 | old 对象表示将要或者已经删除的数据                           |



##### 创建触发器

```sql
create trigger 触发器名称 

before/after insert/update/delete

on tbl_name 

[ for each row ]  -- 行级触发器，注意：mysql中只支持行级触发器，不支持语句触发器。
begin
    -- 一条或SQL语句;
end;
```

举个栗子，通过触发器记录 emp 表的数据变更日志 , 包含增加, 修改 , 删除 ;

首先创建一张职员表与日志表：

```sql
create table emp(
    id int auto_increment primary key,
    name varchar(50),
    age tinyint,
    salary decimal(8,2)
);

create table logs(
  id int(11) not null auto_increment primary key,
  operation varchar(20) not null comment '操作类型, insert/update/delete',
  operate_time datetime not null comment '操作时间',
  operate_id int(11) not null comment '操作表的ID',
  operate_params varchar(500) comment '操作参数',
);
```

创建 insert 类型触发器，完成插入数据时的日志记录 :

```sql
-- 创建添加数据的触发器
DELIMITER $$
create trigger logs_insert_trigger
after insert
on emp
for each row
begin
    insert into logs (id,operation,operate_time,operate_id,operate_params) values(null,'insert',now(),new.id, concat('插入后(id:',new.id,', name:',new.name,', age:',new.age,', salary:',new.salary,')'));
end $$

DELIMITER ;

-- 测试
insert into emp values (null, '小明', 18, 20000);
```

创建 update 类型触发器，完成更新数据时的日志记录 :

```sql
-- 创建更新类型的触发器
DELIMITER $$
create trigger logs_update_trigger
after update
on emp
for each row
begin
  insert into logs (id,operation,operate_time,operate_id,operate_params) values(null,'update',now(),new.id,concat('修改前(id:',old.id,', name:',old.name,', age:',old.age,', salary:',old.salary,') , 修改后(id',new.id, 'name:',new.name,', age:',new.age,', salary:',new.salary,')'));
end $$

DELIMITER ;

-- 测试
update emp set salary=salary+500 where id=1;
```



创建delete 类型的触发器 , 完成删除数据时的日志记录 :

```sql
DELIMITER $$
create trigger logs_delete_trigger
after delete
on emp
for each row
begin
  insert into logs (id,operation,operate_time,operate_id,operate_params) values(null,'delete',now(),old.id,concat('删除前(id:',old.id,', name:',old.name,', age:',old.age,', salary:',old.salary,')'));
end $$

DELIMITER ;

-- 测试
delete from emp where id = 1;
```



##### 删除触发器

```sql
drop trigger [schema_name.]trigger_name;  -- 如果没有指定 schema_name，默认为当前数据库 。
```



##### 查看触发器

可以查看触发器的状态、语法等信息。

```sql
show triggers;
```



#### 索引基础

索引（index，key），是帮助MySQL高效获取数据的数据结构。类似大学图书馆建书目索引，可以提高数据检索的效率，降低数据库的IO成本。
通过索引列对数据进行排序，降低数据排序的成本，降低了CPU的消耗。索引往往存储在磁盘上的文件中，实际上索引也是一张表，该表保存了主键与索引字段，并指向实体表的记录，所以索引列也是要占用空间的。虽然索引大大提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件每次更新添加了索引列的字段，都会调整因为更新所带来的键值变化后的索引信息。索引只是提高效率的一个因素，如果MySQL有大数据量的表，就需要花时间研究建立最优秀的索引，或优化查询。

因此总结来说，索引的使用就是一种**以空间换时间**策略，以硬盘空间保存索引与数据位置的映射关系，在查询数据时间，如果有字段被设置了索引，则MySQL查询优化器会根据索引查找到最优的数据查询计划，可以缩短数据查询所需要消耗的时间。但是数据表在DML操作时，因为数据库需要时刻维护索引与数据位置的关系，因此在DML操作时会耗费额外的资源来完成表的索引检索操作，建议在读多写少的时候创建合适数量的索引。读少写多（类似日志就是读少写多）

索引一般用于在作为排序（order by 关键字后面）、查询条件（where关键字后面）、 字段投影（select关键字后面）。

##### 索引分类和管理

###### 主键索引

一般就是一张表只有1个主键索引。索引值唯一，如果是数字类型的主键则一般设置自增（auto_increment）且不能为NULL。当然，主键字段的数据类型，也可以不设置为数值类型。

```sql
-- 第一种：在表创建时声明主键
CREATE TABLE user_info(
    id int PRIMARY KEY auto_increment,
    name varchar(10)
);

drop table if exists user_info;
CREATE TABLE user_info(
    id int auto_increment,
    name varchar(10),
    primary key(id)
);

-- 第二种：使用alter增加主键
ALTER TABLE table_name ADD PRIMARY KEY (columnName);
alter table user_info modify id int auto_increment primary key;  -- modify修改数据类型
```

###### 唯一索引

索引列的值必须多行唯一，但允许有空值NULL，一张表中可以有多个唯一索引。

```sql
-- 第一种： 建表时设置索引
drop table if exists user_profile;
create table user_profile(
    id int auto_increment primary key ,
    username varchar(50) not null unique comment '登录账号',
    mobile varchar(15) null default null unique  comment '手机号',
    email varchar(150) null default null unique comment '邮箱',
    id_card varchar(18) null default null comment '身份证'
);


drop table if exists user_profile;
create table user_profile(
    id int auto_increment primary key ,
    username varchar(50) not null comment '登录账号',
    mobile varchar(15) null default null comment '手机号',
    email varchar(150) null default null comment '邮箱',
    id_card varchar(18) null default null comment '身份证',
    unique index username_unique(username),
    unique index mobile_unique(mobile),
    unique index email_unique(email)
);

-- 第二种：也可以后续新增或修改字段
ALTER TABLE user_profile ADD UNIQUE INDEX id_card_unique (id_card);
ALTER TABLE user_profile modify id_card varchar(18) null default null unique comment '登录账号';
```

###### 普通索引

索引字段的值可重复出现多次，一张表中可以有多个普通索引。

```sql
-- 第一种：
drop table if exists article;
create table article(
    id int auto_increment primary key ,
    title varchar(50) comment '文章标题',
    pud_date datetime default now()
     index title_index(title),
     key pud_date_index(pud_date)
);

-- 第二种：也可以后续新增或修改字段
create index title_index on article (title);
ALTER TABLE article ADD INDEX pud_date_index (pud_date);
```

###### 全文索引

主要是针对大文本字段的内容检索，如：文章内容。全文索引在mysql5.7版本以前，只针对MyISAM存储引擎有效，在MySQL5.7以后，InnoDB存储引擎才支持全文索引。虽然MySQl8.0版本中InnoDB支持全文索引，但是只针对英文内容生效，对中文不生效，所以如果我们将来要完成中文全文索引的话，我们一般会采用elastiscsearch、xunsearch、sphinx等。

```sql
-- 建表
CREATE TABLE article_info(
	id int auto_increment primary key,
	title VARCHAR(200),
	body TEXT,
	FULLTEXT(title, body)
);

insert into article_info values (null, 'welcome to python', 'hello world');
insert into article_info values (null, 'welcome to beijing', 'hello, beijing');

-- 可以通过查询计划关键字explain 来查看是否命中了索引
-- 使用方法是match(字段名...) against(‘关键字') 进行全文差早
explain select * from article_info where match(title,body) against('welcome');  -- type=FULLTEXT 命中全文索引
explain select * from article_info where title like 'welcome';  -- type=ALL表示 全表扫描，最慢
explain select * from article_info where id =2; -- type=const, key=PRIMARY 表示命中主键索引，最快
-- MySQL中的全文索引只针对英语内容生效，要针对中文进行全文搜索，我们后面会学习到es可以实现
```

```sql
ALTER TABLE article_info ADD FULLTEXT title_fulltext (title, body);
```



###### 单值索引

也叫单列索引，即一个索引只包含单个字段列，一个表可以有多个单列索引，单列索引有单列主键索引，单列唯一索引，单列普通索引，单列全文索引。

```sql
-- 第一种： 
create table goods_info(
    id int auto_increment primary key,        -- 单列主键索引
    goods_sn varchar(64) unique,                -- 单列唯一索引
    title varchar(255),
    description text,
    index title_index(title),                            -- 单列普通索引
    fulltext description_fulltext(description) -- 单列全文索引
)

-- 第二种：
CREATE unique| INDEX | fulltext index_name ON table_name(columnName);
ALTER TABLE table_name ADD INDEX index_name ON (columnName);
```

###### 复合索引

也叫联合索引或多列索引，即一个索引包含多个字段列，一个表中可以有多个复合索引。但是使用时要使用复合索引的字段列就不要其他索引重复了。

```sql
-- 第一种：

create table order_items(
    order_id int,
    goods_id int,
    primary key(order_id, goods_id)  -- 联合主键
);

create table users2(
    id int auto_increment primary key,
    username varchar(20),
    email varchar(255),
    unique username_mail_unique(username, email)
);

CREATE TABLE article_info(
	id int auto_increment primary key,
	title VARCHAR(200),
	body TEXT,
	FULLTEXT(title, body)
);

-- 第二种：
CREATE INDEX index_name ON table_name(columnName1，columnName2...);
ALTER TABLE table_name ADD INDEX index_name ON (columnName1，columnName2...);
```



###### 查询索引

```sql
-- 第一种：
SHOW INDEX FROM 数据表名;
-- 第二种：
SHOW KEYS FROM 数据表名;
```

###### 删除索引

```sql
-- 第一种： 
DROP INDEX 索引名称 ON 数据表名;

-- 第二种：
ALTER TABLE 数据表名 DROP INDEX 索引名称;

-- 删除主键索引，不需要主键索引名称，因为一个表中只允许1个主键
ALTER TBALE 数据表名 DROP PRIMARY KEY;
```



##### 哪些情况适合建索引

```
1. 主键自动建立唯一索引
2. 频繁作为查询条件的字段应该创建索引
3. 查询中与其它表关联的字段，外键关系建立索引
4. 单列/组合索引的选择问题，who?(在高并发下倾向创建组合索引)
5. 查询中排序的字段，排序字段若通过索引去访问将大大提高排序速度
6. 查询中统计或者分组字段
```

##### 哪些情况不适合建索引

```
1. Where条件里用不到的字段不创建索引
2. 表记录太少（300w以上建）
3. 写多读少的表（提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件）
4. 数据重复且分布平均的表字段，因此应该只为最经常查询和最经常排序的数据列建立索引。注意，如果某个数据列包含许多重复的内容，为它建立索引就没有太大的实际效果。（比如：国籍、性别）
```



#### 外键约束

外键(FOREIGN KEY)也是索引的一种，是通过A表中的一个字段列指向B表中的主键，来对两张表进行关联的一种索引。对于两个具有关联关系的表而言，相关联字段中主键所在的表就是主表（父表），外键所在的表就是从表（子表）。当然使用外键会影响数据库性能，而且在对数据表进行DML写操作时，还会引起从表数据的完整性约束检查，所以一般开发中都是不采用数据库提供的物理外键约束，而是基于代码层面来实现逻辑外键，也叫虚拟外键。

1:1的关联关系中，两张表的主键进行主外键关联，或者把其中1张表的主键放到另外一张表中充当外键。

1:多的关联关系中，1的表中的主键放在多表中作为外键

多:多的关联关系中，两张多表中的主键，保存到第三张关系表中记录为外键。

商品分类表(主表)

| ID(主键) | 分类名 |
| -------- | ------ |
| 1        | 手机   |
| 2        | 电脑   |
| 3        | 洗衣机 |

商品信息表(子表)

| ID   | 商品标题        | 分类ID(外键) |
| ---- | --------------- | ------------ |
| 1    | 华为meta40      | 1            |
| 2    | 华为meta50      | 1            |
| 3    | 华为meta30      | 1            |
| 4    | 海尔Mate1洗衣机 | 3            |

##### 创建外键

###### 1:1关系的主外键约束

```sql
# 1:1 主外键关联
create table article(
    id int auto_increment primary key,
    title varchar(20)
);

create table article_info(
    id int auto_increment primary key,
    content text,
    CONSTRAINT article_info_foreign_key FOREIGN KEY(id) REFERENCES article(id)
);

create table goods(
    id int auto_increment primary key,
    title varchar(20)
);

create table goods_info(
    id int auto_increment primary key,
    goods_id int unique,
    content text,
    CONSTRAINT goods_info_foreign_key FOREIGN KEY(goods_id) REFERENCES goods(id)
);
```

###### 1:多的主外键约束

```sql
create table goods_category(
    id int auto_increment primary key,
    name varchar(20)
);

create table goods(
    id int auto_increment primary key,
    cid int,
    title varchar(20),
    CONSTRAINT goods_foreign_key FOREIGN KEY(cid) REFERENCES goods_category(id)
);
```

###### 多对多的主外键约束

```sql
create table user(
    id int auto_increment primary key,
    name varchar(20)
);

create table coupon(
    id int auto_increment primary key,
    title varchar(50),
    money decimal(8,2)
);

create table user_coupon(
    id int auto_increment primary key ,
    uid int,
    cid int,
    CONSTRAINT coupon_foreign_key FOREIGN KEY(cid) REFERENCES coupon(id),
    CONSTRAINT user_foreign_key FOREIGN KEY(uid) REFERENCES user(id)
);
```

除了上面在建表时创建外键约束以外，还可以在后续通过 alter table 来创建外键。

```sql
ALTER TABLE 当前表名 ADD CONSTRAINT 外键名 FOREIGN KEY(外键名)
REFERENCES 外键表名(外键表的主键名)
[ON DELETE {RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT}]
[ON UPDATE {RESTRICT | CASCADE | SET NULL | NO ACTION | SET DEFAULT}]
```



##### 级联操作

所以的级联（CASCADE）操作，是通过MySQL的内部维护主外键的过程中，在操作主表时，是否对于外键表进行联动操作的一种机制。

MySQL中，提供的级联类型：

| 级联类型       | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| **`RESTRICT`** | 限制保护，当删除主键对应的数据时，必须先把当前主键对应的外键数据全部删除。也就是必须先删外键才能删主键。 |
| **`CASCADE`**  | 联动删除，当删除主键对应的数据时，外键所在的数据也会被删除掉 |
| **`SET NULL`** | 空值保留，当删除主键对应的数据时，外键被设置值为NULL         |
| NO ACTION      | 无操作，当删除主键对应的数据时，外键所在的数据不进行任何操作[mysql 8.0以后，无效] |
| SET DEFAULT    | 默认取值，当删除主键对应的数据时，外键会被DEFAULT默认值取代[mysql 8.0以后废弃] |

举个例子。

```sql
-- 限制保护
create table article(
    id int auto_increment primary key,
    title varchar(20)
);

create table article_info(
    id int auto_increment primary key,
    content text,
    CONSTRAINT article_info_foreign_key FOREIGN KEY(id) REFERENCES article(id)
     ON DELETE RESTRICT
);


-- 级联操作
drop table if exists goods_category, goods;
create table goods_category(
    id int auto_increment primary key,
    name varchar(20)
);

create table goods(
    id int auto_increment primary key,
    cid int,
    title varchar(20),
    CONSTRAINT goods_foreign_key FOREIGN KEY(cid) REFERENCES goods_category(id)
    on delete cascade
);

insert into goods_category values (null, '手机');
insert into goods values (null, 1, '华为meta40'), (null, 1, '华为meta50'), (null, 1, '华为P50');


-- set null 空值保留
drop table if exists goods_category, goods;
create table goods_category(
    id int auto_increment primary key,
    name varchar(20)
);

create table goods(
    id int auto_increment primary key,
    cid int,
    title varchar(20),
    CONSTRAINT goods_foreign_key FOREIGN KEY(cid) REFERENCES goods_category(id)
    on delete SET NULL
);

insert into goods_category values (null, '手机');
insert into goods values (null, 1, '华为meta40'), (null, 1, '华为meta50'), (null, 1, '华为P50');

```



## Python操作MySQL

编程语言作为客户端，连接并操作mysql，通常都是2种方式：

1. 数据库驱动模块：pymysql 、mysqldb。
2. 数据库ORM模块：SQLAlchemy。

不管哪一种方式，mysql都只能识别SQL语句，所以上面的几个模块的作用就是充当客户端发送sql语句，通过socket通信间接并操作mysql。当然，其中第二种操作方式，是基于第一种方式而进行高度封装实现的。

### pymysql

官方代码托管仓库：https://github.com/PyMySQL/PyMySQL

官方文档：https://pymysql.readthedocs.io/en/latest/

#### 安装pymysql模块

```shell
pip install pymysql
# 因为客户端连接mysql时需要针对密码进行加密，而且socket通信也是加密连接通信，linux/uxin需要安装以下模块
pip install cryptography
```

#### 快速入门

##### 直接调用connect与cursor操作数据库

```python
import pymysql.cursors


# 创建和数据库服务器的连接
# 返回值：pymysql.connections.Connection 的实例对象
# from pymysql.connections import Connection
conn = pymysql.connect(user="root", password="123", host="127.0.0.1", port=3306, database="students")

# 操作数据库，需要创建游标对象
cursor = conn.cursor()

sql = """SELECT * FROM `student` where name!='吴杰' and sex=1"""
# 数据库完成以后，手动关闭连接
result = cursor.execute(sql)
print(result)
for row in cursor.fetchall():
    print(row)
    # print(f'row["id"]={row["id"]}, row["name"]={row["id"]}')

# 关闭回收游标[相当于关闭文件操作的管道资源]
cursor.close()
# 关闭数据库连接[相当于关闭socket通信的连接资源]
conn.close()
```



##### 基于上下文管理器操作数据库

Connection类与Cursor类都在内部实现了执行上下文管理器协议，所以可以使用with来操作，自动完成关闭操作

```python
import pymysql.cursors


with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    print(conn)
    # 要操作数据，就需要创建游标对象
    # from pymysql.cursors import Cursor
    with conn.cursor() as cursor:
        print(cursor)
        # 中间可以使用游标完成对数据库的操作
        sql = """SELECT * FROM `student` where name!='吴杰' and sex=1"""  # 在python操作SQL语句，单个SQL语句不加分号也可以

        # 执行SQL语句
        # 如果查询语句，则返回值是查询结果的总数
        # 如果DML语句，则返回值是当前当前数据表受影响的行数
        result = cursor.execute(sql)
        print(result)
        for row in cursor.fetchall():
            print(row)
            # print(f'row["id"]={row["id"]}, row["name"]={row["id"]}')
```



#### 数据操作

##### 添加一条数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """添加一条数据"""
        sql = "insert into student (name, sex, class, age, description) VALUES ('王小明', 1, 301, 17, '这家伙很懒，一句话都没有留下.')"
        result = cursor.execute(sql)
        # cursor是默认把单个DML语句作为事务进行包装执行的，所以需要在执行SQL语句，手动提交事务
        conn.commit()
        # 查看受影响的行数
        print(result)
        # 查看新增数据的主键
        print(cursor.lastrowid)

```



##### 预处理SQL语句

预处理SQL（Prepare），是一种特殊的 SQL 处理方式；预处理不会直接执行 SQL 语句，而是先将 SQL 语句进行语句编译，生成执行计划，然后通过 Execute 命令携带 SQL 参数执行 SQL 语句，在使用过程中一共提供了2种预处理机制：参数绑定与命名绑定。

预处理SQL语句，可以有效地防止SQL注入攻击。

MySQL终端下准备数据表和数据

```python
create table users(
    id int auto_increment primary key ,
    username varchar(50),
    password varchar(64)
);

insert into users values (null, 'root', 'asdklasdfgmdm233232'),
                         (null, 'admin', 'dmt44m3mfdf90vxcvm,()*I');
```

模拟SQL注入攻击

在终端下输入一些特殊字符或者特殊内容，让SQL语句的判断，执行结果失效，这个行为就是SQL注入攻击

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """模拟SQL注入攻击"""
        username = input('请输入登录账户:')
        password = input('请输入登录口令:')
        sql = f'select username, password from users where username="{username}" and password="{password}"'
        print(sql)
        result = cursor.execute(sql)
        if result:
            print("登录成功！")
        """
        正常使用肯定没有问题，
        root
        123456
        但是防止不了SQL注入
        在终端下输入一些特殊字符或者特殊内容，让SQL语句的判断，执行结果失效，这个行为就是SQL注入攻击
        root
        12345' or '1
        12345" or "1
        """
        # ' or '1 表示让where表达式，后面跟着一个永远为True的条件，让where条件判断失效


```

采用预处理SQL防止SQL注入

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        username = input('请输入登录账户:')
        password = input('请输入登录口令:')
        # 预处理，可以识别并检测SQL语句参数中是否携带了攻击代码或者SQL注入语句
        sql = f"select username, password from users where username=%(username)s and password=%(password)s"
        print(sql)
        params = {"username": username, "password": password}
        result = cursor.execute(sql, params)
        if result:
            print("登录成功！")
        else:
            print("登录失败！")
        """
        在终端下输入一些特殊字符或者特殊内容，让SQL语句的判断，执行结果失效，这个行为就是SQL注入攻击
        root
        12345' or '1
        """

```



##### 基于预处理添加一条数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """添加一条数据"""
        # 预处理SQL语句[参数绑定]
        # sql = "insert into student (name, sex, class, age, description) VALUES (%s, %s, %s, %s, %s)"
        # args = ("小明1号", 1, 301, 17, "这家伙很懒，一句话都没有留下.")
        # 预处理SQL语句[命名绑定]
        sql = "insert into student (name, sex, class, age, description) VALUES (%(name)s, %(sex)s, %(class)s, %(age)s, %(description)s)"
        args = {
            "name": "小明2号",
            "sex": 1,
            "class": 301,
            "age": 17,
            "description": "这家伙很懒，一句话都没有留下."
        }
        # 批量执行SQL语句
        result = cursor.execute(sql, args)
        # cursor是默认把单个DML语句作为事务进行包装执行的，所以需要在执行SQL语句，手动提交事务
        conn.commit()
        # 查看受影响的行数
        print(result)
        # 查看新增数据的主键
        print(cursor.lastrowid)

```

##### 添加多条数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """添加多条数据"""
        sql = "insert into student (name, sex, class, age, description) VALUES (%s, %s, %s, %s, %s)"
        args = [
            ("王晓红1号", 1, 301, 17, "这家伙很懒，一句话都没有留下."),
            ("王晓红2号", 1, 301, 17, "这家伙很懒，一句话都没有留下."),
            ("王晓红3号", 1, 301, 17, "这家伙很懒，一句话都没有留下."),
            ("王晓红4号", 1, 301, 17, "这家伙很懒，一句话都没有留下."),
        ]
        # 批量执行SQL语句
        result = cursor.executemany(sql, args)
        # cursor是默认把单个DML语句作为事务进行包装执行的，所以需要在执行SQL语句，手动提交事务
        conn.commit()
        # 查看受影响的行数
        print(result)
        # 查看新增数据的主键
        print(cursor.lastrowid)
```

##### 查询数据

###### 查询一条数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """查询一条数据"""
        sql = "select id,name,age,sex from student where id=%(id)s"
        args = {"id": 1}

        cursor.execute(sql, args)
        row = cursor.fetchone()
        print(row)
```

###### 查询多条数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """查询多条数据"""
        sql = "select id,name,age,sex from student where class=%(class)s"
        args = {"class": 301}
        cursor.execute(sql, args)

        # cursor的游标会记录每次读取的状态，所以如果前面有执行了fetch方法读取数据，则后续再次调用fetch会在上一次读取数据的基础往后读取

        # 可以使用fetchmany 从结果集_rows中读取指定数量的结果
        for row in cursor.fetchmany(3):
            print(row)
        print(">>>>>>> ")

        # 可以使用fetchall一次性从结果集_rows中读取全部结果
        for row in cursor.fetchall():
            print(row)

```



##### 更新数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """更新数据，可以更新一条，也可以更新多条，主要看设置的where条件"""
        # 先读取要更新的数据【当然，现在是学习阶段，所以也可以不读取，直接更新】
        sql = "select id,name,age,sex from student where name=%(name)s"
        args = {"name": "小明2号"}
        cursor.execute(sql, args)
        row = cursor.fetchone()  # 举例修改1条
        sql = f"update student set name=%(name)s where id=%(id)s"
        args = {"name": "小明同学", "id": row["id"]}
        result = cursor.execute(sql, args)
        conn.commit()
        print(result)
```



##### 删除数据

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """删除数据"""
        sql = f"delete from  student where id=%(id)s"
        args = {"id": 113}
        result = cursor.execute(sql, args)
        conn.commit()
        print(result)
```

练习：

```bash
1. 在python中操作pymysql，获取 301班所有女生的信息[id,name,sex,age]
2. 在python中操作pymysql，获取黄老师的学生信息以及学生的课程成绩
3. 基于python操作pymysql实现一个商品信息管理系统[终端版本]，在以前基于文件存储数据的基础上，现在改成数据库存储商品信息。
```



#### 事务处理

mysql本身是支持事务的，所以在Pymysql使用过程中，当游标cursor建立时就自动开始了一个隐形的事务管理了。

数据准备

```sql
drop table if exists users;

create table users(
  id int auto_increment primary key,
  name varchar(50),
  money decimal(8,2)
);

insert into users values(1, '小明',1000);
insert into users values(2, '小红',1000);
insert into users values(3, '小白',1000);

-- update users set money=money-200 where name = '小明';
-- update users set money=money+200 where name = '小红';
```

演示代码：

```python
import pymysql.cursors

with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """
        事务处理
        只要小明有钱，并且小红的钱低于1600，就继续转钱
        """
        conn.begin()
        sql1 = "select money from users where name = '小明'"
        cursor.execute(sql1)
        res1 = cursor.fetchone()
        if res1["money"] > 0:
            sql2 = "update users set money=money-200 where name = '小明'"
            cursor.execute(sql2)

        sql3 = "select money from users where name = '小红'"
        cursor.execute(sql3)
        res2 = cursor.fetchone()
        if res1["money"] > 0 and res2["money"] < 1600:
            sql4 = "update users set money=money+200 where name = '小红'"
            cursor.execute(sql4)
            conn.commit()
            print("转账成功")
        else:
            conn.rollback()
            print("转账失败，事务回滚")

```

事务多点回滚

```python
import pymysql.cursors
with pymysql.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="students",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor  # 设置pymysql针对查询结果的返回值为字典格式，默认是元组格式
    ) as conn:
    with conn.cursor() as cursor:
        """
        事务处理
        只要小明有钱，并且小红的钱低于1600，就继续转钱
        """
        conn.begin()
        # 把小明的money减去200
        sql = "update users set money=money-200 where name='小明'"
        cursor.execute(sql)

        sql = "select * from users"
        cursor.execute(sql)
        print(cursor.fetchall())

        sql = "SAVEPOINT s1"
        cursor.execute(sql)
       # -- 给小红分100
        sql = "update users set money=money+100 where name='小红'"
        cursor.execute(sql)

        sql = "select * from users"
        cursor.execute(sql)
        print(cursor.fetchall())

        sql = "SAVEPOINT s2"
        cursor.execute(sql)
       # -- 给小白分100
        sql = "update users set money=money+100 where name='小白'"
        cursor.execute(sql)

        sql = "select * from users"
        cursor.execute(sql)
        print(cursor.fetchall())

        sql = "SAVEPOINT s3"
        cursor.execute(sql)

        sql = "ROLLBACK TO s1"  # 表示从s1事务保存点，到当前一行的中间所有DML操作全部失效
        cursor.execute(sql)

        sql = "select * from users"
        cursor.execute(sql)
        print(cursor.fetchall())

        conn.commit()

```



#### 基于面向对象封装工具类

在工作中，手写SQL语句基于execute执行，这种方式，性能是最好的！但是往往开发中，如果我们编写大量固定的SQL语句，也会导致程序的维护成本提升，同时将来如果应用程序要切换底层数据库的话，将会带来巨大的兼容问题。

```python
import pymysql.cursors


class DB(object):
    """数据库工具类"""
    connected = False  # 数据库连接状态，False表示没有连接或连接失败
    __conn = None  # 数据库连接对象

    class DBError(Exception):
        """数据库异常基类"""
        pass

    class DBConfigError(DBError):
        """数据库配置异常类"""
        pass

    class ConnectionError(DBError):
        """数据库连接异常类"""
        pass

    class ExecuteError(DBError):
        """数据库执行异常类"""
        pass

    def __init__(self, conf):
        if type(conf) is not dict:
            raise self.DBConfigError("错误: 数据库连接参数必须是字典类型！")

        for key in ["host", "user", "password", "database"]:
            if key not in conf.keys():
                raise self.DBConfigError(f"错误: 数据库连接缺少'{key}'参数")

        if not conf.get("port", None):
            conf["port"] = 3306

        if 'charset' not in conf.keys():
            conf["charset"] = "utf8mb4"

        try:
            self.__conn = pymysql.connect(
                host=conf['host'],
                port=conf['port'],
                user=conf['user'],
                password=conf['password'],
                database=conf['database'],
                charset=conf['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            self.connected = True
        except pymysql.Error as e:
            raise self.ConnectionError(f"数据库连接失败: {e}")

        self.sql = ""  # 记录最后一次执行的SQL语句

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        del exc_info
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        try:
            self.__conn.close()
        except pymysql.Error as e:
            pass

    def insert(self, table, **kwargs):
        """
        添加一条数据
        :param table: 表名
        :param kwargs: 字典格式数据[字段名与字段值]
        :return: 新增数据的ID
        """
        fields = kwargs.keys()
        fields_params = [f'%({item})s' for item in fields]
        self.sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(fields_params)})"
        with self.__conn.cursor() as cursor:
            try:
                cursor.execute(self.sql, kwargs)
                self.__conn.commit()
                return cursor.lastrowid
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def insert_many(self, table, data):
        """
        添加多条数据
        :param table: 表名
        :param data: 添加数据列表
        :return: 成功添加的数据数量
        """
        if type(data) not in [tuple, list]:
            raise self.ExecuteError("错误：添加多条数据，参数data格式必须是元组或字典!")
        if len(data) < 1:
            raise self.ExecuteError("错误，待添加必须至少1条！")

        fields = data[0].keys()
        fields_params = [f'%({item})s' for item in fields]
        self.sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(fields_params)})"
        with self.__conn.cursor() as cursor:
            try:
                result = cursor.executemany(self.sql, data)
                self.__conn.commit()
                return result
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def get_one(self, sql):
        """
        查询一条数据
        :param sql: 原生DQL
        :return: 查询的第一条数据结果[字典格式]
        """
        with self.__conn.cursor() as cursor:
            try:
                self.sql = sql
                cursor.execute(self.sql)
                return cursor.fetchone()
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def get_all(self, sql):
        """
        查询多条数据
        :param sql: 原生DQL
        :return: 列表结构的所有查询结果
        """
        with self.__conn.cursor() as cursor:
            try:
                self.sql = sql
                cursor.execute(self.sql)
                return cursor.fetchall()
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def update(self, table, condition=None, **kwargs):
        """
        更新数据
        :param table: 表名
        :param condition: 更新条件，原生SQL语句
        :param kwargs: 字段参数
        :return: 受影响行数
        """
        fields = ', '.join([f"{item}=%({item})s" for item in kwargs.keys()])
        self.sql = f"UPDATE {table} SET {fields} WHERE {condition}"
        print(self.sql)
        with self.__conn.cursor() as cursor:
            try:
                result = cursor.execute(self.sql, kwargs)
                self.__conn.commit()
                return result
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def delete(self, table, condition=None):
        """
        删除数据
        :param table: 表名
        :param condition: 删除条件，原生SQL语句
        :return: 受影响行数
        """
        self.sql = f"DELETE FROM {table} WHERE {condition}"
        print(self.sql)
        with self.__conn.cursor() as cursor:
            try:
                result = cursor.execute(self.sql)
                self.__conn.commit()
                return result
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def count(self, table, condition=None):
        """
        统计数据表中符合条件的总数量
        :param table: 表名
        :param condition: 过滤条件，原生SQL语句
        :return:
        """
        where_sql = ""
        if condition:
            where_sql = f"WHERE {condition}"

        self.sql = f"SELECT count(id) as c FROM {table} {where_sql}"
        with self.__conn.cursor() as cursor:
            try:
                cursor.execute(self.sql)
                return cursor.fetchone()["c"]
            except pymysql.Error as e:
                raise self.ExecuteError(e)

    def truncate(self, table):
        """
        重置表
        :param table: 表名
        :return:
        """
        self.sql = f"TRUNCATE TABLE {table}"
        print(self.sql)
        with self.__conn.cursor() as cursor:
            try:
                result = cursor.execute(self.sql)
                self.__conn.commit()
                return result
            except pymysql.Error as e:
                raise self.ExecuteError(e)


if __name__ == '__main__':
    config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123",
        "database": "students",
    }

    with DB(config) as db:
        # """添加一条数据"""
        # data = {
        #     "name": "李小白",
        #     "sex": 1,
        #     "class": 306,
        #     "age": 18,
        #     "description": "不想说话~"
        # }
        # res = db.insert("student", **data)
        # print(res)


        # """添加多条数据"""
        # data = [
        #     {
        #         "name": "李大白",
        #         "sex": 1,
        #         "class": 302,
        #         "age": 18,
        #         "description": "1-不想说话~"
        #     },
        #     {
        #         "name": "李中白",
        #         "sex": 1,
        #         "class": 307,
        #         "age": 18,
        #         "description": "2-不想说话~"
        #     },
        # ]
        # res = db.insert_many("student", data)
        # print(res)

        # """查询一条数据"""
        # result = db.get_one("select id,name from student")
        # print(result)

        # """查询多条数据"""
        # result = db.get_all("select id,name from student")
        # print(result)

        """更新数据"""
        # res = db.update("student", "id>=115", name="不白", age=16, description="就是说一句话....")
        # print(res)

        """删除数据"""
        # res = db.delete("student", "id in (115,116)")
        # print(res)

        """查询数据总数"""
        # res = db.count("student")
        # print(res)
        # res = db.count("student", "class=301")
        # print(res)

        """重置表状态"""
        db.truncate("goods")

```

注意：我们一般不会在代码层面，对数据表、数据库进行创建或删除，否则存在相当大的安全隐患。



#### 异步操作MySQL

针对异步操作MySQL，我们直接使用第三方封装号的开源模块：aiomysql。aiomysql实际上就是pymysql的异步封装，所以针对数据操作，在使用过程中，基本所有的方法名与参数都是pymysql是类似的

安装aiomysql

```bash
pip install aiomysql
```

##### 快速使用

```python
import asyncio, aiomysql

settings = {
    "host":"127.0.0.1",
    "port": 3306,
    "database": "students",
    "password": "123",
    "user": "root",
}


async def main():
    # 基于连接池连接数据库
    pool = await aiomysql.create_pool(
        host=settings["host"],
        port=settings["port"],
        user=settings["user"],
        password=settings["password"],
        db=settings["database"],
        charset="utf8mb4",
        cursorclass=aiomysql.cursors.DictCursor,
        minsize=5,   # 最小连接数，默认在初始化创建5个数据库连接对象在连接池中
        maxsize=20,  # 最多连接数，当数据库并发下，最多创建20个数据库连接对象在连接池中
        echo=True,   # 设置打印内部执行的SQL语句
    )

    async with pool.acquire() as conn:
        """基于互斥锁，从连接池中获取一个数据库连接对象"""
        async with conn.cursor() as cursor:
            """创建一个游标"""
            # 异步执行SQL语句
            await cursor.execute("SELECT * from student")
            # 异步获取结果
            # fetchmany(3)  # 获取指定数量
            # fetchone      # 获取一条
            # fetchall      # 获取所有
            data = await cursor.fetchmany(3)
            data = await cursor.fetchall()
            print(data)

    pool.close()
    await pool.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())

```

如果觉得aiomysql对于数据库的操作比较底层，想要更加方便的操作数据库，则可以类似上面DB数据库工具类，对aiomysql也进行一次异步封装即可。



### SQLAlchemy

SQLAlchemy 是 Python 著名开源的 ORM 工具包（也叫框架）。通过 ORM，开发者可以用面向对象的方式来操作数据库，不再需要编写 SQL 语句,支持绝大部分流行的关系型数据库。

官方文档：https://www.sqlalchemy.org/



#### ORM框架

ORM是对象关系映射器（Object Relational Mapper）的简写，是一种对数据库底层的SQL语句进行封装，然后对外提供面向对象操作的一种数据库操作方式。

O是Object，也就**类对象**的意思。

R是Relational，译作联系或关系，也就是关系型数据库中**数据表**的意思。

M是Mapper，是**映射**的意思，表示类对象和数据表的映射关系。

ORM框架会帮我们把类对象和数据表进行了一对一的映射，让我们可以**通过类对象提供的属性或方法就可以操作对应的数据表**。

ORM框架还可以**根据我们设计的类自动帮我们生成数据表**，省去了我们自己建表的过程。这个操作一般叫数据迁移（migrate）

我们后面的学习过程中，要开发项目一般都选择在项目内嵌ORM框架，这样就可以不需要直接编写SQL语句进行数据库操作，而是通过定义模型类对象，操作模型类对象即可完成对数据库中数据的增删改查和数据表的创建删除等操作。

![image-20220610101828521](assets/image-20220610101828521.png)

##### ORM的优点

> - 数据模型类都在一个地方定义，容易更新和维护，也利于代码复用。
>- ORM 有现成的工具，很多功能都可以自动完成，比如数据消除、预处理、事务等等。
> - 使用了ORM以后迫使开发者在开发项目时采用MVC架构，ORM 就是天然的 Model（M模型），最终使代码组织更清晰，更加容易维护。
>- 基于ORM 的业务代码比较简单，代码量少，语义性好，容易理解。
> - 新手对于复杂业务容易写出性能不好的原生SQL，但有了ORM不必编写复杂的SQL语句, 只需要通过操作模型对象即可同步修改数据表中的数据.
>- 开发中应用ORM将来如果要切换底层数据库，只需要切换ORM底层对接数据库的驱动类和配置信息即可，例如从mysql数据库切换成postgreSQL数据库，则把底层驱动(mysqldb或pymysql) 切换成 psycopg2，然后把连接配置修改即可。开发代码基本不需要调整与修改。

##### ORM也有缺点

> - ORM库不是轻量级模块工具，初学者需要花很多精力学习和使用ORM模块，甚至不同的ORM框架，会存在不同操作代码。
>
> - 对于复杂的数据业务查询，ORM表达起来比原生SQL语句要更加困难和复杂，例如子查询，事务，连表查询。
>
> - ORM操作数据库的性能要比使用原生的SQL语句差。
>
>   因为直接使用pymysql或mysqldb数据库驱动，只需发送SQL语句即可，而ORM不仅要发送，还要在发送前组装拼接SQL语句，里面使用了大量的正则以及字符串拼接，所以性能低下。
>
> - ORM 抽象掉了底层数据库，开发者无法了解底层的数据库操作，也无法定制一些特殊的 SQL。
>
>   针对这种情况，可以使用pymysql或mysqlDB另外编写SQl语句操作即可，用了ORM并不表示当前项目不能使用别的数据库操作模块了。



模块安装

```bash
pip install -U SQLAlchemy
# 注意，使用ORM务必保证已经安装了ORM底层所需要的数据库驱动模块，如pymysql或mysqlDB

# 如果SQLAlchemy底层使用pymysql连接数据库，则安装如下
# pip install pymysql
# 如果SQLAlchemy底层使用MySQLdb连接数据库，则安装如下
# pip install mysqlclient -i https://pypi.douban.com/simple
```



#### 快速入门

##### 初始化配置

db.py，代码：

```python
# from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text  # 字段、整型
from sqlalchemy import *


# 1. 创建数据库驱动（引擎）
engine = create_engine(
    # 连接数据库的URL
    # url="驱动名称://账户:密码@IP地址:端口/数据库名?charset=utf8mb4",  # 如果底层驱动是pymysql
    # url="mysql+pymysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是pymysql
    url="mysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是MySQLdb
    echo=True,  # 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
    pool_size=10,  # 连接池的数据库连接数量，默认为5个，设置为0时表示连接无限制
    max_overflow=30,    # 连接池的数据库连接最大数量，默认为10个
    pool_recycle=60*30  # 设置时间以限制数据库连接多久没使用则自动断开（指代max_overflow-pool_size），单位：秒
)

# 基于底层数据库驱动建立数据库连接会话，相当于cursor游标
DbSession = sessionmaker(bind=engine)
session = DbSession()
# 模型类对象的基类，内部提供了数据库的基本操作以及共同方法
Model = declarative_base()

```



##### 数据迁移

基于上面初始化模块，创建模型，如果模型绑定的数据表不存在，则自动新建数据表。数据表存在，则不会新建。这个操作一般称之为数据迁移（Migrate）。

代码：

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    # 1. 把当前模型与数据库中指定的表名进行关联
    __tablename__ = "tb_student"

    # 2. 绑定字段信息
    # 模型属性 = db.Column(数据类型, 字段约束)
    # primary_key=True 设置当前字段为整型，主键，SQLAlchemy会自动设置auto_increment为自增
    id = db.Column(db.Integer, primary_key=True)
    # db.String(20) 设置当前字段为字符串，varchar(20)
    name = db.Column(db.String(20))
    # db.Boolean 设置当前字段为布尔类型，本质上在数据库中是 0/1
    # default=True 设置当前字段的默认值
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    # 当前字段名如果是python关键字，则需要给第一个参数则字段的别名使用
    # SmallInteger = SMALLINT
    classes = db.Column("class", db.SMALLINT)
    # Text 表示设置当前字段为文本格式，因为文本与字符串varchar在python都是字符串，所以此处可以兼容
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    # DateTime 设置字段为日期时间类型
    # 注意：如果设置当前日期时间为默认值，不能在now加上小括号
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)


if __name__ == '__main__':
    # 如果没有提前声明模型中的数据表，则可以采用以下代码生成新的数据表，这个操作叫数据迁移
    # 如果数据库中已经声明了有数据表，则不会继续生成新的数据表
    db.Model.metadata.create_all(db.engine)
```

> 在实际开发中，因为中大型的IT企业，开发团队相对比较完整，所以会存在DBA工程师，所以有些公司是不使用数据迁移的，因为在我们编写服务端代码之前，DBA就已经设计好整个项目的数据表结构了。当然，也有些DBA比较坑，所以我们也要对这种数据迁移要了解，以防万一。同时，我们不能依赖于ORM提供的数据迁移功能，因为在数据库操作层面，最终的核心还是SQL语句。

##### 字段类型

官方文档：https://docs.sqlalchemy.org/en/14/core/type_basics.html#generic-types

| ORM模型提供字段类型 | 对应的python中数据类型 | 描述                                                         |
| :------------------ | :--------------------- | :----------------------------------------------------------- |
| **Integer**         | int                    | 普通整数，一般是32位                                         |
| **SmallInteger**    | int                    | 取值范围小的整数，一般是16位                                 |
| **BigInteger**      | int                    | 不限制精度的整数，替代integer                                |
| Float               | float                  | 浮点数                                                       |
| **Numeric**         | decimal.Decimal        | 普通数值，一般是32位                                         |
| **String**          | str                    | 变长字符串                                                   |
| **Text**            | str                    | 变长字符串，对较长或不限长度的字符串做了优化                 |
| Unicode             | unicode                | 变长Unicode字符串                                            |
| UnicodeText         | unicode                | 变长Unicode字符串，对较长或不限长度的字符串做了优化          |
| **Boolean**         | bool                   | 布尔值                                                       |
| **DateTime**        | datetime.datetime      | 日期和时间                                                   |
| Date                | datetime.date          | 日期                                                         |
| Time                | datetime.time          | 时间                                                         |
| LargeBinary         | bytes                  | 二进制文件内容                                               |
| **Enum**            | enum.Enum              | 枚举类型，相当于django的choices，但是功能没有choices那么强大 |



##### 字段约束

| 选项名          | 说明                                                        |
| :-------------- | :---------------------------------------------------------- |
| **primary_key** | 如果为True，代表当前数据表的主键                            |
| **unique**      | 如果为True，为这列创建唯一 索引，代表这列不允许出现重复的值 |
| **index**       | 如果为True，为这列创建普通索引，提高查询效率                |
| **nullable**    | 如果为True，允许有空值，如果为False，不允许有空值           |
| **default**     | 为这列定义默认值                                            |

##### 数据操作

###### 添加一条数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)


if __name__ == '__main__':
    """添加一条数据"""
    student = Student(
        name="小明1号",
        classes="305",
        sex=True,
        age=18,
        description="滚出去..",
    )
    db.session.add(student)  # 相当于 pymysql的execute
    db.session.commit()      # 相当于 事务提交 commit
```

###### 添加多条数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)


if __name__ == '__main__':
    """添加多条数据"""
    student1 = Student(name="小明1号", classes="302", sex=True, age=18, description="滚出去..")
    student2 = Student(name="小明2号", classes="303", sex=True, age=18, description="滚出去..")
    student3 = Student(name="小明3号", classes="304", sex=True, age=18, description="滚出去..")
    student4 = Student(name="小明4号", classes="305", sex=True, age=18, description="滚出去..")

    db.session.add_all([student1, student2,student3,student4])  # 相当于 pymysql的executemany
    db.session.commit()      # 相当于 事务提交 commit

```

###### 查询一条数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    # def __str__(self):
    #     return f"<{self.__class__.__name__} {self.name}>"

    def __repr__(self):
        """
        当实例对象被使用print打印时，自动执行此处当前，
        当前__repr__使用与上面__str__一致，返回值必须时字符串格式，否则报错！！！
        """
        return f"<{self.__class__.__name__} {self.name}>"


if __name__ == '__main__':
    """查询一条数据"""

    """
    get 用于根据主键值获取一条，如果查不到数据，则返回None，查到结果则会被ORM底层使用当前模型类来进行实例化成模型对象
    get 可以接收1个或多个主键参数，只能作为主键值
    """
    # get(4) 相当于 where id=4;
    student = db.session.query(Student).get(4)  # 如果查询的是联合主键 写法： get((5,10)) 或 get({"id": 5, "version_id": 10})
    print(student)
    # <__main__.Student object at 0x7f4161c69520> <class '__main__.Student'>


    """
    使用first获取查询结果集的第一个结果
    first 不能接收任何参数，所以一般配合filter或者filter_by 来进行使用的
    """
    student = db.session.query(Student).first()

    # 获取属性值
    if student:
        print(f"id={student.id}, name={student.name}, age={student.age}")
```

###### 查询多条数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"


if __name__ == '__main__':
    """查询多条数据"""
    student_list = db.session.query(Student).all()
    print(student_list)

    # 基于循环输出每一个模型对象中的属性
    for student in student_list:
        print(f"id={student.id}, name={student.name}, classes={student.classes}")
 
```

###### 过滤条件查询

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def todict(self):
        return {
            "id": self.id,
            "name": self.name
        }


if __name__ == '__main__':
     """模型对象转字典"""
    # student_list = db.session.query(Student).all()
    # print([student.todict() for student in student_list])
    
    """过滤条件查询"""
    """
    filter_by - 精确查询
    filter_by支持值相等=号操作，不能使用大于、小于或不等于的操作一律不能使用
    """
    # # 单个字段条件
    # students = db.session.query(Student).filter_by(name="小明1号").all()
    # print(students)

    # # 多个and条件
    # students = db.session.query(Student).filter_by(sex=1, age=18).all()
    # print(students)

    """
    filter - 匹配查询
    支持所有的运算符表达式，比filter精确查询要更强大
    注意：条件表达式中的字段名必须写上模型类名
    filter中的判断相等必须使用==2个等号
    """
    # # 获取查询结果集的所有数据，列表
    # students = db.session.query(Student).filter(Student.age > 17).all()
    # print(students) # [<Student 小明1号>, <Student 小明1号>, <Student 小明3号>, <Student 小明4号>]
    #
    # # 获取查询结果集的第一条数据，模型对象
    # students = db.session.query(Student).filter(Student.age < 18).first()
    # print(students) # <Student 小明1号>

    """in运算符"""
    students = db.session.query(Student).filter(Student.id.in_([1, 3, 4])).all()
    print(students) # [<Student 小明1号>, <Student 小明1号>, <Student 小明2号>]

    """多条件表达式"""
    """多个or条件"""
    # from sqlalchemy import or_
    # # 查询302或303班的学生
    # students = db.session.query(Student).filter(or_(Student.classes==303, Student.classes==302)).all()
    # print(students) # [<Student 小明1号>, <Student 小明2号>]

    """多个and条件"""
    # students = db.session.query(Student).filter(Student.age==18, Student.sex==1).all()
    # print(students) # [<Student 小明1号>, <Student 小明3号>]

    # from sqlalchemy import and_
    # students = db.session.query(Student).filter(and_(Student.age == 18, Student.sex == 1)).all()
    # print(students) # [<Student 小明1号>, <Student 小明3号>]

    """and_主要用于与or_一起使用的"""
    # 查询305的18岁男生 或者 305班的17岁女生
    from sqlalchemy import and_, or_
    # students = db.session.query(Student).filter(
    #     or_(
    #         and_(Student.classes==305, Student.age==18, Student.sex==1),
    #         and_(Student.classes==305, Student.age==17, Student.sex==2),
    #     )
    # ).all()

    students = db.session.query(Student).filter(
        and_(
            Student.classes == 305,
            or_(
                and_(Student.age == 18, Student.sex == 1),
                and_(Student.age == 17, Student.sex == 2)
            )
        )
    ).all()

    print(students) # [<Student 小明1号>, <Student 小明4号>]

```

###### 更新数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def todict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    
if __name__ == '__main__':
    """更改数据"""
    # 查询要更改的数据[目的为了让ORM实现表记录与模型对象的映射]
    student = db.session.query(Student).get(6)
    student.age = 16
    student.classes = 301
    db.session.commit()

```



###### 删除数据

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def todict(self):
        return {
            "id": self.id,
            "name": self.name
        }


if __name__ == '__main__':
    """更改数据"""
    # 查询要删除的数据[目的为了让ORM实现表记录与模型对象的映射]
    student = db.session.query(Student).get(6)
    db.session.delete(student)
    db.session.commit()

```



###### 其他操作

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def todict(self):
        return {
            "id": self.id,
            "name": self.name,
            "classes": self.classes,
            "age": self.age,
        }


if __name__ == '__main__':
    """限制结果数量"""
    # student_list = db.session.query(Student).limit(3).all()
    # print(student_list)

    # """结果排序"""
    # student_list = db.session.query(Student).order_by(Student.classes.asc(), Student.age.desc()).all()
    # print([student.todict() for student in student_list])

    # # 事务操作
    # db.session.begin()
    # db.session.commit()
    # db.session.rollback()
```



###### 原生SQL操作

针对开发中一些复杂的业务，往往使用ORM提供的方法操作会极其复杂或者书写比较困难，或根本提供对应的方法，此时我们可以考虑直接写原生SQL。

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def todict(self):
        return {
            "id": self.id,
            "name": self.name,
            "classes": self.classes,
            "age": self.age,
        }


if __name__ == '__main__':
    """DQL-读取数据"""
    # # 返回游标对象
    # cursor = db.session.execute("select * from tb_student")
    # # # 获取一条结果,mappings方法表示把结果从元组转换成字典
    # student = cursor.mappings().fetchone()
    # print(student)

    # # 获取指定数量结果
    # student_list = cursor.mappings().fetchmany(2)
    # print(student_list)

    # # 获取所有结果
    # student_list = cursor.mappings().fetchall(cursor=)
    # print(student_list)


    """DML-写入数据"""
    sql = "insert into tb_student(name, class, age, sex, description) values(:name, :class, :age, :sex, :description)"
    data = {
        "class": "305",
        "age": 19,
        "name": "xiaohong",
        "sex": 0,
        "description": ".....",
    }

    cursor = db.session.execute(sql, params=data)
    db.session.commit()
    print(cursor.lastrowid)  # 获取最后添加的主键ID

```

###### 模型对象转字典

```python
import db
from datetime import datetime


# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

if __name__ == '__main__':
    student = db.session.query(Student).get(1)
    # 不仅会返回当前模型的字段属性，
    # 还会返回当前对象与数据表的映射关系
    # 如果有使用了外键，还会记录表与表之间的关联关系
    print(student.__dict__)
```



#### 异步操作sqlalchemy

官方文档：https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html

###### 初始化

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import *

# 1. 创建数据库驱动（引擎）
engine = create_async_engine(
    # 连接数据库的URL
    # url="驱动名称://账户:密码@IP地址:端口/数据库名?charset=utf8mb4",  # 如果底层驱动是greenlet
    url="mysql+aiomysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是aiomysql
    # url="mysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是MySQLdb
    echo=True,  # 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
    pool_size=10,  # 连接池的数据库连接数量，默认为5个，设置为0时表示连接无限制
    max_overflow=30,    # 连接池的数据库连接最大数量，默认为10个
    pool_recycle=60*30  # 设置时间以限制数据库连接多久没使用则自动断开（指代max_overflow-pool_size），单位：秒
)

# 基于底层数据库驱动建立数据库连接会话，相当于cursor游标
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# 模型类对象的基类，内部提供了数据库的基本操作以及共同方法
Model = declarative_base()


```



###### 基本使用

```python
import asyncio
import async_db as db
from datetime import datetime

# 1. 创建一个与数据库对应的模型类对象
class Student(db.Model):
    """学生表模型"""
    __tablename__ = "async_student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    sex = db.Column(db.Boolean, default=True)
    age = db.Column(db.SmallInteger)
    classes = db.Column("class", db.SMALLINT)
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=1)
    addtime = db.Column(db.DateTime, default=datetime.now)
    orders = db.Column(db.SMALLINT, default=1)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

async def main():
    # 异步数据迁移
    async with db.engine.begin() as conn:
        # 删除当前程序中所有的模型对应的数据表
        # await conn.run_sync(Model.metadata.drop_all)

        # 创建当前程序中所有的模型的数据表，如果数据表不存在的情况下
        await conn.run_sync(db.Model.metadata.create_all)

    # 开启会话
    async with db.async_session() as session:
        # 开启事务
        async with session.begin():
            """DQL - 查询数据"""
            # # 拼接SQL语句
            sql = db.select(Student).filter(Student.classes == 305).order_by(Student.id)
            print(sql)
            # 异步执行SQL语句
            student = await session.execute(sql)
            # # 获取一个结果
            # print(student.first())
            # 获取多个结果
            # print(student.mappings().all())

            """DML - 写入数据"""
            # student1 = Student(name="小明1号", classes="302", sex=True, age=18, description="滚出去..")
            # student2 = Student(name="小明2号", classes="303", sex=True, age=18, description="滚出去..")
            # student3 = Student(name="小明3号", classes="304", sex=True, age=18, description="滚出去..")
            # student4 = Student(name="小明4号", classes="305", sex=True, age=18, description="滚出去..")
            # # 添加一条数据
            # session.add(student1)
            # # 添加多条数据
            # session.add_all([student1, student2, student3,student4])

            # 异步提交事务
            await session.commit()

if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```



