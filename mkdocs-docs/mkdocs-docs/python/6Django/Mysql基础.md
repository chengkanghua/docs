# Mysql基础

# Mysql

简单来说，数据库就是一个存储数据的仓库，它将数据按照特定的规律存储在磁盘上。为了方便用户组织和管理数据，其专门提供了数据库管理系统。通过数据库管理系统，用户可以有效的组织和管理存储在数据库中的数据。本教程所要讲解的 MySQL，就是一种非常优秀的数据库管理系统。

# 一、sql介绍

## 1.1、什么是sql？

对数据库进行查询和修改操作的语言叫做 SQL（Structured Query Language，结构化查询语言）。SQL是专为数据库而建立的操作命令集，是一种功能齐全的数据库语言。

SQL 是一种数据库查询和程序设计语言，用于存取数据以及查询、更新和管理关系数据库系统。与其他程序设计语言（如 C语言、Java 等）不同的是，SQL 由很少的关键字组成，每个 SQL 语句通过一个或多个关键字构成。

在使用它时，只需要发出“做什么”的命令，“怎么做”是不用使用者考虑的。SQL功能强大、简单易学、使用方便，已经成为了数据库操作的基础，并且现在几乎所有的数据库(Oracle、DB2、Sybase、SQL Server )均支持sql。

## 1.2、sql规范

<1> 在数据库系统中，SQL语句不区分大小写(建议用大写) 。但字符串常量区分大小写。建议命令大写，表名库名小写；

<2> SQL语句可单行或多行书写，以“;”结尾。关键词不能跨多行或简写。

<3> 用空格和缩进来提高语句的可读性。子句通常位于独立行，便于编辑，提高可读性。

```sql
SELECT * FROM tb_table
            WHERE NAME="YUAN";
```



<4> 注释：

```sql

-- 单行注释
/*
多行注释
*/
```



<5> sql语句可以折行操作

## 1.3、sql构成

（1）数据定义语言（Data Definition Language，DDL）

```sql

-- 用来创建或删除数据库以及表等对象，主要包含以下几种命令：

-- DROP：删除数据库和表等对象
-- CREATE：创建数据库和表等对象
-- ALTER：修改数据库和表等对象的结构
```



(2）数据操作语言（Data Manipulation Language，DML）

```sql
-- 用来变更表中的记录，主要包含以下几种命令：

-- SELECT：查询表中的数据
-- INSERT：向表中插入新数据
-- UPDATE：更新表中的数据
-- DELETE：删除表中的数据
```



(3）数据查询语言（Data Query Language，DQL）

用来查询表中的记录，主要包含 SELECT 命令，来查询表中的数据。

(4）数据控制语言（Data Control Language，DCL）

```sql
-- 用来确认或者取消对数据库中的数据进行的变更。除此之外，还可以对数据库中的用户设定权限。主要包含以下几种命令：

-- GRANT：赋予用户操作权限
-- REVOKE：取消用户的操作权限
-- COMMIT：确认对数据库中的数据进行的变更
-- ROLLBACK：取消对数据库中的数据进行的变更
```



# 二、数据库操作

```sql

-- 1.创建数据库（在磁盘上创建一个对应的文件夹）
    create database [if not exists] db_name [character set xxx] 
   
-- 2.查看数据库
    show databases;  -- 查看所有数据库
    SHOW DATABASES LIKE '%test%';-- 查看名字中包含 test 的数据库
    show create database db_name; -- 查看数据库的创建方式

-- 3.修改数据库
    alter database db_name [character set xxx] 

-- 4.删除数据库
    drop database [if exists] db_name;
    
-- 5.使用数据库
    use db_name; -- 切换数据库  注意：进入到某个数据库后没办法再退回之前状态，但可以通过use进行切换
    select database(); --  查看当前使用的数据库
```



>   使用 DROP DATABASE 命令时要非常谨慎，在执行该命令后，MySQL 不会给出任何提示确认信息。DROP DATABASE 删除数据库后，数据库中存储的所有数据表和数据也将一同被删除，而且不能恢复。因此最好在删除数据库之前先将数据库进行备份。

# 三、数据表操作

数据表是数据库的重要组成部分，每一个数据库都是由若干个数据表组成的。比如，在电脑中一个文件夹有若干excel文件。这里的文件夹就相当于数据库，excel文件就相当于数据表。

## 3.1、创建数据表

```sql
-- 语法
CREATE TABLE tab_name(
            field1 type [约束条件],
            field2 type,
            ...
            fieldn type    -- 一定不要加逗号，否则报错！
        )[character set utf8];
```



案例：

```sql
 CREATE TABLE employee(
            id int primary key auto_increment ,
            name varchar(20),
            gender bit default 1,
            birthday date,
            department varchar(20),
            salary double(8,2) unsigned,
            resume text
          )character set=utf8;
```



```
-- show tables;
```



## 3.2、查看表

```sql
mysql> desc employee;    -- 查看表结构,等同于show columns from tab_name  
+------------+----------------------+------+-----+---------+----------------+
| Field      | Type                 | Null | Key | Default | Extra          |
+------------+----------------------+------+-----+---------+----------------+
| id         | int(11)              | NO   | PRI | NULL    | auto_increment |
| name       | varchar(20)          | YES  |     | NULL    |                |
| gender     | bit(1)               | YES  |     | b'1'    |                |
| birthday   | date                 | YES  |     | NULL    |                |
| department | varchar(20)          | YES  |     | NULL    |                |
| salary     | double(8,2) unsigned | YES  |     | NULL    |                |
| resume     | text                 | YES  |     | NULL    |                |
+------------+----------------------+------+-----+---------+----------------+


show tables 　　　　　　　　　　　-- 查看当前数据库中的所有的表
show create table tab_name      -- 查看当前数据库表建表语句 
```



## 3.3、修改表结构

```sql
   -- (1) 增加列(字段)
      ALTER TABLE <表名> ADD <新字段名><数据类型>[约束条件]［first｜after 字段名］;
      -- 添加多个字段
      alter table users2 
            add addr varchar(20),
            add age  int first,
            add birth varchar(20) after name;

   -- (2) 修改某字段类型
      ALTER TABLE <表名> MODIFY <字段名> <数据类型> [完整性约束条件]［first｜after 字段名］;
   -- (3) 修改某字段名
      ALTER TABLE <表名> CHANGE <旧字段名> <新字段名> <新数据类型>  [完整性约束条件]［first｜after 字段名］;；
   -- (4) 删除某字段
      ALTER TABLE <表名> DROP <字段名>；
   -- (5) 修改表名  
      ALTER TABLE <旧表名> RENAME [TO] <新表名>；
   -- (6)修该表所用的字符集    
      ALTER TABLE 表名 [DEFAULT] CHARACTER SET <字符集名> 
```



## 3.4、删除表

```sql
DROP TABLE [IF EXISTS] 表名1 [ ,表名2, 表名3 ...]
```



# 四、表记录操作

## 4.1、添加记录

INSERT 语句有两种语法形式，分别是 INSERT…VALUES 语句和 INSERT…SET 语句。

#### (1) INSERT…VALUES语句

```sql
INSERT [INTO] <表名> [ <列名1> [ , … <列名n>] ] VALUES (值1) [… , (值n) ];

```



>   1.  指定需要插入数据的列名。若向表中的所有列插入数据，则全部的列名均可以省略，直接采用 INSERT<表名>VALUES(…) 即可。
>
>   2.  INSERT 语句后面的列名称顺序可以不是 表定义时的顺序，即插入数据时，不需要按照表定义的顺序插入，只要保证值的顺序与列字段的顺序相同就可以。
>
>   3.  使用 INSERT…VALUES 语句可以向表中插入一行数据，也可以插入多行数据；
>
>       ```sql
>       INSERT [INTO] <表名> [ <列名1> [ , … <列名n>] ] VALUES (值1…,值n),
>                                                             (值1…,值n),
>                                                             ...
>                                                             (值1…,值n);
>       -- 用单条 INSERT 语句处理多个插入要比使用多条 INSERT 语句更快。
>       ```
>
>       

案例：

```sql
INSERT employee (name,gender,birthday,salary,department) VALUES 
                                                               ("yuan",1,"1985-12-12",8000,"教学部"),
                                                               ("alvin",1,"1987-08-08",5000,"保安部"),
                                                               ("rain",1,"1990-06-06",20000,"销售部");
```



#### (2) INSERT…SET语句

```sql
INSERT INTO <表名>
       SET <列名1> = <值1>,
           <列名2> = <值2>,
            …
```



此语句用于直接给表中的某些列指定对应的列值，即要插入的数据的列名在 SET 子句中指定。对于未指定的列，列值会指定为该列的默认值。

## 4.2、查询记录

标准语法：

```sql
-- 查询语法：

   SELECT *|field1,filed2 ...   FROM tab_name
                  WHERE 条件
                  GROUP BY field
                  HAVING 筛选
                  ORDER BY field
                  LIMIT 限制条数


-- Mysql在执行sql语句时的执行顺序：
                -- from  where  select  group by  having order by
```



准备数据：

```sql
CREATE TABLE emp(
    id       INT PRIMARY KEY AUTO_INCREMENT,
    name     VARCHAR(20),
    gender   ENUM("male","female","other"),
    age      TINYINT,
    dep      VARCHAR(20),
    city     VARCHAR(20),
   salary    DOUBLE(7,2)
)character set=utf8;


INSERT INTO emp (name,gender,age,dep,city,salary) VALUES
                ("yuan","male",24,"教学部","河北省",8000),
                ("eric","male",34,"销售部","山东省",8000),
                ("rain","male",28,"销售部","山东省",10000),
                ("alvin","female",22,"教学部","北京",9000),
                ("George", "male",24,"教学部","河北省",6000),
                ("danae", "male",32,"运营部","北京",12000),
                ("Sera", "male",38,"运营部","河北省",7000),
                ("Echo", "male",19,"运营部","河北省",9000),
                ("Abel", "female",24,"销售部","北京",9000);


```



### 4.2.1、查询字段（select）

```sql
mysql> SELECT  * FROM emp;
+----+--------+--------+------+--------+--------+----------+
| id | name   | gender | age  | dep    | city   | salary   |
+----+--------+--------+------+--------+--------+----------+
|  1 | yuan   | male   |   24 | 教学部 | 河北省 |  8000.00 |
|  2 | eric   | male   |   34 | 销售部 | 山东省 |  8000.00 |
|  3 | rain   | male   |   28 | 销售部 | 山东省 | 10000.00 |
|  4 | alvin  | female |   22 | 教学部 | 北京   |  9000.00 |
|  5 | George | male   |   24 | 教学部 | 河北省 |  6000.00 |
|  6 | danae  | male   |   32 | 运营部 | 北京   | 12000.00 |
|  7 | Sera   | male   |   38 | 运营部 | 河北省 |  7000.00 |
|  8 | Echo   | male   |   19 | 运营部 | 河北省 |  9000.00 |
|  9 | Abel   | female |   24 | 销售部 | 北京   |  9000.00 |
+----+--------+--------+------+--------+--------+----------+
mysql> SELECT  name,dep,salary FROM emp;
+--------+--------+----------+
| name   | dep    | salary   |
+--------+--------+----------+
| yuan   | 教学部 |  8000.00 |
| eric   | 销售部 |  8000.00 |
| rain   | 销售部 | 10000.00 |
| alvin  | 教学部 |  9000.00 |
| George | 教学部 |  6000.00 |
| danae  | 运营部 | 12000.00 |
| Sera   | 运营部 |  7000.00 |
| Echo   | 运营部 |  9000.00 |
| Abel   | 销售部 |  9000.00 |
+--------+--------+----------+
```



### 4.2.2、where语句

```sql
-- where字句中可以使用：

         -- 比较运算符：
                        > < >= <= <> !=
                        between 80 and 100 值在10到20之间
                        in(80,90,100) 值是10或20或30
                        like 'yuan%'
                        /*
                        pattern可以是%或者_，
                        如果是%则表示任意多字符，此例如唐僧,唐国强
                        如果是_则表示一个字符唐_，只有唐僧符合。两个_则表示两个字符：__
                        */

         -- 逻辑运算符
                        在多个条件直接可以使用逻辑运算符 and or not
                        
         -- 正则 
                      SELECT * FROM emp WHERE emp_name REGEXP '^yu';
                      SELECT * FROM emp WHERE name REGEXP 'n$';
                      
```



练习：

```sql
-- 查询年纪大于24的员工
SELECT * FROM emp WHERE age>24;

-- 查询教学部的男老师信息
SELECT * FROM emp WHERE dep="教学部" AND gender="male";
```



### 4.2.3、order：排序

按指定的列进行，排序的列即可是表中的列名，也可以是select语句后指定的别名。

```sql
-- 语法：

select *|field1,field2... from tab_name order by field [Asc|Desc]
         -- Asc 升序、Desc 降序，其中asc为默认值 ORDER BY 子句应位于SELECT语句的结尾。
```



练习：

```sql
-- 按年龄从高到低进行排序
SELECT * FROM emp ORDER BY age DESC ;

-- 按工资从低到高进行排序
SELECT * FROM emp ORDER BY salary;

-- 先按工资排序，工资相同的按年龄排序
SELECT * FROM emp ORDER BY salary,age;
```



### 4.2.4、group by：分组查询

GROUP BY 语句根据某个列对结果集进行分组。分组一般配合着聚合函数完成查询。

**常用聚合(统计)函数**

-   `max()`：最大值。
-   `min()`：最小值。
-   `avg()`：平均值。
-   `sum()`：总和。
-   `count()`：个数。

在MySQL的SQL执行逻辑中，where条件必须放在group by前面！也就是先通过where条件将结果查询出来，再交给group by去分组，完事之后进行统计，统计之后的查询用having。

练习：

```sql
-- 查询男女员工各有多少人
SELECT gender 性别,count(*) 人数 FROM emp GROUP BY gender;
 
-- 查询各个部门的人数
SELECT dep 部门,count(*) 人数 FROM emp GROUP BY dep;
 
-- 查询每个部门最大的年龄
SELECT dep 部门,max(age) 最大年纪 FROM emp GROUP BY dep;
 
-- 查询每个部门年龄最大的员工姓名
SELECT * FROM emp5 WHERE age in (SELECT max(age) FROM emp5 GROUP BY dep);
 
-- 查询每个部门的平均工资
SELECT dep 部门,avg(salary) 最大年纪 FROM emp GROUP BY dep;
 
--  查询教学部的员工最高工资:
SELECT dep,max(salary) FROM emp11 GROUP BY dep HAVING dep="教学部";
 
-- 查询平均薪水超过8000的部门
SELECT dep,AVG(salary) FROM  emp GROUP BY dep HAVING avg(salary)>8000;
 
--  查询每个组的员工姓名
SELECT dep,group_concat(name) FROM emp GROUP BY dep;
 
-- 查询公司一共有多少员工(可以将所有记录看成一个组)
SELECT COUNT(*) 员工总人数 FROM emp;
```



### 4.2.5、limit：记录条数限制

```sql
SELECT * from emp limit 1;
SELECT * from emp limit 2,5;        --  跳过前两条显示接下来的五条纪录
SELECT * from emp limit 2,2;
```



### 4.2.6、distinct：查询去重

```sql
SELECT distinct salary from emp order by salary;
```



## 4.3、更新记录

```sql
UPDATE <表名> SET 字段 1=值 1 [,字段 2=值 2… ] [WHERE 子句 ]
```



## 4.4、删除记录

```sql
DELETE FROM <表名> [WHERE 子句] [ORDER BY 子句] [LIMIT 子句]
```



>   -   `<表名>`：指定要删除数据的表名。
>   -   `ORDER BY` 子句：可选项。表示删除时，表中各行将按照子句中指定的顺序进行删除。
>   -   `WHERE` 子句：可选项。表示为删除操作限定删除条件，若省略该子句，则代表删除该表中的所有行。
>   -   `LIMIT` 子句：可选项。用于告知服务器在控制命令被返回到客户端前被删除行的最大值。

# 五、表的关联关系

## 5.1、一对多

一对多关系为关系数据库中两个表之间的一种关系，该关系中第一个表中的单个行可以与第二个表中的一个或多个行相关，但第二个表中的一个行只可以与第一个表中的一个行相关。

```sql
-- 书籍表
CREATE TABLE book(
id INT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(32),
price DOUBLE(5,2),    
pub_id INT NOT NULL
)ENGINE=INNODB CHARSET=utf8;


-- 出版社表
CREATE TABLE publisher(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(32),
email VARCHAR(32),
addr VARCHAR(32)
)ENGINE=INNODB CHARSET=utf8;

-- 插入数据
INSERT INTO book(title,price,pub_id) VALUES
('西游记',15,1),
('三国演义',45,2),
('红楼梦',66,3),
('水浒传',21,2),
('红与黑',67,3),
('乱世佳人',44,6),
('飘',56,1),
('放风筝的人',78,3);

INSERT INTO publisher(id,name,email,addr) VALUES
(1,'清华出版社',"123","bj"),
(2,'北大出版社',"234","bj"),
(3,'机械工业出版社',"345","nj"),
(4,'邮电出版社',"456","nj"),
(5,'电子工业出版社',"567","bj"),
(6,'人民大学出版社',"678","bj");
```



```sql
mysql> select * from book;
+----+------------+-------+--------+
| id | title      | price | pub_id |
+----+------------+-------+--------+
|  1 | 西游记     | 15.00 |      1 |
|  2 | 三国演义   | 45.00 |      2 |
|  3 | 红楼梦     | 66.00 |      3 |
|  4 | 水浒传     | 21.00 |      2 |
|  5 | 红与黑     | 67.00 |      3 |
|  6 | 乱世佳人   | 44.00 |      6 |
|  7 | 飘         | 56.00 |      1 |
|  8 | 放风筝的人 | 78.00 |      3 |
+----+------------+-------+--------+
8 rows in set (0.00 sec)

mysql> select * from publisher;
+----+----------------+-------+------+
| id | name           | email | addr |
+----+----------------+-------+------+
|  1 | 清华出版社     | 123   | bj   |
|  2 | 北大出版社     | 234   | bj   |
|  3 | 机械工业出版社 | 345   | nj   |
|  4 | 邮电出版社     | 456   | nj   |
|  5 | 电子工业出版社 | 567   | bj   |
|  6 | 人民大学出版社 | 678   | bj   |
+----+----------------+-------+------+
6 rows in set (0.00 sec)
```



## 5.2、多对多

多对多，在数据库中也比较常见，可以理解为是一对多和多对一的组合。要实现多对多，一般都需要有一张中间表（也叫关联表），将两张表进行关联，形成多对多的形式。

比如一本书有多个作者，一个作者可以出版多本书籍。

```sql
-- 作者表
CREATE TABLE author(
id INT PRIMARY KEY AUTO_INCREMENT,
NAME VARCHAR(32) NOT NULL
)ENGINE=INNODB CHARSET=utf8;

-- 作者表和书籍表的多对多关系表
CREATE TABLE book2author(
id INT NOT NULL UNIQUE AUTO_INCREMENT,
author_id INT NOT NULL,
book_id INT NOT NULL
)ENGINE=INNODB CHARSET=utf8;

-- 插入数据

INSERT INTO author(NAME) VALUES
('yuan'),
('rain'),
('alvin'),
('eric');

-- 插入关系数据
INSERT INTO book2author(author_id,book_id) VALUES
(1,1),
(1,2),
(2,1),
(3,3),
(3,4),
(1,3);
```



## 5.3、一对一

一对一是将数据表“垂直切分”，其实是不常见，或不常用的。也就是 A 表的一条记录对应 B 表的一条记录。

>   场景：
>
>   1.  一个系统必然有 Employee（员工表）（包含字段：EmployeeId、姓名、性别、年龄、电话、地址等），每个员工都为一个用户，所以还有张 User 表（包含字段：UserId（关联 EmployeeId）、用户名、密码、角色等），这样你会发现，整合为一张表是否不太妥当？因为，User 的记录只会在登录时用到，感觉有点违背三大范式中的“**确保每列都和主键列直接关联，而不是间接关联**”。
>   2.  还有种情况，这就要根据具体的业务来决定了。如果，当一张表的字段过于太多，而很多字段可能只有在某些情况下，才会使用到，这时也可以考虑使用一对一设计。

在我们这个例子中，比如，作者表可以有一张一对一的作者详细信息表。

```sql
CREATE TABLE authorDetail(
id INT PRIMARY KEY AUTO_INCREMENT,
tel VARCHAR(32),
addr VARCHAR(32),
author_id INT NOT NULL unique -- 也可以给author添加一个关联字段：   alter table author add authorDetail_id INT NOT NULL
)ENGINE=INNODB CHARSET=utf8;

-- 插入数据
INSERT INTO authorDetail(tel,addr,author_id) VALUES
("110","北京",1),
("911","成都",2),
("119","上海",3),
("111","广州",4);


```



>   区别于一对多，关联字段加唯一约束！

# 六、关联查询

## 6.1、子查询

子查询是 MySQL 中比较常用的查询方法，通过子查询可以实现多表关联查询。子查询指将一个查询语句嵌套在另一个查询语句中。

练习：

```sql
-- 查询乱世佳人的出版社名称
 select pub_id from book where title="乱世佳人";
 select name from publisher where id = 6;
-- 查询清华出版社出版所有书籍名称
select id from publisher where name="清华出版社";
select id,title from book where pub_id = 1;
-- 查询西游记的作者名字
select id from book where title="西游记";
select author_id from book2author where book_id=1;
select name from author where id in (1,2);
```



## 6.2、join查询

#### 6.2.1、笛卡尔积查询

```sql
mysql> select * from book,publisher;

```



![image-20210810152409411](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810152409411.png)

#### 6.2.2、内连接(inner join)

查询两张表中都有的关联数据,相当于利用条件从笛卡尔积结果中筛选出了正确的结果。

案例1：

```sql
-- 查询两张表中都有的关联数据,相当于利用条件从笛卡尔积结果中筛选出了正确的结果。

select * from book,publisher where book.pub_id=publisher.id;
OR
SELECT * FROM book INNER JOIN publisher ON book.pub_id=publisher.id;
```



![image-20210810151907238](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810151907238.png)

案例2：

```sql
SELECT * FROM book INNER JOIN book2author ON book.id=book2author.book_id;

```



![image-20210810152714427](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810152714427.png)

```sql
SELECT * FROM book INNER JOIN book2author ON book.id=book2author.book_id 
                   INNER JOIN author on book2author.author_id=author.id
```



![image-20210810152835332](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810152835332.png)

#### 6.2.3、左连接(left join)

左外连接又称为左连接，使用 **LEFT OUTER JOIN** 关键字连接两个表，并使用 ON 子句来设置连接条件。

```sql
 SELECT * FROM publisher LEFT JOIN book ON book.pub_id=publisher.id;

```



上述语法中，“表1”为基表，“表2”为参考表。左连接查询时，可以查询出“表1”中的所有记录和“表2”中匹配连接条件的记录。如果“表1”的某行在“表2”中没有匹配行，那么在返回结果中，“表2”的字段值均为空值（NULL）。

![image-20210810153258219](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810153258219.png)

#### 6.2.4、右连接(right join)

右外连接又称为右连接，右连接是左连接的反向连接。使用 **RIGHT OUTER JOIN** 关键字连接两个表，并使用 ON 子句来设置连接条件。

与左连接相反，右连接以“表2”为基表，“表1”为参考表。右连接查询时，可以查询出“表2”中的所有记录和“表1”中匹配连接条件的记录。如果“表2”的某行在“表1”中没有匹配行，那么在返回结果中，“表1”的字段值均为空值（NULL）。

```sql
 SELECT * FROM book RIGHT JOIN publisher ON book.pub_id=publisher.id;

```



![image-20210810153745139](http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/assets/image-20210810153745139.png)

# 七、约束

约束是一种限制，它通过限制表中的数据，来确保数据的完整性和唯一性。使用约束来限定表中的数据很多情况下是很有必要的。在 MySQL 中，约束是指对表中数据的一种约束，能够帮助数据库管理员更好地管理数据库，并且能够确保数据库中数据的正确性和有效性。例如，在数据表中存放年龄的值时，如果存入 200、300 这些无效的值就毫无意义了。因此，使用约束来限定表中的数据范围是很有必要的。

在 MySQL 中，主要支持以下 6 种约束：

## 7.1、主键约束

#### （1）主键约束

主键约束是使用最频繁的约束。在设计数据表时，一般情况下，都会要求表中设置一个主键。主键是表的一个特殊字段，该字段能唯一标识该表中的每条信息。

```sql
-- 方式1

CREATE TABLE t1(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20)
);

-- 方式2

CREATE TABLE t2(
  id INT NOT NULL,
  name VARCHAR(20)
);
```



>   1、一张表中最多只能有一个主键
>
>   2、表中如果没有设置主键，默认设置NOT NULL的字段为主键；此外，表中如果有多个NOT NULL的字段，则按顺序将第一个设置NOT NULL的字段设为主键。所以主键一定是非空且唯一，但非空且唯一的字段不一定是主键。
>
>   3、主键类型不一定必须是整型

#### （2）添加删除主键

```sql
 alter table t2 add primary key(id);
 alter table t2 drop primary key;
 alter table t2 add primary key(name);
```



#### （3）复合(联合)主键

所谓的复合主键 就是指你表的主键含有一个以上的字段。

所谓的联合主键，就是这个主键是由一张表中多个字段组成的。

比如，设置学生选课数据表时，使用学生编号做主键还是用课程编号做主键呢？如果用学生编号做主键，那么一个学生就只能选择一门课程。如果用课程编号做主键，那么一门课程只能有一个学生来选。显然，这两种情况都是不符合实际情况的。

实际上设计学生选课表，要限定的是一个学生只能选择同一课程一次。因此，学生编号和课程编号可以放在一起共同作为主键，这也就是联合主键了。

```sql
-- ①创建时：

create table sc (
    studentid int,
    courseid int,
    score int,
primary key (studentid,courseid)
);        
-- ②修改时：
alter table tb_name add primary key (字段1,字段2,字段3);
```



#### (4) 主键自增约束

当主键定义为自增长后，这个主键的值就不再需要用户输入数据了，而由数据库系统根据定义自动赋值。每增加一条记录，主键会自动以相同的步长进行增长。

通过给字段添加`AUTO_INCREMENT`属性来实现主键自增长

```sql
 CREATE TABLE t1(
    id INT(4) PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) 
    );
```



## 7.2、唯一约束

唯一约束（Unique Key）是指所有记录中字段的值不能重复出现。例如，为 id 字段加上唯一性约束后，每条记录的 id 值都是唯一的，不能出现重复的情况。

#### （1）创建约束

例如，在用户信息表中，要避免表中的用户名重名，就可以把用户名列设置为唯一约束。

```sql
 CREATE TABLE user(
    id INT(11) PRIMARY KEY,
    name VARCHAR(22) UNIQUE
    );
    
INSERT user (id,name) values (1,"yuan"),(2,"rain");   
INSERT user (id,name) values (3,"alvin"),(4,"alvin");
-- ERROR 1062 (23000): Duplicate entry 'alvin' for key 'name'
```



#### （2）改表时添加删除唯一约束

```sql
ALTER TABLE <表名> DROP INDEX <唯一约束名>;  -- 删除唯一约束
ALTER TABLE <数据表名> ADD CONSTRAINT <唯一约束名> UNIQUE(<列名>);  -- 添加唯一约束
```



```sql
ALTER TABLE user  DROP INDEX name;
ALTER TABLE user ADD CONSTRAINT NAME_INDEX UNIQUE(name);
```



## 7.3、非空约束

非空约束用来约束表中的字段不能为空。比如，在用户信息表中，如果不添加用户名，那么这条用户信息就是无效的，这时就可以为用户名字段设置非空约束。

创建表时可以使用`NOT NULL`关键字设置非空约束

```sql
CREATE TABLE user(
    id INT(11) PRIMARY KEY,
    name VARCHAR(22) UNIQUE NOT NULL
    );
```



添加和删除非空约束：

```sql
-- 删除非空约束
ALTER TABLE <数据表名>
CHANGE COLUMN <字段名> <字段名> <数据类型> NULL;
ALTER TABLE user CHANGE COLUMN name name varchar(32) NULL;
-- 添加非空约束
ALTER TABLE <数据表名>
CHANGE COLUMN <字段名> <字段名> <数据类型> NOT NULL;
ALTER TABLE user CHANGE COLUMN name name varchar(32) NOT NULL;
```



## 7.4、默认值约束

默认值约束用来约束当数据表中某个字段不输入值时，自动为其添加一个已经设置好的值。

创建表时可以使用`DEFAULT`关键字设置默认值约束

```sql
 CREATE TABLE stu(
    id INT(11) PRIMARY KEY,
    name VARCHAR(22) UNIQUE NOT NULL,
    gender VARCHAR(22) DEFAULT "male"
    );
```



添加和删除默认值：

```sql
-- 删除非空约束
ALTER TABLE <数据表名>
CHANGE COLUMN <字段名> <字段名> <数据类型> DEFAULT NULL;
ALTER TABLE stu CHANGE COLUMN gender gender varchar(32) DEFAULT NULL;
-- 添加非空约束
ALTER TABLE <数据表名>
CHANGE COLUMN <字段名> <数据类型> DEFAULT <默认值>;
ALTER TABLE stu CHANGE COLUMN gender gender varchar(32) DEFAULT "female";
```



## 7.5、外键约束

外键约束经常和主键约束一起使用，用来确保数据的一致性。

外键约束（FOREIGN KEY）是表的一个特殊字段，经常与主键约束一起使用。对于两个具有关联关系的表而言，相关联字段中主键所在的表就是主表（父表），外键所在的表就是从表（子表）。

外键用来建立主表与从表的关联关系，为两个表的数据建立连接，约束两个表中数据的一致性和完整性。主表删除某条记录时，从表中与之对应的记录也必须有相应的改变。一个表可以有一个或多个外键，外键可以为空值，若不为空值，则每一个外键的值必须等于主表中主键的某个值。

比如上面的书籍管理案例，若删除一个清华出版社记录，没有任何影响，但是，书籍表中pub_id = 1 的记录出版社字段就没有意义了。

>   定义外键时，需要遵守下列规则：
>
>   -   主表必须已经存在于数据库中，或者是当前正在创建的表。如果是后一种情况，则主表与从表是同一个表，这样的表称为自参照表，这种结构称为自参照完整性。
>   -   必须为主表定义主键。
>   -   主键不能包含空值，但允许在外键中出现空值。也就是说，只要外键的每个非空值出现在指定的主键中，这个外键的内容就是正确的。
>   -   在主表的表名后面指定列名或列名的组合。这个列或列的组合必须是主表的主键或候选键。
>   -   外键中列的数目必须和主表的主键中列的数目相同。
>   -   外键中列的数据类型必须和主表主键中对应列的数据类型相同（非常重要）。

#### （1）创建表时设置外键约束

```sql
[CONSTRAINT <外键名>] FOREIGN KEY 字段名 [，字段名2，…]
REFERENCES <主表名> 主键列1 [，主键列2，…]
```



例如：

```sql
-- 书籍表
CREATE TABLE book(
id INT PRIMARY KEY AUTO_INCREMENT,
title VARCHAR(32),
price DOUBLE(5,2),    
pub_id INT NOT NULL,
FOREIGN KEY(pub_id) REFERENCES publisher(id) ON DELETE CASCADE ON UPDATE CASCADE -- 建立外键约束    
)ENGINE=INNODB CHARSET=utf8;


-- 出版社表
CREATE TABLE publisher(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(32),
email VARCHAR(32),
addr VARCHAR(32)
)ENGINE=INNODB CHARSET=utf8;

-- 作者表
CREATE TABLE author(
id INT PRIMARY KEY AUTO_INCREMENT,
NAME VARCHAR(32) NOT NULL
)ENGINE=INNODB CHARSET=utf8;

-- 作者表和书籍表的多对多关系表
CREATE TABLE book2author(
id INT NOT NULL UNIQUE AUTO_INCREMENT,
author_id INT NOT NULL,
book_id INT NOT NULL,
FOREIGN KEY(author_id) REFERENCES author(id) ON UPDATE CASCADE ON DELETE CASCADE, -- 建立外键约束
FOREIGN KEY(book_id) REFERENCES book(id) ON UPDATE CASCADE ON DELETE CASCADE     -- 建立外键约束
)ENGINE=INNODB CHARSET=utf8;


```



#### （2）添加删除外键约束

```sql
-- 添加外键约束
ALTER TABLE <数据表名> ADD CONSTRAINT <外键名>
FOREIGN KEY(<列名>) REFERENCES <主表名> (<列名>);

-- 删除外键约束
ALTER TABLE <表名> DROP FOREIGN KEY <外键约束名>;
drop index 外键约束名 on<表名>; -- 同时将索引删除 
```



```sql
ALTER TABLE book ADD CONSTRAINT dep_fk
FOREIGN KEY(pub_id) REFERENCES publisher(id) ON DELETE CASCADE;
show create table book;
-- 尝试删除一个出版社记录
DELETE FROM publisher WHERE id=1;
/*
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`yuan`.`book`, CONSTRAINT `dep_fk` FOREIGN KEY (`pub_id`) REFERENCES `publisher` (`id`)) */
-- 删除外键约束
ALTER TABLE book DROP FOREIGN KEY dep_fk;
show index from book;
drop index dep_fk on book;
show create table book;

ALTER TABLE book ADD CONSTRAINT dep_fk FOREIGN KEY(pub_id) REFERENCES publisher(id) ON DELETE CASCADE; 


--  再次尝试删除一个出版社记录，此时就是级联删除了，所有book表中关联publisher表中id=1的记录都会级联删除
DELETE FROM publisher WHERE id=1;
select * from book;
```



#### （3）INNODB支持的ON语句

外键约束对子表的含义: 如果在主表中(比如dep)找不到候选键,则不允许在子表(比如emp)上进行insert/update

外键约束对父表的含义: 在主表上进行update/delete以更新或删除在子表中有一条或多条应匹配行的候选键时,父表的行为取决于：在定义子表的外键时指定的 – on update/on delete子句

```sql
FOREIGN KEY () REFERENCES () ON DELETE CASCADE;

```



```sql
-- (1) cascade
cascade方式 在父表上update/delete记录时，同步update/delete掉子表的匹配记录外键的级联删除：如果父表中的记录被删除，则子表中对应的记录自动被删除

-- (2) cascade     
set null方式 在父表上update/delete记录时，将子表上匹配记录的列设为null ; 要注意子表的外键列不能为not null

-- (3) Restrict
Restrict方式 :拒绝对父表进行删除更新操作(了解)

-- (4) No action
No action方式 在mysql中同Restrict,如果子表中有匹配的记录,则不允许对父表对应候选键 ; 进行update/delete操作（了解）

```



-   **原文作者：**[Yuan](http://www.yuan316.com/)

-   **原文链接：**[http://www.yuan316.com/post/Mysql%E5%9F%BA%E7%A1%80/](http://www.yuan316.com/post/Mysql基础/)

    