# Marshmallow

官方文档：https://marshmallow.readthedocs.io/en/latest/

Marshmallow，中文译作：棉花糖。是一个轻量级的数据格式转换的模块，也叫序列化和反序列化模块，常用于将复杂的orm模型对象与python原生数据类型之间相互转换。marshmallow提供了丰富的api功能。如下：

>   1.  **Serializing**
>
>       序列化[可以把数据对象转化为可存储或可传输的数据类型，例如：objects/object->list/dict，dict/list->string]
>
>   2.  **Deserializing**
>
>       反序列化器[把可存储或可传输的数据类型转换成数据对象，例如：list/dict->objects/object，string->dict/list]
>
>   3.  **Validation**
>
>       数据校验，可以在反序列化阶段，针对要转换数据的内容进行类型验证或自定义验证。

Marshmallow本身是一个单独的库，基于我们当前项目使用框架是flask并且数据库ORM框架使用SQLAlchemy，所以我们可以通过安装flask-sqlalchemy和marshmallow-sqlalchemy集成到项目就可以了。

## 基本安装和配置

模块安装：

```bash
pip install -U marshmallow-sqlalchemy
pip install -U flask-sqlalchemy
pip install -U flask-marshmallow
```

Marshmallow模块快速使用，我们单独创建一个python文件进行基本的使用，docs/main.py：

```python
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123@127.0.0.1:3306/mofang?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

ma = Marshmallow()
ma.init_app(app)


class User(db.Model):
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    username = db.Column(db.String(255), index=True, comment="用户名")
    password = db.Column(db.String(255), comment="登录密码")
    mobile = db.Column(db.String(15), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(255), index=True, comment="邮箱")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.name,self.username)


@app.route("/")
def index():
    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5555)
```



## 基本构造器(Schema)

也可以叫基本模式类或基本序列化器类。

marshmallow转换数据格式主要通过构造器类（序列化器）来完成。在marshmallow使用过程中所有的构造器类必须直接或间接继承于Schema基类，而Schema基类提供了数据转换的基本功能：序列化，验证数据和反序列化。



### 基于Schema完成数据序列化转换

```python
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123@127.0.0.1:3306/yingming?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy()
db.init_app(app)

ma = Marshmallow()
ma.init_app(app)


"""模型"""
class User(db.Model):
    __tablename__ = "desc_user"
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    username = db.Column(db.String(255), index=True, comment="用户名")
    password = db.Column(db.String(255), comment="登录密码")
    mobile = db.Column(db.String(15), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(255), index=True, comment="邮箱")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.username)


"""序列化器"""

from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.String()
    mobile = fields.String()
    sex = fields.Boolean()
    email = fields.Email()
    created_time = fields.DateTime()
    updated_time = fields.DateTime()



@app.route("/1")
def index1():
    """序列化一个对象成字典或字符串"""
    # 模拟从数据库中读取出来的模型类
    user = User(
        username="xiaoming",
        mobile="13312345677",
        sex=True,
        email="133123456@qq.com",
        created_time=datetime.now(),
        updated_time=datetime.now()
    )

    db.session.add(user)
    db.session.commit()
    print(user)

    # 序列化成一个字典
    us = UserSchema()
    result = us.dump(user)
    print(result, type(result))

    # 序列化器成一个字符串[符合json语法]
    result = us.dumps(user)
    print(result, type(result))

    # 如果要序列化多个模型对象，可以使用many=True
    result = us.dump([user,user,user], many=True)
    print(result)
    result = us.dumps([user,user,user], many=True)
    print(result)
    return "ok"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
```



**schema常用属性数据类型**

| 类型                                                         | 描述                                     |
| ------------------------------------------------------------ | ---------------------------------------- |
| fields.[`Dict`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Dict)(keys, type]] = None, values, …) | 字典类型，常用于接收json类型数据         |
| fields.[`List`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.List)(cls_or_instance, type], **kwargs) | 列表类型，常用于接收数组数据             |
| fields.[`Tuple`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Tuple)(tuple_fields, *args, **kwargs) | 元组类型                                 |
| fields.[`String`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.String)(*, default, missing, data_key, …) | 字符串类型                               |
| fields.[`UUID`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.UUID)(*, default, missing, data_key, …) | UUID格式类型的字符串                     |
| fields.[`Number`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Number)(*, as_string, **kwargs) | 数值基本类型                             |
| fields.[`Integer`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Integer)(*, strict, **kwargs) | 整型                                     |
| fields.[`Decimal`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Decimal)(places, rounding, *, allow_nan, …) | 数值型                                   |
| fields.[`Boolean`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Boolean)(*, truthy, falsy, **kwargs) | 布尔型                                   |
| fields.[`Float`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Float)(*, allow_nan, as_string, **kwargs) | 浮点数类型                               |
| fields.[`DateTime`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.DateTime)(format, **kwargs) | 日期时间类型                             |
| fields.[`Time`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Time)(format, **kwargs) | 时间类型                                 |
| fields.[`Date`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Date)(format, **kwargs) | 日期类型                                 |
| fields.[`Url`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Url)(*, relative, schemes, Set[str]]] = None, …) | url网址字符串类型，自带url地址的校验规则 |
| fields.[`Email`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Email)(*args, **kwargs) | 邮箱字符串类型，自带email地址的校验规则  |
| fields.[`IP`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.IP)(*args[, exploded]) | IP地址字符串类型                         |
| fields.[`IPv4`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.IPv4)(*args[, exploded]) | IPv4地址字符串类型                       |
| fields.[`IPv6`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.IPv6)(*args[, exploded]) | IPv6地址字符串类型                       |
| fields.[`Method`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Method)(serialize, deserialize, **kwargs) | 基于Schema类方法返回值的字段             |
| fields.[`Function`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Function)(serialize, Any], Callable[[Any, …) | 基于函数返回值得字段                     |
| fields.[`Nested`](https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Nested)(nested, type, str, Callable[[], …) | 嵌套类型或外键类型                       |



**Schema数据类型的常用通用属性**

| 属性名             | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **default**        | 序列化阶段中设置字段的默认值                                 |
| **missing**        | 反序列化阶段中设置字段的默认值                               |
| **validate**       | 反序列化阶段调用的内置数据验证器或者内置验证集合             |
| **required**       | 反序列化阶段调用的，设置当前字段的必填字段                   |
| **allow_none**     | 反序列化阶段调用的，是否允许为空                             |
| **load_only**      | 是否在反序列化阶段才使用到当前字段，相当于drf框架的write_only |
| **dump_omly**      | 是否在序列化阶段才使用到当前字段，相当于drf框架的read_only   |
| **error_messages** | 使用校验值validate选项以后设置的错误提示，字典类型，可以用来替代默认的字段异常提示语，格式：<br>error_messages={“required”: “用户名为必填项。”} |



#### 构造器嵌套使用

```python
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123@127.0.0.1:3306/yingming?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy()
db.init_app(app)

ma = Marshmallow()
ma.init_app(app)


"""模仿ORM的模型"""
class Model(object):
    pass

class User(Model):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.now()
        self.books = []    # 用来代替MySQL中的外检关系，实现1对多或多对多
        self.friends = []  # 用来代替MySQL中的外检关系，实现自关联


class Book(Model):
    def __init__(self, title, author):
        self.title = title
        self.author = author  # 用来代替MySQL中的外键关系，1对1

"""序列化器"""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """用户的序列化器"""
    name = fields.String()
    email = fields.Email()
    """1对多，多对多"""
    # 在fields.Nested外围包裹一个List列表字段，则可以返回多个结果了。exclude表示排除
    # books = fields.List(fields.Nested(lambda: BookSchema(exclude=["author"])))
    # 简写方式:
    books = fields.Nested(lambda : BookSchema(many=True, exclude=["author"]))
    """自关联"""
    # 自关联就是一个模型中既存在主键关系，也存在外键关系的情况
    # 方式1：使用自身"self"作为外键的方式，并可以指定序列化模型的多个字段
    # friends = fields.Nested(lambda: "self", only=("name", "email", "books"), many=True)
    # 方式2：使用Pluck字段可以用单个值来替换嵌套的数据，只可以得到模型的单个字段值
    friends = fields.Pluck(lambda: "self", "name", many=True)

class BookSchema(Schema):
    """图书的序列化器"""
    title = fields.String()
    author = fields.Nested(lambda: UserSchema(exclude=["books"]))

@app.route("/1")
def index1():
    """构造器嵌套使用"""
    # 假设根据当前作者，查找对应的作者发布的图书列表
    user0 = User(name="南派三叔", email="sanshu@163.com")

    book1 = Book(title="盗墓笔记1", author=user0)
    book2 = Book(title="盗墓笔记2", author=user0)
    book3 = Book(title="盗墓笔记3", author=user0)
    user0.books = [book1, book2, book3]

    us = UserSchema()
    result = us.dump(user0)
    print(result)

    bs = BookSchema()
    result = bs.dump([book1, book2, book3], many=True)
    print(result)

    return "ok"


@app.route("/2")
def index2():
    """自关联"""
    user0 = User(name="南派三叔", email="sanshu@163.com")
    user1 = User(name="刘慈欣", email="sanshu@163.com")
    user2 = User(name="天下霸唱", email="sanshu@163.com")
    user0.friends = [user1, user2]

    us = UserSchema()
    result = us.dump(user0)
    print(result)

    return "ok"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
```



### 基于Schema完成数据反序列化转换

代码：

```python
from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    # required=True 必填字段，否则可以不填写
    name = fields.Str(required=True, validate=validate.Length(min=3,max=16, error="用户名有误！name必须在{min}~{max}个字符长度之间"))
    email = fields.Email(error_messages={"invalid": "无效的邮箱地址！"})
    age = fields.Int(validate=validate.Range(min=18, max=40, error="{input}有误！age的数值范围是{min}~{max}"))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"], error="permisson只能是read，write和admin，三者之一"))


if __name__ == '__main__':
    # 模拟客户端提交过来的数据
    user_data = {"name": "xiaoming", "email": "ronnie@stones.com", "age": 35, "permission": "write"}
    data_list = [user_data, user_data, user_data]

    us = UserSchema()  # 校验数据
    """校验一个数据"""
    # # 反序列化验证
    # result = us.load(user_data)
    # print(result)

    """校验多个数据"""
    # # 反序列化验证
    result = us.load(data_list, many=True)
    print(result)
```



#### 反序列化转换时忽略部分数据

```python
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    avatar = fields.String(required=True, error_messages={"required":"avatar必须填写！"})

if __name__ == '__main__':
    # result = UserSchema().load({"name":"xiaoming", "age": 42, "avatar": "1.png"})
    result = UserSchema().load({"name":"xiaoming", "age": 42}, partial=("avatar",))  # 取消字段在构造器中设置的required=True的效果
    print(result)  # => {'age': 42}
```



#### 设置字段只在序列化或反序列化阶段才启用

```python
class UserSchema(Schema):
    name = fields.Str()
    password = fields.Str(load_only=True) # 相当于只写字段 "write-only"
    created_time = fields.DateTime(dump_only=True) # 相当于只读字段 "read-only"
```



#### MarshMallow提供的钩子方法

marshmallow提供了一些在反序列化或者序列化阶段时自动执行的钩子装饰器。

```bash
# 序列化之前执行的钩子方法
pre_dump([fn，pass_many]) 注册要在序列化对象之前调用的方法，它会在序列化对象之前被调用。
# 序列化之后执行的钩子方法
post_dump([fn，pass_many，pass_original]) 注册要在序列化对象后调用的方法，它会在对象序列化后被调用。

# 反序列化之前执行的钩子方法
pre_load([fn，pass_many]) 在反序列化对象之前，注册要调用的方法，它会在验证数据之前调用
# 反序列化之后执行的钩子方法
post_load([fn，pass_many，pass_original]) 注册反序列化对象后要调用的方法，它会在验证数据之后被调用。

# 校验指定字段的装饰器，相当于drf的 validate_<字段>(data)
validates(field_name)

# 校验整个构造器中所有数据的装饰器，相当于drf的 validate(data)
validates_schema([fn, pass_many, ...])
```

```python
from datetime import datetime
from marshmallow import Schema, fields, validate, ValidationError, decorators
from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    def __init__(self, name, password, avatar):
        self.name = name
        self.password = password
        self.avatar = avatar
        self.created_time = datetime.now()

    def __str__(self):
        return f"<{self.__class__.__name__} [{self.name}]>"


class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6,max=16))
    # password = fields.Str(load_only=True, required=True)
    # 确认密码是不需要保存到数据库的，仅仅判断用户两次输入密码是否正确
    re_password = fields.Str(required=True, validate=validate.Length(min=6,max=16))
    created_time = fields.DateTime(dump_only=True)
    avatar = fields.Str()

    # 验证单个字段
    @decorators.validates(field_name="name")
    def validate_name(self, data):
        if data == "柯南":
            raise ValidationError(message="对不起，这名字不适合我们学校！！", field_name="name")
        return data


    # 验证所有字段的
    @decorators.validates_schema
    def validate(self, data, *args, **kwargs):
        if data["re_password"] != data["password"]:
            raise ValidationError(message="密码和确认密码不一致！", field_name="re_password")

        # 因为确认密码时不会入库的，所以检验完成以后，就从data中剔除
        data.pop("re_password")
        return data

    @decorators.pre_load
    def pre_load(self, data, *args, **kwargs):
        # 常见：上传文件的处理
        data["avatar"] = "1.png"
        return data

    # 反序列化成功之后自动执行的钩子方法
    @decorators.post_load
    def save_model(self, data, *args, **kwargs):
        # print("反序列化之后")
        # 密码加密或者数据入库
        data["password"] = generate_password_hash(data["password"])
        # 模拟入库代码
        user = User(**data)
        # db.session.add(user)
        # db.session.commit()
        return user

    @decorators.post_dump(pass_many=True) # pass_many 表示是否接受传递进来的many参数
    def post_dump(self, data, many, **kwargs):
        # many=True，则返回多个结果
        print("序列化之前，data=", data)
        return data

    @decorators.pre_dump(pass_many=True)  # pass_many 表示是否接受传递进来的many参数
    def pre_dump(self, data, many, **kwargs):
        # many=True，则返回多个结果
        print("序列化之前，data=", data)
        return data

    @decorators.post_dump(pass_many=True) # pass_many 表示是否接受传递进来的many参数
    def post_dump(self, data, many, **kwargs):
        # many=True，则返回多个结果
        data["created_time"] = data["created_time"].replace("T", " ").split(".")[0]
        print("序列化之后，data=", data)
        return data

if __name__ == '__main__':
    # 模拟客户端提交过来的数据
    data = {"name": "xiaoming", "password": "123456", "re_password": "123456"}
    us = UserSchema()
    ret = us.load(data)
    print(ret.password) # 在这里保存数据到数据库，re_password已经被钩子方法中移除了。

    # # 序列化
    user = User(name="小红", password="password", avatar="1.png")
    ret = us.dump(user)
    print(ret)
```



### 反序列化阶段对数据进行验证

#### 基于内置验证器进行数据验证

| 内置验证器                                                   | 描述            |
| ------------------------------------------------------------ | --------------- |
| validate.[`Email`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.Email)(*, error) | 邮箱验证        |
| validate.[`Equal`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.Equal)(comparable, *, error) | 判断值是否相等  |
| validate.[`Length`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.Length)(min, max, *, equal, error) | 值长度/大小验证 |
| validate.[`OneOf`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.OneOf)(choices, labels, *, error) | 选项验证        |
| validate.[`Range`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.Range)([min, max]) | 范围验证        |
| validate.[`Regexp`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.Regexp)(regex, bytes, Pattern][, flags]) | 正则验证        |
| validate.[`URL`](https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.URL)(*, relative, schemes, Set[str]]] = None, …) | 验证是否为URL   |

代码：

```python
from marshmallow import Schema, fields, validate, ValidationError
class UserSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1))
    permission = fields.Str(validate=validate.OneOf(["read", "write", "admin"]))
    age = fields.Int(validate=validate.Range(min=18, max=40))

if __name__ == '__main__':
    data = {"name": "", "permission": "hello", "age": 71}
	try:
    	UserSchema().load(data)
	except ValidationError as err:
    	pprint(err.messages)
```



#### 自定义验证方法

```python
class ItemSchema(Schema):
    age = fields.Integer()

    @validates_schema
    def validate(self,data):
        """对所有数据进行验证"""
    	return data 
    
    @validates("age")
    def validate_age(self, data):
        """对单个数据进行验证"""
        if data < 10:
            raise ValidationError("年龄必须大于10岁")
        if data > 70:
            raise ValidationError("年龄必须小于70岁")
```



## 模型构造器(ModelSchema)

官方提供了**SQLAlchemyAutoSchema**和**SQLAlchemySchema**这2个类提供给我们用于编写模型构造器。

官方文档：https://github.com/marshmallow-code/marshmallow-sqlalchemy

​                   https://marshmallow-sqlalchemy.readthedocs.io/en/latest/



### SQLAlchemySchema

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123@127.0.0.1:3306/mofang?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)

class User(db.Model):
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    username = db.Column(db.String(255), index=True, comment="用户名")
    password = db.Column(db.String(255), comment="登录密码")
    mobile = db.Column(db.String(15), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(255), index=True, comment="邮箱")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.username)

"""模型构造器"""
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


class UserSQLAlchemySchema(SQLAlchemySchema):
    """
    SQLAlchemySchema提供了一个auto_field方法可以自动从模型中提取当前对应字段声明信息到构造器中，
    但是，我们需要手动声明序列化器中调用的哪些字段，每一个都要写上
    """
    id = auto_field()
    username = auto_field()
    mobile = auto_field()
    email = auto_field()
    created_time = auto_field()
    sex = auto_field()

    class Meta:
        model = User  # 指定当前模型构造器绑定的模型对象
        load_instance = True

@app.route("/")
def index():
    """序列化器数据"""
    """序列化一个数据"""
    # usas = UserSQLAlchemySchema()
    # # user = User.query.get(1)
    # # ret = usas.dump(user)
    # # print(ret)
    """
    {'username': 'xiaoming', 'email': '123@qq.com', 'id': 1, 'sex': True, 'created_time': '2021-11-09T18:26:48', 'mobile': '13312345678'}
    """


    """序列化多个数据"""
    usas = UserSQLAlchemySchema(many=True)
    user = User.query.all()
    ret = usas.dump(user)
    print(ret)
    """
    [{'email': '123@qq.com', 'created_time': '2021-11-09T18:26:48', 'username': 'xiaoming', 'id': 1, 'mobile': '13312345678', 'sex': True}, {'email': '321@qq.com', 'created_time': '2021-11-09T18:26:48', 'username': 'xiaoming', 'id': 2, 'mobile': '13312345671', 'sex': True}]
    """
    return "ok"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8088)
```



#### SQLAlchemyAutoSchema

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123@127.0.0.1:3306/mofang?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)

class User(db.Model):
    __tablename__ = "tb_user"
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    username = db.Column(db.String(255), index=True, comment="用户名")
    password = db.Column(db.String(255), comment="登录密码")
    mobile = db.Column(db.String(15), index=True, comment="手机号码")
    sex = db.Column(db.Boolean, default=True, comment="性别")
    email = db.Column(db.String(255), index=True, comment="邮箱")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.username)

"""模型构造器"""
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from marshmallow import validate


class UserSQLAlchemySchema(SQLAlchemyAutoSchema):
    """
    SQLAlchemyAutoSchema提供了一个fields和exclude属性可以设置从模型类导入指定的字段声明，
    其中，fields设置包含的字段，而exclude设置的排除字段，所以2个属性不能同时使用，互斥的。
    另外，如果针对模型导入的字段声明，我们需要增加对字段的验证、约束，则还是可以手动声明使用auto_fields来进行
    """
    username = auto_field(validate=validate.Length(min=1,max=15))

    class Meta:
        model = User  # 指定当前模型构造器绑定的模型对象
        load_instance = True
        include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理，True表示一并进行序列化器，用于针对序列化器嵌套调用的情况
        include_fk = True  # 序列化阶段是否也一并返回主键
        sql_session = db.session  # 数据库连接会话对象，针对在钩子装饰器中如果希望调用db数据库回话对象，可以在此处声明完成以后，使用时通过sql_session直接调用
        fields = ["id", "username", "mobile", "email", "created_time", "sex"]
        # exclude = ["id", "name"]  # 排除字段列表

@app.route("/")
def index():
    """序列化器数据"""
    # """序列化一个数据"""
    # usas = UserSQLAlchemySchema()
    # user = User.query.get(1)
    # ret = usas.dump(user)
    # print(ret)
    # """
    # {'username': 'xiaoming', 'email': '123@qq.com', 'id': 1, 'sex': True, 'created_time': '2021-11-09T18:26:48', 'mobile': '13312345678'}
    # """


    """序列化多个数据"""
    usas = UserSQLAlchemySchema(many=True)
    user = User.query.all()
    ret = usas.dump(user)
    print(ret)
    """
    [{'email': '123@qq.com', 'created_time': '2021-11-09T18:26:48', 'username': 'xiaoming', 'id': 1, 'mobile': '13312345678', 'sex': True}, {'email': '321@qq.com', 'created_time': '2021-11-09T18:26:48', 'username': 'xiaoming', 'id': 2, 'mobile': '13312345671', 'sex': True}]
    """
    return "ok"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8088)
```

