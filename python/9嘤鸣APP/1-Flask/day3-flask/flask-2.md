# 请求全局钩子[hook]

此处的全局钩子，其实就是类似django里面的中间件。 也就是只要调用或者注册了，在http请求响应中是必然执行的。

在客户端和服务器交互的过程中，有些准备工作或扫尾工作需要处理，比如：

- 在项目运行开始时，建立数据库连接，或创建连接池；
- 在客户端请求开始时，根据需求进行身份识别，权限校验；
- 在请求结束视图返回数据时，指定转换数据的格式，或者记录操作日志；

为了让每个视图函数避免编写重复功能的代码，Flask提供了通用设置的功能，即请求钩子。

请求钩子是**通过装饰器的形式**实现，Flask支持如下四种请求钩子（注意：钩子的装饰器名字是固定)：

- before_first_request
  - 在处理第一个请求前执行[项目刚运行第一次被客户端请求时执行的钩子]
- before_request
  - 在每一次请求前执行[项目运行后，每一次接收到客户端的request请求都会执行一次]
  - 如果在某修饰的函数中返回了一个响应，视图函数将不再被调用
- after_request
  - 如果没有抛出错误，在每次请求后执行视图结束以后，都会执行一次
  - 接受一个参数：视图函数作出的响应
  - 在此函数中可以对响应值在返回之前做最后一步修改处理
  - 需要将参数中的响应在此参数中进行返回
- teardown_request：
  - 在每一次请求后执行
  - 接受一个参数：错误信息，如果有相关错误抛出
  - 需要设置flask的配置DEBUG=False，teardown_request才会接受到异常对象。



代码

```python
from flask import Flask


app = Flask(__name__)

# @app.before_first_request
def before_first_request():
    """
    当项目启动以后，首次被客户端访问时自动执行被 @app.before_first_request 所装饰的函数
    用于项目初始化
    可以编写一些初始化项目的代码，例如，数据库初始化，加载一些可以延后引入的全局配置
    :return:
    """
    print("before_first_request执行了!!!!")


app.before_first_request_funcs.append(before_first_request)


@app.before_request
def before_request():
    """
    每次客户端访问，视图执行之前，都会自动执行被 @app.before_request 所装饰的函数
    用于每次视图访问之前的公共逻辑代码的运行[身份认证，权限判断]
    :return:
    """
    print("before_request执行了！！！！")


@app.after_request
def after_request(response):
    """
        每次客户端访问，视图执行之后，都会自动执行被 @app.after_request 所装饰的函数
    用于每次视图访问之后的公共逻辑代码的运行[返回结果的加工，格式转换，日志记录]
    :param response: 本次视图执行的响应对象
    :return:
    """
    print("after_request执行了！！！！！")
    response.headers["Content-Type"] = "application/json"
    response.headers["Company"] = "python.Edu..."
    return response


@app.teardown_request
def teardown_request(exc):
    """
    每次客户端访问，视图执行报错以后，会自动执行 @app.teardown_request 所装饰的函数
    注意：在flask2.2之前，只有在DEBUG=False时，才会自动执行 @app.teardown_request 所装饰的函数
    :param exc: 本次出现的异常实例对象
    :return:
    """
    print("teardown_request执行了！！！！！")
    print(f"错误提示：{exc}")  # 异常提示


@app.route("/")
def index():
    print("----------------视图执行了！！！！--------------")
    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

通过打印终端，可以看到各种钩子执行的时间：

```bash
before_first_request执行了!!!!
before_request执行了！！！！
----------------视图执行了！！！！--------------
after_request执行了！！！！！
teardown_request执行了！！！！！
错误提示：None

before_request执行了！！！！
----------------视图执行了！！！！--------------
after_request执行了！！！！！
teardown_request执行了！！！！！
错误提示：None
```



# 异常抛出和捕获异常

## 主动抛出HTTP异常

- abort 方法
  - 抛出一个给定状态代码的 HTTPException 或者 指定响应，例如想要用一个页面未找到异常来终止请求，你可以调用 abort(404)
- 参数：
  - code – HTTP的错误状态码

```python
from flask import Flask, request, abort


app = Flask(__name__)


@app.route("/")
def index():
    password = request.args.get("password")
    if password != "123456":
        # 主动抛出异常！
        # abort的第一个参数：表示本次抛出的HTTP异常状态码，后续其他参数，表示错误相关的提示内容。
        abort(400)
    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

abort，只能抛出 HTTP 协议的错误状态码，一般用于权限等页面上错误的展示提示.

abort 在有些前后端分离的项目里面不会被使用，往往在业务错误的时候使用raise进行抛出错误类型，而不是抛出http异常。



## 捕获错误

- app.errorhandler 装饰器
  - 注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
- 参数：
  - code_or_exception – HTTP的错误状态码或指定异常
- 例如统一处理状态码为500的错误给用户友好的提示：

```python
@app.errorhandler(500)  # 此处的errorhandler的参数不仅可以是abort抛出的HTTP异常，也可以是系统抛出的。
def internal_server_error(e):
    return '服务器搬家了'
```

- 捕获指定异常类型

```python
@app.errorhandler(ZeroDivisionError)
def zero_division_error(e):
    return '除数不能为0'
```

代码:

```python
from flask import Flask, request, abort


app = Flask(__name__)

class NetWorkError(Exception):
    pass

@app.route("/")
def index():
    password = request.args.get("password")
    if password != "123456":
        # 主动抛出HTTP异常！
        # abort的第一个参数：表示本次抛出的HTTP异常状态码，后续其他参数，表示错误相关的提示内容。
        # abort(400, "密码错误！")
        raise NetWorkError("网络请求出错！")
        # print(hello)
    return "ok"


# @app.errorhandler的参数是异常类型或者HTTP状态码
@app.errorhandler(NameError)
def NameErrorFunc(exc):
    """
    针对变量命名的异常处理
    :param exc:
    :return:
    """
    print(exc.__traceback__)
    return {"error": f"{exc}"}


@app.errorhandler(400)
def error_400(exc, *args, **kwargs):
    print(exc.__traceback__)
    print(exc.code)        # 上面abort传递的错误状态码
    print(exc.description) # 上面abort传递的错误描述
    return {"error": f"{exc.description}"}


@app.errorhandler(404)
def error_404(exc):
    print(exc.code)        # 上面abort传递的错误状态码
    print(exc.description) # 上面abort传递的错误描述
    return {"error": "当前页面不存在！"}

@app.errorhandler(NetWorkError)
def network_error(exc):
    return {"error": f"{exc}"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

# 执行上下文[context]

执行上下文：即语境，语意，在程序中可以理解为在代码执行到某一行时，根据之前代码所做的操作以及下文即将要执行的逻辑，可以决定在当前时刻下可以使用到的变量，或者可以完成的事情。

Flask中提供的执行上下文对象：相当于一个容器，保存了 Flask 程序运行过程中的一些信息[变量、函数、类与对象等信息]。

Flask中有两种上下文，请求上下文(request context)和应用上下文(application context)。

1. *application* 指的就是当服务端调用`app = Flask(__name__)`创建的这个对象`app`；
2. *request* 指的是每次客户端发生`http`请求时，`WSGI server`(比如uwsgi/gunicorn)调用`Flask.__call__()`之后，在`Flask`对象内部创建本次客户端的`Request`对象；
3. *application* 表示用于响应WSGI请求的应用本身，*request* 表示服务端每次响应客户端的http请求；
4. *application*的生命周期大于*request*，一个*application*存活期间，可能发生多次http请求，所以也就会有多个*request*



## 请求上下文(request context)

思考：在视图函数中，如何取到当前请求的相关数据？比如：请求地址，请求方式，cookie等等

在 flask 中，可以直接在视图函数中使用 **request** 这个对象进行获取相关数据，而 **request** 就是请求上下文提供的对象，保存了当前本次请求的相关数据，请求上下文提供的对象有：request、session

所以每次客户端发生不同的HTTP请求时，得到的request和session的对象都是同一个，但是内部的数据都是不一样的。

- request
  - 封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。
- session
  - 用来记录请求会话中的信息，针对的是会话状态。举例：session['name'] = user.id，可以记录用户的状态信息。还可以通过session.get('name')获取用户的状态信息。

>注意：
>
>请求上下文提供的变量/属性/方法/函数/类与对象，只能在视图中或者被视图调用的地方使用。

代码：

```python
from flask import Flask, request, session


app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"

def test():
    print(request) # 请求上下文所提供的对象[request或session]只能被视图直接或间接调用！

@app.route("/")
def index():
    print(request)
    print(session)
    test()
    return "ok"


if __name__ == '__main__':
    # print(request) # 没有发生客户端请求时，调用request会超出请求上下文的使用范围！
    app.run(host="0.0.0.0", port=5000, debug=True)

```



## 应用上下文(application context)

它的字面意思是 应用上下文，但它不是一直存在的，它只是request context 中操作当前falsk应用对象 app 的代理对象，就是所谓本地代理(local proxy)。它的作用主要是帮助 request 获取当前的flask应用相关的信息，它是伴 request 而生，随 request 而灭的。

应用上下文提供的对象有：current_app，g



### current_app

应用程序上下文,用于存储flask应用实例对象中的变量，可以通过current_app.name打印当前app的名称，也可以在current_app中存储一些变量，例如：

- 应用的启动脚本是哪个文件，启动时指定了哪些参数
- 加载了哪些配置文件，导入了哪些配置
- 连接了哪个数据库
- 有哪些可以调用的工具类、常量
- 当前flask应用在哪个机器上，哪个IP上运行，内存多大

```python
from flask import Flask,request,session,current_app,g

# 初始化
app = Flask(import_name=__name__)

# 声明和加载配置
class Config():
    DEBUG = True
app.config.from_object(Config)

# 编写路由视图
@app.route(rule='/')
def index():
    # 应用上下文提供给我们使用的变量，也是只能在视图或者被视图调用的地方进行使用，
    # 但是应用上下文的所有数据来源于于app，每个视图中的应用上下文基本一样
    print(current_app.config)   # 获取当前项目的所有配置信息
    print(current_app.url_map)  # 获取当前项目的所有路由信息

    return "<h1>hello world!</h1>"

if __name__ == '__main__':
    # 运行flask
    app.run(host="0.0.0.0")
```



### g变量

g 作为 flask 程序全局的一个临时变量,充当者中间媒介的作用,我们可以通过它传递一些数据，g 保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别

```python
g.name='abc' # name是举例，实际要保存什么数据到g变量中，可以根据业务而定，你可以任意的数据进去
```

> 注意：
>
> 客户端不同的请求，会有不同的全局变量g，或者说，每一个客户端都拥有属于自己的g变量。

```python
from flask import Flask, current_app, g


app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"

@app.route("/")
def index():
    print(app == current_app)  # current_app就是app应用实例对象在视图中的本地代理对象
    print(g)  # 全局数据存储对象，用于保存服务端存储的全局变量数据[可以理解为用户级别的全局变量存储对象]
    t1()
    t2()
    return "ok"

def t1():
    # 存储数据
    g.user_id = 100

def t2():
    # 提取数据
    print(g.user_id)

if __name__ == '__main__':
    # print(app)
    # with app.app_context(): # 构建一个应用上下文环境
    #     print(current_app)
    # print(request) # 没有发生客户端请求时，调用request会超出请求上下文的使用范围！
    app.run(host="0.0.0.0", port=5000, debug=True)

```



## 两者区别：

- 请求上下文：保存了客户端和服务器交互的数据，一般来自于客户端的HTTP请求。

- 应用上下文：flask 应用程序运行过程中，保存的一些配置信息，比如路由列表，程序名、数据库连接、应用信息等

  应用上下文提供的对象，可以直接在请求上下文中使用，但是如果在请求上下文之外调用，则需要使用

  `with app.app_context()`创建一个应用上下文环境才能调用。

# 终端脚本命令

flask在0.11版本之前都是采用flask-script第三方模块来实现终端脚本命令的执行，flask在0.11版本以后不再使用这个模块了，因为存在兼容性问题，所以内置了Click模块来实现终端脚本命令的执行。



## flask1.0的终端命令使用[了解]

flask-script模块的作用可以让我们通过终端来控制flask项目的运行，类似于django的manage.py

官方文档：https://flask-script.readthedocs.io/en/latest/

安装命令:

```bash
conda create -n py38 python=3.8
conda activate py38
pip install -U flask==1.1.4
pip install -U flask-script -i https://pypi.douban.com/simple
```

集成 Flask-Script到flask应用中，创建一个主应用程序，一般我们叫`manage.py/run.py/main.py`都行。

manage.py，代码：

```python
from flask import Flas 

app = Flask(__name__)

"""使用flask_script启动项目"""
from flask_script import Manager
manage = Manager(app)

@app.route('/')
def index():
    return 'hello world'

if __name__ == "__main__":
    manager.run()
```

启动终端脚本的命令：

```python
# 端口和域名不写，默认为127.0.0.1:5000
python manage.py runserver

# 通过-h设置启动域名，-p设置启动端口 -d
python manage.py runserver -h0.0.0.0 -p8888     # 关闭debug模式
python manage.py runserver -h0.0.0.0 -p8888  -d # 开启debug模式


# 进入flask交互终端，在这个终端下，可以直接调用flask代码进行测试。
python manage.py shell
```

安装flask==1.1.4版本启动项目时，如果出现错误如下：

```bash
from markupsafe import soft_unicode
```

则找到报错代码位置，修改如下：

```bash
from markupsafe import soft_str as soft_unicode
```



### 自定义终端命令

Flask-Script 还可以为当前应用程序添加脚本命令

```python
1. 引入Command命令基类
    from flask_script import Command
2. 创建命令类必须直接或间接继承Command，并在内部实现run方法或者__call__()方法，
   同时如果有自定义的其他参数，则必须实现get_options方法或者option_list属性来接收参数
3. 使用flask_script应用对象manage.add_command对命令类进行注册，并设置调用终端别名。
```

manage.py，代码：

```python
from flask import Flask


app = Flask(__name__)

"""使用flask_script管理项目"""
from flask_script import Manager
manager = Manager(app)

from abc import ABC
from flask_script import Command, Option

class PrintCommand(Command, ABC):
    """
    命令的相关描述: 打印数据
    """
    def get_options(self):
        # 必须返回选项
        return (
            # Option('简写选项名', '参数选项名', dest='变量名', type=数据类型, default="默认值"),
            Option('-h', '--host', dest='host', type=str, default="127.0.0.1"),
            Option('-p', '--port', dest='port', type=int, default=8000),
            Option('-d', '--debug', dest='debug', type=bool, default=False)
        )

    # 也可以使用option_list来替代get_options
    # option_list = (
    #     Option('-h', '--host', dest='host', type=str, default="127.0.0.1"),
    #     Option('-p', '--port', dest='port', type=int, default="7000"),
    #     Option('-d', '--debug', dest='debug', type=bool, default=False)
    # )

    # 没有flask的应用实例对象---->app对象
    # def run(self, host, port, debug):
    #     print("测试命令")
    #     print(f"self.host={host}")
    #     print(f"self.port={port}")
    #     print(f"self.debug={debug}")

    def __call__(self, app, host, port, debug):  # 会自动传递当前flask实例对象进来
        print(f"测试命令,{app}")
        print(f"self.host={host}")
        print(f"self.port={port}")
        print(f"self.debug={debug}")


# manage.add_command("终端命令名称", 命令类)
manager.add_command("print", PrintCommand)  # python manage.py print

@app.route("/")
def index():
    return "ok"

if __name__ == '__main__':
    manager.run()

```

使用效果：

```bash
(flask) moluo@ubuntu:~/Desktop/flaskdemo$ python manage.py print -h 0.0.0.0 -p 8000
测试命令
self.host=0.0.0.0
self.port=8000
self.debug=False

(flask) moluo@ubuntu:~/Desktop/flaskdemo$ python manage.py print -h 0.0.0.0 -p 8000 -d true
测试命令
self.host=0.0.0.0
self.port=8000
self.debug=True

(flask) moluo@ubuntu:~/Desktop/flaskdemo$ python manage.py print -h 0.0.0.0 -d true
测试命令
self.host=0.0.0.0
self.port=8000
self.debug=True

(flask) moluo@ubuntu:~/Desktop/flaskdemo$ python manage.py print --host=0.0.0.0 -debug=true
测试命令
self.host=0.0.0.0
self.port=8000
self.debug=True
```



## flask2.0的终端命令使用

flask0.11.0版本以后，flask内置了一个Click模块，这个模块是终端命令模块，可以让我们直接通过Click的装饰器，编写和运行一些终端命令。在flask2.0版本已经不能兼容flask-script模块了，所以需要改成使用Click模块来运行和自定义管理终端命令了。

文档地址：https://dormousehole.readthedocs.io/en/latest/cli.html#id10

click文档：https://click.palletsprojects.com/en/8.0.x/

```bash
conda activate flask
pip install -U flask==2.2.2
```

安装了flask2.0以后，当前项目所在的python环境就提供了一个全局的flask命令，这个flask命令是Click提供的。

```bash
# 要使用Click提供的终端命令flask，必须先在环境变量中声明当前flask项目的实例对象所在的程序启动文件。
# 例如：manage.py中使用了 app = Flask(__name__)，则manage.py就是程序启动文件


# 使用flask终端命令之前，可以配置2个环境变量。
# 指定入口文件，开发中入口文件名一般：app.py/run.py/main.py/index.py/manage.py/start.py
export FLASK_APP=manage.py
# 指定项目所在环境
export FLASK_DEBUG=True   # 开发环境，开启DEBUG模式
# export FLASK_DEBUG=False    # 生产环境，关闭DEBUG模式
```

默认情况下，flask命令提供的子命令。

```bash
flask routes  # 显示当前项目中所有路由信息
flask run     # 把flask项目运行在内置的测试服务器下
# flask run --host=0.0.0.0 --port=5055
flask shell   # 基于项目的应用上下文提供终端交互界面，可以进行代码测试。
```



### Click自定义终端命令

官方文档：https://flask.palletsprojects.com/en/2.2.x/cli/

```python
import click
from flask import Flask


app = Flask(__name__)


@app.cli.command("faker")  # 假设这个用于生成测试数据
@click.argument("data", type=str, default="user") # 位置参数
@click.argument("position", type=str, default="mysql") # 位置参数
@click.option('-n', '--number', 'number', type=int, default=1, help='生成的数据量.')  # 选项参数
def faker_command(data, position, number):
    """
    命令的说明文档：添加测试信息
    """
    print("添加测试信息")
    print(f"数据类型：data={data}")
    print(f"数据类型：position={position}")
    print(f"生成数量：number={number}")


@app.route("/")
def index():
    return "ok"

if __name__ == '__main__':
    app.run()

```

终端下的运行效果：

```bash
(flask) moluo@ubuntu:~/Desktop/flaskdemo$ flask faker -n10 user
添加测试信息
数据类型：data=user
生成数量：number=10
(flask) moluo@ubuntu:~/Desktop/flaskdemo$ flask faker user
添加测试信息
数据类型：data=user
生成数量：number=1
(flask) moluo@ubuntu:~/Desktop/flaskdemo$ flask faker goods
添加测试信息
数据类型：data=goods
生成数量：number=1
```



练习：

```
1. flask2.0的终端下，输入 python manage.py startapp home 则可以在当前目录下创建以下目录和文件
项目目录/
 └── home
     ├── views.py
     ├── models.py
     ├── urls.py
     └── tests.py
```

代码：

```python
import click, os
from flask import Flask


app = Flask(__name__)
# 配置
app.config.update({
    "DEBUG": False
})


@app.cli.command("startapp")
@click.argument("name")
# @click.option('-n', 'name', help='app name')
def startapp(name):
    """生成子模块或子应用"""
    if os.path.isdir(name):
        print(f"当前{name}目录已存在！请先处理完成以后再创建。")
        return

    os.mkdir(name)
    open(f"{name}/views.py", "w")
    open(f"{name}/models.py", "w")
    open(f"{name}/documents.py", "w")
    open(f"{name}/ws.py", "w")
    open(f"{name}/services.py", "w")
    open(f"{name}/urls.py", "w")
    open(f"{name}/test.py", "w")
    print(f"{name}子应用创建完成....")


@app.route("/")
def index():
    return "ok"


if __name__ == '__main__':
    app.run()
```

终端调用：

```bash
flask startapp home
flask startapp users
```

# Jinja2模板引擎

![image-20211228100615753](assets/image-20211228100615753.png)

Flask内置的模板语言Jinja2，它的设计思想来源于 Django 的模板引擎DTP(DjangoTemplates)，并扩展了其语法和一系列强大的功能。

- Flask提供的 **render_template** 函数封装了该模板引擎Jinja2
- **render_template** 函数的第一个参数是模板的文件名，后面的参数都是键值对，表示模板中变量对应的数据值。



## 模板基本使用

1. 在flask应用对象创建的时候，设置template_folder参数，默认值是templates也可以自定义为其他目录名，需要手动创建模板目录。

   ```python
   from flask import Flask, render_template
   
   app = Flask(__name__, template_folder="templates")
   ```

2. 在手动创建 `templates` 目录下创建一个模板html文件 `index.html`，代码：

   ```django
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8">
     <title>{{title}}</title>
   </head>
   <body>
     <h1>{{content}}</h1>
   </body>
   </html>
   ```

3. 在视图函数设置渲染模板并设置模板数据

   ```python
   from flask import Flask, render_template
   
   app = Flask(__name__, template_folder="templates")
   
   
   @app.route("/")
   def index():
       title = "网页标题"
       content = "网页正文内容"
       return render_template("index.html", **locals())
   
   if __name__ == '__main__':
       app.run()
   
   ```

flask中提供了2个加载模板的函数：render_template与render_template_string。

render_template：基于参数1的模板文件路径，读取html模板内容，返回渲染后的HTML页面内容。

render_template_string：基于参数1的模板内容，返回渲染后的HTML页面内容。

```python
from flask import Flask, render_template, render_template_string

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    title = "网页标题"
    content = "网页正文内容"
    html = render_template("index.html", **locals())
    print(html, type(html))
    return html


@app.route("/tmp")
def tmp():
    title = "网页标题"
    content = "网页正文内容"
    temp = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
</head>
<body>
  <h1>{{content}}</h1>
</body>
</html>
    """
    html = render_template_string(temp, **locals())
    print(html, type(html))
    return html

if __name__ == '__main__':
    app.run(debug=True)
```



### 输出变量

```
{{ 变量名 }}，这种 {{ }} 语法叫做 变量代码块
```

视图代码：

```python
import click
from flask import Flask,render_template
# flask开发小型的项目，直接在当前flask应用配置即可。手动创建模板目录。
# flask开发中大型项目，直接在当前flask的每一个子应用(蓝图)下构建目录。
app = Flask(import_name=__name__, template_folder="templates")

# 配置类
class Config(object):
    DEBUG = True  # 开启调试模式

# 加载配置
app.config.from_object(Config)

@app.route("/")
def index():
    title = "站点标题"
    user_list = [
        {"id":1, "name": "xiaoming", "age":16},
        {"id":2, "name": "xiaoming", "age":16},
        {"id":3, "name": "xiaoming", "age":16},
    ]
    return render_template("index.html", **locals())

if __name__ == '__main__':
    app.run()
```

模板代码

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
</head>
<body>
    <h1>{{title}}</h1>
    <p>{{ user_list.0 }}</p>
    <p>{{ user_list.0.name }}</p>
</body>
</html>
```



pycharm中设置当前项目的模板语言：

files/settings/languages & frameworks/python template languages。

设置下拉框为jinja2，保存

![1596532209377](assets/1596532209377.png)

设置指定目录为模板目录，鼠标右键->Mark Directory as ...-> Template Folder

![image-20211026175126077](assets/image-20211026175126077.png)



Jinja2 模版中的变量代码块的输出的内容可以是Python的任意类型数据或者对象，只要它能够被 Python 的 `__str__` 方法或者str()转换为一个字符串就可以，比如，可以通过下面的方式显示一个字典或者列表中的某个元素:

视图代码：

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    title = "我的flask"
    data_list = ["a", "b", "c"]
    data_dict = {
        "name": "xiaoming",
        "id": 100,
    }
    user_list = [
        {"id":1, "name": "xiaoming", "age":16},
        {"id":2, "name": "xiaoming", "age":16},
        {"id":3, "name": "xiaoming", "age":16},
    ]

    return render_template("index.html", **locals())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

模板代码：

```jinja2
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}!!</h1>
    <p>{{ data_list }}</p>
    <p>{{ data_list.1 }}</p>
    <p>{{ data_list[-1]}}</p>
    <p>{{ data_list | last }}</p>
    <p>{{ data_list | first }}</p>
    <p>{{ data_dict }}</p>
    <p>{{ data_dict.name }}</p>
    <p>{{ user_list.0 }}</p>
    <p>{{ user_list.0.name }}</p>
</body>
</html>
```

使用 {# #} 进行注释，注释的内容不会在html中被渲染出来

```jinja2
{#    <h1>{{ title }}!!</h1>#}
{#    <p>{{ data_list }}</p>#}
{#    <p>{{ data_list.1 }}</p>#}
    <p>{{ data_list[-1]}}</p>
    <p>{{ data_list | last }}</p>
    <p>{{ data_list | first }}</p>
    <p>{{ data_dict }}</p>
    <p>{{ data_dict.name }}</p>
    <p>{{ user_list.0 }}</p>
{#    <p>{{ user_list.0.name }}</p>#}
```



## 模板中内置的变量和函数

你可以在自己的模板中访问一些 Flask 默认内置的函数和对象

#### config

你可以从模板中直接访问Flask当前的config对象:

```jinja2
    <p>{{ config.ENV }}</p>
    <p>{{ config.DEBUG }}</p>
```

#### request

就是flask中代表当前请求的request对象：

```jinja2
    <p>{{ request.url }}</p>
    <p>{{ request.path }}</p>
    <p>{{ request.method }}</p>
```

#### session

为Flask的session对象，显示session数据

```jinja2
{{session.new}}
False
```

#### g变量

在视图函数中设置g变量的 name 属性的值，然后在模板中直接可以取出

```jinja2
{{ g.name }}
```

#### url_for()

url_for会根据传入的路由器函数名,返回该路由对应的URL,在模板中始终使用url_for()就可以安全的修改路由绑定的URL,则不比担心模板中渲染出错的链接:

```jinja2
{{url_for('home')}}
```

如果我们定义的路由URL是带有参数的,则可以把它们作为关键字参数传入url_for(),Flask会把他们填充进最终生成的URL中:

```jinja2
{{ url_for('index', id=1)}}
/index/1      {#  /index/<int:id> id被声明成路由参数 #}
/index?id=1   {#  /index          id被声明成路由参数 #}
```

课堂代码：

主程序 manage.py：

```python
from flask import Flask, render_template,g

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    g.name = "xiaohei"
    title = "我的flask"
    data_list = ["a", "b", "c"]
    data_dict = {
        "name": "xiaoming",
        "id": 100,
    }
    user_list = [
        {"id":1, "name": "xiaoming", "age":16},
        {"id":2, "name": "xiaoming", "age":16},
        {"id":3, "name": "xiaoming", "age":16},
    ]

    return render_template("index.html", **locals())


@app.route("/user/<int:uid>")
def user(uid):
    print(uid)
    return f"uid={uid}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

模板 templates/index.html：

```jinja2
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
{#    <h1>{{ title }}!!</h1>#}
{#    <p>{{ data_list }}</p>#}
{#    <p>{{ data_list.1 }}</p>#}
    <p>{{ data_list[-1]}}</p>
    <p>{{ data_list | last }}</p>
    <p>{{ data_list | first }}</p>
    <p>{{ data_dict }}</p>
    <p>{{ data_dict.name }}</p>
    <p>{{ user_list.0 }}</p>
{#    <p>{{ user_list.0.name }}</p>#}

    <p>{{ config.ENV }}</p>
    <p>{{ config.DEBUG }}</p>
    <p>{{ request.url }}</p>
    <p>{{ request.path }}</p>
    <p>{{ request.method }}</p>

    <p>{{ session.new }}</p>
    <p>{{ g.name }}</p>

    <p>{{ url_for("user", uid=3) }}</p>    {# /user/3 #}

</body>
</html>
```



## 流程控制

主要包含两个：

```
- if / elif /else / endif
- for / else / endfor

```



### if语句

Jinja2 语法中的if语句跟 Python 中的 if 语句相似,后面的布尔值或返回布尔值的表达式将决定代码中的哪个流程会被执行.

用 {**%%**} 定义的**控制代码块**，可以实现一些语言层次的功能，比如循环或者if语句

视图代码：

```python
import random
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    data = random.randint(1,100)
    return render_template("index6.html", **locals())


@app.route("/user/<int:uid>")
def user(uid):
    print(uid)
    return f"uid={uid}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

index.html，模板代码：

```jinja2
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    {% if data < 60 %}
        <p>本次生成的数字不及格！</p>
    {% else %}
        <p>本次生成的数字及格了！</p>
    {% endif %}


    {% if data < 60 %}
        <p>本次生成的数字不及格！</p>
    {% elif data <80 %}
        <p>本次生成的数字一般般，不算高！</p>
    {% else %}
        <p>本次生成的数字超过80，非常好！</p>
    {% endif %}

</body>
</html>
```



### 循环语句

- 我们可以在 Jinja2 中使用循环来迭代任何列表或者生成器函数

```jinja2
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
    table, td,th{
        border: 1px solid red;
        border-collapse: collapse;
    }
    table{
        width: 800px;
    }
    td,th{
        padding: 4px;
    }
    .last{
        background: orange;
    }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>序号</th>
            <th>ID</th>
            <th>name</th>
            <th>age</th>
        </tr>
        {% for user in user_list %}
        {% if loop.last %}
        <tr class="last">
        {% else %}
        <tr>
        {% endif %}
{#            <th>{{ loop.index }}</th>#}
{#            <th>{{ loop.index0 }}</th>#}
{#            <th>{{ loop.revindex0 }}</th>#}
            <th>{{ loop.revindex }}</th>
            <th>{{ user.id }}</th>
            <th>{{ user.name }}</th>
            <th>{{ user.age }}</th>
        </tr>
        {% endfor %}

    </table>
</body>
</html>
```

- 循环和if语句可以组合使用，以模拟 Python 循环中的 continue 功能，下面这个循环将只会渲染user.id为偶数的那些user：

```jinja2
    <table border="1" width="1200">
        <tr>
            <th width="200">序号[从小到大，从0开始]</th>
            <th width="200">序号[从小到大，从1开始]</th>
            <th width="200">序号[从大到小，到0结束]</th>
            <th width="200">序号[从大到小，到1结束]</th>
            <th>ID</th>
            <th>name</th>
            <th>age</th>
        </tr>
        {% for user in user_list if user.id%2==0 %}
        <tr>
            <td>{{ loop.index0 }}</td>
            <td>{{ loop.index }}</td>
            <td>{{ loop.revindex0 }}</td>
            <td>{{ loop.revindex }}</td>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.age }}</td>
        </tr>
        {% endfor %}
    </table>
```

- 在一个 for 循环块中你可以访问这些特殊的变量:

| 变量           | 描述                                           |
| :------------- | :--------------------------------------------- |
| loop.index     | 当前循环迭代的次数（从 1 开始）                |
| loop.index0    | 当前循环迭代的次数（从 0 开始）                |
| loop.revindex  | 到循环结束需要迭代的次数（从 1 开始）          |
| loop.revindex0 | 到循环结束需要迭代的次数（从 0 开始）          |
| loop.first     | 如果是第一次迭代，为 True 。                   |
| loop.last      | 如果是最后一次迭代，为 True 。                 |
| loop.length    | 序列中的项目数。                               |
| loop.cycle     | 在一串序列间期取值的辅助函数。见下面示例程序。 |

- 在循环内部,你可以使用一个叫做loop的特殊变量来获得关于for循环的一些信息
  - 比如：要是我们想知道当前被迭代的元素序号，并模拟Python中的enumerate函数做的事情，则可以使用loop变量的index属性,例如:

```jinja2
<ul>
{% for item in data_list %}
<li>{{ loop.index0 }}，item={{ item }}</li>
{% endfor %}
</ul>
```

- 会输出这样的结果

```python
0，item=a
1，item=b
2，item=c
```

- loop.cycle函数会在每次循环的时候,返回其参数中的下一个元素,可以拿上面的例子来说明:

```python
    <ul>
        {% for item in data_list %}
        <li>{{ loop.cycle("男","女")}}，item={{ item }}</li>
        {% endfor %}
    </ul>
```

- 会输出这样的结果：

```python
男，item=a
女，item=b
男，item=c
```

#### 课堂代码

视图代码：

```python
import click
from flask import Flask,render_template,g
# flask开发小型的项目，直接在当前flask应用配置即可。手动创建模板目录。
# flask开发中大型项目，直接在当前flask的每一个子应用(蓝图)下构建目录。
app = Flask(import_name=__name__, template_folder="templates")

# 加载配置
app.config.from_object(Config)

@app.route("/")
def index():
    title = "站点标题"
    data_list = ["a","b","c"]
    data_dict = {
        "name": "xiaoming",
        "id": 100,
    }
    user_list = [
        {"id":2, "name": "xiaoming", "age":15},
        {"id":3, "name": "xiaoming", "age":16},
        {"id":4, "name": "xiaoming", "age":17},
    ]

    g.name = "来自视图"

    return render_template("index.html", **locals())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

index.html，模板代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
</head>
<body>
{#    <h1>{{title}}</h1>
    <p>{{ data_list }}</p>
    <p>{{ data_list.1 }}</p>
    <p>{{ data_list | first }}</p>
    <p>{{ data_list | last }}</p>
    <p>{{ data_dict }}</p>
    <p>{{ data_dict.name }}</p>
#}{#    <p>{{ data_list.-1 }}</p>#}{#
    <p>{{ user_list.0 }}</p>
    <p>{{ user_list.0.name }}</p>
#}

{#    <p>{{ data_list[0] }}</p>#}
{#    <p>{{ data_list[-1] }}</p>#}
{#    <p>{{ data_dict['name'] }}</p>#}
{#    <p>{{ config }}</p>#}
{#    <p>{{ config.ENV }}</p>#}
{#    <p>{{ request }}</p>#}
{#    <p>获取地址栏参数：id={{ request.args.id }}</p>#}
{#    <p>{{ session }}</p>#}
{#    <p>{{ session.new }}</p>#}
{#    <p>{{ g.name }}</p>#}
{#    <p>{{ url_for("index",id=1) }}</p>#}


    {% if "a" in data_list %}
        <p>{{ data_list }}包含a字符</p>
    {% endif %}

    {% if "A" in data_list %}
        <p>{{ data_list }}包含A字符</p>
    {% else  %}
        <p>{{ data_list }}不包含A字符</p>
    {% endif %}

    <table border="1" width="1200">
        <tr>
            <th width="200">序号[从小到大，从0开始]</th>
            <th width="200">序号[从小到大，从1开始]</th>
            <th width="200">序号[从大到小，到0结束]</th>
            <th width="200">序号[从大到小，到1结束]</th>
            <th>ID</th>
            <th>name</th>
            <th>age</th>
        </tr>
        {% for user in user_list if user.id%2==0 %}
        <tr>
            <td>{{ loop.index0 }}</td>
            <td>{{ loop.index }}</td>
            <td>{{ loop.revindex0 }}</td>
            <td>{{ loop.revindex }}</td>
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.age }}</td>
        </tr>
        {% endfor %}
    </table>


    <ul>
        {% for item in data_list %}
        <li>{{ loop.index0 }}，item={{ item }}</li>
        {% endfor %}
    </ul>

    <ul>
        {% for item in data_list %}
        <li>{{ loop.cycle("男","女")}}，item={{ item }}</li>
        {% endfor %}
    </ul>

</body>
</html>
```



## 过滤器

django中的模板引擎里面曾经使用过滤器，在flask中也有过滤器，并且也可以被用在 if 语句或者for语句中:

视图代码：

```python
import random
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    book_list = [
        {"id":1, "price": 78.50, "title":"javascript入门", "cover": "<img src='/static/images/course.png'>"},
        {"id":2, "price": 78.5, "title":"python入门", "cover": "<img src='/static/images/course.png'>"},
        {"id":3, "price": 78.6666, "title":"django web项目实战", "cover": "<img src='/static/images/course.png'>"}
    ]
    return render_template("index8.html", **locals())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

index8.html，模板代码：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
    table, td,th{
        border: 1px solid red;
        border-collapse: collapse;
    }
    table{
        width: 800px;
    }
    td,th{
        padding: 4px;
    }
    img{
        width: 100px;
    }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>title</th>
            <th>price</th>
            <th>cover</th>
        </tr>
        {% for book in book_list %}
        <tr>
            <th>{{ book.id }}</th>
            <th>{{ book.title | title }}</th>
            <th>{{ book.price }}</th>
            <th>{{ book.cover | safe }}</th>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

flask中， **过滤器的本质就是函数**。有时候我们不仅仅只是需要输出变量的值，我们还需要修改变量的显示，甚至格式化、运算等等，而在模板中是不能直接调用 Python 的方法，那么这就用到了过滤器。

使用方式：

- 过滤器的使用方式为：变量名 | 过滤器 | 。。。。。

```python
{{variable | filter_name(args1,args2,....)}}
```

- 如果没有任何参数传给过滤器,则可以把括号省略掉

```python
{{variable | title }}
```

- 如：`title`过滤器的作用：把变量的值的首字母转换为大写，其他字母转换为小写



在 jinja2 中，过滤器是可以支持链式调用的，示例如下：

```python
{{ "hello world" | reverse | upper }}
```



### 常见的内建过滤器

源代码：`from jinja2.filters import FILTERS`

#### 字符串操作

- safe：禁用实体字符的转义

```python
{{ '<h1>hello</h1>' | safe }}
```

- lower：把值转成小写

```python
<p>{{ 'HELLO' | lower }}</p>
```

- upper：把值转成大写

```python
<p>{{ 'hello' | upper }}</p>
```

- reverse：字符串反转

```python
<p>{{ 'olleh' | reverse }}</p>
```

- format：格式化输出

```python
<p>{{ '%s = %d' | format('name',17) }}</p>

<p>{{ '%s = %d' % ('name', 17) }}</p>
```

- striptags：渲染之前把值中所有的HTML标签都删掉

    如果内容中，存在大小于号的情况，则不要使用这个过滤器，容易误删内容。

```python
<p>{{ '<script>alert("hello")</script>' | striptags }}</p>
<p>{{ "如果x<y，z>x，那么x和z之间是否相等？" | striptags }}</p>
```

- truncate: 字符串截断

```python
<p>{{ 'hello every one' | truncate(9)}}</p>
```

#### 列表操作

- first：取第一个元素

```python
<p>{{ [1,2,3,4,5,6] | first }}</p>
```

- last：取最后一个元素

```python
<p>{{ [1,2,3,4,5,6] | last }}</p>
```

- length：获取列表长度

```python
<p>{{ [1,2,3,4,5,6] | length }}</p>
<p>{{ [1,2,3,4,5,6] | count }}</p>
```

- sum：列表求和

```python
<p>{{ [1,2,3,4,5,6] | sum }}</p>
```

- sort：列表排序

```
<p>{{ [6,2,3,1,5,4] | sort }}</p>
```

#### 语句块过滤

```pyhton
    {% filter upper %}
        <p>abc</p>
        <p>{{ ["a","c"] }}</p>
        <p>{{ ["a","c"] }}</p>
        <p>{{ ["a","c"] }}</p>
        <p>{{ ["a","c"] }}</p>
    {% endfilter %}
```



### 自定义过滤器

过滤器的本质是函数。当模板内置的过滤器不能满足项目需求，可以自定义过滤器。自定义过滤器有两种实现方式：

- 一种是通过Flask应用对象的 **app.add_template_filter** 方法进行注册
- 通过装饰器来实现自定义过滤器进行注册

**注意：自定义的过滤器名称如果和内置的过滤器重名，会覆盖内置的过滤器。**



需求：编写一个过滤器，保留2位小数

方式一

通过调用应用程序实例的 add_template_filter 方法实现自定义过滤器。该方法第一个参数是函数名，第二个参数是自定义的过滤器名称：

```python
# 自定义过滤器
def do_fixed(data, length):
    return f"%.{length}f" % data


# 注册过滤器到当前应用实例对象
app.add_template_filter(do_fixed, "fixed")
```

方式二

用装饰器来实现自定义过滤器。装饰器传入的参数是自定义的过滤器名称。

```python
# 自定义过滤器，通过装饰器注册到app应用实例对象
@app.template_filter("fixed")
def do_fixed(data, length):
    return f"%.{length}f" % data
```

- 主程序中创建和注册过滤器

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

# 自定义过滤器，通过装饰器注册到app应用实例对象
@app.template_filter("fixed")
def do_fixed(data):
    return f"{data:.2f}"

@app.route("/")
def index():
    title = "网页标题"
    book_list = [
        {"id":1, "price": 78.50, "title":"javascript入门", "cover": "<img src='/static/images/course.png'>"},
        {"id":2, "price": 78.5, "title":"python入门", "cover": "<img src='/static/images/course.png'>"},
        {"id":3, "price": 78.6666, "title":"django web项目实战", "cover": "<img src='/static/images/course.png'>"}
    ]
    return render_template("index9.html", **locals())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

```

- html9.html，调用过滤器，代码：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
    table, td,th{
        border: 1px solid red;
        border-collapse: collapse;
    }
    table{
        width: 800px;
    }
    td,th{
        padding: 4px;
    }
    img{
        width: 100px;
    }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>title</th>
            <th>price</th>
            <th>cover</th>
        </tr>
        {% for book in book_list %}
        <tr>
            <th>{{ book.id }}</th>
            <th>{{ book.title | title }}</th>
            <th>{{ book.price | fixed }}</th>
            <th>{{ book.cover | safe }}</th>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```



#### 练习：给手机进行部分屏蔽  `13112345678` ---> `131****5678`

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")
# 配置
app.config.update({
    "DEBUG": True
})

# 自定义过滤器
@app.template_filter("mobile")
def do_mobile(data, flag):
    return data[:3] + str(flag) + data[-4:]

@app.route("/")
def index():
    user_list = [
        {"id":1,"name":"张三","mobile":"13112345678"},
        {"id":2,"name":"张三","mobile":"13112345678"},
        {"id":3,"name":"张三","mobile":"13112345678"},
        {"id":4,"name":"张三","mobile":"13112345678"},
    ]
    return render_template("index5.html", **locals())


if __name__ == '__main__':
    app.run()

```

index2.html，模板代码：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
    table, td,th{
        border: 1px solid red;
        border-collapse: collapse;
    }
    table{
        width: 800px;
    }
    td,th{
        padding: 4px;
    }
    img{
        width: 100px;
    }
    </style>
</head>
<body>
    <table>
        <tr>
            <th>ID</th>
            <th>name</th>
            <th>mobile</th>
        </tr>
        {% for user in user_list %}
        <tr>
            <th>{{ user.id }}</th>
            <th>{{ user.name }}</th>
            <th>{{ user.mobile | mobile("****") }}</th>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

效果：

![image-20211228113255976](assets/image-20211228113255976.png)



## 模板继承

在模板中，可能会遇到以下情况：

- 多个模板具有完全相同的顶部和底部内容
- 多个模板中具有相同的模板代码内容，但是内容中部分值不一样，弹窗
- 多个模板中具有完全相同的 html 代码块内容，侧边栏

像遇到这种情况，可以使用 JinJa2 模板中的 **模板继承** 来进行实现

模板继承是为了重用模板中的公共内容。一般Web开发中，继承主要使用在网站的顶部菜单、底部、弹窗。这些内容可以定义在父模板中，子模板直接继承，而不需要重复书写。

- block标签定义的可重写的内容范围

```python
{% block 区块名称 %} {% endblock 区块名称 %}

{% block 区块名称 %} {% endblock %}

例如：顶部菜单
{% block menu %}{% endblock %}
```

- block相当于在父模板中挖个坑，当子模板继承父模板时，可以进行对应指定同名区块进行代码填充。
- 子模板使用 extends 标签声明继承自哪个父模板
- 父模板中定义的区块在子模板中被重新定义，在子模板中调用父模板的内容可以使用super()调用父模板声明的区块内容。



manage.py，视图代码：

```python
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")
# 配置
app.config.update({
    "DEBUG": True
})

@app.route("/")
def index():
    title = "我的首页"
    return render_template("base.html", **locals())

@app.route("/list")
def list_page():
    title = "商品列表"
    content = "商品列表ng "
    return render_template("list.html", **locals())

if __name__ == '__main__':
    app.run()

```



父模板代码：

base.html

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title | default("默认标题") }}</title>
    {% block css %}
    {% endblock %}
</head>
<body>
    <h1>头部公共内容-菜单-登录窗口</h1>
    {% block main %}
    <div>公共页面中间部分内容 - {{ title }}</div>
    {% endblock main %}
    <h1>脚部公共内容-版权信息，网点地图</h1>
</body>
</html>
```



子模板代码：

- extends指令声明这个模板继承自哪

list.html，代码：

```jinja2
{% extends "./base.html" %}

{% block css %}
    <style>
    body{
        color: red;
    }
    </style>
{% endblock css %}

{% block main %}
    {{ super() }} {# 继承父级模板的内容 #}
    <p>{{ content }}</p>
{% endblock %}
```



模板继承使用时注意点：

1. 不支持多继承，不能使用多个extends

2. 为了便于阅读，在子模板中使用extends时，尽量写在模板的第一行。

3. 不能在一个模板文件中定义多个相同名字的block标签，否则会覆盖。

4. 当在页面中使用多个block标签时，建议给结束标签起个名字，当多个block嵌套时，阅读性更好。



## CSRF 攻击防范

CSRF: 跨域请求伪造攻击。

```bash
pip install flask_wtf
```

flask_wtf本身提供了生成表单HTML页面的功能(基于wtforms提供)，常用于开发前后端不分离的表单页面，同时Flask-wtf 扩展模块还提供了一套完善的 csrf 防护体系，对于我们开发者来说，使用flask_wtf模块就可以非常简单解决CSRF攻击问题。

1. 设置应用程序的 secret_key，用于加密生成的 csrf_token 的值

```python
# 1. session加密的时候已经配置过了.如果没有在配置项中设置,则如下:
app.secret_key = "#此处可以写随机字符串#"

# 2. 也可以写在配置类中。
class Config(object):
    DEBUG = True
    SECRET_KEY = "dsad32DASSLD*13%^32"
    
"""加载配置"""
app.config.from_object(Config)
```



2. 导入 flask_wtf 中的 CSRFProtect类，进行初始化，并在初始化的时候关联 app

```python
# 方式1：
from flask_wtf import CSRFProtect
csrf = CSRFProtect() # 这块代码可能在文件中。
app = Flask(import_name=__name__, template_folder="templates")
# 项目配置代码之后
csrf.init_app(app) # 避免出现引用导包，所以提供了init_app的用法

# 方式2：
# from flask_wtf import CSRFProtect
# app = Flask(import_name=__name__, template_folder="templates")
# 项目配置代码之后
# CSRFProtect(app)
```



1. 在表单中使用 CSRF 令牌:

```html
    <form action="/login" method="post">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
    </form>
```



视图代码;

```python
from flask import Flask, render_template, request, session
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
app = Flask(__name__, template_folder="templates", static_folder="static")

# csrf = CSRFProtect()



# 配置
app.config.update({
    "DEBUG": True,
    "SECRET_KEY": ":123.,2,s,"
})

# csrf.init_app(app)

CSRFProtect(app)



@app.route("/")
def index():
    title = "网站首页"
    return render_template("index.html", **locals())


@app.route("/login", methods=["GET","POST"])
def login():
    title = "登录页面"
    print(">>>> 1")
    if request.method == "GET":
        print(">>>> 2")
        token = generate_csrf()
        return render_template("login.html", **locals())
    else:
        print(">>>> 3")
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "xiaoming" and password == "123456":
            print(">>>> 4")
            session["username"] = "xiaoming"
            session["is_login"] = True
            print(">>>> 6")
            return "登录成功！<br><a href='/'>返回首页</a>"
        else:
            print(">>>> 5")
            return "登录失败！<br><a href='/login'>重新登录！</a>"

if __name__ == '__main__':
    app.run()

```

login.html，模板代码：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <form action="http://127.0.0.1:5000/login" method="post">
        <input type="hidden" name="csrf_token" value="{{ token2() }}" />
        <input type="hidden" name="csrf_token" value="{{ token }}" />
        登录账号： <input type="text" name="username"> <br><br>
        登录密码： <input type="password" name="password"> <br><br>
        <button>登录</button>
    </form>
</body>
</html>
```

index.html，代码：

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    {% if session.get("is_login") %}
        <a href="/user">欢迎回到网站，{{ session["username"] }}</a>
    {% else %}
    <a href="{{ url_for('login') }}">登录</a>
    {% endif %}
</body>
</html>
```

