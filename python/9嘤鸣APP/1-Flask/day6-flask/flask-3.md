数据库操作

数据库驱动（drivers）模块：pymysql、MySQLDB



# ORM

**ORM** 全拼`Object-Relation Mapping`，中文意为 **对象-关系映射**。主要实现模型对象到关系数据库数据的映射。

ORM提供了一种面向对象操作数据库的方式给开发者。不需要编写原生SQL语句也能操作数据库，实现了业务代码与底层数据的解耦。

优点：

- 只需要面向对象编程, 不需要面向数据库编写SQL。
  - 对数据库的操作都转化成对类/对象的属性和方法的操作.    表字段--->对象属性,   SQL关键字-> 操作方法
  - 不用编写各种数据库的`原生sql语句`，当然也可以编写原生SQL语句。
- 实现了数据模型代码与数据库数据的解耦, 屏蔽了不同数据库操作上的差异。
  - 不再需要关注当前项目使用的是哪种数据库。
  - 通过简单的配置就可以轻松更换数据库, 而不需要修改业务代码.

缺点：

- 相比较直接使用SQL语句操作数据库,ORM需要把操作转换成SQL语句，所以有性能损失.
- 根据对象的操作转换成SQL语句,根据查询的结果转化成模型实例对象, 在映射过程中有性能损失.
- 不同的ORM提供的操作不一样，增加了学习成本



## Flask-SQLAlchemy

flask默认不提供数据库操作，也并没有提供ORM，所以一般开发的时候我们会采用flask-SQLAlchemy模块来实现ORM操作。

SQLAlchemy是一个python语言编写的高性能的关系型数据库ORM框架，它提供了高层的 ORM 和底层的原生数据库的操作。

我们使用sqlalchemy 不需要调用sqlalchemy 本身这个模块，而是采用flask-sqlalchemy ，这是一个简化了 SQLAlchemy 操作的flask扩展模块。（主要是简化了sqlalchemy初始化代码和分页操作等）

SQLAlchemy：https://docs.sqlalchemy.org/en/14/

中文文档：https://www.osgeo.cn/sqlalchemy/orm/index.html

flask-SQLAlchemy：https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

安装 flask-sqlalchemy【清华源】

```bash
pip install flask-sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

如果sqlalchemy连接的是 mysql /MariaDB数据库，需要安装 mysqldb 或pymysql**驱动**

```bash
conda install flask-mysqldb -c conda-forge
# 如果上面一句代码安装失败，去掉-c后面的选项内容。
```

pip安装flask-mysqldb时，注意

```
使用pip install 安装 flask-mysqldb的时候，python底层依赖于一个底层的模块 mysqlclient 模块
如果没有这个模块，则会报错如下：

Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-install-21hysnd4/mysqlclient/
```

解决方案：

```bash
sudo apt-get install -y libmysqlclient-dev python3-dev

# 运行上面的安装命令如果再次报错如下：
#   dpkg 被中断，您必须手工运行 ‘sudo dpkg --configure -a’ 解决此问题。

# 则根据提示执行命令以下命令，再次安装mysqlclient
#    sudo dpkg --configure -a
#    apt-get install libmysqlclient-dev python3-dev

解决了mysqlclient问题以后，重新安装 flask-mysqldb即可。
pip install flask-mysqldb -i https://pypi.tuna.tsinghua.edu.cn/simple
```

原生SQLAlchemy连接配置操作

db.py，代码：

```python
from sqlalchemy import create_engine   # 驱动引擎
from sqlalchemy.ext.declarative import declarative_base # 数据库基类
from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text # 字段、整型
from sqlalchemy.orm import sessionmaker  # 连接会话

engine = create_engine(
    # 连接数据库的URL
    # url="mysql+pymysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",  # 如果底层驱动是pymysql
    url="mysql://root:123@127.0.0.1:3306/students?charset=utf8mb4",    # 如果底层驱动是MysqlDB
    echo=True, # 当设置为True时会将orm语句转化为sql语句打印，一般debug的时候可用
    pool_size=8, # 连接池的大小，默认为5个，设置为0时表示连接无限制
    pool_recycle=60*30 # 设置时间以限制数据库多久没连接自动断开
)

DbSession = sessionmaker(bind=engine)
session = DbSession()

# 创建数据基类
Model = declarative_base()
```

manage.py，代码：

```python
import models

class Student(models.Model):
    # 声明表名
    __tablename__ = "student"
    id = models.Column(models.Integer, primary_key=True,)
    name = models.Column(models.String(255))
    sex = models.Column(models.Boolean)
    age = models.Column(models.SmallInteger)
    class_name = models.Column("class",models.String(255),)
    description = models.Column(models.Text)

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

if __name__ == '__main__':
    # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
    # 如果数据库中已经声明了有数据表，则不会继续生成
    models.Model.metadata.create_all(models.engine)

    # # 获取模型对应表的所有数据
    # student_list = models.session.query(Student).all()
    #
    # # 循环输出
    # for student in student_list:
    #     print(student, student.id, student.name ,student.age)

    # # 获取一条数据[参数为主键，如果查询不到，则返回结果为None]
    # student = models.session.query(Student).get(105)
    # if student:
    #     print(student, student.name, student.class_name)
    # else:
    #     print("查无此人")

    # # 按条件查询
    # student_list = models.session.query(Student).filter(Student.sex==True, Student.class_name=='301').all()
    # print(student_list)

    # # 添加一条数据
    # student = Student(
    #     name="张三丰",
    #     sex=True,
    #     age=17,
    #     class_name="305",
    #     description="太极生两仪..."
    # )
    #
    # models.session.add(student)
    # models.session.commit()


    # # 修改操作
    # student = models.session.query(Student).filter_by(name="张三丰").first()
    # if student:
    #     student.name="张四封"
    #     student.age = 21
    #     models.session.commit()

    # # 删除一条数据操作
    # student = models.session.query(Student).filter_by(name="xiaohui").first()
    # models.session.delete(student)
    # models.session.commit()


    # # 添加多条数据
    # student_list = [
    #     Student(name="xiaohei", class_name="305", sex=False, age=18, description="美美的..",),
    #     Student(name="xiaobai", class_name="304", sex=True, age=18, description="美美的..",),
    #     Student(name="xiaohui", class_name="303", sex=False, age=18, description="美美的..",),
    # ]
    #
    # models.session.add_all(student_list)
    # models.session.commit()


    # # 更新多条数据
    # models.session.query(Student).filter(Student.class_name=="303").update({Student.age: Student.age+1})
    # models.session.commit()


    # # 删除多条数据
    # models.session.query(Student).filter(Student.id > 100).delete()
    # models.session.commit()

    # # 原生SQL语句
    # # 读
    # cursor = models.session.execute('select * from student')
    # # 一条
    # data = cursor.fetchone()
    # print(data)

    # # 多条
    # data_list = cursor.fetchall()
    # print(data_list)

    # 写[添加、删除、修改]
    cursor = models.session.execute(
        'insert into student(name, class, age, sex, description) values(:name, :class, :age, :sex, :description)',
        params={
            "name": "xiaohong",
            "class": "307",
            "age": 19,
            "sex": 0,
            "description": ".....",
        })
    models.session.commit()
    print(cursor.lastrowid)  # 获取最后添加的主键ID

```



### 数据库连接设置

- 在 Flask-SQLAlchemy 中，数据库的链接配置信息使用URL指定，而且程序使用的数据库必须保存到Flask的 **SQLALCHEMY_DATABASE_URI** 配置项中

manage.py，代码：

```python
# SQLAlchemy的链接配置："数据库名://账户名:密码@服务器地址:端口/数据库名称?配置参数选项"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/flaskdemo?charset=utf8mb4"


# 如果不使用mysqldb改用pymysql，则需要在连接时指定pymysql
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123@127.0.0.1:3306/flaskdemo?charset=utf8mb4"
```

其他设置项：

```python
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

```

- 配置完成需要去 MySQL 中创建项目所使用的数据库

```bash
mysql -uroot -p123
create database school charset=utf8mb4;
```



### 常用的SQLAlchemy字段类型

| 模型字段类型名   | python中数据类型  | 说明                                                         |
| :--------------- | :---------------- | :----------------------------------------------------------- |
| **Integer**      | int               | 普通整数，一般是32位                                         |
| **SmallInteger** | int               | 取值范围小的整数，一般是16位                                 |
| BigInteger       | int               | 不限制精度的整数                                             |
| Float            | float             | 浮点数                                                       |
| **Numeric**      | decimal.Decimal   | 普通数值，一般是32位                                         |
| **String**       | str               | 变长字符串                                                   |
| **Text**         | str               | 变长字符串，对较长或不限长度的字符串做了优化                 |
| Unicode          | unicode           | 变长Unicode字符串                                            |
| UnicodeText      | unicode           | 变长Unicode字符串，对较长或不限长度的字符串做了优化          |
| **Boolean**      | bool              | 布尔值                                                       |
| **DateTime**     | datetime.datetime | 日期和时间                                                   |
| Date             | datetime.date     | 日期                                                         |
| Time             | datetime.time     | 时间                                                         |
| LargeBinary      | bytes             | 二进制文件内容                                               |
| **Enum**         | enum.Enum         | 枚举类型，相当于django的choices，但是功能没有choices那么强大 |



### 常用的SQLAlchemy列约束选项

| 选项名          | 说明                                                        |
| :-------------- | :---------------------------------------------------------- |
| **primary_key** | 如果为True，代表当前数据表的主键                            |
| **unique**      | 如果为True，为这列创建唯一 索引，代表这列不允许出现重复的值 |
| **index**       | 如果为True，为这列创建普通索引，提高查询效率                |
| **nullable**    | 如果为True，允许有空值，如果为False，不允许有空值           |
| **default**     | 为这列定义默认值                                            |



## 数据库基本操作

- 在SQLAlchemy中，添加、修改、删除操作，均由数据库会话(sessionSM)管理。
  - 会话用 db.session 表示。在准备把数据写入数据库前，要先将数据添加到会话中然后调用 db.session.commit() 方法提交会话。
- 在SQLAlchemy 中，查询操作是通过 query 对象操作数据。
  - 最基本的查询是返回表中所有数据，也可以通过filter或filter_by过滤器进行更精确的数据库查询。



## 模型类定义

我们后面会把模型创建到单独的文件中，但是现在我们先把模型类写在main.py文件中。

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(15) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱地址', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Course(db.Model):
    """课程模型"""
    """
        CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '课程', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )

    """
    __tablename__ = "tb_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    price = db.Column(db.Numeric(8, 2), comment="价格")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Teacher(db.Model):
    """老师模型"""
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT,
        name VARCHAR(255) COMMENT '姓名',
        `option` ENUM('讲师','助教','班主任'),
        PRIMARY KEY (id),
        UNIQUE (name)
    )
    """
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"

if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
        # 如果数据库中已经声明了有数据表，则不会继续生成
        db.create_all()
    app.run(debug=True)
```

# 数据表操作

### 创建和删除表

创建表

```python
# 在视图内调用：
@app.route("/create")
def create_table():
    db.create_all() # 为项目中被识别的所有模型创建数据表
    return "ok"


# 在视图以外的地方调用：
with app.app_context():
    # create_all()方法执行的时候，需要放在模型的后面
    # 检测数据库中是否存在和模型匹配的数据表。
    # 如果没有，则根据模型转换的建表语句进行建表。
    # 如果找到，则不会进行额外处理
    db.create_all()
```

删除表

```python
# 在视图内调用：
@app.route("/drop")
def drop_table():
    db.drop_all()   # 为项目中被识别的所有模型删除数据表
    return "ok"


# 在视图以外的地方调用：
    with app.app_context():
        db.drop_all()  # 慎用，很给力的！！这表示删除数据库中所有模型对应的表。
```

代码：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(15) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱地址', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Course(db.Model):
    """课程模型"""
    """
        CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '课程', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )

    """
    __tablename__ = "tb_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    price = db.Column(db.Numeric(8, 2), comment="价格")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Teacher(db.Model):
    """老师模型"""
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT,
        name VARCHAR(255) COMMENT '姓名',
        `option` ENUM('讲师','助教','班主任'),
        PRIMARY KEY (id),
        UNIQUE (name)
    )
    """
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"

if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
        # 如果数据库中已经声明了有数据表，则不会继续生成
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
```

# 数据操作

添加一条数据

```python
    # 添加一条数据
    student = Student(
        name="小明",
        age=17,
        sex=True,
        email="xiaoming@qq.com",
        money=30.50
    )
    db.session.add(student)
    db.session.commit()
```



一次插入多条数据

```python
    # 添加多条数据
    student_list = [
        Student(name="小黑", age=16, sex=True, email="xiaohei@qq.com", money=1000),
        Student(name="小红", age=15, sex=False, email="xiaohong@qq.com", money=1200),
        Student(name="小兰", age=11, sex=True, email="xiaolan@qq.com", money=600),
        Student(name="小白", age=21, sex=False, email="xiaobai@qq.com", money=2900),
    ]
    db.session.add_all(student_list)
    db.session.commit()
```

更新一条数据

```python
    # 更新一条数据
    student = Student.query.get(3)
    student.age = 18
    db.session.commit()
```

更新多条数据

```python
    # 更新多条数据
    Student.query.filter(Student.sex == True).update({
        Student.money: Student.age * 100,
    })
    db.session.commit()
```

删除一条数据

```python
    # 删除一条数据
    student = Student.query.get(5)
    db.session.delete(student)
    db.session.commit()
```

删除多条数据

```python
    # 删除多条数据
    Student.query.filter(Student.sex==False).delete()
    db.session.commit()
```



```python
"""
悲观锁，是属于数据库中的一种互斥锁机制，但是乐观锁并非真正的数据库锁。
2种锁都是数据库在应对并发操作时，防止出现资源抢夺的，基于不同人生观所实现2种解决方案。
悲观锁的基本使用：
    >>> 数据库终端开始

    begin;  -- 开启事务
    select * from db_student where student_id = 5 for update; -- 添加一把更新锁【悲观锁】
    ....    -- 在事务提交之前，任何第三方连接都不能修改 student_id = 5这条数据 
    update from db_student set age = 16 where student_id = 5;
    commit; -- 提交事务

    <<< 数据库终端开始

悲观锁的问题：
1. 提前锁定数据，形成串行化，形成阻塞，不利于性能发挥，不适用高并发场景。
2. 悲观锁只能保证数据的一致性，不能保证脏数据的出现

乐观锁的出现就是为了解决悲观锁的问题。
举例：双11活动，商城里面id=5的商品的库存num=10了，现在我们要基于乐观锁和悲观锁来解决下单过程中，出现的资源抢夺现象，避免出现超卖（商品数量不能为负数）。

乐观锁：
---> begin;  开启事务
---> 先查看库存，记录当前库存 original_num=10
---> 进行下单操作，买6件 
---> 付款
---> 扣除库存 update from goods set num=num-6 where num=original_num and id=5;  # 增加更新条件，判断库存是否还是原来
       如果执行成功，则表示没有人抢，购买成功
---> commit;
       如果执行失败，则表示已经有人先抢购
---> rollback;

悲观锁：
---> begin; 开启事务
---> 先给id=5的数据，加锁
        select * from goods where id=5 for update;
---> 进行下单操作，买6件
---> 付款
---> 扣除库存  update from  goods set num=num-6 where id=5;
---> 执行成功解锁
---- commit;  提交事务
"""
```



## 基本查询

### SQLAlchemy常用的查询过滤器

| 过滤器         | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| **filter()**   | 把过滤器添加到原查询上，返回一个新查询                       |
| filter_by()    | 把等值过滤器添加到原查询上，返回一个新查询                   |
| **limit()**    | 使用指定的值限定原查询返回的**结果数量**                     |
| **offset()**   | 设置结果范围的**开始位置**，偏移原查询返回的结果，返回一个新查询 |
| **order_by()** | 根据指定条件对原查询结果进行**排序**，返回一个新查询         |
| **group_by()** | 根据指定条件对原查询结果进行**分组**，返回一个新查询         |



### SQLAlchemy常用的查询结果方法

| 方法           | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| **all()**      | 以**列表形式**返回查询的所有结果                             |
| **first()**    | 返回查询结果的第一个结果，**模型对象**，如果未查到，返回**None** |
| first_or_404() | 返回查询的第一个结果，**模型对象**，如果未查到，通过 abort抛出404异常 |
| **get()**      | 可以设置查询主键参数，返回**指定主键**对应的**模型对象**，如不存在，返回None |
| get_or_404()   | 可以设置查询主键参数，返回**指定主键**对应的**模型对象**，如不存在，通过 abort抛出404异常 |
| **count()**    | 返回查询结果的**数量**                                       |
| **paginate()** | 返回一个Paginate**分页器对象**，它包含指定范围内的结果       |
| **having()**   | 返回分组结果中符合条件的数据，**必须跟在group by后面**，其他地方无法使用。 |

 

get():参数为主键，表示根据主键查询数据，如果主键不存在返回None

```python
    student = Student.query.get(1)
    if student:
        print(student.name)

    student = Student.query.get(100)
    if student:
        print(student.name)
```



all()返回查询到的所有对象

```python
    # 如果不设置条件，则默认查询全表
    student_list = Student.query.all()
    print(student_list)

    # 设置过滤条件查询全部结果
    # 如果查不到数据，返回空列表
    student_list = Student.query.filter(Student.sex==False).all()
    print(student_list)

    # all()的返回值是一个python列表，可以直接使用切片，与django的QuerySet完全不是一回事。
    student_list = Student.query.all()[1:]
    print(student_list)

```



count 返回查询结果的数量

```python
    # 如果不设置过滤条件，则默认统计全表记录的数量
    total = Student.query.count()
    print(total)

    # 设置条件，作为返回满足条件的记录数量
    total = Student.query.filter(Student.age>16).count()
    print(total)
```



first()返回查询到的第一个对象【first的结果只有一个模型对象】

```python
    """获取查询结果的第一个结果"""
    student = Student.query.first()
    print(student, student.name)

    student = Student.query.filter(Student.sex==True).first()
    print(student, student.name)

    """获取查询结果的最后一个结果"""
    student = Student.query.filter(Student.sex==True)[-1]
    print(student, student.name)
```



filter条件查询，支持各种运算符和查询方法或者模糊查询方法。

基于filter进行模糊查询

```python
    # 名字包含"黑"的学生
    student_list = Student.query.filter(Student.name.contains("黑")).all()
    print(student_list)

    # 名字以"小"开头的学生
    student_list = Student.query.filter(Student.name.startswith("小")).all()
    print(student_list)

    # 名字以"红"结尾的学生
    student_list = Student.query.filter(Student.name.endswith("兰")).all()
    print(student_list)
```

基于filter进行比较查询

```python
    # 比较查询需要指定条件格式为: filter(模型.字段 比较运算符 值)。
    # 运算符可以是: ==表示相等, !=不相等，> 表示大于  < 表示小于，>=大于等于，<=小于等于
    # 单个条件的比较查询
    student_list = Student.query.filter(Student.age>15).all()
    print(student_list)

    # 多个条件的比较查询
    # 要求多个条件都要满足，相当于逻辑查询中的 并且(and)！！
    student_list = Student.query.filter(Student.age>15, Student.sex==True).all()
    print(student_list)
```



filter_by精确条件查询

filter_by 只支持字段的**值是否相等**的情况，对于大于、小于、大于等于、等等其他条件是不支持的。

例如：返回age等于16的学生

```python
    # 单条件格式：filter_by(字段=值)
    # 多条件格式：filter_by(字段=值, 字段=值, 字段=值...)
    student_list = Student.query.filter_by(age=16).all()  # 字段添加不需要附带模型类
    print(student_list)
```



练习：

```python
查询所有男生[Student.sex==True]数据

查询id为4的学生[3种方式]
 
查询年龄大于16的所有学生数据

查询name为小名的学生数据

查询17岁的男生
```

代码：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(15) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱地址', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):  # 相当于django的__str__
        return f"<{self.name} {self.__class__.__name__}>"

class Course(db.Model):
    """课程模型"""
    """
        CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '课程', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )

    """
    __tablename__ = "tb_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    price = db.Column(db.Numeric(8, 2), comment="价格")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Teacher(db.Model):
    """老师模型"""
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT,
        name VARCHAR(255) COMMENT '姓名',
        `option` ENUM('讲师','助教','班主任'),
        PRIMARY KEY (id),
        UNIQUE (name)
    )
    """
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"


@app.route("/data")
def data():
    """查询所有男生[Student.sex==True]数据"""
    student_list = Student.query.filter(Student.sex==True).all()
    print(student_list)

    """查询id为4的学生[3种方式]"""
    student = Student.query.get(4)
    print(student)
    student = Student.query.filter(Student.id==4).first()
    print(student)
    student = Student.query.filter_by(id=4).first()
    print(student)


    """查询年龄大于16的所有学生数据"""
    student_list = Student.query.filter(Student.age>16).all()
    print(student_list)

    """查询name为小明的学生数据"""
    student_list = Student.query.filter(Student.name=="小明").all()
    print(student_list)

    """查询17岁的男生"""
    student_list = Student.query.filter(Student.age==17, Student.sex==True).all()
    print(student_list)

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
        # 如果数据库中已经声明了有数据表，则不会继续生成
        # db.drop_all()
        db.create_all()
    app.run(debug=True)

```



### 逻辑查询

逻辑与，需要导入`and_`，返回`and_()`条件满足的所有数据

```python
    # 默认情况下， 多个条件并且的情况，可以直接基于filter或者filter_by采用逗号拼接多个查询条件实现
    # 查询年龄大于16的男生
    student_list = Student.query.filter(Student.age>16, Student.sex==True).all()
    print(student_list)

    #  filter(and_(条件1,条件2,....))  等价于  filter(条件1,条件2,.....)
    from sqlalchemy import and_
    student_list = Student.query.filter(and_(Student.age>16, Student.sex==True)).all()
    print(student_list)
```



逻辑或，需要导入or_

```python
    # # 查询年龄大于16(Student.age>16)或者钱包余额大于1500（Student.money>1500） 女生
    from sqlalchemy import or_
    student_list = Student.query.filter(or_(Student.age>16, Student.money>1500), Student.sex==False).all()
    print(student_list)

    # 查询 年龄大于16的男生(Student.age>16, Student.sex==True) 和 钱包余额大于1500的女生（Student.money>1500, Student.sex==False)
    from sqlalchemy import or_, and_
    student_list = Student.query.filter(
        or_(
            and_(Student.age>16, Student.sex==True),
            and_(Student.money>1500, Student.sex==False)
        )
    ).all()
    print(student_list)
```



逻辑非，返回名字不等于"小白"的所有数据

```python
Student.query.filter(Student.name!='小白').all()
```

not_ 相当于取反

```python
from sqlalchemy import not_
student = Student.query.filter(Student.name != '小白').all()
print(student)

student = Student.query.filter(not_(Student.name == '小白')).all()
print(student)
```



in_范围查询

```python
    student_list = Student.query.filter(Student.id.in_([1,3,4,5])).all()
    print(student_list)
```

is_判断值查询

```python
    # 查询邮箱为Null的用户
    student_list = Student.query.filter(Student.email.is_(None)).all()
    print(student_list)
    
    """判断是否存在"""
    # 查询是否存在"小辉"这个学生
    # query = Student.query.filter(Student.name == "小辉").exists()
    # ret = db.session.query(query).scalar()
    # print(ret)

    # student = Student.query.filter(Student.name=="小明").first()
    # print(bool(student))
```



order_by 排序

```python
    # 按年龄倒叙排序
    student_list = Student.query.order_by(Student.age.desc()).all()
    print(student_list)

    # 按钱包余额进行倒序，如果余额一致，按id倒序
    student_list = Student.query.order_by(Student.money.desc(), Student.id.desc()).all()
    print(student_list)
```



对查询结果进行偏移量和数量的限制

```python
    student_list = Student.query.order_by(Student.age.desc()).limit(3).all()
    print(student_list)

    # 查询钱包余额最少的三个人
    student_list = Student.query.order_by(Student.money.asc()).limit(3).all()
    print(student_list)

    # 按钱包余额进行倒序排列，查询出排名在4-5之间的学生
    student_list = Student.query.order_by(Student.money.desc()).offset(3).limit(2).all()
    print(student_list)

    student_list = Student.query.order_by(Student.money.desc()).all()[3:5]
    print(student_list)
```

SQL

```sql
# 查询年龄最大的3个学生
# select * from db_student order by age desc limit 3;

# 查询年龄排第4到第5名的学生
select * from db_student order by age desc limit 3, 4;
# select * from db_student order by age desc limit 4 offset 3;

# 查询年龄最小的3个人
# select * from db_student order by age asc limit 3;
```



练习

```python
# 查询age是18 或者 money是1600的所有学生

# 查询id为 [1, 3, 5, 7, 9] 的学生列表

```



### 分页器

manage.py，代码：

```python
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = False

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    """
    CREATE TABLE tb_student (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(15) COMMENT '姓名', 
        age SMALLINT COMMENT '年龄', 
        sex BOOL COMMENT '性别', 
        email VARCHAR(128) COMMENT '邮箱地址', 
        money NUMERIC(10, 2) COMMENT '钱包', 
        PRIMARY KEY (id), 
        UNIQUE (email)
    )
    """
    # 声明与当前模型绑定的数据表名称
    __tablename__ = "tb_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):  # 相当于django的__str__
        return f"<{self.name} {self.__class__.__name__}>"

class Course(db.Model):
    """课程模型"""
    """
        CREATE TABLE tb_course (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT, 
        name VARCHAR(255) COMMENT '课程', 
        price NUMERIC(8, 2) COMMENT '价格', 
        PRIMARY KEY (id), 
        UNIQUE (name)
    )

    """
    __tablename__ = "tb_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    price = db.Column(db.Numeric(8, 2), comment="价格")

    def __repr__(self):  # 相当于django的__str__
        return f"{self.name}<{self.__class__.__name__}>"


class Teacher(db.Model):
    """老师模型"""
    """
    CREATE TABLE tb_teacher (
        id INTEGER NOT NULL COMMENT '主键' AUTO_INCREMENT,
        name VARCHAR(255) COMMENT '姓名',
        `option` ENUM('讲师','助教','班主任'),
        PRIMARY KEY (id),
        UNIQUE (name)
    )
    """
    __tablename__ = "tb_teacher"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="姓名")
    option = db.Column(db.Enum("讲师", "助教", "班主任"), default="讲师")

    def __repr__(self):
        return f"{self.name}<{self.__class__.__name__}>"


@app.route("/data")
def data():
    # student_list = Student.query.all()
    # print(student_list)

    # 分页器对象 = 模型.query.filter(过滤条件).paginate(page=页码, per_page=单页数据量,max_per_page=最大单页数据量，默认100)
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5))
    pagination = Student.query.paginate(page=page, per_page=size, max_per_page=10)

    # print(pagination.total)  # 总数据量
    # print(pagination.items)  # 当前页展示的数据列表
    # print(pagination.pages)  # 总页码
    #
    # print(pagination.has_prev) # 是否有上一页
    # print(pagination.prev_num) # 上一页的页码
    # print(pagination.prev())   # 上一页的分页器对象
    # print(pagination.prev().items)   # 上一页展示的数据列表
    #
    # print(pagination.has_next) # 是否有上一页
    # print(pagination.next_num) # 上一页的页码
    # print(pagination.next())   # 上一页的分页器对象
    # print(pagination.next().items)   # 上一页展示的数据列表

    # """前后端分离"""
    # data = {
    #     "page": pagination.page, # 当前页码
    #     "pages": pagination.pages, # 总页码
    #     "has_prev": pagination.has_prev, # 是否有上一页
    #     "prev_num": pagination.prev_num, # 上一页页码
    #     "has_next": pagination.has_next, # 是否有下一页
    #     "next_num": pagination.next_num, # 下一页页码
    #     "items": [{
    #         "id": item.id,
    #         "name": item.name,
    #         "age": item.age,
    #         "sex": item.sex,
    #         "money": item.money,
    #     } for item in pagination.items]
    # }
    # return data

    """前后端不分离"""
    return render_template("list.html",**locals())


if __name__ == '__main__':
    with app.app_context():
        # 如果没有提前声明模型中的数据表，则可以采用以下代码生成数据表，
        # 如果数据库中已经声明了有数据表，则不会继续生成
        # db.drop_all()
        db.create_all()
    app.run(debug=True)

```

list.html，代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
    .page a,.page span{
        padding: 2px 6px;
        color: #fff;
        background: #6666ff;
        text-decoration: none;
    }
    .page span{
        color: #fff;
        background: orange;
    }

    </style>
</head>
<body>
    <table border="1" align="center" width="600">
        <tr>
           <th>ID</th>
           <th>age</th>
           <th>name</th>
           <th>sex</th>
           <th>money</th>
        </tr>
        {% for student in pagination.items %}
        <tr>
           <td>{{ student.id }}</td>
           <td>{{ student.age }}</td>
           <td>{{ student.name }}</td>
           <td>{{ "男" if student.sex else "女" }}</td>
           <td>{{ student.money }}</td>
        </tr>
        {% endfor %}
        <tr align="center">
            <td colspan="5" class="page">
                {% if pagination.has_prev %}
                <a href="?page=1">首  页</a>
                <a href="?page={{ pagination.page-1 }}">上一页</a>
                <a href="?page={{ pagination.page-1 }}">{{ pagination.page-1 }}</a>
                {% endif %}
                <span>{{ pagination.page }}</span>
                {% if pagination.has_next %}
                <a href="?page={{ pagination.page+1 }}">{{ pagination.page+1 }}</a>
                <a href="?page={{ pagination.page+1 }}">下一页</a>
                <a href="?page={{ pagination.pages }}">尾  页</a>
                {% endif %}
            </td>
        </tr>
    </table>
</body>
</html>
```



### 聚合分组

分组查询和分组查询结果过滤

一般分组都会结合**聚合函数**来一起使用。SQLAlchemy中所有的聚合函数都在`func`模块中声明的。

```python
from sqlalchemy import func
```

| 函数名     | 说明     |      |
| ---------- | -------- | ---- |
| func.count | 统计总数 |      |
| func.avg   | 平均值   |      |
| func.min   | 最小值   |      |
| func.max   | 最大值   |      |
| func.sum   | 求和     |      |

代码：

```python
    """聚合函数"""
    from sqlalchemy import func

    #  获取所有学生的money总数
    ret = db.session.query(func.sum(Student.money)).first()[0]
    print(ret)

    # 查询女生的数量
    ret = db.session.query(func.count(Student.id)).filter(Student.sex==False).first()[0]
    print(ret)

    ret = db.session.query(func.count(Student.id)).filter(Student.sex==False).scalar()
    print(ret)


    # 查询所有学生的平均年龄
    ret = db.session.query(func.avg(Student.age)).scalar()
    print(ret)


    """分组查询"""
    # 查询男生女生的平均年龄
    ret = db.session.query(func.avg(Student.age)).group_by(Student.sex).all()
    print(ret)  # [(Decimal('17.0000'),), (Decimal('17.5000'),)]

    # 查询各个年龄段的学生数量
    # 分组时， db.session.query()中的字段，只能要么是被分组的字段，要么是聚合结果
    ret = db.session.query(Student.age, func.count(Student.id)).group_by(Student.age).all()

    # 多字段分组，
    # 查询查询各个年龄段的女生与男生学生数量
    ret = db.session.query(Student.age, Student.sex, func.count(Student.id)).group_by(Student.sex, Student.age).all()
    print(ret)

    # 分组后的过滤操作 having
    # 在所有学生中，找出各个年龄中拥有最多钱的同学，并在这些同学里面筛选出money > 1500的数据
    subquery = func.max(Student.money)
    ret = db.session.query(Student.age, subquery).group_by(Student.age).having(subquery > 1500).all()
    print(ret)
```



SQLAlchemy方法中的关键字顺序：

```python
模型.query.   // db.session.query.
filter/ filter_by
group by
having
order_by
limit / offset
all / get / first / count / paginate
```



### 执行原生SQL语句

```python
"""执行原生SQL语句"""
# # 查询多条数据
# ret = db.session.execute("select * from db_student").fetchall()
# print(ret)
# # 查询一条数据
# ret = db.session.execute("select * from db_student").fetchone()
# print(ret)

"""
    name  age  achievement
               80
    小明   17   81
               83

    group_concat 逗号合并效果：
    小明   17   80,81,83

    concat  字符串拼接效果：
    小明   17   808183
    """

# # 添加数据
# db.session.execute("insert db_student (name,age,sex,email,money) select name,age,sex,concat(now(),email),money from db_student")
# db.session.commit()

# # # 更新/删除
# db.session.execute("UPDATE db_student SET money=(db_student.money + %s) WHERE db_student.age = %s" % (200, 22))
# db.session.commit()


"""分组合并"""
# 统计各个年龄段的学生人数，并记录对应年龄段的学生ID
ret = db.session.execute("select age,count(id),group_concat(id) from db_student group by age").fetchall()
print(ret)
return "ok"
```



## 关联查询

### 常用的SQLAlchemy关系选项

| 选项名         | 说明                                                         |
| :------------- | :----------------------------------------------------------- |
| backref        | 在关系的另一模型中添加**反向引用**，用于设置外键名称,在1查多的 |
| primary join   | 明确指定两个模型之间使用的连表条件, 用于1对1 或者1对多连表中 |
| lazy           | 指定如何加载关联模型数据的方式，用于1对1或1对多链表中。参数值:<br>select（立即加载，查询所有相关数据显示，相当于lazy=True）<br>subquery（立即加载，但使用子查询）<br>dynamic（不立即加载，但提供加载记录的查询对象） |
| uselist        | 指定1对1或1对多连表时，返回的数据结果是模型对象还是模型列表，如果为False，不使用列表，而使用模型对象。<br>1对1或多对1关系中，需要设置relationship中的uselist=Flase，1对多或多对多关系中，需要设置relationshio中的uselist=True。 |
| secondary      | 指定多对多关系中关系表的名字。<br>多对多关系中，需建立关系表，设置 secondary=关系表 |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级连表条件，绑定主外键。 |

### 模型之间的关联

#### 一对一

常见的业务：主表和详情表（用户、会员、学生、商品、文章、主机）

```python
class Student(db.Model):
    """个人信息主表"""
	....
    # 关联属性，这个不会被视作表字段，只是模型对象的属性。
    # 因为StudentInfo和Student是一对一的关系，所以uselist=False表示关联一个数据
    info = db.relationship("StudentInfo", uselist=False, backref="own")


class StudentInfo(db.Model):
    """个人信息附加表"""

    # 外键，
    # 如果是一对一，则外键放在附加表对应的模型中
    # 如果是一对多，则外键放在多的表对象的模型中
    # sid = db.Column(db.Integer, db.ForeignKey(Student.id),comment="外键")
    sid = db.Column(db.Integer, db.ForeignKey("student表名.主键"),comment="外键")
```

代码：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_1v1_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")
    # 关联属性[提供给SQLAlchemy]
    info = db.relationship("StudentInfo", uselist=False, backref=backref("student", uselist=False))

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class StudentInfo(db.Model):
    __tablename__ = "t_1v1_student_info"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    # 外键字段[提供给数据库]
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student外键")
    # # 关联属性[提供给SQLAlchemy，关联属性的声明，可以在2个关联模型中任意一个模型里面]
    # student = db.relationship("Student", uselist=False, backref=backref("info", uselist=False))
    address = db.Column(db.String(255), index=True, comment="注册地址")
    mobile = db.Column(db.String(15), index=True, comment="手机号码")

    def __repr__(self):
        return f"<{self.student.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """添加操作"""
    """添加主模型的同时也添加外键模型[2个数据都是新建的]"""
    # student = Student(
    #     name="张小明",
    #     age=16,
    #     sex=True,
    #     email="zhangxm@qq.com",
    #     money=1000,
    #     info=StudentInfo(
    #         address= "北京大兴",
    #         mobile = "13312345678"
    #     )
    # )
    #
    # db.session.add(student)
    # db.session.commit()

    # """已经有了主模型，基于主模型新增外键模型"""
    # student = Student(name="小白", sex=True, age=18, email="xiaobai@qq.com", money=1000)
    # db.session.add(student)
    # db.session.commit()
    #
    # student.info = StudentInfo(address="北京朝阳", mobile="13512345678")
    # db.session.commit()

    # """添加外键模型的同时，同时新新增主模型"""
    # info = StudentInfo(
    #     mobile="13300010003",
    #     address="北京市昌平区百沙路206号",
    #     student=Student(
    #         name="xiaolan04",
    #         age=17,
    #         sex=False,
    #         money=10000,
    #         email="xiaolan04@qq.com",
    #     ),
    # )
    #
    # db.session.add(info)
    # db.session.commit()

    """查询操作"""
    # # 以外键模型的字段作为主模型的查找条件
    # student = Student.query.filter(StudentInfo.mobile=="13312345678").first()
    # print(student)

    # # 以主键模型的字段作为外键模型的查找条件
    # info = StudentInfo.query.filter(Student.name=="张小明").first()
    # print(info)

    # # 通过主模型调用外键模型
    # student = Student.query.filter(Student.name=="张小明").first()
    # print(student.info)
    # print(student.info.mobile)

    # # 通过外键模型调用主键模型
    # info = StudentInfo.query.filter(StudentInfo.mobile == "13312345678").first()
    # print(info.student)
    # print(info.student.name)


    """更新操作"""
    # # 根据主模型修改外键模型的数据
    # student = Student.query.filter(Student.name=="张小明").first()
    # student.age = 17
    # student.info.address = "北京密云"
    # db.session.commit()

    # # 根据外键模型修改主模型的数据
    # info = StudentInfo.query.filter(StudentInfo.mobile == "13312345678").first()
    # info.student.age = 23
    # db.session.commit()


    """删除操作"""
    # # 删除主模型，SQLAlchemy会自动把对应的外键字段值设置为null
    # student = Student.query.get(4)
    # db.session.delete(student)
    # db.session.commit()

    # # 如果删除附加模型数据，则直接删除，不会修改主模型数据
    # info = StudentInfo.query.get(4)
    # db.session.delete(info)
    # db.session.commit()

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```



#### 一对多

常见业务：商品分类和商品、文章分类和文章、班级与学生、部门与员工、角色与会员、订单与订单详情、用户与收货地址。。。

```python
class User(db.Model):
	...
    # 关联属性，一的一方添加模型关联属性
    address_list = db.relationship("UserAddress", uselist=True, backref=backref("user", uselist=False), lazy='dynamic')
   
class UsertAddress(db.Model):
	...
    # 外键，多的一方模型中添加外间
    user_id = db.Column(db.ForeignKey(User.id))
```

- 其中realtionship描述了Student和StudentAddress的关系。第1个参数为对应参照的类"StudentAddress"
- 第3个参数backref为类StudentAddress声明关联属性
- 第4个参数lazy决定了什么时候SQLALchemy什么时候执行读取关联模型的SQL语句
  - lazy='subquery'，查询当前数据模型时，采用子查询(subquery)，把外键模型的属性也同时查询出来了。
  - lazy=True或lazy='select'，查询当前数据模型时，不会把外键模型的数据查询出来，只有操作到外键关联属性时，才进行连表查询数据[执行SQL]
  - lazy='dynamic'，查询当前数据模型时，不会把外键模型的数据立刻查询出来，只有操作到外键关联属性并操作外键模型具体字段时，才进行连表查询数据[执行SQL]
- 常用的lazy选项：dynamic和select

课堂代码：

manage.py，代码：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_1v1_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")
    address_list = db.relationship("StudentAddress", uselist=True, backref=backref("student", uselist=False), lazy="dynamic")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class StudentAddress(db.Model):
    __tablename__ = "t_1vn_student_address"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(50), default="默认", comment="地址名称")
    province = db.Column(db.String(50), comment="省份")
    city = db.Column(db.String(50), comment="城市")
    area = db.Column(db.String(50), comment="地区")
    address = db.Column(db.String(500), comment="详细地址")
    mobile = db.Column(db.String(15), comment="收货人电话")
    # 外键字段[记录到数据库中的字段]
    student_id = db.Column(db.Integer, db.ForeignKey("t_1v1_student.id"), comment="student外键")
    # 关联属性
    # 外键模型--> 主模型   StudentAddress.student  结果是一个模型对象
    # 主模型  --> 外键模型 Student.address_list  结果是一个列表
    # student = db.relationship("Student", uselist=False, backref=backref("address_list", uselist=True, lazy="dynamic"))

    def __repr__(self):
        return f"<{self.student.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """添加操作"""
    # # 主模型已存在，添加外键模型
    # student = Student(name="张小白", age=15, sex=True, email="zhangxb@qq.com", money=10000)
    # db.session.add(student)
    # db.session.commit()
    #
    # student.address_list = [
    #     StudentAddress(name="家里", province="北京市", city="北京市", area="昌平区", address="百沙路201", mobile="13012345678"),
    #     StudentAddress(name="学校", province="北京市", city="北京市", area="昌平区", address="百沙路202", mobile="13012345678"),
    #     StudentAddress(name="公司", province="北京市", city="北京市", area="昌平区", address="百沙路203", mobile="13012345678"),
    # ]
    # db.session.commit()


    # # 添加主模型的同时，添加外键模型
    # student = Student(
    #     name="李大宝",
    #     age=21,
    #     sex=True,
    #     email="lidabao@qq.com",
    #     money=10000,
    #     address_list=[
    #         StudentAddress(name="家里", province="北京市", city="北京市", area="昌平区", address="百沙路301", mobile="13312345678"),
    #         StudentAddress(name="学校", province="北京市", city="北京市", area="昌平区", address="百沙路302", mobile="13312345678"),
    #         StudentAddress(name="公司", province="北京市", city="北京市", area="昌平区", address="百沙路303", mobile="13312345678"),
    #     ]
    # )
    # db.session.add(student)
    # db.session.commit()


    # # 添加外键模型的同时，添加主模型
    # address = StudentAddress(
    #     name="家里",
    #     province="北京市",
    #     city="北京市",
    #     area="昌平区",
    #     address="顺沙路102",
    #     mobile="13312345678",
    #     student = Student(
    #         name="李小白",
    #         age=18,
    #         sex=True,
    #         email="lixiaobai@qq.com",
    #         money=10000,
    #     )
    # )
    # db.session.add(address)
    # db.session.commit()


    """查询操作"""
    student = Student.query.filter(Student.name=="张小白").first()

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```



#### 多对多

常见业务：用户收藏文章/商品、用户与用户之间的好友关系、点赞、评论、关注、用户浏览商品的历史记录、订阅文章、专题/活动与商品/文章的关系。

```python
# 关系表[这种表，无法提供给python进行操作的，仅仅用于在数据库中记录两个模型之间的关系]
student_and_course = db.Table(
    "table_student_course",
    db.Column("id", db.Integer, primary_key=True, comment="主键ID"),
    db.Column("sid", db.Integer, db.ForeignKey("table_student.id"), comment="学生"),
    db.Column("cid", db.Integer, db.ForeignKey("table_course.id"), comment="课程"),
    db.Column("created_time", db.DateTime, default=datetime.now, comment="购买时间"), # 当前字段无法操作
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True,comment="主键")
    ...
    course_list = db.relationship("Course", secondary=student_and_course, backref="student_list", lazy="dynamic")

class Course(db.Model):
    ...

# 关系模型，[关系模型和关系表，任选其一]
class Achievement(db.Model):
    ...
```



##### 基于第三方关系表构建多对多

代码：

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


# 购买关系表[这种表，无法提供给flask进行数据操作的，仅仅用于在数据库中记录两个模型之间的关系]
student_course_table = db.Table(
    "t_nvm_student_course",
    db.Column("id", db.Integer, primary_key=True, comment="主键"),
    db.Column("sid", db.Integer, db.ForeignKey("t_nvm_student.id"), comment="学生ID"),
    db.Column("cid", db.Integer, db.ForeignKey("t_nvm_course.id"), comment="课程ID"),
    db.Column("created_time", db.DateTime, default=datetime.now, comment="购买时间"),  # 当前字段无法操作
)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_nvm_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")
    # 只有设置关联属性以后，flask中才提供模型关联的操作
    # course_list = db.relationship("Course", secondary=student_course_table, backref="student_list", lazy="dynamic")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_nvm_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")
    student_list = db.relationship("Student", secondary=student_course_table, backref="course_list", lazy="dynamic")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """添加数据"""

    # 添加其中一个主模型数据时，同时绑定添加另外一个主模型的数据，这个过程中，关系表会自动写入2者的关系数据，绑定2个模型之间的关系

    # student = Student(
    #     name="xiaozhao",
    #     age=13,
    #     sex=False,
    #     course_list=[
    #         Course(name="python入门"),
    #         Course(name="python初级"),
    #         Course(name="python进阶"),
    #     ]
    # )
    # db.session.add(student)
    # db.session.commit()


    # 在已有课程模型的基础上，新增学生，新增报读课程。

    # student = Student(
    #     name="xiaohong",
    #     age=14,
    #     sex=False,
    # )
    # db.session.add(student)
    # db.session.commit()
    #
    # student = Student.query.filter(Student.name == "xiaohong").first()
    # # 让小红新增报读课程id为3的课程
    # student.course_list.append(Course.query.get(3))
    # student.course_list.append(Course(name="python高级"))
    # db.session.commit()


    # 让学生一次性报读多个已有课程

    # student1 = Student.query.get(2)
    # course_list = Course.query.filter(Course.id.in_([1,2])).all()
    # student1.course_list.extend(course_list)
    # db.session.commit()


    """查询数据"""
    # # 查询id为1的学生购买的课程
    # student = Student.query.get(1)
    # print(student.course_list)
    #
    # # 查询id为4的课程，有哪些学生购买了
    # course = Course.query.get(4)
    # print(course.student_list.all())


    """更新数据"""
    # # 给报读了4号课程的同学，返现红包200块钱
    # course = Course.query.get(4)
    # for student in course.student_list:
    #     student.money += 200
    # db.session.commit()


    # db.Table的缺陷: 无法通过主模型直接操作db.Table中的外键之外的其他字段，例如：无法读取购买课程的时间
    course = Course.query.get(3)
    print(course.student_list.all())

    # 解决：在声明2个模型是多对多的关联关系时，如果需要在python中操作关系表的数据，则可以把关联关系使用第三个模型来创建声明，
    # 就是不要使用db.Table创建关系表了，改成关系模型来绑定2者的关系，把模型的多对多拆分成2个1对多

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```

多对多，也可以拆解成3个模型（2个主模型，1个关系模型，关系模型保存了2个主模型的外键），其中tb_achievement作为单独模型存在。



##### 基于第三方关系模型构建多对多

在SQLAlchemy中，基于db.Table创建的关系表，如果需要新增除了外键以外其他字段，无法操作。所以将来实现多对多的时候，除了上面db.Table方案以外，还可以把关系表声明成模型的方法，如果声明成模型，则原来课程和学生之间的多对多的关系，就会变成远程的1对多了。

代码：

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = False

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class StudentCourse(db.Model):
    __tablename__ = "t_nvm_student_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    sid = db.Column(db.Integer, db.ForeignKey("t_nvm_student_2.id"), comment="学生ID")
    cid = db.Column(db.Integer, db.ForeignKey("t_nvm_course_2.id"), comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")
    # 关联属性
    student = db.relationship("Student", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"))
    course = db.relationship("Course", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"))


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_nvm_student_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_nvm_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """添加数据"""
    # 添加其中一个主模型数据时，同时绑定添加另外一个主模型的数据
    # student = Student(
    #     name="xiaozhao",
    #     age=13,
    #     sex=False,
    #     to_relation=[
    #         StudentCourse(course=Course(name="python入门")),
    #         StudentCourse(course=Course(name="python初级")),
    #         StudentCourse(course=Course(name="python进阶")),
    #     ]
    # )
    # db.session.add(student)
    # db.session.commit()

    """在已有课程的基础上，新增学生报读课程。"""
    # student = Student(
    #     name="xiaohong",
    #     age=14,
    #     sex=False,
    #     money=30000,
    # )
    # db.session.add(student)
    # db.session.commit()
    #
    # student = Student.query.filter(Student.name == "xiaohong").first()
    # student.to_relation.extend([
    #     StudentCourse(
    #         course=Course.query.get(1)  # 已经存在的课程，给学生报读
    #     ),
    #     StudentCourse(
    #         course=Course(name="python高级")  # 新增课程，并让当前学生报读该课程
    #     )
    # ])
    # db.session.commit()


    # 已有学生和课程，对学生购买课程进行记录

    # student1 = Student.query.get(2)
    # course_list = Course.query.filter(Course.id.in_([2,3])).all()
    # student1.to_relation.extend([StudentCourse(course=course) for course in course_list])
    # db.session.commit()

    """查询操作"""
    # 查询学生购买的课程
    # student = Student.query.get(1)
    # print([relation.course for relation in student.to_relation])

    # 查看指定课程有哪些学生购买了
    # course = Course.query.get(1)
    # print([relation.student for relation in course.to_relation])

    # 查询2号学生购买的每个课程的时间
    student = Student.query.get(2)
    for relation in student.to_relation:
        print(relation.course.name, relation.created_time)

    """更新数据"""
    # # 给购买了2号课程的学生返现
    # course = Course.query.get(2)
    # for relation in course.to_relation:
    #     relation.student.money += 200
    # db.session.commit()

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```

relationship还有一个设置外键级联级别的属性：cascade="all, delete, delete-orphan"

```
练习：
1. flask中的SQLAlchemy如何进行自关联查询？ 这里自己写一个关于行政区划的1对多的自关联操作[增删查改]。
```



## 逻辑外键

也叫虚拟外键。主要就是在开发中为了减少数据库的性能消耗，提升系统运行效率，一般项目中如果单表数据太大[千万级别]就不会使用数据库本身维护的物理外键，而是采用由ORM或者我们逻辑代码进行查询关联的逻辑外键。当然，不在使用mysql的物理外键，会给数据的一致性带来一定的风险。

SQLAlchemy设置外键模型的虚拟外键，有2种方案：

方案1，查询数据时**临时指定逻辑外键**的映射关系：

```python
模型类.query.join(模型类,主模型.主键==外键模型.外键).join(模型类,主模型.主键==外键模型.外键).with_entities(字段1,字段2.label("字段别名"),....).all()
```

方案2，在**模型声明时指定逻辑外键的映射关系**(最常用，这种设置方案，在操作模型时与原来默认设置的物理外键的关联操作是一模一样的写法)：

```python
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    # 虚拟外键，原有参数不变，新增2个表达关联关系的属性：
    # primaryjoin, 指定2个模型之间的主外键关系，相当于原生SQL语句中的join
    # foreign_keys，指定外键
    address_list = db.relationship("StudentAddress", uselist=True, backref="student", lazy="subquery", primaryjoin="Student.id==StudentAddress.student_id", foreign_keys="StudentAddress.student_id")

class StudentAddress(db.Model):
    # 原来的外键设置为普通索引即可。
    student_id = db.Column(db.Integer, comment="学生id")
```



例1，虚拟外键使用的方案1，代码：

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class StudentCourse(db.Model):
    __tablename__ = "t_virtual_foreign_key_student_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    student_id = db.Column(db.Integer, index=True, comment="学生ID")
    course_id = db.Column(db.Integer, index=True, comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_virtual_foreign_key_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_virtual_foreign_key_course"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """分别给不同的模型添加测试数据"""
    # stu0 = Student(name="xiaozhao", age=15, sex=True, money=1000)
    # stu1 = Student(name="xiaoming", age=16, sex=True, money=1000)
    # stu2 = Student(name="xiaobai", age=18, sex=False, money=1000)
    # stu3 = Student(name="xiaohei", age=21, sex=True, money=1000)
    # stu4 = Student(name="xiaolan", age=18, sex=False, money=1000)
    # db.session.add_all([stu0, stu1, stu2, stu3, stu4])
    #
    # course1 = Course(name="python基础")
    # course2 = Course(name="python入门")
    # course3 = Course(name="python进阶")
    # course4 = Course(name="python高级")
    # course5 = Course(name="python实战")
    # db.session.add_all([course1, course2, course3, course4, course5])
    #
    # # 学生购买课程
    # data = [
    #     StudentCourse(student_id=1,course_id=1),
    #     StudentCourse(student_id=1,course_id=2),
    #     StudentCourse(student_id=1,course_id=3),
    #     StudentCourse(student_id=2,course_id=1),
    #     StudentCourse(student_id=2,course_id=2),
    #     StudentCourse(student_id=3,course_id=3),
    #     StudentCourse(student_id=3,course_id=4),
    #     StudentCourse(student_id=4,course_id=1),
    #     StudentCourse(student_id=4,course_id=2),
    #     StudentCourse(student_id=4,course_id=5),
    #     StudentCourse(student_id=5,course_id=1),
    #     StudentCourse(student_id=5,course_id=2),
    #     StudentCourse(student_id=5,course_id=3),
    #     StudentCourse(student_id=5,course_id=4),
    # ]
    # db.session.add_all(data)
    # db.session.commit()


    """查询3号学生购买了哪些课程？"""
    # # 1. 手动基于代码进行关联查询
    # student_course_list = StudentCourse.query.filter(StudentCourse.student_id==3).all()
    # course_id_list = [relation.course_id for relation in student_course_list]
    # course_list = Course.query.filter(Course.id.in_(course_id_list)).all()
    # print(course_list)

    # 2. 基于临时逻辑外键来关联查询
    # 主模型.query.join(从模型类名, 关系语句)
    # 主模型.query.join(从模型类名, 主模型.主键==从模型类名.外键)

    # # 两个模型的临时逻辑外键关联
    # data = Student.query.join(
    #     StudentCourse, Student.id == StudentCourse.student_id
    # ).with_entities(StudentCourse.course_id).filter(Student.id==3).all()
    # print(data)

    # # 两个以上模型的临时逻辑外键关联
    data = Student.query.join(
        StudentCourse, Student.id == StudentCourse.student_id
    ).join(
        Course, StudentCourse.course_id == Course.id
    ).with_entities(
        StudentCourse.course_id, Course.name
    ).filter(Student.id==3).all()

    print(data)


    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```



例2，虚拟外键使用的方案2，代码：

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class StudentCourse(db.Model):
    __tablename__ = "t_virtual_foreign_key_student_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    student_id = db.Column(db.Integer, index=True, comment="学生ID")
    course_id = db.Column(db.Integer, index=True, comment="课程ID")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="购买时间")
    # 关联属性[比原来设置物理外键，多出2个属性设置：primaryjoin与foreign_keys]
    student = db.relationship("Student", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"),
       primaryjoin="Student.id==StudentCourse.student_id",
       foreign_keys="StudentCourse.student_id"
    )
    course = db.relationship("Course", uselist=False, backref=backref("to_relation", uselist=True, lazy="dynamic"),
       primaryjoin="Course.id==StudentCourse.course_id",
       foreign_keys="StudentCourse.course_id"
    )

class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_virtual_foreign_key_student_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class Course(db.Model):
    """课程信息模型"""
    __tablename__ = "t_virtual_foreign_key_course_2"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(255), unique=True, comment="课程")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    """分别给不同的模型添加测试数据"""
    # stu0 = Student(name="xiaozhao", age=15, sex=True, money=1000)
    # stu1 = Student(name="xiaoming", age=16, sex=True, money=1000)
    # stu2 = Student(name="xiaobai", age=18, sex=False, money=1000)
    # stu3 = Student(name="xiaohei", age=21, sex=True, money=1000)
    # stu4 = Student(name="xiaolan", age=18, sex=False, money=1000)
    # db.session.add_all([stu0, stu1, stu2, stu3, stu4])
    #
    # course1 = Course(name="python基础")
    # course2 = Course(name="python入门")
    # course3 = Course(name="python进阶")
    # course4 = Course(name="python高级")
    # course5 = Course(name="python实战")
    # db.session.add_all([course1, course2, course3, course4, course5])
    #
    # # 学生购买课程
    # data = [
    #     StudentCourse(student_id=1,course_id=1),
    #     StudentCourse(student_id=1,course_id=2),
    #     StudentCourse(student_id=1,course_id=3),
    #     StudentCourse(student_id=2,course_id=1),
    #     StudentCourse(student_id=2,course_id=2),
    #     StudentCourse(student_id=3,course_id=3),
    #     StudentCourse(student_id=3,course_id=4),
    #     StudentCourse(student_id=4,course_id=1),
    #     StudentCourse(student_id=4,course_id=2),
    #     StudentCourse(student_id=4,course_id=5),
    #     StudentCourse(student_id=5,course_id=1),
    #     StudentCourse(student_id=5,course_id=2),
    #     StudentCourse(student_id=5,course_id=3),
    #     StudentCourse(student_id=5,course_id=4),
    # ]
    # db.session.add_all(data)
    # db.session.commit()

    """查询3号学生购买了哪些课程？"""
    student = Student.query.get(3)
    print([{"id":relation.course.id, "name": relation.course.name} for relation in student.to_relation.all()])

    """查询5个课程都有哪些学生购买了?"""
    course = Course.query.get(5)
    print([{"id":relation.student.id, "name": relation.student.name} for relation in course.to_relation.all()])

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```

# 数据迁移

- 在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据，所以往往更常见的方式就是使用alter来改变数据结构，原有数据中的新字段值设置默认值或null=True.
- 更好的解决办法是使用数据迁移，它可以追踪数据库表结构的变化，然后把变动的历史信息记录到数据库中。
- 在Flask中可以使用Flask-Migrate的第三方扩展来实现数据迁移。并且集成到Flask终端脚本中，所有操作通过`flask db`命令就能完成。
- 为了导出数据库迁移命令，Flask-Migrate提供了一个MigrateCommand类，可以注册到flask框架中。

首先要在虚拟环境中安装Flask-Migrate。

```bash
pip install Flask-Migrate
```

官网地址：https://flask-migrate.readthedocs.io/en/latest/

为了方便迁移操作，我们新建一个flask_student的数据库。

```bash
create database flask_student charset=utf8mb4;
```



代码文件内容：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import backref

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/school?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)
# 把数据迁移绑定当前应用对象中，与SQLAlchemy的数据库ORM模块进行关联
migrate = Migrate()
migrate.init_app(app, db)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_migrate_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), unique=True, comment="邮箱地址")
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")
    address_list = db.relationship("StudentAddress", uselist=True, backref=backref("student", uselist=False), lazy="dynamic")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"


class StudentAddress(db.Model):
    __tablename__ = "t_migrate_student_address"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(50), default="默认", comment="地址名称")
    province = db.Column(db.String(50), comment="省份")
    city = db.Column(db.String(50), comment="城市")
    area = db.Column(db.String(50), comment="地区")
    address = db.Column(db.String(500), comment="详细地址")
    mobile = db.Column(db.String(15), comment="收货人电话")
    student_id = db.Column(db.Integer, db.ForeignKey("t_migrate_student.id"), comment="student外键")

    def __repr__(self):
        return f"<{self.student.name} {self.__class__.__name__}>"

@app.route("/")
def index():
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)

```

## 创建迁移版本仓库

```bash
# 切换到项目根目录下
cd ~/Desktop/flaskdemo
# 设置flask项目的启动脚本位置，例如我们现在的脚本叫manage.py
export FLASK_APP=manage.py
# 数据库迁移初始化，这个命令会在当前项目根目录下创建migrations文件夹，将来所有数据表相关的迁移文件都放在里面。
flask db init
```



## 创建迁移版本

- 自动创建迁移版本文件中有两个函数，用于进行数据迁移同步到数据库操作的。
  - upgrade()：把迁移中的改动代码同步到数据库中。
  - downgrade()：则将改动代码从数据库中进行还原。
- 自动创建的迁移脚本会根据模型定义和数据库当前状态的差异，生成upgrade()和downgrade()函数的内容。
- 生成的迁移文件不一定完全正确，有可能代码中存在细节遗漏导致报错，需要开发者进行检查，特别在多对多的时候

```bash
# 根据flask项目的模型生成迁移文件 -m的后面你不要使用中文！！
flask db migrate -m 'initial migration'
# 这里等同于django里面的 makemigrations，生成迁移版本文件
# 完成2件事情：
# 1. 在migrations/versions生成一个数据库迁移文件
# 2. 如果是首次生成迁移文件的项目，则迁移工具还会在数据库创建一个记录数据库版本的alembic_version表
```



## 升级版本库的版本

把当前ORM模型中的代码改动同步到数据库。

```bash
# 从migations目录下的versions中根据迁移文件upgrade方法把数据表的结构同步到数据库中。
flask db upgrade
```

## 降级版本库的版本

```bash
# 从migations目录下的versions中根据迁移文件downgrade把数据表的结构同步到数据库中。
flask db downgrade
```



## 版本库的历史管理

可以根据history命令找到版本号,然后传给downgrade命令:

```bash
flask db history

输出格式：<base> ->  版本号 (head), initial migration
```



## 回滚到指定版本

```bash
flask db downgrade # 默认返回上一个版本
flask db downgrade 版本号   # 回滚到指定版本号对应的版本
flask db upgrade 版本号     # 升级到指定版本号对应的版本
```



数据迁移的步骤：

```bash
# 1. 初始化数据迁移的目录
export FLASK_APP=4-manage.py
flask db init

# 2. 数据库的数据迁移版本初始化，生成迁移文件
flask db migrate -m 'initial migration'

# 3. 升级版本[新增一个迁移记录]
flask db upgrade

# 4. 降级版本[回滚一个迁移记录]
flask db downgrade
```

> 注意：
>
> 使用数据迁移的过程中，不管是upgrade还是downgrade，只会影响到数据表结构，不会还原代码中的模型代码，所以，如果要恢复还原某些字段的删除操作，还需要开发者自己手动还原代码。

# 常用模块

## Faker[阅读]

文档: https://faker.readthedocs.io/en/master/locales/zh_CN.html

批量生成测试数据: https://github.com/joke2k/faker

```bash
pip install faker -i https://pypi.douban.com/simple
```

代码：

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 连接数据库连接url
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3306/flask_student?charset=utf8mb4"
# 动态追踪修改设置，如未设置只会提示警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()
db.init_app(app)


class Student(db.Model):
    """学生信息模型"""
    __tablename__ = "t_faker_student"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    name = db.Column(db.String(15), index=True, comment="姓名")
    age = db.Column(db.SmallInteger, comment="年龄")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(128), comment="邮箱地址")
    created_time = db.Column(db.DateTime, default=datetime.now)
    money = db.Column(db.Numeric(10, 2), default=0.0, comment="钱包")

    def __repr__(self):
        return f"<{self.name} {self.__class__.__name__}>"



"""基于Faker生成仿真数据的终端命令"""
# 自定义批量生成学生
import random, click
from faker import Faker

faker = Faker(locale="ZH_CN")

# 自定义终端命令
@app.cli.command("faker_user")
@click.argument("num", default=10, type=int)  # 命令的选项
def faker_user_command(num):
    """生成测试学生信息"""
    data_list = []
    for i in range(num):
        sex = bool( random.randint(0,1) )
        student = Student(
            name= faker.name_male() if sex else faker.name_female(),
            age=random.randint(15,60),
            sex=sex,
            email=faker.unique.free_email(),
            money=float( random.randint(100,100000) / 100 ),
            created_time=faker.date_time(),
        )
        data_list.append(student)
    # 在循环外
    db.session.add_all(data_list)
    db.session.commit()


@app.route("/")
def index():

    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```



## flask-session

flask框架中，默认会以cookie的方式把session数据分散保存到客户端中，并非真正意义上的session，所以这种session不能保存一些相对隐秘的数据。因此，我们可以使用第三方模块 flask-session，把session重新指定保存到服务端的数据库或缓存中。

flask-session，允许设置session到指定的存储空间中，例如：**redis**/mongoDB/mysql。

官方文档: https://flask-session.readthedocs.io/en/latest/

```
pip install Flask-Session -i https://pypi.douban.com/simple
```

使用session之前,必须配置一下配置项:

```python
# session秘钥
app.config["SECRET_KEY"] = "*(%#4sxcz(^(#$#8423"
```



### SQLAlchemy存储session的基本配置

需要手动创建session表，在项目第一次启动的时候，使用`db.create_all()`来完成创建。

```python
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# 引入sessio操作类，注意：引入路径不同，大小写不同的。
from flask_session import Session as SessionStore
from flask import session

app = Flask(__name__)

# 把SQLAlchemy组件注册到项目中
db = SQLAlchemy()

# 初始化session存储类
session_store = SessionStore()

app.config.update({
    # 使用session必须设置秘钥
    "SECRET_KEY": "*(%#4sxcz(^(#$#8423",

    # 要把存储到SQLAlchemy，必须配置数据库连接
    "SQLALCHEMY_DATABASE_URI": "mysql://root:123@127.0.0.1:3306/flask_student?charset=utf8mb4",
    "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    "SQLALCHEMY_ECHO": False,

    # 把session通过SQLAlchmey保存到mysql中
    "SESSION_TYPE": "sqlalchemy",  # session类型为sqlalchemy
    "SESSION_SQLALCHEMY": db,  # SQLAlchemy的数据库连接对象
    "SESSION_SQLALCHEMY_TABLE": 'sessions',  # session要保存的表名称
    "SESSION_PERMANENT": True,  # 如果设置为True，则关闭浏览器session就失效
    "SESSION_USE_SIGNER": True,  # 是否对发送到浏览器上session的cookie值进行添加签名，防止串改。
    "SESSION_KEY_PREFIX": "session:"  # session数据表中sessionID的前缀，默认就是 session:
})

db.init_app(app)
# 务必保证在数据库配置初始化以后才进行session存储类的初始化
session_store.init_app(app)

@app.route("/")
def index():
    return "ok"

@app.route("/set_session")
def set_session():
    session["uname"] = "xiaoming"
    session["age"] = 18
    return "ok"


@app.route("/get_session")
def get_session():
    print(session.get("uname"))
    print(session.get("age"))
    return "ok"


@app.route("/del_session")
def del_session():
    # 此处的删除，不是删除用户对应的session表记录，而是删除session值而已。
    print(session.pop("uname"))
    print(session.pop("age"))
    return "ok"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

```



### redis保存session的基本配置[常用]

这个功能必须确保，服务器必须已经安装了redis而且当前项目虚拟环境中已经安装了redis扩展库

```bash
pip install flask-redis -i https://pypi.douban.com/simple
```

flask-redis是第三方开发者为了方便我们在flask框架中集成redis数据库操作所封装一个redis操作库,（底层还是pyredis）、

在flask中要基于flask-redis进行数据库则可以完成以下3个步骤即可：

```bash
from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)

app.config.update({
    "REDIS_SESSION_URL": "redis://default:default@127.0.0.1:6379/0",
    "REDIS_USER_URL": "redis://default:default@127.0.0.1:6379/1",
    "REDIS_ORDER_URL": "redis://default:default@127.0.0.1:6379/2",
})

# redis中默认有16个数据库，我们可以让flask_redis初始化时，默认连接到不同的库中，当然这需要我们设置配置redis的前缀config_prefix
session_redis = FlaskRedis(config_prefix="REDIS_SESSION")
user_redis = FlaskRedis(config_prefix="REDIS_USER")
order_redis = FlaskRedis(config_prefix="REDIS_ORDER")

# 初始化 flask_redis
session_redis.init_app(app)
user_redis.init_app(app)
order_redis.init_app(app)

@app.route("/")
def index():
    session_redis.setnx("age", 100)
    user_redis.setnx("user_id", 100)
    order_redis.setnx("order_id", 100)
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)

```



在redis中保存session，代码：

```python
from flask import Flask
from flask_redis import FlaskRedis
from flask import session
from flask_session import Session as SessionStore

app = Flask(__name__)

# redis中默认有16个数据库，我们可以让flask_redis初始化时，默认连接到不同的库中，当然这需要我们设置配置redis的前缀config_prefix
session_redis = FlaskRedis(config_prefix="REDIS_SESSION")
user_redis = FlaskRedis(config_prefix="REDIS_USER")
order_redis = FlaskRedis(config_prefix="REDIS_ORDER")

app.config.update({
    "SECRET_KEY": "my-secret_key",
    "REDIS_SESSION_URL": "redis://default:default@127.0.0.1:6379/0",
    "REDIS_USER_URL": "redis://default:default@127.0.0.1:6379/1",
    "REDIS_ORDER_URL": "redis://default:default@127.0.0.1:6379/2",

    # 把session保存到redis中
    "SESSION_TYPE": "redis",  # session类型为sqlalchemy, redis 或 mongodb
    "SESSION_PERMANENT": True,  # 如果设置为True，则关闭浏览器session就失效
    "SESSION_USE_SIGNER": True,  # 是否对发送到浏览器上session的cookie值进行添加签名，防止串改。
    "SESSION_KEY_PREFIX": "session:",  # session数据表中sessionID的前缀，默认就是 session:
    # session保存数据到redis时启用的链接对象
    "SESSION_REDIS": session_redis,  # 用于连接redis的配置
})

# 初始化 flask_redis
session_redis.init_app(app)
user_redis.init_app(app)
order_redis.init_app(app)


# 务必保证session存储类初始化之前，redis已经完成初始化了。
session_store = SessionStore()
session_store.init_app(app)


@app.route("/")
def index():
    session_redis.setnx("age", 100)
    user_redis.setnx("user_id", 100)
    order_redis.setnx("order_id", 100)
    return "ok"


@app.route("/set_session")
def set_session():
    session["uname"] = "xiaoming"
    session["age"] = 18
    return "ok"


@app.route("/get_session")
def get_session():
    print(session.get("uname"))
    print(session.get("age"))
    return "ok"


@app.route("/del_session")
def del_session():
    # 此处的删除，不是删除用户对应的session表记录，而是删除session值而已。
    print(session.pop("uname"))
    print(session.pop("age"))
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)

```

# 蓝图 Blueprint

## 模块化

随着flask程序越来越复杂,我们需要对程序进行模块化的处理,之前学习过django的子应用管理,flask程序进行可以进行类似的模块化处理保存代码。

简单来说，Blueprint 是一个存储视图方法/模型代码的容器（目录），这些操作在这个Blueprint 被注册到flask的APP实例对象应用之后就可以被调用，Flask 可以通过Blueprint来组织URL以及处理客户端请求的视图。

Flask使用Blueprint让应用实现模块化，在Flask中Blueprint具有如下属性：

- 一个项目可以具有多个Blueprint
- 可以将一个Blueprint注册到任何一个未使用的URL下比如 “/”、“/users”或者子域名，也就是说每一个蓝图都可以像django那样有属于自己的路由前缀
- 在一个flask项目中，同一个BluePrint模块可以注册多次，也就是说一个蓝图可以对应多个不同的url地址。
- Blueprint目录可以保存单独属于自己的模板目录保存自己的模板文件、静态文件或者其它的通用操作方法，它并不是必须要实现应用的视图和函数的
- 在一个flask项目初始化时，就应该要注册需要使用的Blueprint，否则项目不识别Blueprint蓝图

注意：flask中的Blueprint并不是一个完整的项目应用，它不能独立运行，而必须要把蓝图blueprint注册到某一个flask项目中才能使用。

在flask中，要使用蓝图Blueprint可以分为四个步骤：



1.手动创建一个蓝图的包目录,例如**users**,并在``__init__.py``文件中创建蓝图实例对象users_blueprint

`users/__init.py`，代码：

```python
from flask import Blueprint

# 等同于 app = Flask(__name__)，只是这里并非一个独立的flask项目，
# 所以需要在第一个参数中，指定蓝图名称，其他参数与之前实例化app应用对象是一样的。
users_blueprint = Blueprint("users", __name__)
```

2.在这个users蓝图目录下创建蓝图的子文件, 其中我们可以创建views.py文件,保存当前蓝图使用的视图函数

`users/views.py`，代码：

```python
# 光写视图，不用写路由
def login():
    return "用户登录视图"

def register():
    return "用户注册视图"
```

3.在`users/__init__.py`中引入views.py中所有的视图函数并绑定路由，`users/__init__.py`，代码：

```python
from flask import Blueprint
from . import views

# 等同于 app = Flask(__name__)，只是这里并非一个独立的flask项目，
# 所以需要在第一个参数中，指定蓝图名称，其他参数与之前实例化app应用对象是一样的。
users_blueprint = Blueprint("users", __name__)

# 把蓝图下的视图与蓝图下的路由进行绑定
users_blueprint.add_url_rule(rule="/login", view_func=views.login)
users_blueprint.add_url_rule(rule="/register", view_func=views.register)
```

4.在主应用下程序入口manage.py文件中把这个**users_blueprint**蓝图对象注册app实例对象中，运行起来。

manage.py，代码：

```python
from flask import Flask

app = Flask(__name__)

# 注册蓝图
from users import users_blueprint
app.register_blueprint(blueprint=users_blueprint, url_prefix="/users")

if __name__ == '__main__':
    app.run(debug=True)
```

当这个应用启动后,通过/users/login或者/users/register可以访问到蓝图中定义的视图函数

![image-20221009205503415](assets/image-20221009205503415.png)



## 蓝图运行机制

- 蓝图Blueprint实际上的作用就是，充当当前蓝图目录下的所有视图和url路由地址的绑定关系的临时容器
- 在视图函数被蓝图对象的add_url_rule方法注册时,这个操作本质就是将视图和url地址的映射关系添加到蓝图的子路由列表deferred_functions中。
- 蓝图对象根本没有路由机制的，当我们在蓝图中的视图函数上调用route装饰器（或者add_url_role函数）注册路由时,它只是在蓝图对象的内部的 deferred_functions（子路由列表）中添加了一个路由项（路由项实际上就是一个绑定了视图和url地址的lambda匿名函数）
- 当执行app.register_blueprint()注册蓝图时，app应用实例对象会将从蓝图对象的 deferred_functions列表中循环取出每一个之前注册的路由项，并把app应用实例对象自己作为参数执行路由项对应的lambda匿名函数，lambda匿名函数执行以后就会调用app.add_url_rule() 方法，这就将蓝图下子路由列表之前暂存的路由全部添加到了app应用实例对象的url_map总路由表中了，所以用户就可以在flask中访问到了蓝图中的视图。当然，能访问蓝图下的视图，自然也就可以通过视图调用其他的功能，例如：蓝图下的其他功能函数或其他的模型对象了。

![image-20221009210031552](assets/image-20221009210031552.png)



## 蓝图的url拼接

当我们在app应用实例对象上注册一个蓝图时，可以指定一个url_prefix关键字参数（这个参数默认是/）

![image-20220105173129138](assets/image-20220105173129138.png)

在app应用实例对象的最终的路由表 url_map中，在蓝图上注册的路由URL自动被加上了这个路由前缀，这个可以保证在多个蓝图中使用相同的子路由而不会最终引起冲突，只要在注册蓝图时将不同的蓝图挂接到不同的自路径即可。

注意：有了蓝图以后，在flask使用url_for在使用时，如果要生成一个蓝图里面的视图对应的路由地址，则需要声明当前蓝图名称+视图名称

```python
# url_for('蓝图名称.视图函数名')
url_for('users.login') # /users + /login   /users就是蓝图中的路由前缀  /login就是子路由
```

users/views.py，代码：

```python
from flask import url_for
# 光写视图，不用写路由
def login():
    return "用户登录视图"

def register():
    return f"用户注册视图，登录视图的url地址：{url_for('users.login')}"
```

访问：

![image-20220105173329978](assets/image-20220105173329978.png)



## 注册蓝图下的静态文件[很少使用]

和没有学习蓝图之前的app应用对象不同，蓝图对象创建时不会默认注册静态目录的路由。需要我们在创建时手动指定 static_folder参数。

下面的代码将蓝图所在目录下的static_users目录设置为静态目录

`users/__init__.py`,代码：

```python
from flask import Blueprint
from . import views

# 等同于 app = Flask(__name__)，只是这里并非一个独立的flask项目，
# 所以需要在第一个参数中，指定蓝图名称，其他参数与之前实例化app应用对象是一样的。
users_blueprint = Blueprint("users", __name__, static_folder="static")

# 把蓝图下的视图与蓝图下的路由进行绑定
users_blueprint.add_url_rule(rule="/login", view_func=views.login)
users_blueprint.add_url_rule(rule="/register", view_func=views.register)

print(users_blueprint.deferred_functions)
```

![image-20221009214224702](assets/image-20221009214224702.png)

现在就可以使用http://127.0.0.1:5000/users/static/6.png 访问users/static/目录下的静态文件了。



## 设置蓝图下的html模版[很少使用]

创建蓝图下的模板目录templates，`users/__init__.py`，代码：

```python
from flask import Blueprint
from . import views

# 等同于 app = Flask(__name__)，只是这里并非一个独立的flask项目，
# 所以需要在第一个参数中，指定蓝图名称，其他参数与之前实例化app应用对象是一样的。
users_blueprint = Blueprint("users", __name__, static_folder="static", template_folder="templates")

# 把蓝图下的视图与蓝图下的路由进行绑定
users_blueprint.add_url_rule(rule="/login", view_func=views.login)
users_blueprint.add_url_rule(rule="/register", view_func=views.register)

print(users_blueprint.deferred_functions)
```

视图`users/views.py`，代码：

```python
from flask import url_for, render_template
# 光写视图，不用写路由
def login():
    title = "用户登录视图"
    return render_template("login.html", **locals())

def register():
    return f"用户注册视图，登录视图的url地址：{url_for('users.login')}"
```

模板代码，`users/templates/index.html`，代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>
  <h1>{{title}}</h1>
  <p>templates/login.html</p>
</body>
</html>
```

![image-20221009214546376](assets/image-20221009214546376.png)

> 注意：
>
> 如果公司使用了flask1.x版本，则不能出现项目根目录下和蓝图目录下2个templates目录的情况，否则项目根目录下的templates模板会覆盖蓝图目录下的同名模板，flask会优先加载项目根目录下的模板。flask2.x版本已经解决上面的问题。