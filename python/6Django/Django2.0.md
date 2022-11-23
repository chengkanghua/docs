# 1 web应用

Web应用程序是一种可以通过Web访问的应用程序，程序的最大好处是用户很容易访问应用程序，用户只需要有浏览器即可，不需要再安装其他软件。应用程序有两种模式C/S、B/S。C/S是客户端/服务器端程序，也就是说这类程序一般独立运行。而B/S就是浏览器端/服务器端应用程序，这类应用程序一般借助谷歌，火狐等浏览器来运行。WEB应用程序一般是B/S模式。Web应用程序首先是“应用程序”，和用标准的程序语言，如java，python等编写出来的程序没有什么本质上的不同。在网络编程的意义下，浏览器是一个socket客户端，服务器是一个socket服务端。

```python
import socket

def handle_request(client):

    request_data = client.recv(1024)
    print("request_data: ",request_data)

    client.send("HTTP/1.1 200 OK\r\nstatus: 200\r\nContent-Type:text/html\r\n\r\n".encode("utf8"))
    client.send("<h1>Hello, luffycity!</h1><img src=''>".encode("utf8"))

def main():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost',8812))
    sock.listen(5)

    while True:
        print("the server is waiting for client-connection....")
        connection, address = sock.accept()
        handle_request(connection)
        connection.close()

if __name__ == '__main__':

    main()
```


# 2 http协议

## http协议简介

HTTP协议是Hyper Text  Transfer Protocol（超文本传输协议）的缩写,是用于万维网（WWW:World Wide Web ）服务器与本地浏览器之间传输超文本的传送协议。

HTTP是一个属于应用层的面向对象的协议，由于其简捷、快速的方式，适用于分布式超媒体信息系统。它于1990年提出，经过几年的使用与发展，得到不断地完善和扩展。HTTP协议工作于客户端-服务端架构为上。浏览器作为HTTP客户端通过URL向HTTP服务端即WEB服务器发送所有请求。Web服务器根据接收到的请求后，向客户端发送响应信息。

![img](assets2.0/877318-20180418160227278-698810818.png)

## http协议特性

 

### (1) 基于TCP/IP

http协议是基于TCP/IP协议之上的应用层协议。

### (2) 基于请求－响应模式

HTTP协议规定,请求从客户端发出,最后服务器端响应该请求并 返回。换句话说,肯定是先从客户端开始建立通信的,服务器端在没有 接收到请求之前不会发送响应

![img](assets2.0/877318-20180418160433297-1726664935.png)

### (3) 无状态保存

HTTP是一种不保存状态,即无状态(stateless)协议。HTTP协议 自身不对请求和响应之间的通信状态进行保存。也就是说在HTTP这个 级别,协议对于发送过的请求或响应都不做持久化处理。

1.  1.  1.  1.  ![img](assets2.0/877318-20180418160546133-1479186889.png)

使用HTTP协议,每当有新的请求发送时,就会有对应的新响应产 生。协议本身并不保留之前一切的请求或响应报文的信息。这是为了更快地处理大量事务,确保协议的可伸缩性,而特意把HTTP协议设计成 如此简单的。可是,随着Web的不断发展,因无状态而导致业务处理变得棘手 的情况增多了。比如,用户登录到一家购物网站,即使他跳转到该站的 其他页面后,也需要能继续保持登录状态。针对这个实例,网站为了能 够掌握是谁送出的请求,需要保存用户的状态。HTTP/1.1虽然是无状态协议,但为了实现期望的保持状态功能, 于是引入了Cookie技术。有了Cookie再用HTTP协议通信,就可以管 理状态了。有关Cookie的详细内容稍后讲解。

### 无连接

无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即断开连接。采用这种方式可以节省传输时间。

## http请求协议与响应协议

http协议包含由浏览器发送数据到服务器需要遵循的请求协议与服务器发送数据到浏览器需要遵循的请求协议。用于HTTP协议交互的信被为HTTP报文。请求端(客户端)的HTTP报文 做请求报文,响应端(服务器端)的 做响应报文。HTTP报文本身是由多行数据构成的字 文本。 

![img](assets2.0/877318-20180418160732113-669528378.png)

### 请求协议

#### 请求格式

![img](assets2.0/877318-20180418160914403-902015370.png)

#### 请求方式: get与post请求

-   GET提交的数据会放在URL之后，以?分割URL和传输数据，参数之间以&相连，如EditBook?name=test1&id=123456. POST方法是把提交的数据放在HTTP包的请求体中.
-   GET提交的数据大小有限制（因为浏览器对URL的长度有限制），而POST方法提交的数据没有限制.
-   GET与POST请求在服务端获取请求数据方式不同。

### 响应协议

#### 响应格式

![img](assets2.0/877318-20180418161014087-738990087.png)

#### 响应状态码

状态码的职 是当客户端向服务器端发送请求时, 返回的请求 结果。借助状态码,用户可以知道服务器端是正常 理了请求,还是出 现了 。状态码如200 OK,以3位数字和原因 成。数字中的 一位指定了响应 别,后两位无分 。响应 别有以5种。

![img](assets2.0/877318-20180418161321986-304902913.png)

```python
import socket

sock=socket.socket()
sock.bind(("127.0.0.1",8808))
sock.listen(5)

while 1:
    print("server waiting.....")
    conn,addr=sock.accept()
    data=conn.recv(1024)
    print("data",data)

    # 读取html文件
    with open("login.html","rb") as f:
        data=f.read()

    conn.send((b"HTTP/1.1 200 OK\r\n\r\n%s"%data))
    conn.close()
```

login.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<form action="" method="post">
    用户名 <input type="text" name="user">
    密码 <input type="password" name="pwd">
    <input type="submit">
</form>

</body>
</html>
```

# 3 web框架

Web框架（Web framework）是一种开发框架，用来支持动态网站、网络应用和网络服务的开发。这大多数的web框架提供了一套开发和部署网站的方式，也为web行为提供了一套通用的方法。web框架已经实现了很多功能，开发人员使用框架提供的方法并且完成自己的业务逻辑，就能快速开发web应用了。浏览器和服务器的是基于HTTP协议进行通信的。也可以说web框架就是在以上十几行代码基础张扩展出来的，有很多简单方便使用的方法，大大提高了开发的效率。

### wsgiref模块

最简单的Web应用就是先把HTML用文件保存好，用一个现成的HTTP服务器软件，接收用户请求，从文件中读取HTML，返回。

如果要动态生成HTML，就需要把上述步骤自己来实现。不过，接受HTTP请求、解析HTTP请求、发送HTTP响应都是苦力活，如果我们自己来写这些底层代码，还没开始写动态HTML呢，就得花个把月去读HTTP规范。

正确的做法是底层代码由专门的服务器软件实现，我们用Python专注于生成HTML文档。因为我们不希望接触到TCP连接、HTTP原始请求和响应格式，所以，需要一个统一的接口协议来实现这样的服务器软件，让我们专心用Python编写Web业务。这个接口就是WSGI：Web Server Gateway Interface。而wsgiref模块就是python基于wsgi协议开发的服务模块。

```python
from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']


httpd = make_server('', 8080, application)

print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()
```

### DIY一个web框架

![img](assets2.0/877318-20180425174338237-444563046.png)

models.py

```python
import pymysql
#连接数据库
conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='',db='web') #db：库名
#创建游标
cur = conn.cursor()

sql='''
create table userinfo(
        id INT PRIMARY KEY ,
        name VARCHAR(32) ,
        password VARCHAR(32)
)

'''

cur.execute(sql)

#提交
conn.commit()
#关闭指针对象
cur.close()
#关闭连接对象
conn.close()
```

启动文件manage.py

```python
from wsgiref.simple_server import make_server

from app01.views import *
import urls


def routers():

    URLpattern=urls.URLpattern
    return URLpattern


def applications(environ,start_response):

    path=environ.get("PATH_INFO")
    start_response('200 OK', [('Content-Type', 'text/html'),('Charset', 'utf8')])
    urlpattern=routers()
    func=None
    for item in urlpattern:
        if path==item[0]:
            func=item[1]
            break
    if func:
        return [func(environ)]
    else:
        return [b"<h1>404!<h1>"]

if __name__ == '__main__':

    server=make_server("",8889,applications)
    print("server is working...")
    server.serve_forever()
```

urls.py

```python
from app01.views import *


URLpattern = (
    ("/login/", login),
)
```

views

```python
import pymysql

from urllib.parse import parse_qs


def login(request):

    if request.get("REQUEST_METHOD")=="POST":

        try:
            request_body_size = int(request.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = request['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)


        user=data.get(b"user")[0].decode("utf8")
        pwd=data.get(b"pwd")[0].decode("utf8")

        #连接数据库
        conn = pymysql.connect(host='127.0.0.1',port= 3306,user = 'root',passwd='',db='web') # db：库名
        #创建游标
        cur = conn.cursor()
        SQL="select * from userinfo WHERE NAME ='%s' AND PASSWORD ='%s'"%(user,pwd)
        cur.execute(SQL)

        if cur.fetchone():

            f=open("templates/backend.html","rb")
            data=f.read()
            data=data.decode("utf8")
            return data.encode("utf8")

        else:
             print("OK456")
             return b"user or pwd is wrong"

    else:
        f = open("templates/login.html", "rb")
        data = f.read()
        f.close()
        return data
```

login.html

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h4>登录页面</h4>
<form action="" method="post">
     用户名 <input type="text" name="user">
     密码 <input type="text" name="pwd">
    <input type="submit">
</form>

</body>
</html>
```

backend.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h4>welcome to oldboy!</h4>
</body>
</html>
```

yuan这个package就是一个web框架，下载这个web框架就可以快速实现一些简单的web功能，比如查看时间。

# 4 [4 Django简介](https://www.cnblogs.com/yuanchenqi/articles/8875659.html)

## MVC与MTV模型

## MVC

Web服务器开发领域里著名的MVC模式，所谓MVC就是把Web应用分为模型(M)，控制器(C)和视图(V)三层，他们之间以一种插件式的、松耦合的方式连接在一起，模型负责业务对象与数据库的映射(ORM)，视图负责与用户的交互(页面)，控制器接受用户的输入调用模型和视图完成用户的请求，其示意图如下所示：

![img](assets2.0/877318-20180418162558974-92667466.png)

## MTV

Django的MTV模式本质上和MVC是一样的，也是为了各组件间保持松耦合关系，只是定义上有些许不同，Django的MTV分别是值：

-   M 代表模型（Model）： 负责业务对象和数据库的关系映射(ORM)。
-   T 代表模板 (Template)：负责如何把页面展示给用户(html)。
-   V 代表视图（View）：  负责业务逻辑，并在适当时候调用Model和Template。

除了以上三层之外，还需要一个URL分发器，它的作用是将一个个URL的页面请求分发给不同的View处理，View再调用相应的Model和Template，MTV的响应模式如下所示：

![img](assets2.0/877318-20180418162350672-193671507.png)

一般是用户通过浏览器向我们的服务器发起一个请求(request)，这个请求回去访问视图函数，（如果不涉及到数据调用，那么这个时候视图函数返回一个模板也就是一个网页给用户），视图函数调用模型，模型去数据库查找数据，然后逐级返回，视图函数把返回的数据填充到模板中空格中，最后返回网页给用户。



# Django的下载与基本命令

### 1、下载Django：

```
pip3 install django
pip3 install django==2.0.1
```

### 2、创建一个django project

```
#安装之后 文件所在位置
/Library/Frameworks/Python.framework/Versions/3.9/bin/django-admin.py  

django-admin.py startproject mysite
```

 当前目录下会生成mysite的工程，目录结构如下：

​    ![img](assets2.0/877318-20160724114201404-1121087959.png)

-   manage.py ----- Django项目里面的工具，通过它可以调用django shell和数据库等。
-   settings.py ---- 包含了项目的默认设置，包括数据库信息，调试标志以及其他一些工作的变量。
-   urls.py ----- 负责把URL模式映射到应用程序。

### 3、在mysite目录下创建应用

```
python manage.py startapp blog
```

​    ![img](assets2.0/877318-20160724114930826-472002646.png)

### 4、启动django项目

```
python manage.py runserver 8080
```

​    这样我们的django就启动起来了！当我们访问：http://127.0.0.1:8080/时就可以看到：

​    ![img](assets2.0/877318-20160724120547497-22629173.png)

# 基于Django实现的一个简单示例

###  url控制器

```python
from django.contrib import admin
from django.urls import path


from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
]
```



### 视图

```python
from django.shortcuts import render

# Create your views here.


def index(request):

    import datetime
    now=datetime.datetime.now()
    ctime=now.strftime("%Y-%m-%d %X")

    return render(request,"index.html",{"ctime":ctime})
```



### 模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h4>当前时间:{{ ctime }}</h4>

</body>
</html>

```



执行效果如下：

 ![img](assets2.0/877318-20180423153419047-864210640.png)

 ```python
 #小提示:
 #settings.py 配置 应用名称 和templates 路径
 
 INSTALLED_APPS = [
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     'blog'   # 创建的应用名称
 ]
 
 
 TEMPLATES = [
     {
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': [os.path.join(BASE_DIR,'templates')],  # templates 目录路径
         'APP_DIRS': True,
         'OPTIONS': {
             'context_processors': [
                 'django.template.context_processors.debug',
                 'django.template.context_processors.request',
                 'django.contrib.auth.context_processors.auth',
                 'django.contrib.messages.context_processors.messages',
             ],
         },
     },
 ]
 
 
 # 在pycharm 中导入老师的代码
 # 用pycharm 打开终端,在项目目录下 运行运行 
 python3.9 manage.py runserver
 #配置到pycharm中直接点运行
 open ---> new window  -- > edit Configurations... -->配置 host 127.0.0.1
 # 数据库迁移
 python manage.py makemigrations   # 创建数据库的映射关系
 python manage.py migrate  # 根据上条命令生成的映射关系，在数据库中生成相应的表
 ```





# 5 Django-2的路由层(URLconf)



URL配置(URLconf)就像Django 所支撑网站的目录。它的本质是URL与要为该URL调用的视图函数之间的映射表；你就是以这种方式告诉Django，对于客户端发来的某个URL调用哪一段逻辑代码对应执行。

##  简单的路由配置



```python
from django.urls import path,re_path

from app01 import views

urlpatterns = [
    re_path(r'^articles/2003/$', views.special_case_2003),
    re_path(r'^articles/([0-9]{4})/$', views.year_archive),
    re_path(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    re_path(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]

```

注意：

-   若要从URL 中捕获一个值，只需要在它周围放置一对圆括号。
-   不需要添加一个前导的反斜杠，因为每个URL 都有。例如，应该是`^articles` 而不是 `^/articles`。 
-   每个正则表达式前面的'r' 是可选的但是建议加上。它告诉Python 这个字符串是“原始的” —— 字符串中任何字符都不应该转义

示例：

```
    '''
 一些请求的例子：

/articles/2005/03/ 请求将匹配列表中的第三个模式。Django 将调用函数views.month_archive(request, '2005', '03')。
/articles/2005/3/ 不匹配任何URL 模式，因为列表中的第三个模式要求月份应该是两个数字。
/articles/2003/ 将匹配列表中的第一个模式不是第二个，因为模式按顺序匹配，第一个会首先测试是否匹配。请像这样自由插入一些特殊的情况来探测匹配的次序。
/articles/2003 不匹配任何一个模式，因为每个模式要求URL 以一个反斜线结尾。
/articles/2003/03/03/ 将匹配最后一个模式。Django 将调用函数views.article_detail(request, '2003', '03', '03')。
   
    '''
```



## 有名分组

上面的示例使用简单的、没有命名的正则表达式组（通过圆括号）来捕获URL 中的值并以位置 参数传递给视图。在更高级的用法中，可以使用命名的正则表达式组来捕获URL 中的值并以关键字 参数传递给视图。

在Python 正则表达式中，命名正则表达式组的语法是`(?P<name>pattern)`，其中`name` 是组的名称，`pattern` 是要匹配的模式。

下面是以上URLconf 使用命名组的重写：

```
from django.urls import path,re_path

from app01 import views

urlpatterns = [
    re_path(r'^articles/2003/$', views.special_case_2003),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]
```



这个实现与前面的示例完全相同，只有一个细微的差别：捕获的值作为关键字参数而不是位置参数传递给视图函数。例如：

```
    '''
    /articles/2005/03/ 请求将调用views.month_archive(request, year='2005', month='03')函数，而不是views.month_archive(request, '2005', '03')。
    /articles/2003/03/03/ 请求将调用函数views.article_detail(request, year='2003', month='03', day='03')。

    '''
```

在实际应用中，这意味你的URLconf 会更加明晰且不容易产生参数顺序问题的错误 —— 你可以在你的视图函数定义中重新安排参数的顺序。当然，这些好处是以简洁为代价；

## 分发

```
'''
At any point, your urlpatterns can “include” other URLconf modules. This
essentially “roots” a set of URLs below other ones.

'''

from django.urls import path,re_path,include
from app01 import views

urlpatterns = [
   re_path(r'^admin/', admin.site.urls),
   re_path(r'^blog/', include('blog.urls')),   # 这个blog/路径分发给 blog.urls 文件里处理
   re_path(r'^', include('blog.urls')),   # 这个跟目录路径分发给 blog.urls 文件里处理
	 # re_path(r"^app02/",include(("app02.urls","app02"))), #第二个参数对应的是应用名称-名称空间

]
```



## 反向解析

在使用Django 项目时，一个常见的需求是获得URL 的最终形式，以用于嵌入到生成的内容中（视图中和显示给用户的URL等）或者用于处理服务器端的导航（重定向等）。人们强烈希望不要硬编码这些URL（费力、不可扩展且容易产生错误）或者设计一种与URLconf 毫不相关的专门的URL 生成机制，因为这样容易导致一定程度上产生过期的URL。

在需要URL 的地方，对于不同层级，Django 提供不同的工具用于URL 反查：

-   在模板中：使用url 模板标签。
-   在Python 代码中：使用`from django.urls import reverse()函数` 

urls.py:

```
from django.conf.urls import url

from . import views

urlpatterns = [
    #...   name 是起了一个别名, 在模板中引用 {% url 'news-year-archive' %}
    re_path(r'^articles/([0-9]{4})/$', views.year_archive, name='news-year-archive'),
    #...
]
```



在模板中：

```
<a href="{% url 'news-year-archive' 2012 %}">2012 Archive</a>  # 反向解析

<ul>
{% for yearvar in year_list %}
<li><a href="{% url 'news-year-archive' yearvar %}">{{ yearvar }} Archive</a></li>
{% endfor %}
</ul>
```



在python中：

```
from django.urls import reverse     #导入反向解析函数
from django.http import HttpResponseRedirect

def redirect_to_year(request):
    # ...
    year = 2006
    # ...
    return HttpResponseRedirect(reverse('news-year-archive', args=(year,)))   # 同redirect("/path/")
```



当命名你的URL 模式时，请确保使用的名称不会与其它应用中名称冲突。如果你的URL 模式叫做`comment`，而另外一个应用中也有一个同样的名称，当你在模板中使用这个名称的时候不能保证将插入哪个URL。在URL 名称中加上一个前缀，比如应用的名称，将减少冲突的可能。我们建议使用`myapp-comment` 而不是`comment`。

## 名称空间

命名空间（英语：Namespace）是表示标识符的可见范围。一个标识符可在多个命名空间中定义，它在不同命名空间中的含义是互不相干的。这样，在一个新的命名空间中可定义任何标识符，它们不会与任何已有的标识符发生冲突，因为已有的定义都处于其它命名空间中。

由于name没有作用域，Django在反解URL时，会在项目全局顺序搜索，当查找到第一个name指定URL时，立即返回

我们在开发项目时，会经常使用name属性反解出URL，当不小心在不同的app的urls中定义相同的name时，可能会导致URL反解错误，为了避免这种事情发生，引入了命名空间。

#### **project的urls.py:**

```
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    #re_path(r'^app01/', include("app01.urls",namespace="app01")), #报错
    #re_path(r'^app02/', include("app02.urls",namespace="app02")), #
    re_path(r'^app01/', include(("app01.urls","app01"))), #指定名称空间 app01
    re_path(r'^app02/', include(("app02.urls","app02"))), 

]
```

#### **app01.urls:**

```
urlpatterns = [
    re_path(r'^index/', index,name="index"),   # name 别名
]
```

#### **app02.urls:**

```
urlpatterns = [
    re_path(r'^index/', index,name="index"),  # name 别名
]
```

#### **app01.views** 

```
from django.core.urlresolvers import reverse

def index(request):

    return  HttpResponse(reverse("app01:index"))  #reverse反向解析("名称空间app01下的index")
```

#### app02.views

```
from django.core.urlresolvers import reverse

def index(request):

    return  HttpResponse(reverse("app02:index")) # 指定名称空间app02 下的index
```

## django2.0版的path

思考情况如下：

```
urlpatterns = [  
    re_path('articles/(?P<year>[0-9]{4})/', year_archive),  
    re_path('article/(?P<article_id>[a-zA-Z0-9]+)/detail/', detail_view),  
    re_path('articles/(?P<article_id>[a-zA-Z0-9]+)/edit/', edit_view),  
    re_path('articles/(?P<article_id>[a-zA-Z0-9]+)/delete/', delete_view),  
]
```

考虑下这样的两个问题：

第一个问题，函数 `year_archive` 中year参数是字符串类型的，因此需要先转化为整数类型的变量值，当然`year=int(year)` 不会有诸如如TypeError或者ValueError的异常。那么有没有一种方法，在url中，使得这一转化步骤可以由Django自动完成？

第二个问题，三个路由中article_id都是同样的正则表达式，但是你需要写三遍，当之后article_id规则改变后，需要同时修改三处代码，那么有没有一种方法，只需修改一处即可？

在Django2.0中，可以使用 `path` 解决以上的两个问题。

### 基本示例

这是一个简单的例子：

```
from django.urls import path  
from . import views  
urlpatterns = [  
    path('articles/2003/', views.special_case_2003),  
    # 内置转换器转换成int类型<int:year> 同时也是有名分组
    path('articles/<int:year>/', views.year_archive),   
    path('articles/<int:year>/<int:month>/', views.month_archive),  
    path('articles/<int:year>/<int:month>/<slug>/', views.article_detail),  
]  
```



基本规则：

-   使用尖括号(`<>`)从url中捕获值。
-   捕获值中可以包含一个转化器类型（converter type），比如使用 `<int:name>` 捕获一个整数变量。若果没有转化器，将匹配任何字符串，当然也包括了 `/` 字符。
-   无需添加前导斜杠。

以下是根据 [2.0官方文档](https://docs.djangoproject.com/en/2.0/topics/http/urls/#example) 而整理的示例分析表：

![img](assets2.0/877318-20180424163727952-1649289117.png)

### path转化器

>   文档原文是Path converters，暂且翻译为转化器。

Django默认支持以下5个转化器：

-   str,匹配除了路径分隔符（`/`）之外的非空字符串，这是默认的形式
-   int,匹配正整数，包含0。
-   slug,匹配字母、数字以及横杠、下划线组成的字符串。
-   uuid,匹配格式化的uuid，如 075194d3-6885-417e-a8a8-6c931e272f00。
-   path,匹配任何非空字符串，包含了路径分隔符

### 注册自定义转化器

对于一些复杂或者复用的需要，可以定义自己的转化器。转化器是一个类或接口，它的要求有三点：

-   `regex` 类属性，字符串类型

-   `to_python(self, value)` 方法，value是由类属性 `regex` 所匹配到的字符串，返回具体的Python变量值，以供Django传递到对应的视图函数中。
-   `to_url(self, value)` 方法，和 `to_python` 相反，value是一个具体的Python变量值，返回其字符串，通常用于url反向引用。

例子：

```
# 注册文件建议写在 应用目录里 写urlconvert.py
class FourDigitYearConverter:  
    regex = '[0-9]{4}'   # regex 固定属性写法
    def to_python(self, value):  
        return int(value)  
    def to_url(self, value):   # 反向解析  
        return '%04d' % value  
```

使用`register_converter` 将其注册到URL配置中：

```
# 在主项目的 urls.py注册
from django.urls import register_converter, path    # 导入 register_converter
from app01.urlconvert import FourDigitYearConverter  # 导入app01里写的转化器方法
from . import converters, views  
register_converter(converters.FourDigitYearConverter, 'yyyy')  
register_converter(FourDigitYearConverter, 'yy')  # 注册转化器方法 别名 yy
urlpatterns = [  
    path('articles/2003/', views.special_case_2003),  
    path('articles/<yy:year>/', views.year_archive),   # yy是调用的自定义的转换器
    ...  
]  
```



# [6 Django的视图层](https://www.cnblogs.com/yuanchenqi/articles/8876856.html) 

## 视图函数

一个视图函数，简称视图，是一个简单的Python 函数，它接受Web请求并且返回Web响应。响应可以是一张网页的HTML内容，一个重定向，一个404错误，一个XML文档，或者一张图片. . . 是任何东西都可以。无论视图本身包含什么逻辑，都要返回响应。代码写在哪里也无所谓，只要它在你的Python目录下面。除此之外没有更多的要求了——可以说“没有什么神奇的地方”。为了将代码放在某处，约定是将视图放置在项目或应用程序目录中的名为`views.py`的文件中。

下面是一个返回当前日期和时间作为HTML文档的视图：

```
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
```

让我们逐行阅读上面的代码：

-   首先，我们从 `django.shortcuts`模块导入了`HttpResponse`类，以及Python的`datetime`库。

-   接着，我们定义了`current_datetime`函数。它就是视图函数。每个视图函数都使用`HttpRequest`对象作为第一个参数，并且通常称之为`request`。

    注意,视图函数的名称并不重要；不需要用一个统一的命名方式来命名，以便让Django识别它。我们将其命名为`current_datetime`，是因为这个名称能够精确地反映出它的功能。

-   这个视图会返回一个`HttpResponse`对象，其中包含生成的响应。每个视图函数都负责返回一个`HttpResponse`对象。

#### <img src="assets2.0/877318-20160725101445044-1768854009.jpg" alt="img" style="zoom:50%;" />

视图层，熟练掌握两个对象即可：请求对象(request)和响应对象(HttpResponse)

## HttpRequest对象

### request属性 　　

django将请求报文中的请求行、首部信息、内容主体封装成 HttpRequest 类中的属性。 除了特殊说明的之外，其他均为只读的。

```
/*

1.HttpRequest.GET

　　一个类似于字典的对象，包含 HTTP GET 的所有参数。详情请参考 QueryDict 对象。

2.HttpRequest.POST

　　一个类似于字典的对象，如果请求中包含表单数据，则将这些数据封装成 QueryDict 对象。

　　POST 请求可以带有空的 POST 字典 —— 如果通过 HTTP POST 方法发送一个表单，但是表单中没有任何的数据，QueryDict 对象依然会被创建。
   因此，不应该使用 if request.POST  来检查使用的是否是POST 方法；应该使用 if request.method == "POST"
　　另外：如果使用 POST 上传文件的话，文件信息将包含在 FILES 属性中。
   
   注意：键值对的值是多个的时候,比如checkbox类型的input标签，select标签，需要用：
        request.POST.getlist("hobby")

3.HttpRequest.body

　　一个字符串，代表请求报文的主体。在处理非 HTTP 形式的报文时非常有用，例如：二进制图片、XML,Json等。
　　但是，如果要处理表单数据的时候，推荐还是使用 HttpRequest.POST 。


4.HttpRequest.path

　　一个字符串，表示请求的路径组件（不含域名）。
　　例如："/music/bands/the_beatles/"

5.HttpRequest.method

　　一个字符串，表示请求使用的HTTP 方法。必须使用大写。
　　例如："GET"、"POST"


6.HttpRequest.encoding

　　一个字符串，表示提交的数据的编码方式（如果为 None 则表示使用 DEFAULT_CHARSET 的设置，默认为 'utf-8'）。
   这个属性是可写的，你可以修改它来修改访问表单数据使用的编码。
   接下来对属性的任何访问（例如从 GET 或 POST 中读取数据）将使用新的 encoding 值。
   如果你知道表单数据的编码不是 DEFAULT_CHARSET ，则使用它。


7.HttpRequest.META

 　　一个标准的Python 字典，包含所有的HTTP 首部。具体的头部信息取决于客户端和服务器，下面是一些示例：

    CONTENT_LENGTH —— 请求的正文的长度（是一个字符串）。
    CONTENT_TYPE —— 请求的正文的MIME 类型。
    HTTP_ACCEPT —— 响应可接收的Content-Type。
    HTTP_ACCEPT_ENCODING —— 响应可接收的编码。
    HTTP_ACCEPT_LANGUAGE —— 响应可接收的语言。
    HTTP_HOST —— 客服端发送的HTTP Host 头部。
    HTTP_REFERER —— Referring 页面。
    HTTP_USER_AGENT —— 客户端的user-agent 字符串。
    QUERY_STRING —— 单个字符串形式的查询字符串（未解析过的形式）。
    REMOTE_ADDR —— 客户端的IP 地址。
    REMOTE_HOST —— 客户端的主机名。
    REMOTE_USER —— 服务器认证后的用户。
    REQUEST_METHOD —— 一个字符串，例如"GET" 或"POST"。
    SERVER_NAME —— 服务器的主机名。
    SERVER_PORT —— 服务器的端口（是一个字符串）。
 　　从上面可以看到，除 CONTENT_LENGTH 和 CONTENT_TYPE 之外，请求中的任何 HTTP 首部转换为 META 的键时，
    都会将所有字母大写并将连接符替换为下划线最后加上 HTTP_  前缀。
    所以，一个叫做 X-Bender 的头部将转换成 META 中的 HTTP_X_BENDER 键。

8.HttpRequest.FILES

　　一个类似于字典的对象，包含所有的上传文件信息。
   FILES 中的每个键为<input type="file" name="" /> 中的name，值则为对应的数据。
　　注意，FILES 只有在请求的方法为POST 且提交的<form> 带有enctype="multipart/form-data" 的情况下才会
   包含数据。否则，FILES 将为一个空的类似于字典的对象。


9.HttpRequest.COOKIES

　　一个标准的Python 字典，包含所有的cookie。键和值都为字符串。



10.HttpRequest.session

 　　一个既可读又可写的类似于字典的对象，表示当前的会话。只有当Django 启用会话的支持时才可用。
    完整的细节参见会话的文档。


11.HttpRequest.user(用户认证组件下使用)

　　一个 AUTH_USER_MODEL 类型的对象，表示当前登录的用户。

　　如果用户当前没有登录，user 将设置为 django.contrib.auth.models.AnonymousUser 的一个实例。你可以通过 is_authenticated() 区分它们。

    例如：

    if request.user.is_authenticated():
        # Do something for logged-in users.
    else:
        # Do something for anonymous users.


     　　user 只有当Django 启用 AuthenticationMiddleware 中间件时才可用。

     -------------------------------------------------------------------------------------

    匿名用户
    class models.AnonymousUser

    django.contrib.auth.models.AnonymousUser 类实现了django.contrib.auth.models.User 接口，但具有下面几个不同点：

    id 永远为None。
    username 永远为空字符串。
    get_username() 永远返回空字符串。
    is_staff 和 is_superuser 永远为False。
    is_active 永远为 False。
    groups 和 user_permissions 永远为空。
    is_anonymous() 返回True 而不是False。
    is_authenticated() 返回False 而不是True。
    set_password()、check_password()、save() 和delete() 引发 NotImplementedError。
    New in Django 1.8:
    新增 AnonymousUser.get_username() 以更好地模拟 django.contrib.auth.models.User。

*/
```



### request常用方法



```
/*

1.HttpRequest.get_full_path()

　　返回 path，如果可以将加上查询字符串。

　　例如："/music/bands/the_beatles/?print=true"


2.HttpRequest.is_ajax()

　　如果请求是通过XMLHttpRequest 发起的，则返回True，方法是检查 HTTP_X_REQUESTED_WITH 相应的首部是否是字符串'XMLHttpRequest'。

　　大部分现代的 JavaScript 库都会发送这个头部。如果你编写自己的 XMLHttpRequest 调用（在浏览器端），你必须手工设置这个值来让 is_ajax() 可以工作。

　　如果一个响应需要根据请求是否是通过AJAX 发起的，并且你正在使用某种形式的缓存例如Django 的 cache middleware，
   你应该使用 vary_on_headers('HTTP_X_REQUESTED_WITH') 装饰你的视图以让响应能够正确地缓存。

*/

```



## HttpResponse对象

响应对象主要有三种形式：

-   HttpResponse()
-   render()
-   redirect()

HttpResponse()括号内直接跟一个具体的字符串作为响应体，比较直接很简单，所以这里主要介绍后面两种形式。

### render()

```
render(request, template_name[, context]）` `结合一个给定的模板和一个给定的上下文字典，并返回一个渲染后的 HttpResponse 对象。
参数：
     request： 用于生成响应的请求对象。

     template_name：要使用的模板的完整名称，可选的参数

     context：添加到模板上下文的一个字典。默认是一个空字典。如果字典中的某个值是可调用的，视图将在渲染模板之前调用它。

render方法就是将一个模板页面中的模板语法进行渲染，最终渲染成一个html页面作为响应体。

```

### redirect()

传递要重定向的一个硬编码的URL

```
def my_view(request):
    ...
    return redirect('/some/url/')
```

也可以是一个完整的URL：

```
def my_view(request):
    ...
    return redirect('http://example.com/')　
```

key：两次请求　

```
1）301和302的区别。

　　301和302状态码都表示重定向，就是说浏览器在拿到服务器返回的这个状态码后会自动跳转到一个新的URL地址，这个地址可以从响应的Location首部中获取
  （用户看到的效果就是他输入的地址A瞬间变成了另一个地址B）——这是它们的共同点。

　　他们的不同在于。301表示旧地址A的资源已经被永久地移除了（这个资源不可访问了），搜索引擎在抓取新内容的同时也将旧的网址交换为重定向之后的网址；

　　302表示旧地址A的资源还在（仍然可以访问），这个重定向只是临时地从旧地址A跳转到地址B，搜索引擎会抓取新的内容而保存旧的网址。 SEO302好于301

2）重定向原因：
（1）网站调整（如改变网页目录结构）；
（2）网页被移到一个新地址；
（3）网页扩展名改变(如应用需要把.php改成.Html或.shtml)。
        这种情况下，如果不做重定向，则用户收藏夹或搜索引擎数据库中旧地址只能让访问客户得到一个404页面错误信息，访问流量白白丧失；再者某些注册了多个域名的
    网站，也需要通过重定向让访问这些域名的用户自动跳转到主站点等。
    
```

用redirect可以解释APPEND_SLASH的用法！

```
小提示:
HttpResponse() #用于回复一个字符串 HttpResponse("aaa")  开发中很少用.
```



 # [7 Django的模板层](https://www.cnblogs.com/yuanchenqi/articles/8876892.html)

你可能已经注意到我们在例子视图中返回文本的方式有点特别。 也就是说，HTML被直接硬编码在 Python代码之中。

```
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
```

尽管这种技术便于解释视图是如何工作的，但直接将HTML硬编码到你的视图里却并不是一个好主意。 让我们来看一下为什么：

-   对页面设计进行的任何改变都必须对 Python 代码进行相应的修改。 站点设计的修改往往比底层 Python 代码的修改要频繁得多，因此如果可以在不进行 Python 代码修改的情况下变更设计，那将会方便得多。

-   Python 代码编写和 HTML 设计是两项不同的工作，大多数专业的网站开发环境都将他们分配给不同的人员（甚至不同部门）来完成。 设计者和HTML/CSS的编码人员不应该被要求去编辑Python的代码来完成他们的工作。

-   程序员编写 Python代码和设计人员制作模板两项工作同时进行的效率是最高的，远胜于让一个人等待另一个人完成对某个既包含 Python又包含 HTML 的文件的编辑工作。

基于这些原因，将页面的设计和Python的代码分离开会更干净简洁更容易维护。 我们可以使用 Django的 *模板系统* (Template System)来实现这种模式，这就是本章要具体讨论的问题。

```
python的模板：HTML代码＋模板语法
```



```
def current_time(req):
    # ================================原始的视图函数
    # import datetime
    # now=datetime.datetime.now()
    # html="<html><body>现在时刻：<h1>%s.</h1></body></html>" %now


    # ================================django模板修改的视图函数
    # from django.template import Template,Context
    # now=datetime.datetime.now()
    # t=Template('<html><body>现在时刻是:<h1>{{current_date}}</h1></body></html>')
    # #t=get_template('current_datetime.html')
    # c=Context({'current_date':str(now)})
    # html=t.render(c)
    #
    # return HttpResponse(html)


    #另一种写法(推荐)
    import datetime
    now=datetime.datetime.now()
    return render(req, 'current_datetime.html', {'current_date':str(now)[:19]})
```



## 1 模板语法之变量

在 Django 模板中遍历复杂数据结构的关键是句点字符, 语法： 

```
{{var_name}}
```

**views.py：**

```python
def index(request):
    import datetime
    s="hello"
    l=[111,222,333]    # 列表
    dic={"name":"yuan","age":18}  # 字典
    date = datetime.date(1993, 5, 2)   # 日期对象
 
    class Person(object):
        def __init__(self,name):
            self.name=name
 
    person_yuan=Person("yuan")  # 自定义类对象
    person_egon=Person("egon")
    person_alex=Person("alex")
 
    person_list=[person_yuan,person_egon,person_alex]
 
    return render(request,"index.html",{"l":l,"dic":dic,"date":date,"person_list":person_list})
    
```



***template：** 

```
<h4>{{s}}</h4>
<h4>列表:{{ l.0 }}</h4>
<h4>列表:{{ l.2 }}</h4>
<h4>字典:{{ dic.name }}</h4>
<h4>日期:{{ date.year }}</h4>
<h4>类对象列表:{{ person_list.0.name }}</h4>
```

注意：句点符也可以用来引用对象的方法(无参数方法):

```
<h4>字典:{{ dic.name.upper }}<``/``h4>
```

## 2 模板之过滤器

语法：

```
{{obj|filter__name:param}}
```

### `default`

如果一个变量是false或者为空，使用给定的默认值。否则，使用变量的值。例如：

```
{{ value|default:"nothing" }}

```

### length

返回值的长度。它对字符串和列表都起作用。例如：

```
{{ value|length }}
```

如果 value 是 ['a', 'b', 'c', 'd']，那么输出是 4。

### `filesizeformat`

将值格式化为一个 “人类可读的” 文件尺寸 （例如 `'13 KB'`, `'4.1 MB'`, `'102 bytes'`, 等等）。例如：

```
{{ value|filesizeformat }}

```

如果 `value` 是 123456789，输出将会是 `117.7 MB`。　　

### date

如果 value=datetime.datetime.now()

```
{{ value|date:"Y-m-d" }}　　
```

### slice

如果 value="hello world"

```
{{ value|slice:"2:-1" }}
```

### truncatechars[ ](http://python.usyiyi.cn/documents/django_182/ref/templates/builtins.html#truncatechars)

如果字符串字符多于指定的字符数量，那么会被截断。截断的字符串将以可翻译的省略号序列（“...”）结尾。

**参数：**要截断的字符数

例如：

```
{{ value|truncatechars:9 }}
```

### safe

Django的模板中会对HTML标签和JS等语法标签进行自动转义，原因显而易见，这样是为了安全。但是有的时候我们可能不希望这些HTML元素被转义，比如我们做一个内容管理系统，后台添加的文章中是经过修饰的，这些修饰可能是通过一个类似于FCKeditor编辑加注了HTML修饰符的文本，如果自动转义的话显示的就是保护HTML标签的源文件。为了在Django中关闭HTML的自动转义有两种方式，如果是一个单独的变量我们可以通过过滤器“|safe”的方式告诉Django这段代码是安全的不必转义。比如：

```
value="<a href="">点击</a>"

{{ value|safe}}
```

这里简单介绍一些常用的模板的过滤器，

https://docs.djangoproject.com/zh-hans/3.2/ref/templates/builtins/



## 3 模板之标签　

标签看起来像是这样的： `{% tag %}`。标签比变量更加复杂：一些在输出中创建文本，一些通过循环或逻辑来控制流程，一些加载其后的变量将使用到的额外信息到模版中。一些标签需要开始和结束标签 （例如`{% tag %} ...`标签 内容 ... {% endtag %}）。

### **for标签**

遍历每一个元素：

```
{% for person in person_list %}
    <p>{{ person.name }}</p>
{% endfor %}
```

可以利用`{% for obj in list reversed %}`反向完成循环。

遍历一个字典：

```
{% for key,val in dic.items %}
    <p>{{ key }}:{{ val }}</p>
{% endfor %}
```

注：循环序号可以通过｛｛forloop｝｝显示　　

```
forloop.counter            The current iteration of the loop (1-indexed)
forloop.counter0           The current iteration of the loop (0-indexed)
forloop.revcounter         The number of iterations from the end of the loop (1-indexed)
forloop.revcounter0        The number of iterations from the end of the loop (0-indexed)
forloop.first              True if this is the first time through the loop
forloop.last               True if this is the last time through the loop
```

### for ... empty[ ](http://python.usyiyi.cn/documents/django_182/ref/templates/builtins.html#for-empty)

`for` 标签带有一个可选的`{% empty %}` 从句，以便在给出的组是空的或者没有被找到时，可以有所操作。

```
{% for person in person_list %}
    <p>{{ person.name }}</p>

{% empty %}
    <p>sorry,no person here</p>
{% endfor %}
```

### if 标签

`{% if %}`会对一个变量求值，如果它的值是“True”（存在、不为空、且不是boolean类型的false值），对应的内容块会输出。



```
{% if num > 100 or num < 0 %}
    <p>无效</p>
{% elif num > 80 and num < 100 %}
    <p>优秀</p>
{% else %}
    <p>凑活吧</p>
{% endif %}
```

### with[ ](http://python.usyiyi.cn/documents/django_182/ref/templates/builtins.html#with)

使用一个简单地名字缓存一个复杂的变量，当你需要使用一个“昂贵的”方法（比如访问数据库）很多次的时候是非常有用的

例如：

```
{% with total=business.employees.count %}
    {{ total }} employee{{ total|pluralize }}
{% endwith %}
```

### csrf_token

这个标签用于跨站请求伪造保护

这叫跨站请求伪造，Cross Site Request Forgery（**CSRF**）

## 4 自定义标签和过滤器

1、在settings中的INSTALLED_APPS配置当前app，不然django无法找到自定义的simple_tag.

2、在app中创建templatetags模块(模块名只能是templatetags)

3、创建任意 .py 文件，如：my_tags.py

```python
from django import template
from django.utils.safestring import mark_safe
 
register = template.Library()   #register的名字是固定的,不可改变
 
 
@register.filter
def filter_multi(v1,v2):
    return  v1 * v2
<br>
@register.simple_tag
def simple_tag_multi(v1,v2):
    return  v1 * v2
<br>
@register.simple_tag
def my_input(id,arg):
    result = "<input type='text' id='%s' class='%s' />" %(id,arg,)
    return mark_safe(result)
```



**4、在使用自定义simple_tag和filter的html文件中导入之前创建的 my_tags.py**

```
{% load my_tags %}　

```

**5、使用simple_tag和filter（如何调用）**

```
-------------------------------.html
{% load xxx %}  
      
# num=12
{{ num|filter_multi:2 }} #24
 
{{ num|filter_multi:"[22,333,4444]" }}
 
{% simple_tag_multi 2 5 %}  参数不限,但不能放在if for语句中
{% simple_tag_multi num 5 %}
```

注意：filter可以用在if等语句后，simple_tag不可以

```
{% if num|filter_multi:30 > 100 %}
    {{ num|filter_multi:30 }}
{% endif %}
```

```
小笔记:
自定义的过滤器最多两个参数,
自定义标签不限制参数
```



## 5 模板继承 (extend)

Django模版引擎中最强大也是最复杂的部分就是模版继承了。模版继承可以让您创建一个基本的“骨架”模版，它包含您站点中的全部元素，并且可以定义能够被子模版覆盖的 blocks 。

通过从下面这个例子开始，可以容易的理解模版继承：



```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %}My amazing site{%/span> endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```



这个模版，我们把它叫作 `base.html`， 它定义了一个可以用于两列排版页面的简单HTML骨架。“子模版”的工作是用它们的内容填充空的blocks。

在这个例子中， `block` 标签定义了三个可以被子模版内容填充的block。 `block` 告诉模版引擎： 子模版可能会覆盖掉模版中的这些位置。

子模版可能看起来是这样的：

```
{% extends "base.html" %}
 
{% block title %}My amazing blog{% endblock %}
 
{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

`extends` 标签是这里的关键。它告诉模版引擎，这个模版“继承”了另一个模版。当模版系统处理这个模版时，首先，它将定位父模版——在此例中，就是“base.html”。

那时，模版引擎将注意到 `base.html` 中的三个 `block` 标签，并用子模版中的内容来替换这些block。根据 `blog_entries` 的值，输出可能看起来是这样的：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>My amazing blog</title>
</head>
 
<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>
 
    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>
 
        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

请注意，子模版并没有定义 `sidebar` block，所以系统使用了父模版中的值。父模版的 `{% block %}` 标签中的内容总是被用作备选内容（fallback）。

这种方式使代码得到最大程度的复用，并且使得添加内容到共享的内容区域更加简单，例如，部分范围内的导航。

这里是使用继承的一些提示：

-   如果你在模版中使用 `{% extends %}` 标签，它必须是模版中的第一个标签。其他的任何情况下，模版继承都将无法工作。

-   在base模版中设置越多的 `{% block %}` 标签越好。请记住，子模版不必定义全部父模版中的blocks，所以，你可以在大多数blocks中填充合理的默认内容，然后，只定义你需要的那一个。多一点钩子总比少一点好。

-   如果你发现你自己在大量的模版中复制内容，那可能意味着你应该把内容移动到父模版中的一个 `{% block %}` 中。

-   If you need to get the content of the block from the parent template, the `{{ block.super }}` variable will do the trick. This is useful if you want to add to the contents of a parent block instead of completely overriding it. Data inserted using `{{ block.super }}` will not be automatically escaped (see the next section), since it was already escaped, if necessary, in the parent template.

-   为了更好的可读性，你也可以给你的 `{% endblock %}` 标签一个 *名字* 。例如：

    ```python
    {% block content %}
    ...
    {% endblock content %}　　
    ```

    在大型模版中，这个方法帮你清楚的看到哪一个　 `{% block %}` 标签被关闭了。

-   不能在一个模版中定义多个相同名字的 `block` 标签。



# [8 Django 模型层(1)](https://www.cnblogs.com/yuanchenqi/articles/8933283.html)

# ORM简介

-   MVC或者MVC框架中包括一个重要的部分，就是ORM，它实现了数据模型与数据库的解耦，即数据模型的设计不需要依赖于特定的数据库，通过简单的配置就可以轻松更换数据库，这极大的减轻了开发人员的工作量，不需要面对因数据库变更而导致的无效劳动
-   ORM是“对象-关系-映射”的简称。

![img](assets2.0/877318-20180425153356710-1116321211.png)



```
 #sql中的表                                                      

 #创建表:
     CREATE TABLE employee(                                     
                id INT PRIMARY KEY auto_increment ,                    
                name VARCHAR (20),                                      
                gender BIT default 1,                                  
                birthday DATA ,                                         
                department VARCHAR (20),                                
                salary DECIMAL (8,2) unsigned,                          
              );


  #sql中的表纪录                                                  

  #添加一条表纪录:                                                          
      INSERT employee (name,gender,birthday,salary,department)            
             VALUES   ("alex",1,"1985-12-12",8000,"保洁部");               

  #查询一条表纪录:                                                           
      SELECT * FROM employee WHERE age=24;                               

  #更新一条表纪录:                                                           
      UPDATE employee SET birthday="1989-10-24" WHERE id=1;              

  #删除一条表纪录:                                                          
      DELETE FROM employee WHERE name="alex"                             


#python的类
class Employee(models.Model):
     id=models.AutoField(primary_key=True)
     name=models.CharField(max_length=32)
     gender=models.BooleanField()
     birthday=models.DateField()
     department=models.CharField(max_length=32)
     salary=models.DecimalField(max_digits=8,decimal_places=2)


 #python的类对象
      #添加一条表纪录:
          emp=Employee(name="alex",gender=True,birthday="1985-12-12",epartment="保洁部")
          emp.save()
      #查询一条表纪录:
          Employee.objects.filter(age=24)
      #更新一条表纪录:
          Employee.objects.filter(id=1).update(birthday="1989-10-24")
      #删除一条表纪录:
          Employee.objects.filter(name="alex").delete()
```



# 单表操作

## 创建表

### 1 创建模型

<img src="assets2.0/877318-20180426141311697-594587712.png" alt="img" style="zoom:50%;" />

创建名为book的app，在book下的models.py中创建模型：

```
from django.db import models

# Create your models here.

class Book(models.Model):
     id=models.AutoField(primary_key=True)
     title=models.CharField(max_length=32)
     state=models.BooleanField()
     pub_date=models.DateField()
     price=models.DecimalField(max_digits=8,decimal_places=2)
     publish=models.CharField(max_length=32)
     
```



### 2 更多字段和参数

每个字段有一些特有的参数，例如，CharField需要max_length参数来指定`VARCHAR`数据库字段的大小。还有一些适用于所有字段的通用参数。 这些参数在文档中有详细定义，这里我们只简单介绍一些最常用的：

**更多字段：**

```
'''
 
<1> CharField
        字符串字段, 用于较短的字符串.
        CharField 要求必须有一个参数 maxlength, 用于从数据库层和Django校验层限制该字段所允许的最大字符数.
 
<2> IntegerField
       #用于保存一个整数.
 
<3> FloatField
        一个浮点数. 必须 提供两个参数:
         
        参数    描述
        max_digits    总位数(不包括小数点和符号)
        decimal_places    小数位数
                举例来说, 要保存最大值为 999 (小数点后保存2位),你要这样定义字段:
                 
                models.FloatField(..., max_digits=5, decimal_places=2)
                要保存最大值一百万(小数点后保存10位)的话,你要这样定义:
                 
                models.FloatField(..., max_digits=19, decimal_places=10)
                admin 用一个文本框(<input type="text">)表示该字段保存的数据.
 
<4> AutoField
        一个 IntegerField, 添加记录时它会自动增长. 你通常不需要直接使用这个字段;
        自定义一个主键：my_id=models.AutoField(primary_key=True)
        如果你不指定主键的话,系统会自动添加一个主键字段到你的 model.
 
<5> BooleanField
        A true/false field. admin 用 checkbox 来表示此类字段.
 
<6> TextField
        一个容量很大的文本字段.
        admin 用一个 <textarea> (文本区域)表示该字段数据.(一个多行编辑框).
 
<7> EmailField
        一个带有检查Email合法性的 CharField,不接受 maxlength 参数.
 
<8> DateField
        一个日期字段. 共有下列额外的可选参数:
        Argument    描述
        auto_now    当对象被保存时,自动将该字段的值设置为当前时间.通常用于表示 "last-modified" 时间戳.
        auto_now_add    当对象首次被创建时,自动将该字段的值设置为当前时间.通常用于表示对象创建时间.
        （仅仅在admin中有意义...)
 
<9> DateTimeField
         一个日期时间字段. 类似 DateField 支持同样的附加选项.
 
<10> ImageField
        类似 FileField, 不过要校验上传对象是否是一个合法图片.#它有两个可选参数:height_field和width_field,
        如果提供这两个参数,则图片将按提供的高度和宽度规格保存.    
<11> FileField
     一个文件上传字段.
     要求一个必须有的参数: upload_to, 一个用于保存上载文件的本地文件系统路径. 这个路径必须包含 strftime #formatting,
     该格式将被上载文件的 date/time
     替换(so that uploaded files don't fill up the given directory).
     admin 用一个<input type="file">部件表示该字段保存的数据(一个文件上传部件) .
 
     注意：在一个 model 中使用 FileField 或 ImageField 需要以下步骤:
 （1）在你的 settings 文件中, 定义一个完整路径给 MEDIA_ROOT 以便让 Django在此处保存上传文件.
        (出于性能考虑,这些文件并不保存到数据库.) 定义MEDIA_URL 作为该目录的公共 URL. 要确保该目录对
             WEB服务器用户帐号是可写的.
 （2） 在你的 model 中添加 FileField 或 ImageField, 并确保定义了 upload_to 选项,以告诉 Django
      使用 MEDIA_ROOT 的哪个子目录保存上传文件.你的数据库中要保存的只是文件的路径(相对于 MEDIA_ROOT).
      出于习惯你一定很想使用 Django 提供的 get_<#fieldname>_url 函数.举例来说,如果你的 ImageField
    叫作 mug_shot, 你就可以在模板中以 {{ object.#get_mug_shot_url }} 这样的方式得到图像的绝对路径.
 
<12> URLField
    用于保存 URL. 若 verify_exists 参数为 True (默认), 给定的 URL 会预先检查是否存在( 即URL是否被有效装入且没有返回404响应).
   admin 用一个 <input type="text"> 文本框表示该字段保存的数据(一个单行编辑框)
 
<13> NullBooleanField
    类似 BooleanField, 不过允许 NULL 作为其中一个选项. 推荐使用这个字段而不要用 BooleanField 加 null=True 选项admin 用一个选择框 <select> (三个可选择的值: "Unknown", "Yes" 和 "No" ) 来表示这种字段数据.
 
<14> SlugField
      "Slug" 是一个报纸术语. slug 是某个东西的小小标记(短签), 只包含字母,数字,下划线和连字符.#它们通常用于URLs 若你使用 Django 开发版本,你可以指定 maxlength. 若 maxlength 未指定, Django 会使用默认长度: 50.  #在以前的 Django 版本,没有任何办法改变50 这个长度. 这暗示了 db_index=True.
 它接受一个额外的参数: 
 prepopulate_from, which is a list of fields from which to auto-#populate
 the slug, via JavaScript,in the object's admin form: models.SlugField
 (prepopulate_from=("pre_name", "name"))prepopulate_from 不接受 DateTimeFields.
 
<13> XMLField
   一个校验值是否为合法XML的 TextField,必须提供参数: schema_path, 它是一个用来校验文本的 RelaxNG schema #的文件系统路径.
 
<14> FilePathField
可选项目为某个特定目录下的文件名. 支持三个特殊的参数, 其中第一个是必须提供的.
参数    描述
path    必需参数. 一个目录的绝对文件系统路径. FilePathField 据此得到可选项目.
Example: "/home/images".
match    可选参数. 一个正则表达式, 作为一个字符串, FilePathField 将使用它过滤文件名. 
注意这个正则表达式只会应用到 base filename 而不是
路径全名. Example: "foo.*\.txt^", 将匹配文件 foo23.txt 却不匹配 bar.txt 或 foo23.gif.
recursive可选参数.要么 True 要么 False. 默认值是 False. 是否包括 path 下面的全部子目录.
这三个参数可以同时使用.
match 仅应用于 base filename, 而不是路径全名. 那么,这个例子:
FilePathField(path="/home/images", match="foo.*", recursive=True)
...会匹配 /home/images/foo.gif 而不匹配 /home/images/foo/bar.gif
 
<15> IPAddressField
        一个字符串形式的 IP 地址, (i.e. "24.124.1.30").
<16> CommaSeparatedIntegerField
        用于存放逗号分隔的整数值. 类似 CharField, 必须要有maxlength参数.
 
 
 
'''　　
```



**更多参数：**

```
(1)null
 
如果为True，Django 将用NULL 来在数据库中存储空值。 默认值是 False.
 
(1)blank
 
如果为True，该字段允许不填。默认为False。
要注意，这与 null 不同。null纯粹是数据库范畴的，而 blank 是数据验证范畴的。
如果一个字段的blank=True，表单的验证将允许该字段是空值。如果字段的blank=False，该字段就是必填的。
 
(2)default
 
字段的默认值。可以是一个值或者可调用对象。如果可调用 ，每有新对象被创建它都会被调用。
 
(3)primary_key
 
如果为True，那么这个字段就是模型的主键。如果你没有指定任何一个字段的primary_key=True，
Django 就会自动添加一个IntegerField字段做为主键，所以除非你想覆盖默认的主键行为，
否则没必要设置任何一个字段的primary_key=True。
 
(4)unique
 
如果该值设置为 True, 这个数据字段的值在整张表中必须是唯一的
 
(5)choices
由二元组组成的一个可迭代对象（例如，列表或元组），用来给字段提供选择项。 如果设置了choices ，默认的表单将是一个选择框而不是标准的文本框，<br>而且这个选择框的选项就是choices 中的选项。

```



### 3 settings配置

若想将模型转为mysql数据库中的表，需要在settings中配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'bms',     　　 　  # 要连接的数据库，连接前需要创建好
        'USER':'root',　　　　　　  # 连接数据库的用户名
        'PASSWORD':'',　　　　　　  # 连接数据库的密码
        'HOST':'127.0.0.1',       # 连接主机，默认本级
        'PORT'：3306    　　　     #  端口 默认3306
    }
}
```



注意1：NAME即数据库的名字，在mysql连接前该数据库必须已经创建，而上面的sqlite数据库下的db.sqlite3则是项目自动创建 USER和PASSWORD分别是数据库的用户名和密码。设置完后，再启动我们的Django项目前，我们需要激活我们的mysql。然后，启动项目，会报错：no module named MySQLdb 。这是因为django默认你导入的驱动是MySQLdb，可是MySQLdb 对于py3有很大问题，所以我们需要的驱动是PyMySQL 所以，我们只需要找到项目名文件下的__init__,在里面写入：

```
import pymysql
pymysql.install_as_MySQLdb()
```

最后通过两条数据库迁移命令即可在指定的数据库中创建表 ：

```
python manage.py makemigrations
python manage.py migrate
```

注意2:确保配置文件中的INSTALLED_APPS中写入我们创建的app名称

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "book"   #新建的app名称
]
```



注意3:如果报错如下：

```
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.3 or newer is required; you have 0.7.11.None
```

MySQLclient目前只支持到python3.4，因此如果使用的更高版本的python，需要修改如下：

通过查找路径C:\Programs\Python\Python36-32\Lib\site-packages\Django-2.0-py3.6.egg\django\db\backends\mysql
这个路径里的文件把

```
if version < (1, 3, 3):
     raise ImproperlyConfigured("mysqlclient 1.3.3 or newer is required; you have %s" % Database.__version__)
```

注释掉 就OK了。

注意4: 如果想打印orm转换过程中的sql，需要在settings中进行如下配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}

```



## 添加表纪录

### 方式1 

```python
# create方法的返回值book_obj就是插入book表中的python葵花宝典这本书籍纪录对象
 book_obj=Book.objects.create(title="python葵花宝典",state=True,price=100,publish="苹果出版社",pub_date="2012-12-12")
  
```

### 方式2

```python
book_obj=Book(title="python葵花宝典",state=True,price=100,publish="苹果出版社",pub_date="2012-12-12")
book_obj.save()

```



## 查询表纪录

### 查询API

```
<1> all():                  查询所有结果
  
<2> filter(**kwargs):       它包含了与所给筛选条件相匹配的对象
  
<3> get(**kwargs):          返回与所给筛选条件相匹配的对象，返回结果有且只有一个，
                            如果符合筛选条件的对象超过一个或者没有都会抛出错误。
  
<4> exclude(**kwargs):      它包含了与所给筛选条件不匹配的对象
 
<5> order_by(*field):       对查询结果排序
  
<6> reverse():              对查询结果反向排序
  
<8> count():                返回数据库中匹配查询(QuerySet)的对象数量。
  
<9> first():                返回第一条记录
  
<10> last():                返回最后一条记录
  
<11> exists():              如果QuerySet包含数据，就返回True，否则返回False
 
<12> values(*field):        返回一个ValueQuerySet——一个特殊的QuerySet，运行后得到的并不是一系列
                            model的实例化对象，而是一个可迭代的字典序列
<13> values_list(*field):   它与values()非常相似，它返回的是一个元组序列，values返回的是一个字典序列
 
<14> distinct():            从返回结果中剔除重复纪录
```

### 基于双下划线的模糊查询　　

```
Book.objects.filter(price__in=[100,200,300])
Book.objects.filter(price__gt=100)
Book.objects.filter(price__lt=100)
Book.objects.filter(price__range=[100,200])    # range 范围 100 -200 之间
Book.objects.filter(title__contains="python")  # 包含
Book.objects.filter(title__icontains="python") # 包含 不区分大小写
Book.objects.filter(title__startswith="py")    # py开头的
Book.objects.filter(pub_date__year=2012)
Book.objects.filter(pub_date__year=2018,pub_date__month=1,pub_date__day=1) # 过滤年月日
```

## 删除表纪录

删除方法就是 delete()。它运行时立即删除对象而不返回任何值。例如：

```
model_obj.delete()
```

你也可以一次性删除多个对象。每个 QuerySet 都有一个 delete() 方法，它一次性删除 QuerySet 中所有的对象。

例如，下面的代码将删除 pub_date 是2005年的 Entry 对象：

```
Entry.objects.filter(pub_date__year=2005).delete()

```

在 Django 删除对象时，会模仿 SQL 约束 ON DELETE CASCADE 的行为，换句话说，删除一个对象时也会删除与它相关联的外键对象。例如：

```
b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
b.delete()
```

要注意的是： delete() 方法是 QuerySet 上的方法，但并不适用于 Manager 本身。这是一种保护机制，是为了避免意外地调用 Entry.objects.delete() 方法导致 所有的 记录被误删除。如果你确认要删除所有的对象，那么你必须显式地调用：

```
	
Entry.objects.all().delete()　　
```

如果不想级联删除，可以设置为:

```
pubHouse = models.ForeignKey(to='Publisher', on_delete=models.SET_NULL, blank=True, null=True)

```

## 修改表纪录

```
Book.objects.filter(title__startswith="py").update(price=120)

```

此外，update()方法对于任何结果集（QuerySet）均有效，这意味着你可以同时更新多条记录update()方法会返回一个整型数值，表示受影响的记录条数。　　



# 章节作业

### 1 图书管理系统

实现功能：book单表的增删改查

### 2 查询操作练习

```
1 查询老男孩出版社出版过的价格大于200的书籍
 Book.objects.filter(publish__name='老男孩出版社',price__gt = 200)
2 查询2017年8月出版的所有以py开头的书籍名称
 Book.objects.filter(pub_date__year=2017,pub_date__month=7).filter(title__startswith = py)
3 查询价格为50,100或者150的所有书籍名称及其出版社名称
 Book.objects.filter(price__in=[50,100,150]).values(title,Book.publish.name)
4 查询价格在100到200之间的所有书籍名称及其价格
 Book.objects.filter(price__range(100,200)).values(title,price)
5 查询所有人民出版社出版的书籍的价格（从高到低排序，去重）
Book.objects.values(publish__name = '人民出版社').distinct().order_by('-price')
```



# [9 Django 模型层(2)](https://www.cnblogs.com/yuanchenqi/articles/8963244.html)

# 多表操作

## 创建模型

实例：我们来假定下面这些概念，字段和关系

作者模型：一个作者有姓名和年龄。

作者详细模型：把作者的详情放到详情表，包含生日，手机号，家庭住址等信息。作者详情模型和作者模型之间是一对一的关系（one-to-one）

出版商模型：出版商有名称，所在城市以及email。

书籍模型： 书籍有书名和出版日期，一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系就是多对多的关联关系(many-to-many);一本书只应该由一个出版商出版，所以出版商和书籍是一对多关联关系(one-to-many)。

模型建立如下：

```python
from django.db import models

# Create your models here.

# 作者表
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    age=models.IntegerField()

    # 与AuthorDetail建立一对一的关系
    # authorDetail=models.OneToOneField(to="AuthorDetail",on_delete=models.CASCADE)
		# 与AuthorDetail建立一对一的关系  OneToOneField会自动给字段限制unique  
    # 关联是主键nid可不加,django会自动加.  on_delete=models.CASCADE Django2.0之后要加上.
    # on_delete=models.CASCADE,    # 删除关联数据,与之关联也删除
    authorDetail=models.OneToOneField(to="AuthorDetail",to_field="nid", on_delete=models.CASCADE)
    
# 作者详情表
class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday=models.DateField()
    telephone=models.BigIntegerField()
    addr=models.CharField( max_length=64)

# 出版社表
class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)
    email=models.EmailField()


# 图书表
class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)

    # 与Publish建立一对多的关系,外键字段建立在多的一方 #关联出版社表 nid字段  publish生成字段时候会自动生成publish_id
    publish=models.ForeignKey(to="Publish",to_field="nid",on_delete=models.CASCADE)
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表
    authors=models.ManyToManyField(to='Author',)
```

扩展: https://www.django.cn/article/show-6.html   Django2.0外键参数on_delete的使用方法

 生成表如下：

<img src="assets2.0/877318-20180501223306119-1804705285.png" alt="img" style="zoom: 67%;" />

<img src="assets2.0/877318-20180501223412676-377958198.png" alt="img" style="zoom:67%;" />

<img src="assets2.0/877318-20180501223511240-492522724.png" alt="img" style="zoom:67%;" />

<img src="assets2.0/877318-20180501223620025-185160553.png" alt="img" style="zoom:67%;" />

<img src="assets2.0/877318-20180501223701796-763894415.png" alt="img" style="zoom:67%;" />

 

注意事项：

-    表的名称`myapp_modelName`，是根据 模型中的元数据自动生成的，也可以覆写为别的名称　　
-   ` id` 字段是自动添加的
-    对于外键字段，Django 会在字段名上添加`"_id"` 来创建数据库中的列名
-    这个例子中的`CREATE TABLE` SQL 语句使用PostgreSQL 语法格式，要注意的是Django 会根据settings 中指定的数据库类型来使用相应的SQL 语句。
-    定义好模型之后，你需要告诉Django _使用_这些模型。你要做的就是修改配置文件中的INSTALL_APPSZ中设置，在其中添加`models.py`所在应用的名称。
-   外键字段 ForeignKey 有一个 null=True 的设置(它允许外键接受空值 NULL)，你可以赋给它空值 None 。

```
小笔记:
一旦确定一对多关系:  建立一对多的关系----> 在多的表中建立关联字段
一旦确定多对多关系:  建立多对多的关系----> 创建第三张表(关联表)  id 和 两个关联字段
一旦确定一对一关系:  建立一对一的关系----> 在两张表中任意一张表中建立关联字段+Unique

建关联字段是为了查询, 外键约束是为了避免产生脏数据
 
```



## 添加表纪录 

操作前先简单的录入一些数据：

publish表：

![img](assets2.0/877318-20180501231939514-1159349232.png)

author表：

![img](assets2.0/877318-20180501232010534-1683544746.png)

authordetail表:

![img](assets2.0/877318-20180501232217201-492441826.png)

### 一对多

```
方式1:
   publish_obj=Publish.objects.get(nid=1)
   book_obj=Book.objects.create(title="金瓶眉",publishDate="2012-12-12",price=100,publish=publish_obj)
  
方式2:
   book_obj=Book.objects.create(title="金瓶眉",publishDate="2012-12-12",price=100,publish_id=1)　　
```

![img](assets2.0/877318-20180501231012070-1410608284.png)

核心：book_obj.publish与book_obj.publish_id是什么？ 

### 多对多



```
# 当前生成的书籍对象
book_obj=Book.objects.create(title="追风筝的人",price=200,publishDate="2012-11-12",publish_id=1)
# 为书籍绑定的做作者对象
yuan=Author.objects.filter(name="yuan").first() # 在Author表中主键为2的纪录
egon=Author.objects.filter(name="alex").first() # 在Author表中主键为1的纪录

# 绑定多对多关系,即向关系表book_authors中添加纪录
book_obj.authors.add(yuan,egon)    #  将某些特定的 model 对象添加到被关联对象集合中。   ======= book_obj.authors.add(*[])
```



数据库表纪录生成如下：

book表 

![img](assets2.0/877318-20180501233728425-1500453543.png)

book_authors表

![img](assets2.0/877318-20180501233939850-1362764638.png)

核心:book_obj.authors.all()是什么？

多对多关系其它常用API：

```
book_obj.authors.remove()      # 将某个特定的对象从被关联对象集合中去除。 ======   book_obj.authors.remove(*[])
book_obj.authors.clear()       #清空被关联对象集合
book_obj.authors.set()         #先清空再设置　　
```

[more](http://www.cnblogs.com/yuanchenqi/articles/8978167.html)

## 基于对象的跨表查询

### 一对多查询（Publish 与 Book）

正向查询(按字段：publish)：

```
# 查询主键为1的书籍的出版社所在的城市
book_obj=Book.objects.filter(pk=1).first()
# book_obj.publish 是主键为1的书籍对象关联的出版社对象
print(book_obj.publish.city) 　
```

反向查询(按表名：book_set)：

```
publish=Publish.objects.get(name="苹果出版社")
#publish.book_set.all() : 与苹果出版社关联的所有书籍对象集合   按表名小写 book_set.all()
book_list=publish.book_set.all()    
for book_obj in book_list:
       print(book_obj.title)
```

### 一对一查询(Author 与 AuthorDetail)

正向查询(按字段：authorDetail)：

```
egon=Author.objects.filter(name="egon").first()
print(egon.authorDetail.telephone)
```

反向查询(按表名：author)：

```
# 查询所有住址在北京的作者的姓名
 
authorDetail_list=AuthorDetail.objects.filter(addr="beijing")
for obj in authorDetail_list:
     print(obj.author.name)
```

### 多对多查询 (Author 与 Book)

正向查询(按字段：authors)：

```
# 金瓶眉所有作者的名字以及手机号
 
book_obj=Book.objects.filter(title="金瓶眉").first()
authors=book_obj.authors.all()
for author_obj in authors:
     print(author_obj.name,author_obj.authorDetail.telephone)
```

反向查询(按表名：book_set)：

```
# 查询egon出过的所有书籍的名字
 
 author_obj=Author.objects.get(name="egon")
 book_list=author_obj.book_set.all()        #与egon作者相关的所有书籍
 for book_obj in book_list:
     print(book_obj.title)
```

**注意：**

你可以通过在 ForeignKey() 和ManyToManyField的定义中设置 related_name 的值来覆写 FOO_set 的名称。例如，如果 Article model 中做一下更改：

```
publish = ForeignKey(Book, related_name='bookList')
```

那么接下来就会如我们看到这般：

```
# 查询 人民出版社出版过的所有书籍
 
publish=Publish.objects.get(name="人民出版社")
book_list=publish.bookList.all()  # 与人民出版社关联的所有书籍对象集合
```

## 基于双下划线的跨表查询 

Django 还提供了一种直观而高效的方式在查询(lookups)中表示关联关系，它能自动确认 SQL JOIN 联系。要做跨关系查询，就使用两个下划线来链接模型(model)间关联字段的名称，直到最终链接到你想要的model 为止。

 

```
'''
    正向查询按字段,反向查询按表名小写用来告诉ORM引擎join哪张表
'''
```

### 一对多查询



```
# 练习:  查询苹果出版社出版过的所有书籍的名字与价格(一对多)

    # 正向查询 按字段:publish

    queryResult=Book.objects
　　　　　　　　　　　　.filter(publish__name="苹果出版社")
　　　　　　　　　　　　.values_list("title","price")

    # 反向查询 按表名:book

    queryResult=Publish.objects
　　　　　　　　　　　　　　.filter(name="苹果出版社")
　　　　　　　　　　　　　　.values_list("book__title","book__price")
```



### 多对多查询　　



```
# 练习: 查询alex出过的所有书籍的名字(多对多)

    # 正向查询 按字段:authors:
    queryResult=Book.objects
　　　　　　　　　　　　.filter(authors__name="yuan")
　　　　　　　　　　　　.values_list("title")

    # 反向查询 按表名:book
    queryResult=Author.objects
　　　　　　　　　　　　　　.filter(name="yuan")
　　　　　　　　　　　　　　.values_list("book__title","book__price")
```



### 一对一查询



```
    # 查询alex的手机号
    
    # 正向查询
    ret=Author.objects.filter(name="alex").values("authordetail__telephone")

    # 反向查询
    ret=AuthorDetail.objects.filter(author__name="alex").values("telephone")
```



### 进阶练习(连续跨表)



```
# 练习: 查询人民出版社出版过的所有书籍的名字以及作者的姓名


    # 正向查询
    queryResult=Book.objects
　　　　　　　　　　　　.filter(publish__name="人民出版社")
　　　　　　　　　　　　.values_list("title","authors__name")
    # 反向查询
    queryResult=Publish.objects
　　　　　　　　　　　　　　.filter(name="人民出版社")
　　　　　　　　　　　　　　.values_list("book__title","book__authors__age","book__authors__name")


# 练习: 手机号以151开头的作者出版过的所有书籍名称以及出版社名称


    # 方式1:
    queryResult=Book.objects
　　　　　　　　　　　　.filter(authors__authorDetail__telephone__regex="151")
　　　　　　　　　　　　.values_list("title","publish__name")
    # 方式2:    
    ret=Author.objects
              .filter(authordetail__telephone__startswith="151")
              .values("book__title","book__publish__name")
```



### related_name

反向查询时，如果定义了related_name ，则用related_name替换表名，例如：

```
publish = ForeignKey(Blog, related_name='bookList')
```



```
# 练习: 查询人民出版社出版过的所有书籍的名字与价格(一对多)

# 反向查询 不再按表名:book,而是related_name:bookList


    queryResult=Publish.objects
　　　　　　　　　　　　　　.filter(name="人民出版社")
　　　　　　　　　　　　　　.values_list("bookList__title","bookList__price") 
```



## 聚合查询与分组查询

### `聚合`

`aggregate`(*args, **kwargs)

```
# 计算所有图书的平均价格
    >>> from django.db.models import Avg
    >>> Book.objects.all().aggregate(Avg('price'))
    {'price__avg': 34.35}
```

`aggregate()`是`QuerySet` 的一个终止子句，意思是说，它返回一个包含一些键值对的字典。键的名称是聚合值的标识符，值是计算出来的聚合值。键的名称是按照字段和聚合函数的名称自动生成出来的。如果你想要为聚合值指定一个名称，可以向聚合子句提供它。

```
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}
```

如果你希望生成不止一个聚合，你可以向`aggregate()`子句中添加另一个参数。所以，如果你也想知道所有图书价格的最大值和最小值，可以这样查询：

```
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}
```

### 分组

```
###################################－－单表分组查询－－#######################################################

查询每一个部门名称以及对应的员工数

emp:

id  name age   salary    dep
1   alex  12   2000     销售部
2   egon  22   3000     人事部
3   wen   22   5000     人事部


sql语句:
select dep,Count(*) from emp group by dep;

ORM:
emp.objects.values("dep").annotate(c=Count("id")

###################################－－多表分组查询－－###########################


多表分组查询：

查询每一个部门名称以及对应的员工数


emp:

id  name age   salary   dep_id
1   alex  12   2000       1
2   egon  22   3000       2
3   wen   22   5000       2


dep

id   name 
1    销售部
2    人事部



emp－dep:

id  name age   salary   dep_id   id   name 
1   alex  12   2000       1      1    销售部
2   egon  22   3000       2      2    人事部
3   wen   22   5000       2      2    人事部


sql语句:
select dep.name,Count(*) from emp left join dep on emp.dep_id=dep.id group by dep.id

ORM:
dep.objetcs.values("id").annotate(c=Count("emp")).values("name","c")
```



```
class Emp(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    salary=models.DecimalField(max_digits=8,decimal_places=2)
    dep=models.CharField(max_length=32)
    province=models.CharField(max_length=32)
```



annotate()为调用的`QuerySet`中每一个对象都生成一个独立的统计值（统计方法用聚合函数）。

总结 ：跨表分组查询本质就是将关联表join成一张表，再按单表的思路进行分组查询。　

### 查询练习

(1) 练习：统计每一个出版社的最便宜的书

```
publishList=Publish.objects.annotate(MinPrice=Min("book__price"))
for publish_obj in publishList:
    print(publish_obj.name,publish_obj.MinPrice)
```

annotate的返回值是querySet，如果不想遍历对象，可以用上valuelist：

```
queryResult= Publish.objects
　　　　　　　　　　　　.annotate(MinPrice=Min("book__price"))
　　　　　　　　　　　　.values_list("name","MinPrice")
print(queryResult)
```



```
'''

SELECT "app01_publish"."name", MIN("app01_book"."price")  AS "MinPrice" FROM "app01_publish" 
LEFT  JOIN "app01_book" ON ("app01_publish"."nid" = "app01_book"."publish_id") 
GROUP BY "app01_publish"."nid", "app01_publish"."name", "app01_publish"."city", "app01_publish"."email" 

'''
```



(2) 练习：统计每一本书的作者个数

```
ret = Book.objects.annotate(authorsNum=Count("authors__name")).values("title","authorsNum")
```

(3) 统计每一本以py开头的书籍的作者个数：

```
 queryResult=Book.objects.filter(title__startswith="Py").annotate(num_authors=Count('authors'))
　　　　　　　　　 　
ret = Book.objects.filter(title__startswith="py").annotate(authorSnum=Count("authors__name")).values_list("title","authorSnum")

```

(4) 统计不止一个作者的图书：

```
queryResult=Book.objects
　　　　　　　　　　.annotate(num_authors=Count('authors'))
　　　　　　　　　　.filter(num_authors__gt=1)
```

(5) 根据一本图书作者数量的多少对查询集 `QuerySet`进行排序:

```
Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')

```

(6) 查询各个作者出的书的总价格:

```
#   按author表的所有字段 group by
    queryResult=Author.objects
　　　　　　　　　　　　　　.annotate(SumPrice=Sum("book__price"))
　　　　　　　　　　　　　　.values_list("name","SumPrice")
    print(queryResult)
```

## F查询与Q查询

### F查询

在上面所有的例子中，我们构造的过滤器都只是将字段值与某个常量做比较。如果我们要对两个字段的值做比较，那该怎么做呢？

Django 提供 F() 来做这样的比较。F() 的实例可以在查询中引用字段，来比较同一个 model 实例中两个不同字段的值。

```
# 查询评论数大于收藏数的书籍

from django.db.models import F
Book.objects.filter(commnetNum__lt=F('keepNum'))

```

Django 支持 F() 对象之间以及 F() 对象和常数之间的加减乘除和取模的操作。

```
# 查询评论数大于收藏数2倍的书籍
    Book.objects.filter(commnetNum__lt=F('keepNum')*2)
```

修改操作也可以使用F函数,比如将每一本书的价格提高30元：

```
Book.objects.all().update(price=F("price")+30)　
```

```
数据准备:
直接在models.py  book 类中添加两个字段
comment_sum = models.IntegerField(default=0)
read_sum  = models.IntegerField(default=0)

kanghuadeMacBook-Pro:08-ORM2 kanghua$  python3.9 manage.py makemigrations
kanghuadeMacBook-Pro:08-ORM2 kanghua$ python3.9 manage.py migrate

```

### Q查询

`filter()` 等方法中的关键字参数查询都是一起进行“AND” 的。 如果你需要执行更复杂的查询（例如`OR` 语句），你可以使用`Q 对象`。

```
from django.db.models import Q
Q(title__startswith='Py')
```

`Q` 对象可以使用`&` 和`|` 操作符组合起来。当一个操作符在两个`Q` 对象上使用时，它产生一个新的`Q` 对象。

```
	
bookList=Book.objects.filter(Q(authors__name="yuan")|Q(authors__name="egon"))
```

等同于下面的SQL `WHERE` 子句：

```
	
WHERE name ="yuan" OR name ="egon"
```

你可以组合`&` 和`|` 操作符以及使用括号进行分组来编写任意复杂的`Q` 对象。同时，`Q` 对象可以使用`~` 操作符取反，这允许组合正常的查询和取反(`NOT`) 查询：

```
bookList=Book.objects.filter(Q(authors__name="yuan") & ~Q(publishDate__year=2017)).values_list("title")

```

查询函数可以混合使用`Q 对象`和关键字参数。所有提供给查询函数的参数（关键字参数或`Q` 对象）都将"AND”在一起。但是，如果出现`Q` 对象，它必须位于所有关键字参数的前面。例如：

```
bookList=Book.objects.filter(Q(publishDate__year=2016) | Q(publishDate__year=2017), title__icontains="python" )
                             
```



# [9-1 关联管理器(RelatedManager)](https://www.cnblogs.com/yuanchenqi/articles/8978167.html)

# class RelatedManager

"关联管理器"是在一对多或者多对多的关联上下文中使用的管理器。它存在于下面两种情况：

ForeignKey关系的“另一边”。像这样：

```
from django.db import models
 
class Reporter(models.Model):
    # ...
    pass
 
class Article(models.Model):
    reporter = models.ForeignKey(Reporter)
```

在上面的例子中，管理器reporter.article_set拥有下面的方法。

ManyToManyField关系的两边：

```
class Topping(models.Model):
    # ...
    pass
 
class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
```

这个例子中，topping.pizza_set 和pizza.toppings都拥有下面的方法。

**add(obj1[, obj2, ...])**

```
把指定的模型对象添加到关联对象集中。

例如：

>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.add(e)    # Associates Entry e with Blog b.
在上面的例子中，对于ForeignKey关系，e.save()由关联管理器调用，执行更新操作。然而，在多对多关系中使用add()并不会调用任何 save()方法，而是由QuerySet.bulk_create()创建关系。

延伸：

# 1 *[]的使用
>>> book_obj = Book.objects.get(id=1)
>>> author_list = Author.objects.filter(id__gt=2)
>>> book_obj.authors.add(*author_list)


# 2 直接绑定主键
book_obj.authors.add(*[1,3])  # 将id=1和id=3的作者对象添加到这本书的作者集合中
                              # 应用: 添加或者编辑时,提交作者信息时可以用到.  
```

**create(\**kwargs)**

```
创建一个新的对象，保存对象，并将它添加到关联对象集之中。返回新创建的对象：

>>> b = Blog.objects.get(id=1)
>>> e = b.entry_set.create(
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )

# No need to call e.save() at this point -- it's already been saved.
这完全等价于（不过更加简洁于）：

>>> b = Blog.objects.get(id=1)
>>> e = Entry(
...     blog=b,
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )
>>> e.save(force_insert=True)
要注意我们并不需要指定模型中用于定义关系的关键词参数。在上面的例子中，我们并没有传入blog参数给create()。Django会明白新的 Entry对象blog 应该添加到b中。

```



**remove(obj1[, obj2, ...])**

```
从关联对象集中移除执行的模型对象：

>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.remove(e) # Disassociates Entry e from Blog b.
对于ForeignKey对象，这个方法仅在null=True时存在。
```

**clear()**

```
从关联对象集中移除一切对象。

>>> b = Blog.objects.get(id=1)
>>> b.entry_set.clear()
注意这样不会删除对象 —— 只会删除他们之间的关联。

就像 remove() 方法一样，clear()只能在 null=True的ForeignKey上被调用。
```

**set()方法**

先清空，在设置，编辑书籍时即可用到

![img](assets2.0/877318-20171119170926484-683145874.png)

**注意**

对于所有类型的关联字段，add()、create()、remove()和clear(),set()都会马上更新数据库。换句话说，在关联的任何一端，都不需要再调用save()方法。

**直接赋值：**

通过赋值一个新的可迭代的对象，关联对象集可以被整体替换掉。

```
>>> new_list = [obj1, obj2, obj3]
>>> e.related_set = new_list
```

如果外键关系满足null=True，关联管理器会在添加new_list中的内容之前，首先调用clear()方法来解除关联集中一切已存在对象的关联。否则， new_list中的对象会在已存在的关联的基础上被添加。　　



```python
报错记录:
#报错环境  python3.9.4  django2.2  PyMySQL1.0.2  mysql 5.7.31
#数据迁移时候
python3.9 manage.py makemigrations 
AttributeError: 'str' object has no attribute 'decode'

# 修改django 源码
/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/django/db/backends/mysql/operations.py

#140行
def last_executed_query(self, cursor, sql, params):
# With MySQLdb, cursor objects have an (undocumented) "_executed"
# attribute where the exact query sent to the database is saved.
# See MySQLdb/cursors.py in the source distribution.
query = getattr(cursor, '_executed', None)
# 修改前的源码
# if query is not None:
#     # query = query.decode(errors='replace')
#     query = query.encode(errors='replace') # 或者把上一行注释掉 用这一行也可以解决
# return query
# 修改后的源码
from django.utils.encoding import force_str  # 只需要将这个导入，放到该模块的最上面即可
return force_str(query, errors='replace')

更多报错 参考 https://www.cnblogs.com/Neeo/articles/14036364.html
```





# [10 Django与Ajax](https://www.cnblogs.com/yuanchenqi/articles/9070966.html)

# Ajax

## Ajax简介

AJAX（Asynchronous Javascript And XML）翻译成中文就是“异步Javascript和XML”。即使用Javascript语言与服务器进行异步交互，传输的数据为XML（当然，传输的数据不只是XML,现在更多使用json数据）。

-   同步交互：客户端发出一个请求后，需要等待服务器响应结束后，才能发出第二个请求；
-   异步交互：客户端发出一个请求后，无需等待服务器响应结束，就可以发出第二个请求。

AJAX除了**异步**的特点外，还有一个就是：浏览器页面**局部刷新**；（这一特点给用户的感受是在不知不觉中完成请求和响应过程）

场景：

<img src="assets2.0/877318-20180522104832588-1949287384.png" alt="img" style="zoom:50%;" />

#### 优点：

-   AJAX使用Javascript技术向服务器发送异步请求
-   AJAX无须刷新整个页面

## 基于jquery的Ajax实现



```js
<button class="send_Ajax">send_Ajax</button>
<script>

       $(".send_Ajax").click(function(){
					 //	发送ajax请求
           $.ajax({
               url:"/handle_Ajax/",  // 请求url
               type:"POST",          // 请求方式post
               data:{username:"Yuan",password:123},  //发送数据
               success:function(data){    // 回调函数
                   console.log(data)
               },
         　　　　　　
               error: function (jqXHR, textStatus, err) {
                        console.log(arguments);
                    },

               complete: function (jqXHR, textStatus) {
                        console.log(textStatus);
                },

               statusCode: {
                    '403': function (jqXHR, textStatus, err) {
                          console.log(arguments);
                     },

                    '400': function (jqXHR, textStatus, err) {
                        console.log(arguments);
                    }
                }

           })

       })
// 更多参考 https://blog.csdn.net/zhbitxhd/article/details/9946799
</script>

```



### Ajax－服务器－Ajax流程图

![image-20211022103615555](assets2.0/image-20211022103615555.png)

## 案例

### 1 用户名是否已被注册

在注册表单中，当用户填写了用户名后，把光标移开后，会自动向服务器发送异步请求。服务器返回true或false，返回true表示这个用户名已经被注册过，返回false表示没有注册过。客户端得到服务器返回的结果后，确定是否在用户名文本框后显示“用户名已被注册”的错误信息！

### 2 基于Ajax进行登录验证 

用户在表单输入用户名与密码，通过Ajax提交给服务器，服务器验证后返回响应信息，客户端通过响应信息确定是否登录成功，成功，则跳转到首页，否则，在页面上显示相应的错误信息。

<img src="assets2.0/877318-20180522163641613-684273794.png" alt="img" style="zoom:67%;" />



# 文件上传

## 请求头ContentType

ContentType指的是请求体的编码类型，常见的类型共有3种：

### 1 application/x-www-form-urlencoded

这应该是最常见的 POST 提交数据的方式了。浏览器的原生 <form> 表单，如果不设置 `enctype` 属性，那么最终就会以 application/x-www-form-urlencoded 方式提交数据。请求类似于下面这样（无关的请求头在本文中都省略掉了）：

```
POST http://www.example.com HTTP/1.1
Content-Type: application/x-www-form-urlencoded;charset=utf-8

user=yuan&age=22
```

### 2 multipart/form-data

这又是一个常见的 POST 数据提交的方式。我们使用表单上传文件时，必须让 <form> 表单的 `enctype` 等于 multipart/form-data。直接来看一个请求示例：



```
POST http://www.example.com HTTP/1.1
Content-Type:multipart/form-data; boundary=----WebKitFormBoundaryrGKCBY7qhFd3TrwA

------WebKitFormBoundaryrGKCBY7qhFd3TrwA
Content-Disposition: form-data; name="user"

yuan
------WebKitFormBoundaryrGKCBY7qhFd3TrwA
Content-Disposition: form-data; name="file"; filename="chrome.png"
Content-Type: image/png

PNG ... content of chrome.png ...
------WebKitFormBoundaryrGKCBY7qhFd3TrwA--
```



这个例子稍微复杂点。首先生成了一个 boundary 用于分割不同的字段，为了避免与正文内容重复，boundary 很长很复杂。然后 Content-Type 里指明了数据是以 multipart/form-data 来编码，本次请求的 boundary 是什么内容。消息主体里按照字段个数又分为多个结构类似的部分，每部分都是以 `--boundary` 开始，紧接着是内容描述信息，然后是回车，最后是字段具体内容（文本或二进制）。如果传输的是文件，还要包含文件名和文件类型信息。消息主体最后以 `--boundary--` 标示结束。关于 multipart/form-data 的详细定义，请前往 [rfc1867](http://www.ietf.org/rfc/rfc1867.txt) 查看。

这种方式一般用来上传文件，各大服务端语言对它也有着良好的支持。

上面提到的这两种 POST 数据的方式，都是浏览器原生支持的，而且现阶段标准中原生 <form> 表单也[只支持这两种方式](http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4)（通过 <form> 元素的 `enctype` 属性指定，默认为 `application/x-www-form-urlencoded`。其实 `enctype` 还支持 `text/plain`，不过用得非常少）。

随着越来越多的 Web 站点，尤其是 WebApp，全部使用 Ajax 进行数据交互之后，我们完全可以定义新的数据提交方式，给开发带来更多便利。

### 3 application/json

application/json 这个 Content-Type 作为响应头大家肯定不陌生。实际上，现在越来越多的人把它作为请求头，用来告诉服务端消息主体是序列化后的 JSON 字符串。由于 JSON 规范的流行，除了低版本 IE 之外的各大浏览器都原生支持 JSON.stringify，服务端语言也都有处理 JSON 的函数，使用 JSON 不会遇上什么麻烦。

JSON 格式支持比键值对复杂得多的结构化数据，这一点也很有用。记得我几年前做一个项目时，需要提交的数据层次非常深，我就是把数据 JSON 序列化之后来提交的。不过当时我是把 JSON 字符串作为 val，仍然放在键值对里，以 x-www-form-urlencoded 方式提交。

## 基于form表单的文件上传 

### 模板部分

```
<form action="" method="post" enctype="multipart/form-data">
      用户名 <input type="text" name="user">
      头像 <input type="file" name="avatar">
    <input type="submit">
</form>
```

### 视图部分

```
def index(request):
    print(request.body)   # 原始的请求体数据
    print(request.GET)    # GET请求数据
    print(request.POST)   # POST请求数据
    print(request.FILES)  # 上传的文件数据


    return render(request,"index.html")
```

## 基于Ajax的文件上传

### 模板

```js
<form>
      用户名 <input type="text" id="user">
      头像 <input type="file" id="avatar">
     <input type="button" id="ajax-submit" value="ajax-submit">
</form>

<script>

    $("#ajax-submit").click(function(){
        var formdata=new FormData();
        formdata.append("user",$("#user").val());
        formdata.append("avatar_img",$("#avatar")[0].files[0]);
        $.ajax({

            url:"",
            type:"post",
            data:formdata,
            processData: false ,    // 不处理数据
            contentType: false,    // 不设置内容类型

            success:function(data){
                console.log(data)
            }
        })

    })

</script>
```



### 视图

```
def index(request):

    if request.is_ajax():

        print(request.body)   # 原始的请求体数据
        print(request.GET)    # GET请求数据
        print(request.POST)   # POST请求数据
        print(request.FILES)  # 上传的文件数据

        return HttpResponse("ok")


    return render(request,"index.html")
```



检查浏览器的请求头：

```
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryaWl9k5ZMiTAzx3FT
```

```
小笔记:
这里先把 django 的 csrf_token功能关闭
settings.py 文件  注释 MIDDLEWARE=[] 里
# 'django.middleware.csrf.CsrfViewMiddleware',


```



# [11 Django组件-分页器](https://www.cnblogs.com/yuanchenqi/articles/9036515.html)

## Django的分页器（paginator）

### view

```python
from django.shortcuts import render,HttpResponse

# Create your views here.
from app01.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    '''
    批量导入数据:
    Booklist=[]
    for i in range(100):
        Booklist.append(Book(title="book"+str(i),price=30+i*i))
    Book.objects.bulk_create(Booklist)
    '''

    '''
分页器的使用:
    book_list=Book.objects.all()

    paginator = Paginator(book_list, 10)  # 10表示每页显示数

    print("count:",paginator.count)           #数据总数
    print("num_pages",paginator.num_pages)    #总页数
    print("page_range",paginator.page_range)  #页码的列表

    page1=paginator.page(1) #第1页的page对象
    for i in page1:         #遍历第1页的所有数据对象
        print(i)

    print(page1.object_list) #第1页的所有数据

    page2=paginator.page(2)

    print(page2.has_next())            #是否有下一页
    print(page2.next_page_number())    #下一页的页码
    print(page2.has_previous())        #是否有上一页
    print(page2.previous_page_number()) #上一页的页码

    # 抛错
    #page=paginator.page(12)   # error:EmptyPage

    #page=paginator.page("z")   # error:PageNotAnInteger

    '''

    book_list=Book.objects.all()

    paginator = Paginator(book_list, 10)
    page = request.GET.get('page',1)  # 获取浏览传过来的参数page的值,如果没有默认1
    currentPage=int(page)

    try:
        print(page)
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    return render(request,"index.html",{"book_list":book_list,"paginator":paginator,"currentPage":currentPage})
  
  
```



### index.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" 
    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<div class="container">
    <h4>分页器</h4>
    <ul>
        {% for book in book_list %}
             <li>{{ book.title }} -----{{ book.price }}</li>
        {% endfor %}
     </ul>
    <ul class="pagination" id="pager">
                 {% if book_list.has_previous %}  <!-- 判断是否有下一页 -->
                    <li class="previous"><a href="/index/?page={{ book_list.previous_page_number }}">上一页</a></li>
                 {% else %}
                    <li class="previous disabled"><a href="#">上一页</a></li>
                 {% endif %}

                 {% for num in paginator.page_range %}
                     {% if num == currentPage %}
                       <li class="item active"><a href="/index/?page={{ num }}">{{ num }}</a></li>
                     {% else %}
                       <li class="item"><a href="/index/?page={{ num }}">{{ num }}</a></li>

                     {% endif %}
                 {% endfor %}

                 {% if book_list.has_next %}
                    <li class="next"><a href="/index/?page={{ book_list.next_page_number }}">下一页</a></li>
                 {% else %}
                    <li class="next disabled"><a href="#">下一页</a></li>
                 {% endif %}
            </ul>
</div>

</body>
</html>
```



## 扩展

```python
def index(request):

    book_list=Book.objects.all()
    paginator = Paginator(book_list, 15)
    page = request.GET.get('page',1)
    currentPage=int(page)

    #  页数过多时候, 页数始终保持10页显示
    if paginator.num_pages>11:
        if currentPage-5<1:
            pageRange=range(1,11)
        elif currentPage+5>paginator.num_pages:
            pageRange=range(currentPage-5,paginator.num_pages+1)
        else:
            pageRange=range(currentPage-5,currentPage+5)
    else:
        pageRange=paginator.page_range    # 低于10页的显示

    try:
        print(page)
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    return render(request,"index.html",locals())
  
```



# [12 Django组件-forms组件](https://www.cnblogs.com/yuanchenqi/articles/9036474.html)		

# forms组件

## 校验字段功能

针对一个实例：注册用户讲解。

模型：models.py

```python
class UserInfo(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    email=models.EmailField()
    tel=models.CharField(max_length=32)
```

模板: register.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

</head>
<body>

<form action="" method="post">
    {% csrf_token %}
    <div>
        <label for="user">用户名</label>
        <p><input type="text" name="name" id="name"></p>
    </div>
    <div>
        <label for="pwd">密码</label>
        <p><input type="password" name="pwd" id="pwd"></p>
    </div>
    <div>
        <label for="r_pwd">确认密码</label>
        <p><input type="password" name="r_pwd" id="r_pwd"></p>
    </div>
     <div>
        <label for="email">邮箱</label>
        <p><input type="text" name="email" id="email"></p>
    </div>
    <input type="submit">
</form>

</body>
</html>
```



视图函数：register

```python
# forms组件
from django.forms import widgets

wid_01=widgets.TextInput(attrs={"class":"form-control"})
wid_02=widgets.PasswordInput(attrs={"class":"form-control"})

class UserForm(forms.Form): #继承forms类
    name=forms.CharField(max_length=32,widget=wid_01)  # name是字符串最长32
    pwd=forms.CharField(max_length=32,widget=wid_02)
    r_pwd=forms.CharField(max_length=32,widget=wid_02)
    email=forms.EmailField(widget=wid_01)
    tel=forms.CharField(max_length=32,widget=wid_01)

def register(request):
    if request.method=="POST":
        form=UserForm(request.POST)  # 接收的所有值交给UserForm
        if form.is_valid():    # 所有校验的规则都对才返回True
            print(form.cleaned_data)       # 所有干净的字段以及对应的值
        else:
            print(form.cleaned_data)       #
            print(form.errors)             # ErrorDict : {"校验错误的字段":["错误信息",]}
            print(form.errors.get("name")) # ErrorList ["错误信息",]
        return HttpResponse("OK")
    form=UserForm()
    return render(request,"register.html",locals())
```



## 渲染标签功能 

### 渲染方式1

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
   <!-- 最新版本的 Bootstrap 核心 CSS 文件 -->
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
<h3>注册页面</h3>
<div class="container">
    <div class="row">
        <div class="col-md-6 col-lg-offset-3">
                <form action="" method="post">
                    {% csrf_token %}
                    <div>
                        <label for="">用户名</label>
                        {{ form.name }}
                    </div>
                    <div>
                        <label for="">密码</label>
                        {{ form.pwd }}
                    </div>
                    <div>
                        <label for="">确认密码</label>
                        {{ form.r_pwd }}
                    </div>
                    <div>
                        <label for=""> 邮箱</label>
                        {{ form.email }}
                    </div>
                    <input type="submit" class="btn btn-default pull-right">
                </form>
        </div>
    </div>
</div>

</body>
</html>
```



### 渲染方式2

```html
<form action="" method="post">
                    {% csrf_token %}    
                    {% for field in form %}
                        <div>
                            <label for="">{{ field.label }}</label>
                            {{ field }}
                        </div>
                    {% endfor %}
                    <input type="submit" class="btn btn-default pull-right">              
</form>
```



### 渲染方式3

```html
<form action="" method="post">
    {% csrf_token %}    
    {{ form.as_p }}
    <input type="submit" class="btn btn-default pull-right">
</form>
```



## 显示错误与重置输入信息功能

### 视图

```python
def register(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)       # 所有干净的字段以及对应的值
        else:
            print(form.cleaned_data)       #
            print(form.errors)             # ErrorDict : {"校验错误的字段":["错误信息",]}
            print(form.errors.get("name")) # ErrorList ["错误信息",]
        return render(request,"register.html",locals())
    form=UserForm()
    return render(request,"register.html",locals())
```



### 模板

```python
<form action="" method="post" novalidate>
    {% csrf_token %}
    {% for field in form %}
        <div>
            <label for="">{{ field.label }}</label>
            {{ field }} <span class="pull-right" style="color: red">{{ field.errors.0 }}</span>
        </div>
    {% endfor %}
    <input type="submit" class="btn btn-default">
</form>
```



## 局部钩子与全局钩子

### 模板

```python
# forms组件
from django.forms import widgets

wid_01=widgets.TextInput(attrs={"class":"form-control"})
wid_02=widgets.PasswordInput(attrs={"class":"form-control"})

from django.core.exceptions import ValidationError
class UserForm(forms.Form):
    name=forms.CharField(max_length=32,
                         widget=wid_01
                         )
    pwd=forms.CharField(max_length=32,widget=wid_02)
    r_pwd=forms.CharField(max_length=32,widget=wid_02)
    email=forms.EmailField(widget=wid_01)
    tel=forms.CharField(max_length=32,widget=wid_01)

    # 局部钩子
    def clean_name(self):
        val=self.cleaned_data.get("name")
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字!")

    # 全局钩子

    def clean(self):
        pwd=self.cleaned_data.get("pwd")
        r_pwd=self.cleaned_data.get("r_pwd")

        if pwd==r_pwd:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致!')

def register(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)       # 所有干净的字段以及对应的值
        else:
            clean_error=form.errors.get("__all__")
        return render(request,"register.html",locals())
    form=UserForm()
    return render(request,"register.html",locals())
```



### 视图

```python
 <form action="" method="post" novalidate>
            {% csrf_token %}

            {% for field in form %}
                <div>
                    <label for="">{{ field.label }}</label>
                    {{ field }}
                    <span class="pull-right" style="color: red">
                          {% if field.label == 'R pwd' %}
                          <span>{{ clean_error.0 }}</span>
                          {% endif %}
                          {{ field.errors.0 }}
                    </span>
                </div>
            {% endfor %}
            <input type="submit" class="btn btn-default">

</form>
```



# [13 Django组件-cookie与session](https://www.cnblogs.com/yuanchenqi/articles/9036467.html)

## 会话跟踪技术 

### 1 什么是会话跟踪技术 

我们需要先了解一下什么是会话！可以把会话理解为客户端与服务器之间的一次会晤，在一次会晤中可能会包含多次请求和响应。例如你给10086打个电话，你就是客户端，而10086服务人员就是服务器了。从双方接通电话那一刻起，会话就开始了，到某一方挂断电话表示会话结束。在通话过程中，你会向10086发出多个请求，那么这多个请求都在一个会话中。 
在JavaWeb中，客户向某一服务器发出第一个请求开始，会话就开始了，直到客户关闭了浏览器会话结束。 

在一个会话的多个请求中共享数据，这就是会话跟踪技术。例如在一个会话中的请求如下：  请求银行主页； 

-   请求登录（请求参数是用户名和密码）；
-   请求转账（请求参数与转账相关的数据）； 
-   请求信誉卡还款（请求参数与还款相关的数据）。 

在这上会话中当前用户信息必须在这个会话中共享的，因为登录的是张三，那么在转账和还款时一定是相对张三的转账和还款！这就说明我们必须在一个会话过程中有共享数据的能力。

### 2 会话路径技术使用Cookie或session完成 

我们知道HTTP协议是无状态协议，也就是说每个请求都是独立的！无法记录前一次请求的状态。但HTTP协议中可以使用Cookie来完成会话跟踪！在Web开发中，使用session来完成会话跟踪，session底层依赖Cookie技术。 

## Cookie概述 

### 什么叫Cookie 

Cookie翻译成中文是小甜点，小饼干的意思。在HTTP中它表示服务器送给客户端浏览器的小甜点。其实Cookie是key-value结构，类似于一个python中的字典。随着服务器端的响应发送给客户端浏览器。然后客户端浏览器会把Cookie保存起来，当下一次再访问服务器时把Cookie再发送给服务器。 Cookie是由服务器创建，然后通过响应发送给客户端的一个键值对。客户端会保存Cookie，并会标注出Cookie的来源（哪个服务器的Cookie）。当客户端向服务器发出请求时会把所有这个服务器Cookie包含在请求中发送给服务器，这样服务器就可以识别客户端了！

![img](assets2.0/877318-20180516192005344-137605378.png)

### Cookie规范 

-    Cookie大小上限为4KB； 
-    一个服务器最多在客户端浏览器上保存20个Cookie； 
-    一个浏览器最多保存300个Cookie； 

上面的数据只是HTTP的Cookie规范，但在浏览器大战的今天，一些浏览器为了打败对手，为了展现自己的能力起见，可能对Cookie规范“扩展”了一些，例如每个Cookie的大小为8KB，最多可保存500个Cookie等！但也不会出现把你硬盘占满的可能！ 
注意，不同浏览器之间是不共享Cookie的。也就是说在你使用IE访问服务器时，服务器会把Cookie发给IE，然后由IE保存起来，当你在使用FireFox访问服务器时，不可能把IE保存的Cookie发送给服务器。

### Cookie与HTTP头 

Cookie是通过HTTP请求和响应头在客户端和服务器端传递的： 

-   Cookie：请求头，客户端发送给服务器端； 
-   格式：Cookie: a=A; b=B; c=C。即多个Cookie用分号离开；  Set-Cookie：响应头，服务器端发送给客户端； 
-   一个Cookie对象一个Set-Cookie： Set-Cookie: a=A Set-Cookie: b=B Set-Cookie: c=C 

### Cookie的覆盖 

 如果服务器端发送重复的Cookie那么会覆盖原有的Cookie，例如客户端的第一个请求服务器端发送的Cookie是：Set-Cookie: a=A；第二请求服务器端发送的是：Set-Cookie: a=AA，那么客户端只留下一个Cookie，即：a=AA。 

### django中的cookie语法

设置cookie：

```
rep = HttpResponse(...) 或 rep ＝ render(request, ...) 或 rep ＝ redirect()
  
rep.set_cookie(key,value,...)
rep.set_signed_cookie(key,value,salt='加密盐',...)　
```

源码：　　

```
'''
class HttpResponseBase:

        def set_cookie(self, key,                 键
        　　　　　　　　　　　　 value='',            值
        　　　　　　　　　　　　 max_age=None,        超长时间 
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　cookie需要延续的时间（以秒为单位）
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　如果参数是\ None`` ，这个cookie会延续到浏览器关闭为止。
        　　　　　　　　　　　　 expires=None,        超长时间
       　　　　　　　　　　　　　　　　　　　　　　　　　　expires默认None ,cookie失效的实际日期/时间。 　　　　　　　　
        　　　　　　　　　　　　 path='/',           Cookie生效的路径，
                                                 浏览器只会把cookie回传给带有该路径的页面，这样可以避免将
                                                 cookie传给站点中的其他的应用。
                                                 / 表示根路径，特殊的：根路径的cookie可以被任何url的页面访问　　　　　　　　　 
                             domain=None,         Cookie生效的域名             
                                                  你可用这个参数来构造一个跨站cookie。
                                                  如， domain=".example.com"
                                                  所构造的cookie对下面这些站点都是可读的：
                                                  www.example.com 、 www2.example.com 
        　　　　　　　　　　　　　　　　　　　　　　　　　和an.other.sub.domain.example.com 。
                                                  如果该参数设置为 None ，cookie只能由设置它的站点读取。
        　　　　　　　　　　　　 secure=False,        如果设置为 True ，浏览器将通过HTTPS来回传cookie。
        　　　　　　　　　　　　 httponly=False       只能http协议传输，无法被JavaScript获取
                                                 （不是绝对，底层抓包可以获取到也可以被覆盖）
        　　　　　　　　　　): pass

'''
```



获取cookie：

```
request.COOKIES　　
```

删除cookie：

```
response.delete_cookie("cookie_key",path="/",domain=name)
```

[jquery操作cookie](http://www.cnblogs.com/yuanchenqi/articles/9048367.html)　

### 练习

案例1:显示上次访问时间。　

案例2:显示上次浏览过的商品。

## session

Session是服务器端技术，利用这个技术，服务器在运行时可以 为每一个用户的浏览器创建一个其独享的session对象，由于 session为用户浏览器独享，所以用户在访问服务器的web资源时 ，可以把各自的数据放在各自的session中，当用户再去访问该服务器中的其它web资源时，其它web资源再从用户各自的session中 取出数据为用户服务。

![img](assets2.0/877318-20180516210726463-1449400075.png)

### django中session语法

```
1、设置Sessions值
          request.session['session_name'] ="admin"
2、获取Sessions值
          session_name = request.session["session_name"]
3、删除Sessions值
          del request.session["session_name"]
4、flush()
     删除当前的会话数据(seesion)并删除会话的Cookie。
     这用于确保前面的会话数据不可以再次被用户的浏览器访问
            
------------------
5、get(key, default=None)  # 参数1 获取值, 参数2获取不到默认值
  
fav_color = request.session.get('fav_color', 'red')
  
6、pop(key)
  
fav_color = request.session.pop('fav_color')
  
7、keys()
  
8、items()
  
9、setdefault()
  
  
10 用户session的随机字符串
        request.session.session_key
   
        # 将所有Session失效日期小于当前日期的数据删除
        request.session.clear_expired()
   
        # 检查 用户session的随机字符串 在数据库中是否
        request.session.exists("session_key")
   
        # 删除当前用户的所有Session数据
        request.session.delete("session_key")
   
        request.session.set_expiry(value)
            * 如果value是个整数，session会在些秒数后失效。
            * 如果value是个datatime或timedelta，session就会在这个时间后失效。
            * 如果value是0,用户关闭浏览器session就会失效。
            * 如果value是None,session会依赖全局session失效策略。
            
```

session配置

```
Django默认支持Session，并且默认是将Session数据存储在数据库中，即：django_session 表中。
   
a. 配置 settings.py
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
    
    SESSION_COOKIE_NAME = "sessionid"    # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
    SESSION_COOKIE_PATH = "/"                        # Session的cookie保存的路径（默认）
    SESSION_COOKIE_DOMAIN = None                     # Session的cookie保存的域名（默认）
    SESSION_COOKIE_SECURE = False                    # 是否Https传输cookie（默认）
    SESSION_COOKIE_HTTPONLY = True                   # 是否Session的cookie只支持http传输（默认）
    SESSION_COOKIE_AGE = 1209600                     # Session的cookie失效日期（2周）（默认）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False          # 是否关闭浏览器使得Session过期（默认）
    SESSION_SAVE_EVERY_REQUEST = False               # 是否每次请求都保存Session，默认修改之后才保存（默认）
    
```

### 练习

1 登录案例 

```
需要的页面： 
#login.html：登录页面，提供登录表单； 
#index1.html：主页，显示当前用户名称，如果没有登录，显示您还没登录；
#index2.html：主页，显示当前用户名称，如果没有登录，显示您还没登录；
```

思考，如果第二个人再次再同一个浏览器上登录，django-session表会怎样？

2 验证码案例

验证码可以去识别发出请求的是人还是程序！当然，如果聪明的程序可以去分析验证码图片！但分析图片也不是一件容易的事，因为一般验证码图片都会带有干扰线，人都看不清，那么程序一定分析不出来。

 

# [13-1 jquery操作cookie](https://www.cnblogs.com/yuanchenqi/articles/9048367.html)	

cookie

定义：让网站服务器把少量数据储存到客户端的硬盘或内存，从客户端的硬盘读取数据的一种技术；

下载与引入:jquery.cookie.js基于jquery；先引入jquery，再引入：jquery.cookie.js；下载：http://plugins.jquery.com/cookie/

```
<script type="text/javascript" src="js/jquery.min.js"></script>
<script type="text/javascript" src="js/jquery.cookie.js"></script>
```

**1.添加一个"会话cookie"**

```
$.cookie('the_cookie', 'the_value');
```

这里没有指明 cookie有效时间，所创建的cookie有效期默认到用户关闭浏览器为止，所以被称为 “会话cookie（session cookie）”。

**2.创建一个cookie并设置有效时间为 7天**

```
$.cookie('the_cookie', 'the_value', { expires: 7 });
```

这里指明了cookie有效时间，所创建的cookie被称为“持久 cookie （persistent cookie）”。注意单位是：天；

**3.创建一个cookie并设置 cookie的有效路径**

```
$.cookie('the_cookie', 'the_value', { expires: 7, path: '/' });
```

在默认情况下，只有设置 cookie的网页才能读取该 cookie。如果想让一个页面读取另一个页面设置的cookie，必须设置cookie的路径。cookie的路径用于设置能够读取 cookie的顶级目录。将这个路径设置为网站的根目录，可以让所有网页都能互相读取 cookie （一般不要这样设置，防止出现冲突）。

**4.读取cookie**

```
$.cookie('the_cookie');
```

**5.删除cookie**

```
	
$.cookie('the_cookie', null);   //通过传递null作为cookie的值即可
```

**6.可选参数**

```
$.cookie('the_cookie','the_value',{
    expires:7, 
    path:'/',
    domain:'jquery.com',
    secure:true
})　
```

参数

```
expires：（Number|Date）有效期；设置一个整数时，单位是天；也可以设置一个日期对象作为Cookie的过期日期；
path：（String）创建该Cookie的页面路径；
domain：（String）创建该Cookie的页面域名；
secure：（Booblean）如果设为true，那么此Cookie的传输会要求一个安全协议，例如：HTTPS；
```

 

# [14 Django的用户认证组件](https://www.cnblogs.com/yuanchenqi/articles/9064397.html)

# 用户认证　

## auth模块

```
from django.contrib import auth

```

django.contrib.auth中提供了许多方法，这里主要介绍其中的三个：

### **1.1 、authenticate()**  

提供了用户认证，即验证用户名以及密码是否正确,一般需要username password两个关键字参数

如果认证信息有效，会返回一个 User 对象。authenticate()会在User 对象上设置一个属性标识那种认证后端认证了该用户，且该信息在后面的登录过程中是需要的。当我们试图登陆一个从数据库中直接取出来不经过authenticate()的User对象会报错的！！

```python
user = authenticate(username='someone',password='somepassword')
```

### **1.2 、login(HttpRequest, user)**　　

该函数接受一个HttpRequest对象，以及一个认证了的User对象

此函数使用django的session框架给某个已认证的用户附加上session id等信息。

```python
from django.contrib.auth import authenticate, login
   
def my_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    login(request, user)
    # Redirect to a success page.
    ...
  else:
    # Return an 'invalid login' error message.
    ...
```

### **1.3 、logout(request) 注销用户**　　

```python
from django.contrib.auth import logout
   
def logout_view(request):
  logout(request)
  # Redirect to a success page.
```

该函数接受一个HttpRequest对象，无返回值。当调用该函数时，当前请求的session信息会全部清除。该用户即使没有登录，使用该函数也不会报错。

## User对象

User 对象属性：username， password（必填项）password用哈希算法保存到数据库 

### 2.1 、user对象的 is_authenticated()

如果是真正的 User 对象，返回值恒为 True 。 用于检查用户是否已经通过了认证。
通过认证并不意味着用户拥有任何权限，甚至也不检查该用户是否处于激活状态，这只是表明用户成功的通过了认证。 这个方法很重要, 在后台用request.user.is_authenticated()判断用户是否已经登录，如果true则可以向前台展示request.user.name

要求：

1 用户登陆后才能访问某些页面，

2 如果用户没有登录就访问该页面的话直接跳到登录页面

3 用户在跳转的登陆界面中完成登陆后，自动访问跳转到之前访问的地址

方法1:

```python
def my_view(request):
  if not request.user.is_authenticated():
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
```

方法2:

**django已经为我们设计好了一个用于此种情况的装饰器：login_requierd()**

```
from django.contrib.auth.decorators import login_required
      
@login_required
def my_view(request):
  ...
```

若用户没有登录，则会跳转到django默认的 登录URL '/accounts/login/ ' (这个值可以在settings文件中通过LOGIN_URL进行修改)。并传递 当前访问url的绝对路径 (登陆成功后，会重定向到该路径)。

### 2.2 、创建用户

使用 create_user 辅助函数创建用户:

```python
from django.contrib.auth.models import User
user = User.objects.create_user（username='',password='',email=''）
```



```
小笔记: 命令行创建超级用户
kanghuadeMacBook-Pro:authDemo kanghua$ python3.6 manage.py createsuperuser
Username (leave blank to use 'kanghua'): alex
Email address: aa@qq.com
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
This password is entirely numeric.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```



### 2.3 、check_password(passwd)

```
用户需要修改密码的时候 首先要让他输入原来的密码 ，如果给定的字符串通过了密码检查，返回 True
```

### 2.4 、修改密码

使用 set_password() 来修改密码

```
user = User.objects.get(username='')
user.set_password(password='')
user.save　
```

### 2.5 、简单示例

**注册：**

```python
def sign_up(request):
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        email=request.POST.get('email', '')
        username = request.POST.get('username', '')
        if User.objects.filter(username=username):
                state = 'user_exist'
        else:
                new_user = User.objects.create_user(username=username, password=password,email=email)
                new_user.save()
 
                return redirect('/book/')
    content = {
        'state': state,
        'user': None,
    }
    return render(request, 'sign_up.html', content)　　
```



**修改密码：**

```python
@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                return redirect("/log_in/")
        else:
            state = 'password_error'
    content = {
        'user': user,
        'state': state,
    }
    return render(request, 'set_password.html', content)
```



# [15 Django组件-中间件](https://www.cnblogs.com/yuanchenqi/articles/9036479.html)

# 中间件

## 中间件的概念

中间件顾名思义，是介于request与response处理之间的一道处理过程，相对比较轻量级，并且在全局上改变django的输入与输出。因为改变的是全局，所以需要谨慎实用，用不好会影响到性能。

Django的中间件的定义：

```
Middleware is a framework of hooks into Django’s request/response processing. <br>It’s a light, low-level “plugin” system for globally altering Django’s input or output.

```

如果你想修改请求，例如被传送到view中的**HttpRequest**对象。 或者你想修改view返回的**HttpResponse**对象，这些都可以通过中间件来实现。

可能你还想在view执行之前做一些操作，这种情况就可以用 middleware来实现。

Django默认的`Middleware`：

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

每一个中间件都有具体的功能。

### 中间件实现流程

![image-20211028095926926](assets2.0/image-20211028095926926.png)



## 自定义中间件

中间件中一共有四个方法：

```
process_request

process_view

process_exception

process_response
```



### process_request，process_response

当用户发起请求的时候会依次经过所有的的中间件，这个时候的请求时process_request,最后到达views的函数中，views函数处理后，在依次穿过中间件，这个时候是process_response,最后返回给请求者。

![img](assets2.0/877318-20171012212952512-1143032176.png)

上述截图中的中间件都是django中的，我们也可以自己定义一个中间件，我们可以自己写一个类，但是必须继承MiddlewareMixin

需要导入

```python
from django.utils.deprecation import MiddlewareMixin
```

 ![img](assets2.0/877318-20171012215322324-2079210800.png)

**in views:**

```python
def index(request):

    print("view函数...")
    return HttpResponse("OK")
```

**in Mymiddlewares.py：**

```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class Md1(MiddlewareMixin):
    def process_request(self,request):
        print("Md1请求")
    def process_response(self,request,response):
        print("Md1返回")
        return response

class Md2(MiddlewareMixin):
    def process_request(self,request):
        print("Md2请求")
        #return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response
      
```

**结果：**

```
Md1请求
Md2请求
view函数...
Md2返回
Md1返回
```

**注意：**如果当请求到达请求2的时候直接不符合条件返回，即return HttpResponse("Md2中断")，程序将把请求直接发给中间件2返回，然后依次返回到请求者，结果如下：

返回Md2中断的页面，后台打印如下：

```
Md1请求
Md2请求
Md2返回
Md1返回
```

**流程图如下：**

![img](assets2.0/877318-20180523153139864-2049371026.png)

### process_view

```python
process_view(self, request, callback, callback_args, callback_kwargs)
```

 **Mymiddlewares.py**修改如下

```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class Md1(MiddlewareMixin):
    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Md1view")

class Md2(MiddlewareMixin):
    def process_request(self,request):
        print("Md2请求")
        return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Md2view")
```



结果如下：



```
Md1请求
Md2请求
Md1view
Md2view
view函数...
Md2返回
Md1返回
```



下图进行分析上面的过程：

![img](assets2.0/877318-20180523150722556-373788290.png)

当最后一个中间的process_request到达路由关系映射之后，返回到中间件1的process_view，然后依次往下，到达views函数，最后通过process_response依次返回到达用户。

process_view可以用来调用视图函数：



```python
class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):

        # return HttpResponse("hello")

        response=callback(request,*callback_args,**callback_kwargs)
        return response
```



结果如下：

```
Md1请求
Md2请求
view函数...
Md2返回
Md1返回
```

注意：process_view如果有返回值，会越过其他的process_view以及视图函数，但是所有的process_response都还会执行。

### process_exception

```
process_exception(self, request, exception)

```

示例修改如下：

```python
class Md1(MiddlewareMixin):
    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # return HttpResponse("hello")

        # response=callback(request,*callback_args,**callback_kwargs)
        # return response
        print("md1 process_view...")

    def process_exception(self):
        print("md1 process_exception...")



class Md2(MiddlewareMixin):
    def process_request(self,request):
        print("Md2请求")
        # return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("md2 process_view...")
    def process_exception(self):
        print("md1 process_exception...")
```



结果如下：



```
Md1请求
Md2请求
md1 process_view...
md2 process_view...
view函数...

Md2返回
Md1返回
```



流程图如下：

**当views出现错误时：**

![img](assets2.0/877318-20180523152523125-1475347796.png)

 

 将md2的process_exception修改如下：

```
  def process_exception(self,request,exception):

        print("md2 process_exception...")
        return HttpResponse("error")
```

结果如下：

```
Md1请求
Md2请求
md1 process_view...
md2 process_view...
view函数...
md2 process_exception...
Md2返回
Md1返回
```



## 应用案例

### **1、做IP访问频率限制**

某些IP访问服务器的频率过高，进行拦截，比如限制每分钟不能超过20次。

### **2、URL访问过滤**

如果用户访问的是login视图（放过）

如果访问其他视图，需要检测是不是有session认证，已经有了放行，没有返回login，这样就省得在多个视图函数上写装饰器了！





## 源码试读

作为延伸扩展内容，有余力的同学可以尝试着读一下以下两个自带的中间件：

```
'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
```

 

[![返回主页](assets2.0/logo.gif)](https://www.cnblogs.com/yuanchenqi/)



# [Django-form表单](https://www.cnblogs.com/yuanchenqi/articles/7614921.html)



*知识预览*

-   [构建一个表单](https://www.cnblogs.com/yuanchenqi/articles/7614921.html#_label0)
-   [在Django 中构建一个表单](https://www.cnblogs.com/yuanchenqi/articles/7614921.html#_label1)
-   [Django Form 类详解](https://www.cnblogs.com/yuanchenqi/articles/7614921.html#_label2)
-   [使用表单模板](https://www.cnblogs.com/yuanchenqi/articles/7614921.html#_label3)



## 构建一个表单

假设你想在你的网站上创建一个简单的表单，以获得用户的名字。你需要类似这样的模板：

```html
<form action="/your-name/" method="post">
    <label for="your_name">Your name: </label>
    <input id="your_name" type="text" name="your_name">
    <input type="submit" value="OK">
</form>
```

这是一个非常简单的表单。实际应用中，一个表单可能包含几十上百个字段，其中大部分需要预填充，而且我们预料到用户将来回编辑-提交几次才能完成操作。

我们可能需要在表单提交之前，在浏览器端作一些验证。我们可能想使用非常复杂的字段，以允许用户做类似从日历中挑选日期这样的事情，等等。

这个时候，让Django 来为我们完成大部分工作是很容易的。

so,两个突出优点：

  1 form表单提交时，数据出现错误，返回的页面中仍可以保留之前输入的数据。

  2 方便地限制字段条件



## 在Django 中构建一个表单

### Form 类

我们已经计划好了我们的 HTML 表单应该呈现的样子。在Django 中，我们的起始点是这里：

```python
#forms.py
 
from django import forms
 
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
```

 它定义一个`Form` 类，只带有一个字段（`your_name`）。

字段允许的最大长度通过`max_length` 定义。它完成两件事情。首先，它在HTML 的`<input>` 上放置一个`maxlength="100"`（这样浏览器将在第一时间阻止用户输入多于这个数目的字符）。它还意味着当Django 收到浏览器发送过来的表单时，它将验证数据的长度。

`Form` 的实例具有一个`is_valid()` 方法，它为所有的字段运行验证的程序。当调用这个方法时，如果所有的字段都包含合法的数据，它将：

-   返回`True`
-   将表单的数据放到`cleaned_data`属性中。

完整的表单，第一次渲染时，看上去将像：

```html
<label for="your_name">Your name: </label>
<input id="your_name" type="text" name="your_name" maxlength="100">
```

 注意它不包含 `<form>` 标签和提交按钮。我们必须自己在模板中提供它们。

## 视图

发送给Django 网站的表单数据通过一个视图处理，一般和发布这个表单的是同一个视图。这允许我们重用一些相同的逻辑。

当处理表单时，我们需要在视图中实例化它：



```python
#views.py

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
```



如果访问视图的是一个`GET` 请求，它将创建一个空的表单实例并将它放置到要渲染的模板的上下文中。这是我们在第一个访问该URL 时预期发生的情况。

如果表单的提交使用`POST` 请求，那么视图将再次创建一个表单实例并使用请求中的数据填充它：`form = NameForm(request.POST)`。这叫做”绑定数据至表单“（它现在是一个绑定的表单）。

我们调用表单的`is_valid()`方法；如果它不为`True`，我们将带着这个表单返回到模板。这时表单不再为空（未绑定），所以HTML 表单将用之前提交的数据填充，然后可以根据要求编辑并改正它。

如果`is_valid()`为`True`，我们将能够在`cleaned_data` 属性中找到所有合法的表单数据。在发送HTTP 重定向给浏览器告诉它下一步的去向之前，我们可以用这个数据来更新数据库或者做其它处理。

## 模板

我们不需要在name.html 模板中做很多工作。最简单的例子是：

```html
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit" />
</form>
```

 根据`{{ form }}`，所有的表单字段和它们的属性将通过Django 的模板语言拆分成HTML 标记 。

注：Django 原生支持一个简单易用的[跨站请求伪造的防护](http://python.usyiyi.cn/django/ref/csrf.html)。当提交一个启用CSRF 防护的`POST` 表单时，你必须使用上面例子中的`csrf_token` 模板标签。

现在我们有了一个可以工作的网页表单，它通过Django Form 描述、通过视图处理并渲染成一个HTML `<form>`。



## Django Form 类详解

## 绑定的和未绑定的表单实例

绑定的和未绑定的表单 之间的区别非常重要：

-   未绑定的表单没有关联的数据。当渲染给用户时，它将为空或包含默认的值。
-   绑定的表单具有提交的数据，因此可以用来检验数据是否合法。如果渲染一个不合法的绑定的表单，它将包含内联的错误信息，告诉用户如何纠正数据。

## 字段详解

考虑一个比上面的迷你示例更有用的一个表单，我们完成一个更加有用的注册表单：



```python
#forms.py

from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,
                               error_messages={"min_length":"最短为5个字符","required":"该字段不能为空"},
                               )
    password = forms.CharField(max_length=100,
                               widget=widgets.PasswordInput(attrs={"placeholder":"password"})
                                )

    telephone=forms.IntegerField(
        error_messages={
            "invalid":"格式错误"
        }

                                )


    gender=forms.CharField(
          initial=2,
          widget=widgets.Select(choices=((1,'上海'),(2,'北京'),))
             )

    email = forms.EmailField()
    is_married = forms.BooleanField(required=False)
```



### Widgets

每个表单字段都有一个对应的`Widget` 类，它对应一个HTML 表单`Widget`，例如`<input type="text">`。

在大部分情况下，字段都具有一个合理的默认Widget。例如，默认情况下，`CharField` 具有一个`TextInput Widget`，它在HTML 中生成一个`<input type="text">`。

### 字段的数据

不管表单提交的是什么数据，一旦通过调用`is_valid()` 成功验证（`is_valid()` 返回`True`），验证后的表单数据将位于`form.cleaned_data` 字典中。这些数据已经为你转换好为Python 的类型。

注：此时，你依然可以从`request.POST` 中直接访问到未验证的数据，但是访问验证后的数据更好一些。

在上面的联系表单示例中，is_married将是一个布尔值。类似地，`IntegerField` 和`FloatField` 字段分别将值转换为Python 的`int` 和`float`。

[回到顶部](https://www.cnblogs.com/yuanchenqi/articles/7614921.html#_labelTop)

## 使用表单模板

你需要做的就是将表单实例放进模板的上下文。如果你的表单在`Contex`t 中叫做`form`，那么`{{ form }}`将正确地渲染它的`<label>` 和 `<input>`元素。

## 表单渲染的选项

对于`<label>/<input>` 对，还有几个输出选项：

-   `{{ form.as_table }}` 以表格的形式将它们渲染在`<tr>` 标签中
-   `{{ form.as_p }}` 将它们渲染在`<p>` 标签中
-   `{{ form.as_ul }}` 将它们渲染在`<li>` 标签中

注意，你必须自己提供`<table>` 或`<ul>` 元素。

`{{ form.as_p }}`会渲染如下：

```html
<form action="">
    <p>
        <label for="id_username">Username:</label>
        <input id="id_username" maxlength="100" name="username" type="text" required="">
    </p>
 
 
    <p>
        <label for="id_password">Password:</label>
        <input id="id_password" maxlength="100" name="password" placeholder="password" type="password" required="">
    </p>
 
 
    <p>
        <label for="id_telephone">Telephone:</label> <input id="id_telephone" name="telephone" type="number" required="">
    </p>
 
 
    <p>
        <label for="id_email">Email:</label> <input id="id_email" name="email" type="email" required="">
    </p>
 
 
    <p>
        <label for="id_is_married">Is married:</label> <input id="id_is_married" name="is_married" type="checkbox">
    </p>
 
 
    <input type="submit" value="注册">
</form>
```

## 手工渲染字段

我们没有必要非要让Django 来分拆表单的字段；如果我们喜欢，我们可以手工来做（例如，这样允许重新对字段排序）。每个字段都是表单的一个属性，可以使用`{{ form.name_of_field }}` 访问，并将在Django 模板中正确地渲染。例如：

```html
<div class="fieldWrapper">
    {{ form.Username.errors }}
    {{ form.Username.label_tag }}
    {{ form.Username }}
</div>
```

## 渲染表单的错误信息

1、

```python
registerForm=RegisterForm(request.POST)
print(type(registerForm.errors))                      #<class 'django.forms.utils.ErrorDict'>
print(type(registerForm.errors["username"]))          #<class 'django.forms.utils.ErrorList'>

```

2、

使用`{{ form.name_of_field.errors }}` 显示表单错误的一个清单，并渲染成一个`ul`。看上去可能像：

```html
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>
```

##  form组件的钩子



```python
def foo(request):


    if request.method=="POST":

        regForm=RegForm(request.POST)

        if regForm.is_valid():
            pass
            # 可用数据: regForm.cleaned_data,
            # 将数据插入数据库表中


        else:
            pass
            # 可用数据: regForm.errors
            # 可以利用模板渲染讲errors嵌套到页面中返回
            # 也可以打包到一个字典中,用于ajax返回

    else:
        regForm=RegForm()
    return render(request,"register.html",{"regForm":regForm})

    

    '''
    实例化时:

        self.fields={
            "username":"字段规则对象",
            "password":"字段规则对象",

        }


    is_valid时:

        self._errors = {}
        self.cleaned_data = {}


        #局部钩子:

        for name, field in self.fields.items():
              try:

                    value = field.clean(value)
                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
              except ValidationError as e:
                    self.add_error(name, e)

        # 全局钩子:

        self.clean()     # def self.clean():return self.cleaned_data

        return  not self.errors    # True或者False


    '''
```



## form组件补充

1、Django内置字段如下：



```django
Field
    required=True,               是否允许为空
    widget=None,                 HTML插件
    label=None,                  用于生成Label标签或显示内容
    initial=None,                初始值
    help_text='',                帮助信息(在标签旁边显示)
    error_messages=None,         错误信息 {'required': '不能为空', 'invalid': '格式错误'}
    show_hidden_initial=False,   是否在当前插件后面再加一个隐藏的且具有默认值的插件（可用于检验两次输入是否一直）
    validators=[],               自定义验证规则
    localize=False,              是否支持本地化
    disabled=False,              是否可以编辑
    label_suffix=None            Label内容后缀
 
 
CharField(Field)
    max_length=None,             最大长度
    min_length=None,             最小长度
    strip=True                   是否移除用户输入空白
 
IntegerField(Field)
    max_value=None,              最大值
    min_value=None,              最小值
 
FloatField(IntegerField)
    ...
 
DecimalField(IntegerField)
    max_value=None,              最大值
    min_value=None,              最小值
    max_digits=None,             总长度
    decimal_places=None,         小数位长度
 
BaseTemporalField(Field)
    input_formats=None          时间格式化   
 
DateField(BaseTemporalField)    格式：2015-09-01
TimeField(BaseTemporalField)    格式：11:12
DateTimeField(BaseTemporalField)格式：2015-09-01 11:12
 
DurationField(Field)            时间间隔：%d %H:%M:%S.%f
    ...
 
RegexField(CharField)
    regex,                      自定制正则表达式
    max_length=None,            最大长度
    min_length=None,            最小长度
    error_message=None,         忽略，错误信息使用 error_messages={'invalid': '...'}
 
EmailField(CharField)      
    ...
 
FileField(Field)
    allow_empty_file=False     是否允许空文件
 
ImageField(FileField)      
    ...
    注：需要PIL模块，pip3 install Pillow
    以上两个字典使用时，需要注意两点：
        - form表单中 enctype="multipart/form-data"
        - view函数中 obj = MyForm(request.POST, request.FILES)
 
URLField(Field)
    ...
 
 
BooleanField(Field)  
    ...
 
NullBooleanField(BooleanField)
    ...
 
ChoiceField(Field)
    ...
    choices=(),                选项，如：choices = ((0,'上海'),(1,'北京'),)
    required=True,             是否必填
    widget=None,               插件，默认select插件
    label=None,                Label内容
    initial=None,              初始值
    help_text='',              帮助提示
 
 
ModelChoiceField(ChoiceField)
    ...                        django.forms.models.ModelChoiceField
    queryset,                  # 查询数据库中的数据
    empty_label="---------",   # 默认空显示内容
    to_field_name=None,        # HTML中value的值对应的字段
    limit_choices_to=None      # ModelForm中对queryset二次筛选
     
ModelMultipleChoiceField(ModelChoiceField)
    ...                        django.forms.models.ModelMultipleChoiceField
 
 
     
TypedChoiceField(ChoiceField)
    coerce = lambda val: val   对选中的值进行一次转换
    empty_value= ''            空值的默认值
 
MultipleChoiceField(ChoiceField)
    ...
 
TypedMultipleChoiceField(MultipleChoiceField)
    coerce = lambda val: val   对选中的每一个值进行一次转换
    empty_value= ''            空值的默认值
 
ComboField(Field)
    fields=()                  使用多个验证，如下：即验证最大长度20，又验证邮箱格式
                               fields.ComboField(fields=[fields.CharField(max_length=20), fields.EmailField(),])
 
MultiValueField(Field)
    PS: 抽象类，子类中可以实现聚合多个字典去匹配一个值，要配合MultiWidget使用
 
SplitDateTimeField(MultiValueField)
    input_date_formats=None,   格式列表：['%Y--%m--%d', '%m%d/%Y', '%m/%d/%y']
    input_time_formats=None    格式列表：['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']
 
FilePathField(ChoiceField)     文件选项，目录下文件显示在页面中
    path,                      文件夹路径
    match=None,                正则匹配
    recursive=False,           递归下面的文件夹
    allow_files=True,          允许文件
    allow_folders=False,       允许文件夹
    required=True,
    widget=None,
    label=None,
    initial=None,
    help_text=''
 
GenericIPAddressField
    protocol='both',           both,ipv4,ipv6支持的IP格式
    unpack_ipv4=False          解析ipv4地址，如果是::ffff:192.0.2.1时候，可解析为192.0.2.1， PS：protocol必须为both才能启用
 
SlugField(CharField)           数字，字母，下划线，减号（连字符）
    ...
 
UUIDField(CharField)           uuid类型
    ...
```

2、Django内置插件：

```
TextInput(Input)
NumberInput(TextInput)
EmailInput(TextInput)
URLInput(TextInput)
PasswordInput(TextInput)
HiddenInput(TextInput)
Textarea(Widget)
DateInput(DateTimeBaseInput)
DateTimeInput(DateTimeBaseInput)
TimeInput(DateTimeBaseInput)
CheckboxInput
Select
NullBooleanSelect
SelectMultiple
RadioSelect
CheckboxSelectMultiple
FileInput
ClearableFileInput
MultipleHiddenInput
SplitDateTimeWidget
SplitHiddenDateTimeWidget
SelectDateWidget
```



3、常用选择插件：



```
# 单radio，值为字符串
# user = fields.CharField(
#     initial=2,
#     widget=widgets.RadioSelect(choices=((1,'上海'),(2,'北京'),))
# )
 
# 单radio，值为字符串
# user = fields.ChoiceField(
#     choices=((1, '上海'), (2, '北京'),),
#     initial=2,
#     widget=widgets.RadioSelect
# )
 
# 单select，值为字符串
# user = fields.CharField(
#     initial=2,
#     widget=widgets.Select(choices=((1,'上海'),(2,'北京'),))
# )
 
# 单select，值为字符串
# user = fields.ChoiceField(
#     choices=((1, '上海'), (2, '北京'),),
#     initial=2,
#     widget=widgets.Select
# )
 
# 多选select，值为列表
# user = fields.MultipleChoiceField(
#     choices=((1,'上海'),(2,'北京'),),
#     initial=[1,],
#     widget=widgets.SelectMultiple
# )
 
 
# 单checkbox
# user = fields.CharField(
#     widget=widgets.CheckboxInput()
# )
 
 
# 多选checkbox,值为列表
# user = fields.MultipleChoiceField(
#     initial=[2, ],
#     choices=((1, '上海'), (2, '北京'),),
#     widget=widgets.CheckboxSelectMultiple
# )
```

[引入](https://www.cnblogs.com/wupeiqi/articles/6144178.html)



# [Django_form补充](https://www.cnblogs.com/yuanchenqi/articles/7487059.html)

问题1: 注册页面输入为空，报错：keyError：找不到password

```django
def clean(self):
    print("---",self.cleaned_data)
    # if self.cleaned_data["password"]==self.cleaned_data["repeat_password"]:     
    # 报错原因：self.cleaned_data是干净数据，如果页面没有输入内容，则self.cleaned_data没有password。
    # 改如下：
    if self.cleaned_data.get("password")==self.cleaned_data.get("repeat_password"):
        return self.cleaned_data
    else:
        raise ValidationError("两次密码不一致")
```



 

 2 为什么要用全局clean():

![img](assets2.0/877318-20170906212010491-1082705771.png)

![img](assets2.0/877318-20170906212037694-1695702959.png)

![img](assets2.0/877318-20170906212110788-2023823254.png)

![img](assets2.0/877318-20170906212214163-120707747.png)

按子段顺序一一校验，即校验到username时，你无法使用self.cleaned_data.get("password")。

而局部钩子使用完，到全局时，已经可以使用所有的self.cleaned_data

3

![img](assets2.0/877318-20170906212732116-1993581374.png)

 



# [Django-组件拾遗](https://www.cnblogs.com/yuanchenqi/articles/8034442.html)



*知识预览*

-   [一 Django的form组件](https://www.cnblogs.com/yuanchenqi/articles/8034442.html#_label0)
-   [二 Django的model form组件](https://www.cnblogs.com/yuanchenqi/articles/8034442.html#_label1)
-   [三 Django的缓存机制](https://www.cnblogs.com/yuanchenqi/articles/8034442.html#_label2)
-   [四 Django的信号](https://www.cnblogs.com/yuanchenqi/articles/8034442.html#_label3)
-   [五 Django的序列化](https://www.cnblogs.com/yuanchenqi/articles/8034442.html#_label4)



## 一 Django的form组件

[forms组件](http://www.cnblogs.com/yuanchenqi/articles/7614921.html)



## 二 Django的model form组件

这是一个神奇的组件，通过名字我们可以看出来，这个组件的功能就是把model和form组合起来，先来一个简单的例子来看一下这个东西怎么用：比如我们的数据库中有这样一张学生表，字段有姓名，年龄，爱好，邮箱，电话，住址，注册时间等等一大堆信息，现在让你写一个创建学生的页面，你的后台应该怎么写呢？首先我们会在前端一个一个罗列出这些字段，让用户去填写，然后我们从后天一个一个接收用户的输入，创建一个新的学生对象，保存其实，重点不是这些，而是合法性验证，我们需要在前端判断用户输入是否合法，比如姓名必须在多少字符以内，电话号码必须是多少位的数字，邮箱必须是邮箱的格式这些当然可以一点一点手动写限制，各种判断，这毫无问题，除了麻烦我们现在有个更优雅（以后在Python相关的内容里，要多用“优雅”这个词，并且养成习惯）的方法：ModelForm先来简单的，生硬的把它用上，再来加验证条件。

## 创建modelform



```python
#首先导入ModelForm

from django.forms import ModelForm
#在视图函数中，定义一个类，比如就叫StudentList，这个类要继承ModelForm，在这个类中再写一个原类Meta（规定写法，并注意首字母是大写的）
#在这个原类中，有以下属性（部分）：

class StudentList(ModelForm):
    class Meta:
        model =Student #对应的Model中的类
        fields = "__all__" #字段，如果是__all__,就是表示列出所有的字段
        exclude = None #排除的字段
        #error_messages用法：
        error_messages = {
        'name':{'required':"用户名不能为空",},
        'age':{'required':"年龄不能为空",},
        }
        #widgets用法,比如把输入用户名的input框给为Textarea
        #首先得导入模块
        from django.forms import widgets as wid #因为重名，所以起个别名
        widgets = {
        "name":wid.Textarea(attrs={"class":"c1"}) #还可以自定义属性
        }
        #labels，自定义在前端显示的名字
        labels= {
        "name":"用户名"
        }
        
```



然后在url对应的视图函数中实例化这个类，把这个对象传给前端

```python
def student(request):

    if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
        
```

然后前端只需要 {{ student_list.as_p }} 一下，所有的字段就都出来了，可以用as_p显示全部，也可以通过for循环这
student_list，拿到的是一个个input框，现在我们就不用as_p，手动把这些input框搞出来，as_p拿到的页面太丑。
首先 for循环这个student_list，拿到student对象，直接在前端打印这个student，是个input框student.label ，拿到数据库中每个字段的verbose_name ,如果没有设置这个属性，拿到的默认就是字段名，还可以通过student.errors.0 拿到错误信息有了这些，我们就可以通过bootstrap，自己拼出来想要的样式了，比如：



```html
<body>
<div class="container">
    <h1>student</h1>
    <form method="POST" novalidate>
        {% csrf_token %}
        {# {{ student_list.as_p }}#}
        {% for student in student_list %}
            <div class="form-group col-md-6">
                {# 拿到数据字段的verbose_name,没有就默认显示字段名 #}
                <label class="col-md-3 control-label">{{ student.label }}</label>
                <div class="col-md-9" style="position: relative;">{{ student }}</div>
            </div>
        {% endfor %}
        <div class="col-md-2 col-md-offset-10">
            <input type="submit" value="提交" class="btn-primary">
        </div>
    </form>
</div>
</body>
```



现在还缺一个input框的form-contral样式，可以考虑在后台的widget里面添加
比如这样：

```python
from django.forms import widgets as wid #因为重名，所以起个别名
widgets = {
"name":wid.TextInput(attrs={'class':'form-control'}),
"age":wid.NumberInput(attrs={'class':'form-control'}),
"email":wid.EmailInput(attrs={'class':'form-control'})
}
```

当然也可以在js中，找到所有的input框，加上这个样式，也行。

## 添加纪录

保存数据的时候，不用挨个取数据了，只需要save一下



```python
def student(request):

    if request.method == 'GET':
         student_list = StudentList()
         return render(request,'student.html',{'student_list':student_list})
    else:
         student_list = StudentList(request.POST)
         if student_list.is_valid():
         		student_list.save()
         return redirect(request,'student_list.html',{'student_list':student_list})
        
```



## 编辑数据

如果不用ModelForm，编辑的时候得显示之前的数据吧，还得挨个取一遍值，如果ModelForm，只需要加一个instance=obj（obj是要修改的数据库的一条数据的对象）就可以得到同样的效果
保存的时候要注意，一定要注意有这个对象（instance=obj），否则不知道更新哪一个数据
代码示例：



```python
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm
# Create your views here.
from app01 import models
def test(request):
    # model_form = models.Student
    model_form = models.Student.objects.all()
    return render(request,'test.html',{'model_form':model_form})

class StudentList(ModelForm):
    class Meta:
        model = models.Student #对应的Model中的类
        fields = "__all__" #字段，如果是__all__,就是表示列出所有的字段
        exclude = None #排除的字段
        labels = None #提示信息
        help_texts = None #帮助提示信息
        widgets = None #自定义插件
        error_messages = None #自定义错误信息
        #error_messages用法：
        error_messages = {
        'name':{'required':"用户名不能为空",},
        'age':{'required':"年龄不能为空",},
        }
        #widgets用法,比如把输入用户名的input框给为Textarea
        #首先得导入模块
        from django.forms import widgets as wid #因为重名，所以起个别名
        widgets = {
        "name":wid.Textarea
        }
        #labels，自定义在前端显示的名字
        labels= {
        "name":"用户名"
        }
def student(request):
    if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
    else:
        student_list = StudentList(request.POST)
        if student_list.is_valid():
            student_list.save()
            return render(request,'student.html',{'student_list':student_list})

def student_edit(request,pk):
    obj = models.Student.objects.filter(pk=pk).first()
    if not obj:
        return redirect('test')
    if request.method == "GET":
        student_list = StudentList(instance=obj)
        return render(request,'student_edit.html',{'student_list':student_list})
    else:
        student_list = StudentList(request.POST,instance=obj)
        if student_list.is_valid():
            student_list.save()
            return render(request,'student_edit.html',{'student_list':student_list})
```



总结： 从上边可以看到ModelForm用起来是非常方便的，比如增加修改之类的操作。但是也带来额外不好的地方，model和form之间耦合了。如果不耦合的话，mf.save()方法也无法直接提交保存。 但是耦合的话使用场景通常局限用于小程序，写大程序就最好不用了。



## 三 Django的缓存机制

## 1.1 缓存介绍

### **1.缓存的简介**

在动态网站中,用户所有的请求,服务器都会去数据库中进行相应的增,删,查,改,渲染模板,执行业务逻辑,最后生成用户看到的页面.

当一个网站的用户访问量很大的时候,每一次的的后台操作,都会消耗很多的服务端资源,所以必须使用缓存来减轻后端服务器的压力.

缓存是将一些常用的数据保存内存或者memcache中,在一定的时间内有人来访问这些数据时,则不再去执行数据库及渲染等操作,而是直接从内存或memcache的缓存中去取得数据,然后返回给用户.

### **2.Django提供了6种缓存方式**

-   开发调试缓存
-   内存缓存
-   文件缓存
-   数据库缓存
-   Memcache缓存(使用python-memcached模块)
-   Memcache缓存(使用pylibmc模块)

经常使用的有文件缓存和Mencache缓存

## 1.2 各种缓存配置

1.2.1 开发调试(此模式为开发调试使用,实际上不执行任何操作)

settings.py文件配置



```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # 缓存后台使用的引擎
  'TIMEOUT': 300,            # 缓存超时时间（默认300秒，None表示永不过期，0表示立即过期）
  'OPTIONS':{
   'MAX_ENTRIES': 300,          # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  },
 }
}
```



1.2.2 内存缓存(将缓存内容保存至内存区域中)

settings.py文件配置



```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # 指定缓存使用的引擎
  'LOCATION': 'unique-snowflake',         # 写在内存中的变量的唯一值 
  'TIMEOUT':300,             # 缓存超时时间(默认为300秒,None表示永不过期)
  'OPTIONS':{
   'MAX_ENTRIES': 300,           # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  }  
 }
}
```



1.2.3 文件缓存(把缓存数据存储在文件中)

settings.py文件配置



```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', #指定缓存使用的引擎
  'LOCATION': '/var/tmp/django_cache',        #指定缓存的路径
  'TIMEOUT':300,              #缓存超时时间(默认为300秒,None表示永不过期)
  'OPTIONS':{
   'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  }
 }   
}
```



1.2.4 数据库缓存(把缓存数据存储在数据库中)

settings.py文件配置



```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.db.DatabaseCache',  # 指定缓存使用的引擎
  'LOCATION': 'cache_table',          # 数据库表    
  'OPTIONS':{
   'MAX_ENTRIES': 300,           # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,          # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  }  
 }   
}
```



注意,创建缓存的数据库表使用的语句:

```
python manage.py createcachetable
```

1.2.5 Memcache缓存(使用python-memcached模块连接memcache)

Memcached是Django原生支持的缓存系统.要使用Memcached,需要下载Memcached的支持库python-memcached或pylibmc.

settings.py文件配置

```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache', # 指定缓存使用的引擎
  'LOCATION': '192.168.10.100:11211',         # 指定Memcache缓存服务器的IP地址和端口
  'OPTIONS':{
   'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  }
 }
}
```



LOCATION也可以配置成如下:

```python
'LOCATION': 'unix:/tmp/memcached.sock',   # 指定局域网内的主机名加socket套接字为Memcache缓存服务器
'LOCATION': [         # 指定一台或多台其他主机ip地址加端口为Memcache缓存服务器
 '192.168.10.100:11211',
 '192.168.10.101:11211',
 '192.168.10.102:11211',
]
```

1.2.6 Memcache缓存(使用pylibmc模块连接memcache)



```python
settings.py文件配置
 CACHES = {
  'default': {
   'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',  # 指定缓存使用的引擎
   'LOCATION':'192.168.10.100:11211',         # 指定本机的11211端口为Memcache缓存服务器
   'OPTIONS':{
    'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
    'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
   },  
  }
 }
```



LOCATION也可以配置成如下:

```python
'LOCATION': '/tmp/memcached.sock',  # 指定某个路径为缓存目录
'LOCATION': [       # 分布式缓存,在多台服务器上运行Memcached进程,程序会把多台服务器当作一个单独的缓存,而不会在每台服务器上复制缓存值
 '192.168.10.100:11211',
 '192.168.10.101:11211',
 '192.168.10.102:11211',
]
```

Memcached是基于内存的缓存,数据存储在内存中.所以如果服务器死机的话,数据就会丢失,所以Memcached一般与其他缓存配合使用

## **1.3 Django中的缓存应用**

Django提供了不同粒度的缓存,可以缓存某个页面,可以只缓存一个页面的某个部分,甚至可以缓存整个网站.

数据库：

```python
class Book(models.Model):
    name=models.CharField(max_length=32)
    price=models.DecimalField(max_digits=6,decimal_places=1)
```

![img](assets2.0/877318-20171213193539004-1037954462.png)

视图：

```python
from django.views.decorators.cache import cache_page
import time
from .models import *

@cache_page(15)          #超时时间为15秒
def index(request):

 t=time.time()      #获取当前时间
 bookList=Book.objects.all()
 return render(request,"index.html",locals())
```



模板(index.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h3>当前时间:-----{{ t }}</h3>

<ul>
    {% for book in bookList %}
       <li>{{ book.name }}--------->{{ book.price }}$</li>
    {% endfor %}
</ul>

</body>
</html>
```



上面的例子是基于内存的缓存配置,基于文件的缓存该怎么配置呢??

更改settings.py的配置

```python
CACHES = {
 'default': {
  'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # 指定缓存使用的引擎
  'LOCATION': 'E:\django_cache',          # 指定缓存的路径
  'TIMEOUT': 300,              # 缓存超时时间(默认为300秒,None表示永不过期)
  'OPTIONS': {
   'MAX_ENTRIES': 300,            # 最大缓存记录的数量（默认300）
   'CULL_FREQUENCY': 3,           # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
  }
 }
}
```



然后再次刷新浏览器,可以看到在刚才配置的目录下生成的缓存文件

通过实验可以知道,Django会以自己的形式把缓存文件保存在配置文件中指定的目录中. 

**1.3.2 全站使用缓存**

既然是全站缓存,当然要使用Django中的中间件.

用户的请求通过中间件,经过一系列的认证等操作,如果请求的内容在缓存中存在,则使用FetchFromCacheMiddleware获取内容并返回给用户

当返回给用户之前,判断缓存中是否已经存在,如果不存在,则UpdateCacheMiddleware会将缓存保存至Django的缓存之中,以实现全站缓存



```
缓存整个站点，是最简单的缓存方法

在 MIDDLEWARE_CLASSES 中加入 “update” 和 “fetch” 中间件
MIDDLEWARE_CLASSES = (
    ‘django.middleware.cache.UpdateCacheMiddleware’, #第一
    'django.middleware.common.CommonMiddleware',
    ‘django.middleware.cache.FetchFromCacheMiddleware’, #最后
)
“update” 必须配置在第一个
“fetch” 必须配置在最后一个
```



修改settings.py配置文件

```
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',   #响应HttpResponse中设置几个headers
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',   #用来缓存通过GET和HEAD方法获取的状态码为200的响应

)


CACHE_MIDDLEWARE_SECONDS=10
```



视图函数：

```
from django.views.decorators.cache import cache_page
import time
from .models import *


def index(request):

     t=time.time()      #获取当前时间
     bookList=Book.objects.all()
     return render(request,"index.html",locals())

def foo(request):
    t=time.time()      #获取当前时间
    return HttpResponse("HELLO:"+str(t))
```



模板(index.html)：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h3 style="color: green">当前时间:-----{{ t }}</h3>

<ul>
    {% for book in bookList %}
       <li>{{ book.name }}--------->{{ book.price }}$</li>
    {% endfor %}
</ul>

</body>
</html>
```



其余代码不变,刷新浏览器是10秒,页面上的时间变化一次,这样就实现了全站缓存.

**1.3.3 局部视图缓存**

例子,刷新页面时,整个网页有一部分实现缓存

views视图函数

```
from django.views.decorators.cache import cache_page
import time
from .models import *


def index(request):

     t=time.time()      #获取当前时间
     bookList=Book.objects.all()

     return render(request,"index.html",locals())
```



模板(index.html):

```
{% load cache %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
 <h3 style="color: green">不缓存:-----{{ t }}</h3>

{% cache 2 'name' %}
 <h3>缓存:-----:{{ t }}</h3>
{% endcache %}

</body>
</html> 
```



## 四 Django的信号

Django提供一种信号机制。其实就是观察者模式，又叫发布-订阅(Publish/Subscribe) 。当发生一些动作的时候，发出信号，然后监听了这个信号的函数就会执行。

通俗来讲，就是一些动作发生的时候，信号允许特定的发送者去提醒一些接受者。用于在框架执行操作时解耦。

### 2.1、Django内置信号 



```
Model signals
    pre_init                    # django的modal执行其构造方法前，自动触发
    post_init                   # django的modal执行其构造方法后，自动触发
    pre_save                    # django的modal对象保存前，自动触发
    post_save                   # django的modal对象保存后，自动触发
    pre_delete                  # django的modal对象删除前，自动触发
    post_delete                 # django的modal对象删除后，自动触发
    m2m_changed                 # django的modal中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
    class_prepared              # 程序启动时，检测已注册的app中modal类，对于每一个类，自动触发
Management signals
    pre_migrate                 # 执行migrate命令前，自动触发
    post_migrate                # 执行migrate命令后，自动触发
Request/response signals
    request_started             # 请求到来前，自动触发
    request_finished            # 请求结束后，自动触发
    got_request_exception       # 请求异常后，自动触发
Test signals
    setting_changed             # 使用test测试修改配置文件时，自动触发
    template_rendered           # 使用test测试渲染模板时，自动触发
Database Wrappers
    connection_created          # 创建数据库连接时，自动触发
```



```
Django 提供了一系列的内建信号，允许用户的代码获得DJango的特定操作的通知。这包含一些有用的通知：
django.db.models.signals.pre_save & django.db.models.signals.post_save

在模型 save()方法调用之前或之后发送。
django.db.models.signals.pre_delete & django.db.models.signals.post_delete

在模型delete()方法或查询集的delete() 方法调用之前或之后发送。
django.db.models.signals.m2m_changed

模型上的 ManyToManyField 修改时发送。
django.core.signals.request_started & django.core.signals.request_finished

Django建立或关闭HTTP 请求时发送。
```



对于Django内置的信号，仅需注册指定信号，当程序执行相应操作时，自动触发注册函数：

方式1:	

```python
from django.core.signals import request_finished
    from django.core.signals import request_started
    from django.core.signals import got_request_exception

    from django.db.models.signals import class_prepared
    from django.db.models.signals import pre_init, post_init
    from django.db.models.signals import pre_save, post_save
    from django.db.models.signals import pre_delete, post_delete
    from django.db.models.signals import m2m_changed
    from django.db.models.signals import pre_migrate, post_migrate

    from django.test.signals import setting_changed
    from django.test.signals import template_rendered

    from django.db.backends.signals import connection_created


    def callback(sender, **kwargs):
        print("pre_save_callback")
        print(sender,kwargs)

    pre_save.connect(callback)      ＃ 该脚本代码需要写到app或者项目的初始化文件中，当项目启动时执行注册代码
```



方式2:

```python
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```

### 2.2、自定义信号 

a. 定义信号

```
import django.dispatch
pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])

```

b. 注册信号

```
def callback(sender, **kwargs):
    print("callback")
    print(sender,kwargs)
  
pizza_done.connect(callback)
```

c. 触发信号

```
from 路径 import pizza_done
  
pizza_done.send(sender='seven',toppings=123, size=456)
```

由于内置信号的触发者已经集成到Django中，所以其会自动调用，而对于自定义信号则需要开发者在任意位置触发。 

练习：数据库添加一条记录时生成一个日志记录。



## 五 Django的序列化

关于Django中的序列化主要应用在将数据库中检索的数据返回给客户端用户，特别的Ajax请求一般返回的为Json格式。

1、serializers

```
from django.core import serializers
  
ret = models.BookType.objects.all()
  
data = serializers.serialize("json", ret)
```

2、json.dumps

```
import json
  
#ret = models.BookType.objects.all().values('caption')
ret = models.BookType.objects.all().values_list('caption')
  
ret=list(ret)
  
result = json.dumps(ret)
```

由于json.dumps时无法处理datetime日期，所以可以通过自定义处理器来做扩展，如：

```python
import json
from datetime import date
from datetime import datetime

d=datetime.now()

class JsonCustomEncoder(json.JSONEncoder):

    def default(self, field):

        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M---%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)


ds = json.dumps(d, cls=JsonCustomEncoder)

print(ds)
print(type(ds))


'''
Supports the following objects and types by default:

    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

'''
```



# [Django-认证系统](https://www.cnblogs.com/yuanchenqi/articles/7609586.html)



*知识预览*

-   [COOKIE 与 SESSION](https://www.cnblogs.com/yuanchenqi/articles/7609586.html#_label0)
-   [用户认证　](https://www.cnblogs.com/yuanchenqi/articles/7609586.html#_label1)



## COOKIE 与 SESSION

## 概念

cookie不属于http协议范围，由于http协议无法保持状态，但实际情况，我们却又需要“保持状态”，因此cookie就是在这样一个场景下诞生。

cookie的工作原理是：由服务器产生内容，浏览器收到请求后保存在本地；当浏览器再次访问时，浏览器会自动带上cookie，这样服务器就能通过cookie的内容来判断这个是“谁”了。

cookie虽然在一定程度上解决了“保持状态”的需求，但是由于cookie本身最大支持4096字节，以及cookie本身保存在客户端，可能被拦截或窃取，因此就需要有一种新的东西，它能支持更多的字节，并且他保存在服务器，有较高的安全性。这就是session。

问题来了，基于http协议的无状态特征，服务器根本就不知道访问者是“谁”。那么上述的cookie就起到桥接的作用。

我们可以给每个客户端的cookie分配一个唯一的id，这样用户在访问时，通过cookie，服务器就知道来的人是“谁”。然后我们再根据不同的cookie的id，在服务器上保存一段时间的私密资料，如“账号密码”等等。

总结而言：cookie弥补了http无状态的不足，让服务器知道来的人是“谁”；但是cookie以文本的形式保存在本地，自身安全性较差；所以我们就通过cookie识别不同的用户，对应的在session里保存私密的信息以及超过4096字节的文本。

另外，上述所说的cookie和session其实是共通性的东西，不限于语言和框架

## 登陆应用

前几节的介绍中我们已经有能力制作一个登陆页面，在验证了用户名和密码的正确性后跳转到后台的页面。但是测试后也发现，如果绕过登陆页面。直接输入后台的url地址也可以直接访问的。这个显然是不合理的。其实我们缺失的就是cookie和session配合的验证。有了这个验证过程，我们就可以实现和其他网站一样必须登录才能进入后台页面了。

   先说一下这种认证的机制。每当我们使用一款浏览器访问一个登陆页面的时候，一旦我们通过了认证。服务器端就会发送一组随机唯一的字符串（假设是123abc）到浏览器端，这个被存储在浏览端的东西就叫cookie。而服务器端也会自己存储一下用户当前的状态，比如login=true，username=hahaha之类的用户信息。但是这种存储是以字典形式存储的，字典的唯一key就是刚才发给用户的唯一的cookie值。那么如果在服务器端查看session信息的话，理论上就会看到如下样子的字典

{'123abc':{'login':true,'username:hahaha'}}

因为每个cookie都是唯一的，所以我们在电脑上换个浏览器再登陆同一个网站也需要再次验证。那么为什么说我们只是理论上看到这样子的字典呢？因为处于安全性的考虑，其实对于上面那个大字典不光key值123abc是被加密的，value值{'login':true,'username:hahaha'}在服务器端也是一样被加密的。所以我们服务器上就算打开session信息看到的也是类似与以下样子的东西

{'123abc':dasdasdasd1231231da1231231}

知道了原理，下面就来用代码实现。

## Django实现的COOKIE

### **1、获取Cookie**

```
request.COOKIES['key']
request.get_signed_cookie(key, default=RAISE_ERROR, salt='', max_age=None)
    #参数：
        default: 默认值
           salt: 加密盐
        max_age: 后台控制过期时间
```

### **2、设置Cookie**

```
rep = HttpResponse(...) 或 rep ＝ render(request, ...) 或 rep ＝ redirect()
 
rep.set_cookie(key,value,...)
rep.set_signed_cookie(key,value,salt='加密盐',...)　
```

 **参数：**

```
'''

def set_cookie(self, key,                 键
　　　　　　　　　　　　 value='',            值
　　　　　　　　　　　　 max_age=None,        超长时间
　　　　　　　　　　　　 expires=None,        超长时间
　　　　　　　　　　　　 path='/',           Cookie生效的路径，
                                         浏览器只会把cookie回传给带有该路径的页面，这样可以避免将
                                         cookie传给站点中的其他的应用。
                                         / 表示根路径，特殊的：根路径的cookie可以被任何url的页面访问
　　　　　　　　　　　　 
                     domain=None,         Cookie生效的域名
                                        
                                          你可用这个参数来构造一个跨站cookie。
                                          如， domain=".example.com"
                                          所构造的cookie对下面这些站点都是可读的：
                                          www.example.com 、 www2.example.com 　　　　　　　　　　　　　　　　　　　　　　　　　和an.other.sub.domain.example.com 。
                                          如果该参数设置为 None ，cookie只能由设置它的站点读取。

　　　　　　　　　　　　 secure=False,        如果设置为 True ，浏览器将通过HTTPS来回传cookie。
　　　　　　　　　　　　 httponly=False       只能http协议传输，无法被JavaScript获取
                                         （不是绝对，底层抓包可以获取到也可以被覆盖）
　　　　　　　　　　): pass

'''


```

[![复制代码](assets2.0/copycode-20211113232840780.gif)](javascript:void(0);)

由于cookie保存在客户端的电脑上，所以，JavaScript和jquery也可以操作cookie。

```
<script src='/static/js/jquery.cookie.js'>
 
</script> $.cookie("key", value,{ path: '/' });
```

### **3 删除cookie**

```
response.delete_cookie("cookie_key",path="/",domain=name)
	
```

 cookie存储到客户端
    优点：
      数据存在在客户端，减轻服务器端的压力，提高网站的性能。
    缺点：
      安全性不高：在客户端机很容易被查看或破解用户会话信息

## Django实现的SESSION

### **1、 基本操作**

```
1、设置Sessions值
          request.session['session_name'] ="admin"
2、获取Sessions值
          session_name = request.session["session_name"]
3、删除Sessions值
          del request.session["session_name"]
4、检测是否操作session值
          if "session_name" is request.session :

5、get(key, default=None)
 
fav_color = request.session.get('fav_color', 'red')
 
6、pop(key)
 
fav_color = request.session.pop('fav_color')
 
7、keys()
 
8、items()
 
9、setdefault()
 
10、flush() 删除当前的会话数据并删除会话的Cookie。
            这用于确保前面的会话数据不可以再次被用户的浏览器访问
            例如，django.contrib.auth.logout() 函数中就会调用它。
 
 
11 用户session的随机字符串
        request.session.session_key
  
        # 将所有Session失效日期小于当前日期的数据删除
        request.session.clear_expired()
  
        # 检查 用户session的随机字符串 在数据库中是否
        request.session.exists("session_key")
  
        # 删除当前用户的所有Session数据
        request.session.delete("session_key")
  
        request.session.set_expiry(value)
            * 如果value是个整数，session会在些秒数后失效。
            * 如果value是个datatime或timedelta，session就会在这个时间后失效。
            * 如果value是0,用户关闭浏览器session就会失效。
            * 如果value是None,session会依赖全局session失效策略。
```

### **2、 流程解析图**

![img](assets2.0/877318-20170929173142981-2106190717.png)

###  **3、 示例**

**views:**

```
def log_in(request):

    if request.method=="POST":
        username=request.POST['user']
        password=request.POST['pwd']

        user=UserInfo.objects.filter(username=username,password=password)

        if user:
            #设置session内部的字典内容
            request.session['is_login']='true'
            request.session['username']=username

            #登录成功就将url重定向到后台的url
            return redirect('/backend/')

    #登录不成功或第一访问就停留在登录页面
    return render(request,'login.html')

def backend(request):
    print(request.session,"------cookie")
    print(request.COOKIES,'-------session')
    """
    这里必须用读取字典的get()方法把is_login的value缺省设置为False，
    当用户访问backend这个url先尝试获取这个浏览器对应的session中的
    is_login的值。如果对方登录成功的话，在login里就已经把is_login
    的值修改为了True,反之这个值就是False的
    """

    is_login=request.session.get('is_login',False)
    #如果为真，就说明用户是正常登陆的
    if is_login:
        #获取字典的内容并传入页面文件
        cookie_content=request.COOKIES
        session_content=request.session

        username=request.session['username']

        return render(request,'backend.html',locals())
    else:
        """
        如果访问的时候没有携带正确的session，
        就直接被重定向url回login页面
        """
        return redirect('/login/')

def log_out(request):
    """
    直接通过request.session['is_login']回去返回的时候，
    如果is_login对应的value值不存在会导致程序异常。所以
    需要做异常处理
    """
    try:
        #删除is_login对应的value值
        del request.session['is_login']
        
        # OR---->request.session.flush() # 删除django-session表中的对应一行记录

    except KeyError:
        pass
    #点击注销之后，直接重定向回登录页面
    return redirect('/login/')
```



**template:**

```html
===================================login.html==================
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<form action="/login/" method="post">
    <p>用户名: <input type="text" name="user"></p>
    <p>密码: <input type="password" name="pwd"></p>
    <p><input type="submit"></p>
</form>


</body>
</html>


===================================backend.html==================

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

<h3>hello {{ username }}</h3>
<a href="/logout/">注销</a>

</body>
</html>
```



### **4、session存储的相关配置**

**（1）数据库配置（默认）：**

```
Django默认支持Session，并且默认是将Session数据存储在数据库中，即：django_session 表中。
  
a. 配置 settings.py
  
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'   # 引擎（默认）
      
    SESSION_COOKIE_NAME ＝ "sessionid"                       # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
    SESSION_COOKIE_PATH ＝ "/"                               # Session的cookie保存的路径（默认）
    SESSION_COOKIE_DOMAIN = None                             # Session的cookie保存的域名（默认）
    SESSION_COOKIE_SECURE = False                            # 是否Https传输cookie（默认）
    SESSION_COOKIE_HTTPONLY = True                           # 是否Session的cookie只支持http传输（默认）
    SESSION_COOKIE_AGE = 1209600                             # Session的cookie失效日期（2周）（默认）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                  # 是否关闭浏览器使得Session过期（默认）
    SESSION_SAVE_EVERY_REQUEST = False                       # 是否每次请求都保存Session，默认修改之后才保存（默认）

```

**（2）缓存配置**　

```
a. 配置 settings.py
  
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
    SESSION_CACHE_ALIAS = 'default'                            # 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
  
  
    SESSION_COOKIE_NAME ＝ "sessionid"                        # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
    SESSION_COOKIE_PATH ＝ "/"                                # Session的cookie保存的路径
    SESSION_COOKIE_DOMAIN = None                              # Session的cookie保存的域名
    SESSION_COOKIE_SECURE = False                             # 是否Https传输cookie
    SESSION_COOKIE_HTTPONLY = True                            # 是否Session的cookie只支持http传输
    SESSION_COOKIE_AGE = 1209600                              # Session的cookie失效日期（2周）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                   # 是否关闭浏览器使得Session过期
    SESSION_SAVE_EVERY_REQUEST = False                        # 是否每次请求都保存Session，默认修改之后才保存

```

（3）文件配置

```
a. 配置 settings.py
  
    SESSION_ENGINE = 'django.contrib.sessions.backends.file'    # 引擎
    SESSION_FILE_PATH = None                                    # 缓存文件路径，如果为None，则使用tempfile模块获取一个临时地址tempfile.gettempdir()        
    SESSION_COOKIE_NAME ＝ "sessionid"                          # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
    SESSION_COOKIE_PATH ＝ "/"                                  # Session的cookie保存的路径
    SESSION_COOKIE_DOMAIN = None                                # Session的cookie保存的域名
    SESSION_COOKIE_SECURE = False                               # 是否Https传输cookie
    SESSION_COOKIE_HTTPONLY = True                              # 是否Session的cookie只支持http传输
    SESSION_COOKIE_AGE = 1209600                                # Session的cookie失效日期（2周）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False                     # 是否关闭浏览器使得Session过期
    SESSION_SAVE_EVERY_REQUEST = False                          # 是否每次请求都保存Session，默认修改之后才保存

```



## 用户认证　

## auth模块

```
from django.contrib import auth
```

django.contrib.auth中提供了许多方法，这里主要介绍其中的三个：

### **1 、authenticate()**  

提供了用户认证，即验证用户名以及密码是否正确,一般需要username password两个关键字参数

如果认证信息有效，会返回一个 User 对象。authenticate()会在User 对象上设置一个属性标识那种认证后端认证了该用户，且该信息在后面的登录过程中是需要的。当我们试图登陆一个从数据库中直接取出来不经过authenticate()的User对象会报错的！！

```
user = authenticate(username='someone',password='somepassword')
```

### **2 、login(HttpRequest, user)**　　

该函数接受一个HttpRequest对象，以及一个认证了的User对象

此函数使用django的session框架给某个已认证的用户附加上session id等信息。

```
from django.contrib.auth import authenticate, login
   
def my_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    login(request, user)
    # Redirect to a success page.
    ...
  else:
    # Return an 'invalid login' error message.
    ...
```

### **3 、logout(request) 注销用户**　　

```
from django.contrib.auth import logout
   
def logout_view(request):
  logout(request)
  # Redirect to a success page.
```

该函数接受一个HttpRequest对象，无返回值。当调用该函数时，当前请求的session信息会全部清除。该用户即使没有登录，使用该函数也不会报错。

### 4 、user对象的 is_authenticated()

要求：

1 用户登陆后才能访问某些页面，

2 如果用户没有登录就访问该页面的话直接跳到登录页面

3 用户在跳转的登陆界面中完成登陆后，自动访问跳转到之前访问的地址

方法1:

```
def my_view(request):
  if not request.user.is_authenticated():
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

```

方法2:

**django已经为我们设计好了一个用于此种情况的装饰器：login_requierd()**

```
from django.contrib.auth.decorators import login_required
      
@login_required
def my_view(request):
  ...

```

若用户没有登录，则会跳转到django默认的 登录URL '/accounts/login/ ' (这个值可以在settings文件中通过LOGIN_URL进行修改)。并传递 当前访问url的绝对路径 (登陆成功后，会重定向到该路径)。

## User对象

User 对象属性：username， password（必填项）password用哈希算法保存到数据库

is_staff ： 用户是否拥有网站的管理权限.

is_active ： 是否允许用户登录, 设置为``False``，可以不用删除用户来禁止 用户登录

 

### 2.1 、is_authenticated()

如果是真正的 User 对象，返回值恒为 True 。 用于检查用户是否已经通过了认证。
通过认证并不意味着用户拥有任何权限，甚至也不检查该用户是否处于激活状态，这只是表明用户成功的通过了认证。 这个方法很重要, 在后台用request.user.is_authenticated()判断用户是否已经登录，如果true则可以向前台展示request.user.name

### 2.2 、创建用户

使用 create_user 辅助函数创建用户:

```
from django.contrib.auth.models import User
user = User.objects.create_user（username='',password='',email=''）
```

### 2.3 、check_password(passwd)

```
用户需要修改密码的时候 首先要让他输入原来的密码 ，如果给定的字符串通过了密码检查，返回 ``True
```

### 2.4 、修改密码

使用 set_password() 来修改密码

```
user = User.objects.get(username='')
user.set_password(password='')
user.save　

```

### 2.5 、简单示例

**注册：**

```python
def sign_up(request):
 
    state = None
    if request.method == 'POST':
 
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        email=request.POST.get('email', '')
        username = request.POST.get('username', '')
        if User.objects.filter(username=username):
                state = 'user_exist'
        else:
                new_user = User.objects.create_user(username=username, password=password,email=email)
                new_user.save()
 
                return redirect('/book/')
    content = {
        'state': state,
        'user': None,
    }
    return render(request, 'sign_up.html', content)　　
    
```

**修改密码：**

```python
@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                return redirect("/log_in/")
        else:
            state = 'password_error'
    content = {
        'user': user,
        'state': state,
    }
    return render(request, 'set_password.html', content)
```

　　

# [Django-Ajax](https://www.cnblogs.com/yuanchenqi/articles/7638956.html)

*知识预览*

-   [Ajax准备知识：json](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label0)
-   [Ajax简介](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label1)
-   [jquery实现的ajax](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label2)
-   [JS实现的ajax](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label3)
-   [jQuery.serialize()](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label4)
-   [上传文件](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label5)
-   [同源策略与Jsonp](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label6)
-   [CORS](https://www.cnblogs.com/yuanchenqi/articles/7638956.html#_label7)



## Ajax准备知识：json

## 什么是json？

定义：

```
JSON(JavaScript Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。
它基于 ECMAScript (w3c制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。
简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。
```

讲json对象，不得不提到JS对象：

 

![img](assets2.0/877318-20170825211200714-1635996938.png)

 

合格的json对象：

```
["one", "two", "three"]

{ "one": 1, "two": 2, "three": 3 }

{"names": ["张三", "李四"] }

[ { "name": "张三"}, {"name": "李四"} ]
```



 不合格的json对象：

```
{ name: "张三", 'age': 32 }                     // 属性名必须使用双引号

[32, 64, 128, 0xFFF] // 不能使用十六进制值

{ "name": "张三", "age": undefined }            // 不能使用undefined

{ "name": "张三",
  "birthday": new Date('Fri, 26 Aug 2011 07:13:10 GMT'),
  "getName":  function() {return this.name;}    // 不能使用函数和日期对象
}
```



## stringify与parse方法



```javascript
JSON.parse():     用于将一个 JSON 字符串转换为 JavaScript 对象　
eg:
console.log(JSON.parse('{"name":"Yuan"}'));
console.log(JSON.parse('{name:"Yuan"}')) ;   // 错误
console.log(JSON.parse('[12,undefined]')) ;   // 错误



JSON.stringify(): 用于将 JavaScript 值转换为 JSON 字符串。　
eg:  console.log(JSON.stringify({'name':"egon"})) ; 
```



## 和XML的比较

JSON 格式于2001年由 Douglas Crockford 提出，目的就是取代繁琐笨重的 XML 格式。

JSON 格式有两个显著的优点：书写简单，一目了然；符合 JavaScript 原生语法，可以由解释引擎直接处理，不用另外添加解析代码。所以，JSON迅速被接受，已经成为各大网站交换数据的标准格式，并被写入ECMAScript 5，成为标准的一部分。

XML和JSON都使用结构化方法来标记数据，下面来做一个简单的比较。

用XML表示中国部分省市数据如下：

```xml
<?xml version="1.0" encoding="utf-8"?>
<country>
    <name>中国</name>
    <province>
        <name>黑龙江</name>
        <cities>
            <city>哈尔滨</city>
            <city>大庆</city>
        </cities>
    </province>
    <province>
        <name>广东</name>
        <cities>
            <city>广州</city>
            <city>深圳</city>
            <city>珠海</city>
        </cities>
    </province>
    <province>
        <name>台湾</name>
        <cities>
            <city>台北</city>
            <city>高雄</city>
        </cities>
    </province>
    <province>
        <name>新疆</name>
        <cities>
            <city>乌鲁木齐</city>
        </cities>
    </province>
</country>
```



用JSON表示如下：

```json
{
    "name": "中国",
    "province": [{
        "name": "黑龙江",
        "cities": {
            "city": ["哈尔滨", "大庆"]
        }
    }, {
        "name": "广东",
        "cities": {
            "city": ["广州", "深圳", "珠海"]
        }
    }, {
        "name": "台湾",
        "cities": {
            "city": ["台北", "高雄"]
        }
    }, {
        "name": "新疆",
        "cities": {
            "city": ["乌鲁木齐"]
        }
    }]
}

```



　　可以看到，JSON 简单的语法格式和清晰的层次结构明显要比 XML 容易阅读，并且在数据交换方面，由于 JSON 所使用的字符要比 XML 少得多，可以大大得节约传输数据所占用得带宽。

**注意：**

JSON格式取代了xml给网络传输带来了很大的便利,但是却没有了xml的一目了然,尤其是json数据很长的时候,我们会陷入繁琐复杂的数据节点查找中。

但是国人的一款在线工具 BeJson 、SoJson在线工具让众多程序员、新接触JSON格式的程序员更快的了解JSON的结构，更快的精确定位JSON格式错误。



## Ajax简介

AJAX（Asynchronous Javascript And XML）翻译成中文就是“异步Javascript和XML”。即使用Javascript语言与服务器进行异步交互，传输的数据为XML（当然，传输的数据不只是XML）。

-   同步交互：客户端发出一个请求后，需要等待服务器响应结束后，才能发出第二个请求；
-   异步交互：客户端发出一个请求后，无需等待服务器响应结束，就可以发出第二个请求。

AJAX除了**异步**的特点外，还有一个就是：浏览器页面**局部刷新**；（这一特点给用户的感受是在不知不觉中完成请求和响应过程）

**js实现的局部刷新:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

    <style>
        .error{
            color:red
        }
    </style>
</head>
<body>


<form class="Form">

    <p>姓名  <input class="v1" type="text" name="username" mark="用户名"></p>
    <p>密码  <input class="v1" type="text" name="email" mark="邮箱"></p>
    <p><input type="submit" value="submit"></p>

</form>

<script src="jquery-3.1.1.js"></script>

<script>

    $(".Form :submit").click(function(){

        flag=true;

        $("Form .v1").each(function(){

            var value=$(this).val();
            if (value.trim().length==0){
                 var mark=$(this).attr("mark");
                 var $span=$("<span>");
                 $span.html(mark+"不能为空!");
                 $span.prop("class","error");
                 $(this).after($span);

                 setTimeout(function(){
                      $span.remove();
                 },800);

                 flag=false;
                 return flag;

            }
        });
        return flag
    });

</script>
</body>
</html>
```



## **AJAX常见应用情景**

当我们在百度中输入一个“老”字后，会马上出现一个下拉列表！列表中显示的是包含“传”字的4个关键字。

其实这里就使用了AJAX技术！当文件框发生了输入变化时，浏览器会使用AJAX技术向服务器发送一个请求，查询包含“传”字的前10个关键字，然后服务器会把查询到的结果响应给浏览器，最后浏览器把这4个关键字显示在下拉列表中。

-   整个过程中页面没有刷新，只是刷新页面中的局部位置而已！
-   当请求发出后，浏览器还可以进行其他操作，无需等待服务器的响应！

​    ![img](assets2.0/877318-20161025165534625-1155566124.png)

 

当输入用户名后，把光标移动到其他表单项上时，浏览器会使用AJAX技术向服务器发出请求，服务器会查询名为zhangSan的用户是否存在，最终服务器返回true表示名为lemontree7777777的用户已经存在了，浏览器在得到结果后显示“用户名已被注册！”。

-   整个过程中页面没有刷新，只是局部刷新了；
-   在请求发出后，浏览器不用等待服务器响应结果就可以进行其他操作；

## **AJAX的优缺点**

#### 优点：

-   AJAX使用Javascript技术向服务器发送异步请求；
-   AJAX无须刷新整个页面；
-   因为服务器响应内容不再是整个页面，而是页面中的局部，所以AJAX性能高；



## jquery实现的ajax



```js
{% load staticfiles %}

<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="{% static 'JS/jquery-3.1.1.js' %}"></script>
</head>
<body>

<button class="send_Ajax">send_Ajax</button>

<script>
      //$.ajax的两种使用方式:

      //$.ajax(settings);
      //$.ajax(url,[settings]);


       $(".send_Ajax").click(function(){

           $.ajax({
               url:"/handle_Ajax/",
               type:"POST",
               data:{username:"Yuan",password:123},

               success:function(data){
                   alert(data)
               },

                 //=================== error============

                error: function (jqXHR, textStatus, err) {

                        // jqXHR: jQuery增强的xhr
                        // textStatus: 请求完成状态
                        // err: 底层通过throw抛出的异常对象，值与错误类型有关
                        console.log(arguments);
                    },

                 //=================== complete============

                complete: function (jqXHR, textStatus) {
                    // jqXHR: jQuery增强的xhr
                    // textStatus: 请求完成状态 success | error
                    console.log('statusCode: %d, statusText: %s', jqXHR.status, jqXHR.statusText);
                    console.log('textStatus: %s', textStatus);
                },

                //=================== statusCode============
                statusCode: {
                    '403': function (jqXHR, textStatus, err) {
                        console.log(arguments);  //注意：后端模拟errror方式：HttpResponse.status_code=500
                     },

                    '400': function () {
                    }
                }

           })

       })

</script>
</body>
</html>
```



## view：

```python
import json,time
 
def index(request):
 
    return render(request,"index.html")
 
def handle_Ajax(request):
 
    username=request.POST.get("username")
    password=request.POST.get("password")
 
    print(username,password)
    time.sleep(10)
 
    return HttpResponse(json.dumps("Error Data!"))
```



## $.ajax参数

### 请求参数



```text
######################------------data---------################

       data: 当前ajax请求要携带的数据，是一个json的object对象，ajax方法就会默认地把它编码成某种格式
             (urlencoded:?a=1&b=2)发送给服务端；此外，ajax默认以get方式发送请求。

             function testData() {
               $.ajax("/test",{     //此时的data是一个json形式的对象
                  data:{
                    a:1,
                    b:2
                  }
               });                   //?a=1&b=2
######################------------processData---------################

processData：声明当前的data数据是否进行转码或预处理，默认为true，即预处理；if为false，
             那么对data：{a:1,b:2}会调用json对象的toString()方法，即{a:1,b:2}.toString()
             ,最后得到一个［object，Object］形式的结果。
            
######################------------contentType---------################

contentType：默认值: "application/x-www-form-urlencoded"。发送信息至服务器时内容编码类型。
             用来指明当前请求的数据编码格式；urlencoded:?a=1&b=2；如果想以其他方式提交数据，
             比如contentType:"application/json"，即向服务器发送一个json字符串：
               $.ajax("/ajax_get",{
             
                  data:JSON.stringify({
                       a:22,
                       b:33
                   }),
                   contentType:"application/json",
                   type:"POST",
             
               });                          //{a: 22, b: 33}

             注意：contentType:"application/json"一旦设定，data必须是json字符串，不能是json对象             views.py:   json.loads(request.body.decode("utf8"))


######################------------traditional---------################

traditional：一般是我们的data数据有数组时会用到 ：data:{a:22,b:33,c:["x","y"]},
              traditional为false会对数据进行深层次迭代；
```



### 响应参数

```
/*

dataType：  预期服务器返回的数据类型,服务器端返回的数据会根据这个值解析后，传递给回调函数。
            默认不需要显性指定这个属性，ajax会根据服务器返回的content Type来进行转换；
            比如我们的服务器响应的content Type为json格式，这时ajax方法就会对响应的内容
            进行一个json格式的转换，if转换成功，我们在success的回调函数里就会得到一个json格式
            的对象；转换失败就会触发error这个回调函数。如果我们明确地指定目标类型，就可以使用
            data Type。
            dataType的可用值：html｜xml｜json｜text｜script
            见下dataType实例

*/
```



示例：

```python
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import json

def login(request):

    return render(request,'Ajax.html')


def ajax_get(request):

    l=['alex','little alex']
    dic={"name":"alex","pwd":123}

    #return HttpResponse(l)      #元素直接转成字符串alexlittle alex
    #return HttpResponse(dic)    #字典的键直接转成字符串namepwd
    return HttpResponse(json.dumps(l))
    return HttpResponse(json.dumps(dic))# 传到前端的是json字符串,要想使用,需要JSON.parse(data)

//---------------------------------------------------
    function testData() {

        $.ajax('ajax_get', {
           success: function (data) {
           console.log(data);
           console.log(typeof(data));
           //console.log(data.name);
           //JSON.parse(data);
           //console.log(data.name);
                                     },
           //dataType:"json",
                            }
                       )}

注解:Response Headers的content Type为text/html,所以返回的是String;但如果我们想要一个json对象
    设定dataType:"json"即可,相当于告诉ajax方法把服务器返回的数据转成json对象发送到前端.结果为object
    当然，
        return HttpResponse(json.dumps(a),content_type="application/json")

    这样就不需要设定dataType:"json"了。
    content_type="application/json"和content_type="json"是一样的！
```



## csrf跨站请求伪造

### 方式1

```
$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});
```

### 方式2

```
<form>
{% csrf_token %}
</form>

<script>
$.ajax({
	...
  data:{
  "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val();
  	}
  })
</script>
```

### 方式3：

```
<script src="{% static 'js/jquery.cookie.js' %}"></script>


$.ajax({
 
headers:{"X-CSRFToken":$.cookie('csrftoken')},
 
})
```



## JS实现的ajax

## **AJAX核心（**XMLHttpRequest）

   其实AJAX就是在Javascript中多添加了一个对象：XMLHttpRequest对象。所有的异步交互都是使用XMLHttpServlet对象完成的。也就是说，我们只需要学习一个Javascript的新对象即可。

```
var xmlHttp = new XMLHttpRequest()；（大多数浏览器都支持DOM2规范）
```

注意，各个浏览器对XMLHttpRequest的支持也是不同的！为了处理浏览器兼容问题，给出下面方法来创建XMLHttpRequest对象：

```js
function createXMLHttpRequest() {
        var xmlHttp;
        // 适用于大多数浏览器，以及IE7和IE更高版本
        try{
            xmlHttp = new XMLHttpRequest();
        } catch (e) {
            // 适用于IE6
            try {
                xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                // 适用于IE5.5，以及IE更早版本
                try{
                    xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e){}
            }
        }            
        return xmlHttp;
    }
```



## 使用流程

### 步骤1:  打开与服务器的连接（open方法）

当得到XMLHttpRequest对象后，就可以调用该对象的open()方法打开与服务器的连接了。open()方法的参数如下：

open(method, url, async)：

-   method：请求方式，通常为GET或POST；
-   url：请求的服务器地址，例如：/ajaxdemo1/AServlet，若为GET请求，还可以在URL后追加参数；
-   async：这个参数可以不给，默认值为true，表示异步请求；

```
var xmlHttp = createXMLHttpRequest();
xmlHttp.open("GET", "/ajax_get/?a=1", true);　
```

### **步骤2:  发送请求**

当使用open打开连接后，就可以调用XMLHttpRequest对象的send()方法发送请求了。send()方法的参数为POST请求参数，即对应HTTP协议的请求体内容，若是GET请求，需要在URL后连接参数。

注意：若没有参数，需要给出null为参数！若不给出null为参数，可能会导致FireFox浏览器不能正常发送请求！

```
xmlHttp.send(null);

```

### 步骤3:  接收服务器响应

当请求发送出去后，服务器端就开始执行了，但服务器端的响应还没有接收到。接下来我们来接收服务器的响应。

XMLHttpRequest对象有一个onreadystatechange事件，它会在XMLHttpRequest对象的状态发生变化时被调用。下面介绍一下XMLHttpRequest对象的5种状态：

-   0：初始化未完成状态，只是创建了XMLHttpRequest对象，还未调用open()方法；
-   1：请求已开始，open()方法已调用，但还没调用send()方法；
-   2：请求发送完成状态，send()方法已调用；
-   3：开始读取服务器响应；
-   4：读取服务器响应结束。 

onreadystatechange事件会在状态为1、2、3、4时引发。

　　下面代码会被执行四次！对应XMLHttpRequest的四种状态！

```
xmlHttp.onreadystatechange = function() {
            alert('hello');
        };
```

但通常我们只关心最后一种状态，即读取服务器响应结束时，客户端才会做出改变。我们可以通过XMLHttpRequest对象的readyState属性来得到XMLHttpRequest对象的状态。

```
xmlHttp.onreadystatechange = function() {
            if(xmlHttp.readyState == 4) {
                alert('hello');    
            }
        };
```

其实我们还要关心服务器响应的状态码是否为200，其服务器响应为404，或500，那么就表示请求失败了。我们可以通过XMLHttpRequest对象的status属性得到服务器的状态码。

最后，我们还需要获取到服务器响应的内容，可以通过XMLHttpRequest对象的responseText得到服务器响应内容。

```
xmlHttp.onreadystatechange = function() {
            if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                alert(xmlHttp.responseText);    
            }
        };
```

##  if 发送POST请求

<1>需要设置请求头：xmlHttp.setRequestHeader(“Content-Type”, “application/x-www-form-urlencoded”)；注意 :form表单会默认这个键值对不设定，Web服务器会忽略请求体的内容。

<2>在发送时可以指定请求体了：xmlHttp.send(“username=yuan&password=123”)

## JS实现ajax小结



```
/*
    创建XMLHttpRequest对象；
    调用open()方法打开与服务器的连接；
    调用send()方法发送请求；
    为XMLHttpRequest对象指定onreadystatechange事件函数，这个函数会在

    XMLHttpRequest的1、2、3、4，四种状态时被调用；

    XMLHttpRequest对象的5种状态，通常我们只关心4状态。

    XMLHttpRequest对象的status属性表示服务器状态码，它只有在readyState为4时才能获取到。

    XMLHttpRequest对象的responseText属性表示服务器响应内容，它只有在
    readyState为4时才能获取到！

*/
```



测试代码：

```html
<h1>AJAX</h1>
<button onclick="send()">测试</button>
<div id="div1"></div>


<script>
       function createXMLHttpRequest() {
            try {
                return new XMLHttpRequest();//大多数浏览器
            } catch (e) {
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP");
                } catch (e) {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                }
            }
        }

        function send() {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.onreadystatechange = function() {
                if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    var div = document.getElementById("div1");
                    div.innerText = xmlHttp.responseText;
                    div.textContent = xmlHttp.responseText;
                }
            };

            xmlHttp.open("POST", "/ajax_post/", true);
            //post: xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xmlHttp.send(null);  //post: xmlHttp.send("b=B");
        }


</script>
       
#--------------------------------views.py 
from django.views.decorators.csrf import csrf_exempt

def login(request):
    print('hello ajax')
    return render(request,'index.html')

@csrf_exempt   ＃csrf防御
def ajax_post(request):
    print('ok')
    return HttpResponse('helloyuanhao')
```



## 实例（用户名是否已被注册）

### **7.1**　**功能介绍**

在注册表单中，当用户填写了用户名后，把光标移开后，会自动向服务器发送异步请求。服务器返回true或false，返回true表示这个用户名已经被注册过，返回false表示没有注册过。

客户端得到服务器返回的结果后，确定是否在用户名文本框后显示“用户名已被注册”的错误信息！

### **7.2**　**案例分析**

-   页面中给出注册表单；
-   在username表单字段中添加onblur事件，调用send()方法；
-   send()方法获取username表单字段的内容，向服务器发送异步请求，参数为username；
-   django 的视图函数：获取username参数，判断是否为“yuan”，如果是响应true，否则响应false

参考代码：

```html
<script type="text/javascript">
        function createXMLHttpRequest() {
            try {
                return new XMLHttpRequest();
            } catch (e) {
                try {
                    return new ActiveXObject("Msxml2.XMLHTTP");
                } catch (e) {
                    return new ActiveXObject("Microsoft.XMLHTTP");
                }
            }
        }

        function send() {
            var xmlHttp = createXMLHttpRequest();
            xmlHttp.onreadystatechange = function() {
                if(xmlHttp.readyState == 4 && xmlHttp.status == 200) {
                    if(xmlHttp.responseText == "true") {
                        document.getElementById("error").innerText = "用户名已被注册！";
                        document.getElementById("error").textContent = "用户名已被注册！";
                    } else {
                        document.getElementById("error").innerText = "";
                        document.getElementById("error").textContent = "";
                    }
                }
            };
            xmlHttp.open("POST", "/ajax_check/", true, "json");
            xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            var username = document.getElementById("username").value;
            xmlHttp.send("username=" + username);
        }
</script>

//--------------------------------------------------index.html

<h1>注册</h1>
<form action="" method="post">
用户名：<input id="username" type="text" name="username" onblur="send()"/><span id="error"></span><br/>
密　码：<input type="text" name="password"/><br/>
<input type="submit" value="注册"/>
</form>


//--------------------------------------------------views.py
from django.views.decorators.csrf import csrf_exempt

def login(request):
    print('hello ajax')
    return render(request,'index.html')
    # return HttpResponse('helloyuanhao')

@csrf_exempt
def ajax_check(request):
    print('ok')

    username=request.POST.get('username',None)
    if username=='yuan':
        return HttpResponse('true')
    return HttpResponse('false')
```





## jQuery.serialize()

`serialize()`函数用于**序列化一组表单元素，将表单内容编码为用于提交的字符串**。

`serialize()`函数常用于将表单内容序列化，以便用于AJAX提交。

该函数主要根据**用于提交**的**有效**表单控件的name和value，将它们拼接为一个可直接用于表单提交的文本字符串，该字符串已经过标准的URL编码处理(字符集编码为UTF-8)。

该函数不会序列化不需要提交的表单控件，这和常规的表单提交行为是一致的。例如：不在<form>标签内的表单控件不会被提交、没有name属性的表单控件不会被提交、带有disabled属性的表单控件不会被提交、没有被选中的表单控件不会被提交。

```
与常规表单提交不一样的是：常规表单一般会提交带有name的按钮控件，而serialize()函数不会序列化带有name的按钮控件。更多详情请点击这里。

```

### 语法

jQuery 1.0 新增该函数。

```
jQueryObject.serialize( )

```

### 返回值

`serialize()`函数的返回值为String类型，返回将表单元素编码后的可用于表单提交的文本字符串。

请参考下面这段初始HTML代码：



```html
<form name="myForm" action="http://www.365mini.com" method="post">
    <input name="uid" type="hidden" value="1" />
    <input name="username" type="text" value="张三" />
    <input name="password" type="text" value="123456" />
    <select name="grade" id="grade">
        <option value="1">一年级</option>
        <option value="2">二年级</option>
        <option value="3" selected="selected">三年级</option>
        <option value="4">四年级</option>
        <option value="5">五年级</option>
        <option value="6">六年级</option>
    </select>
    <input name="sex" type="radio" checked="checked" value="1" />男
    <input name="sex" type="radio" value="0" />女
    <input name="hobby" type="checkbox" checked="checked" value="1" />游泳
    <input name="hobby" type="checkbox" checked="checked" value="2" />跑步
    <input name="hobby" type="checkbox" value="3" />羽毛球
    <input name="btn" id="btn" type="button" value="点击" />
```



对<form>元素进行序列化可以直接序列化其内部的所有表单元素。

```
// 序列化<form>内的所有表单元素
// 序列化后的结果：uid=1&username=%E5%BC%A0%E4%B8%89&password=123456&grade=3&sex=1&hobby=1&hobby=2
alert( $("form").serialize() );
```

我们也可以直接对部分表单元素进行序列化。

```
// 序列化所有的text、select、checkbox表单元素
// 序列化后的结果：username=%E5%BC%A0%E4%B8%89&password=123456&grade=3&hobby=1&hobby=2
alert( $(":text, select, :checkbox").serialize() );
```

`serialize()`函数通常用于将表单内容序列化，以便通过AJAX方式提交。

```
$("#btn").click( function(){

    // 将当前表单内容以POST请求的AJAX方式提交到"http://www.365mini.com"
    $.post( "http://www.365mini.com", $("form").serialize(), function( data, textStatus, jqXHR ){
        alert( "AJAX提交成功!" );       
    } );
        
} );
```



## 上传文件

## form表单上传文件

### html

```html
<h3>form表单上传文件</h3>


<form action="/upload_file/" method="post" enctype="multipart/form-data">
    <p><input type="file" name="upload_file_form"></p>
    <input type="submit">
</form>
```



### view

```python
def index(request):

    return render(request,"index.html")


def upload_file(request):
    print("FILES:",request.FILES)
    print("POST:",request.POST)
    return HttpResponse("上传成功!")
```



## Ajax(FormData)

FormData是什么呢？

 

XMLHttpRequest Level 2添加了一个新的接口`FormData`.利用`FormData对象`,我们可以通过JavaScript用一些键值对来模拟一系列表单控件,我们还可以使用XMLHttpRequest的`send()`方法来异步的提交这个"表单".比起普通的ajax,使用`FormData`的最大优点就是我们可以异步上传一个二进制文件.

所有主流浏览器的较新版本都已经支持这个对象了，比如Chrome 7+、Firefox 4+、IE 10+、Opera 12+、Safari 5+。

### **html**

```html
<h3>Ajax上传文件</h3>

<p><input type="text" name="username" id="username" placeholder="username"></p>
<p><input type="file" name="upload_file_ajax" id="upload_file_ajax"></p>

<button id="upload_button">提交</button>
{#注意button标签不要用在form表单中使用#}

<script>
    $("#upload_button").click(function(){
        var username=$("#username").val();
        var upload_file=$("#upload_file_ajax")[0].files[0];

        var formData=new FormData();
        formData.append("username",username);
        formData.append("upload_file_ajax",upload_file);


        $.ajax({
            url:"/upload_file/",
            type:"POST",
            data:formData,
            contentType:false,
            processData:false,

            success:function(){
                alert("上传成功!")
            }
        });


    })
</script>
```



### views

```python
def index(request):
  
    return render(request,"index.html")
  
  
def upload_file(request):
    print("FILES:",request.FILES)
    print("POST:",request.POST)
    return HttpResponse("上传成功!")
```



## 伪造Ajax上传文件

### iframe标签

< iframe >标签规定一个内联框架。

一个内联框架被用来在当前 HTML 文档中嵌入另一个文档。

示例：

```text
<iframe src="http://www.baidu.com" width="1000px" height="600px"></iframe>

```



### iframe+form



```html
<h3>伪造Ajax上传文件</h3>
<form action="/upload_file/" method="post" id="form2" target="ifr" enctype="multipart/form-data">
    <p>
        <iframe name="ifr" id="ifr"></iframe></p>
    <p><input type="file" name="upload_file"></p>
    <p><input type="text" name="user"></p>

    <input type="button" value="提交" id="submitBtn">
</form>

<script>



    $("#submitBtn").click(function(){

        $("#ifr").load(iframeLoaded);
        $("#form2").submit();


    });

    function iframeLoaded(){
        alert(123)
    }

</script>
```



**views**

```python
def index(request):
 
    return render(request,"index.html")
 
def upload_file(request):
    print("FILES:",request.FILES)
    print("POST:",request.POST)
    return HttpResponse("上传成功!")
```



## 同源策略与Jsonp

## 同源策略

同源策略（Same origin policy）是一种约定，它是浏览器最核心也最基本的安全功能，如果缺少了同源策略，则浏览器的正常功能可能都会受到影响。可以说Web是构建在同源策略基础之上的，浏览器只是针对同源策略的一种实现。

同源策略，它是由Netscape提出的一个著名的安全策略。现在所有支持JavaScript 的浏览器都会使用这个策略。所谓同源是指，域名，协议，端口相同。当一个浏览器的两个tab页中分别打开来 百度和谷歌的页面当浏览器的百度tab页执行一个脚本的时候会检查这个脚本是属于哪个页面的，即检查是否同源，只有和百度同源的脚本才会被执行。如果非同源，那么在请求数据时，浏览器会在控制台中报一个异常，提示拒绝访问。

 

### 示例：

**项目1:**

```html
==================================http://127.0.0.1:8001项目的index
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
</head>
<body>


<button>ajax</button>
{% csrf_token %}

<script>
    $("button").click(function(){


        $.ajax({
            url:"http://127.0.0.1:7766/SendAjax/",
            type:"POST",
            data:{"username":"yuan","csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
            success:function(data){
                alert(123);
                alert(data)
            }
        })
    })
</script>
</body>
</html>


==================================http://127.0.0.1:8001项目的views

def index(request):


    return render(request,"index.html")


def ajax(request):
    import json
    print(request.POST,"+++++++++++")
    return HttpResponse(json.dumps("hello"))
```



**项目2:**

```html
==================================http://127.0.0.1:8001项目的index
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="http://code.jquery.com/jquery-latest.js"></script>
</head>
<body>


<button>ajax</button>
{% csrf_token %}

<script>
    $("button").click(function(){


        $.ajax({
            url:"http://127.0.0.1:7766/SendAjax/",
            type:"POST",
            data:{"username":"yuan","csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()},
            success:function(data){
                alert(123);
                alert(data)
            }
        })
    })
</script>
</body>
</html>


==================================http://127.0.0.1:8001项目的views

def index(request):


    return render(request,"index.html")


def ajax(request):
    import json
    print(request.POST,"+++++++++++")
    return HttpResponse(json.dumps("hello"))
```



 当点击项目1的按钮时，发送了请求，但是会发现报错如下：

```
已拦截跨源请求：同源策略禁止读取位于 http://127.0.0.1:7766/SendAjax/ 的远程资源。
（原因：CORS 头缺少 'Access-Control-Allow-Origin'）。


```

但是注意，项目2中的访问已经发生了，说明是浏览器对非同源请求返回的结果做了拦截。

## Jsonp

jsonp是json用来跨域的一个东西。原理是通过script标签的跨域特性来绕过同源策略。

思考：这算怎么回事？

```text
<script src="http://code.jquery.com/jquery-latest.js"></script>
```



 借助script标签，实现跨域请求，示例：

```html
# =============================http://127.0.0.1:8001/index


<button>ajax</button>
{% csrf_token %}

<script>
    function func(name){
        alert(name)
    }
</script>

<script src="http://127.0.0.1:7766/SendAjax/"></script>


# =============================http://127.0.0.1:8002/
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt


def SendAjax(request):

    import json

    print("++++++++")
    # dic={"k1":"v1"}
    return HttpResponse("func('yuan')")  # return HttpResponse("func('%s')"%json.dumps(dic))
```



这其实就是JSONP的简单实现模式，或者说是JSONP的原型：创建一个回调函数，然后在远程服务上调用这个函数并且将JSON 数据形式作为参数传递，完成回调。

将JSON数据填充进回调函数，这就是JSONP的JSON+Padding的含义。

   一般情况下，我们希望这个script标签能够动态的调用，而不是像上面因为固定在html里面所以没等页面显示就执行了，很不灵活。我们可以通过javascript动态的创建script标签，这样我们就可以灵活调用远程服务了。



```
<button onclick="f()">sendAjax</button>

<script>
    function addScriptTag(src){
         var script = document.createElement('script');
         script.setAttribute("type","text/javascript");
         script.src = src;
         document.body.appendChild(script);
         document.body.removeChild(script);
    }


    function func(name){
        alert("hello"+name)
    }

    function f(){
         addScriptTag("http://127.0.0.1:7766/SendAjax/")
    }
</script>
```



为了更加灵活，现在将你自己在客户端定义的回调函数的函数名传送给服务端，服务端则会返回以你定义的回调函数名的方法，将获取的json数据传入这个方法完成回调：

将8001的f()改写为：

```
function f(){
         addScriptTag("http://127.0.0.1:7766/SendAjax/?callbacks=func")
    }

```



8002的views改为：

```
def SendAjax(request):
 
    import json
 
    dic={"k1":"v1"}
 
    print("callbacks:",request.GET.get("callbacks"))
    callbacks=request.GET.get("callbacks")
 
    return HttpResponse("%s('%s')"%(callbacks,json.dumps(dic)))
```



## jQuery对JSONP的实现

### getJSON

jQuery框架也当然支持JSONP，可以使用$.getJSON(url,[data],[callback])方法

8001的html改为：

```
<button onclick="f()">sendAjax</button>

<script>

    function f(){
          $.getJSON("http://127.0.0.1:7766/SendAjax/?callbacks=?",function(arg){
            alert("hello"+arg)
        });
    }
    
</script>
```



8002的views不改动。

结果是一样的，要注意的是在url的后面必须添加一个callback参数，这样getJSON方法才会知道是用JSONP方式去访问服务，callback后面的那个问号是内部自动生成的一个回调函数名。

   此外，如果说我们想指定自己的回调函数名，或者说服务上规定了固定回调函数名该怎么办呢？我们可以使用$.ajax方法来实现

###  $.ajax

8001的html改为：



```
<script>

    function f(){
          $.ajax({
                url:"http://127.0.0.1:7766/SendAjax/",
                dataType:"jsonp",
                jsonp: 'callbacks',
                jsonpCallback:"SayHi"
           });

       }

    function SayHi(arg){
                alert(arg);
            }

</script>
```



8002的views不改动。

**当然，最简单的形式还是通过回调函数来处理：**



```js
<script>

    function f(){

            $.ajax({
               url:"http://127.0.0.1:7766/SendAjax/",
               dataType:"jsonp",            //必须有，告诉server，这次访问要的是一个jsonp的结果。
               jsonp: 'callbacks',          //jQuery帮助随机生成的：callbacks="wner"
               success:function(data){
                   alert("hi "+data)
              }
         });

       }

</script>
```



 jsonp: 'callbacks'就是定义一个存放回调函数的键，jsonpCallback是前端定义好的回调函数方法名'SayHi'，server端接受callback键对应值后就可以在其中填充数据打包返回了; 

jsonpCallback参数可以不定义，jquery会自动定义一个随机名发过去，那前端就得用回调函数来处理对应数据了。利用jQuery可以很方便的实现JSONP来进行跨域访问。　　

注意 JSONP一定是GET请求

###  应用

```js
<input type="button" onclick="AjaxRequest()" value="跨域Ajax" />


<div id="container"></div>


    <script type="text/javascript">
        function AjaxRequest() {
            $.ajax({
                url: 'http://www.jxntv.cn/data/jmd-jxtv2.html?callback=list&_=1454376870403',
                type: 'GET',
                dataType: 'jsonp',
                jsonp: 'callback',
                jsonpCallback: 'list',
                success: function (data) {
                    
                    $.each(data.data,function(i){
                        var item = data.data[i];
                        var str = "<p>"+ item.week +"</p>";
                        $('#container').append(str);
                        $.each(item.list,function(j){
                            var temp = "<a href='" + item.list[j].link +"'>" + item.list[j].name +" </a><br/>";
                            $('#container').append(temp);
                        });
                        $('#container').append("<hr/>");
                    })

                }
            });
        }
</script>
```





# CORS

## 一、简介

CORS需要浏览器和服务器同时支持。目前，所有浏览器都支持该功能，IE浏览器不能低于IE10。

整个CORS通信过程，都是浏览器自动完成，不需要用户参与。对于开发者来说，CORS通信与同源的AJAX通信没有差别，代码完全一样。浏览器一旦发现AJAX请求跨源，就会自动添加一些附加的头信息，有时还会多出一次附加的请求，但用户不会有感觉。

因此，实现CORS通信的关键是服务器。只要服务器实现了CORS接口，就可以跨源通信。

## 二、两种请求

浏览器将CORS请求分成两类：简单请求（simple request）和非简单请求（not-so-simple request）。

只要同时满足以下两大条件，就属于简单请求。



```
（1) 请求方法是以下三种方法之一：
HEAD
GET
POST
（2）HTTP的头信息不超出以下几种字段：
Accept
Accept-Language
Content-Language
Last-Event-ID
Content-Type：只限于三个值application/x-www-form-urlencoded、multipart/form-data、text/plain
```



凡是不同时满足上面两个条件，就属于非简单请求。

浏览器对这两种请求的处理，是不一样的。



```
* 简单请求和非简单请求的区别？

   简单请求：一次请求
   非简单请求：两次请求，在发送数据之前会先发一次请求用于做“预检”，只有“预检”通过后才再发送一次请求用于数据传输。
* 关于“预检”

- 请求方式：OPTIONS
- “预检”其实做检查，检查如果通过则允许传输数据，检查不通过则不再发送真正想要发送的消息
- 如何“预检”
     => 如果复杂请求是PUT等请求，则服务端需要设置允许某请求，否则“预检”不通过
        Access-Control-Request-Method
     => 如果复杂请求设置了请求头，则服务端需要设置允许某请求头，否则“预检”不通过
        Access-Control-Request-Headers
```



 

**支持跨域，简单请求**

服务器设置响应头：Access-Control-Allow-Origin = '域名' 或 '*'

**支持跨域，复杂请求**

由于复杂请求时，首先会发送“预检”请求，如果“预检”成功，则发送真实数据。

-   “预检”请求时，允许请求方式则需服务器设置响应头：Access-Control-Request-Method
-   “预检”请求时，允许请求头则需服务器设置响应头：Access-Control-Request-Headers

 

#  [Django-model基础](https://www.cnblogs.com/yuanchenqi/articles/7552333.html)



*知识预览*

-   [ORM](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label0)
-   [创建表(建立模型)](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label1)
-   [添加表记录](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label2)
-   [查询表记录](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label3)
-   [修改表记录](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label4)
-   [删除表记录](https://www.cnblogs.com/yuanchenqi/articles/7552333.html#_label5)



## ORM

**映射关系：**

```
　　　  表名  <－－－－－－－> 类名

       字段  <－－－－－－－> 属性

　　　　表记录 <－－－－－－－>类实例对象
```



## 创建表(建立模型)

实例：我们来假定下面这些概念，字段和关系

作者模型：一个作者有姓名和年龄。

作者详细模型：把作者的详情放到详情表，包含生日，手机号，家庭住址等信息。作者详情模型和作者模型之间是一对一的关系（one-to-one）

出版商模型：出版商有名称，所在城市以及email。

书籍模型： 书籍有书名和出版日期，一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系就是多对多的关联关系(many-to-many);一本书只应该由一个出版商出版，所以出版商和书籍是一对多关联关系(one-to-many)。

模型建立如下：

```
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    age=models.IntegerField()
 
    # 与AuthorDetail建立一对一的关系
    authorDetail=models.OneToOneField(to="AuthorDetail")
 
class AuthorDetail(models.Model):
 
    nid = models.AutoField(primary_key=True)
    birthday=models.DateField()
    telephone=models.BigIntegerField()
    addr=models.CharField( max_length=64)
    
class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)
    email=models.EmailField()
 
 
class Book(models.Model):
 
    nid = models.AutoField(primary_key=True)
    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    keepNum=models.IntegerField()<br>    commentNum=models.IntegerField()
 
    # 与Publish建立一对多的关系,外键字段建立在多的一方
    publish=models.ForeignKey(to="Publish",to_field="nid")
 
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表
    authors=models.ManyToManyField(to='Author')　　
```

通过logging可以查看翻译成的sql语句

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}　　
```



注意事项：

1、 表的名称`myapp_modelName`，是根据 模型中的元数据自动生成的，也可以覆写为别的名称　　

2、`id` 字段是自动添加的

3、对于外键字段，Django 会在字段名上添加`"_id"` 来创建数据库中的列名

4、这个例子中的`CREATE TABLE` SQL 语句使用PostgreSQL 语法格式，要注意的是Django 会根据settings 中指定的数据库类型来使用相应的SQL 语句。

5、定义好模型之后，你需要告诉Django _使用_这些模型。你要做的就是修改配置文件中的INSTALL_APPSZ中设置，在其中添加`models.py`所在应用的名称。

6、外键字段 ForeignKey 有一个 null=True 的设置(它允许外键接受空值 NULL)，你可以赋给它空值 None 。

## 字段选项

每个字段有一些特有的参数，例如，CharField需要max_length参数来指定`VARCHAR`数据库字段的大小。还有一些适用于所有字段的通用参数。 这些参数在文档中有详细定义，这里我们只简单介绍一些最常用的：



```
(1)null

如果为True，Django 将用NULL 来在数据库中存储空值。 默认值是 False.

(1)blank

如果为True，该字段允许不填。默认为False。
要注意，这与 null 不同。null纯粹是数据库范畴的，而 blank 是数据验证范畴的。
如果一个字段的blank=True，表单的验证将允许该字段是空值。如果字段的blank=False，该字段就是必填的。

(2)default

字段的默认值。可以是一个值或者可调用对象。如果可调用 ，每有新对象被创建它都会被调用。

(3)primary_key

如果为True，那么这个字段就是模型的主键。如果你没有指定任何一个字段的primary_key=True，
Django 就会自动添加一个IntegerField字段做为主键，所以除非你想覆盖默认的主键行为，
否则没必要设置任何一个字段的primary_key=True。

(4)unique

如果该值设置为 True, 这个数据字段的值在整张表中必须是唯一的

(5)choices
由二元组组成的一个可迭代对象（例如，列表或元组），用来给字段提供选择项。 如果设置了choices ，默认的表单将是一个选择框而不是标准的文本框，而且这个选择框的选项就是choices 中的选项。

这是一个关于 choices 列表的例子：

YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)
每个元组中的第一个元素，是存储在数据库中的值；第二个元素是在管理界面或 ModelChoiceField 中用作显示的内容。 在一个给定的 model 类的实例中，想得到某个 choices 字段的显示值，就调用 get_FOO_display 方法(这里的 FOO 就是 choices 字段的名称 )。例如：

from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)


>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large'   
```



更多详见[模型字段参考](http://python.usyiyi.cn/documents/django_182/ref/models/fields.html#manytomany-arguments)

一旦你建立好数据模型之后，django会自动生成一套数据库抽象的API，可以让你执行关于表记录的增删改查的操作。



## 添加表记录

## 普通字段

```
方式1
publish_obj=Publish(name="人民出版社",city="北京",email="renMin@163.com")
publish_obj.save() # 将数据保存到数据库

方式2 
# 返回值publish_obj是添加的记录对象
publish_obj=Publish.objects.create(name="人民出版社",city="北京",email="renMin@163.com")

方式3
表.objects.create(**request.POST.dict())

```

## 外键字段

```
方式1:
   publish_obj=Publish.objects.get(nid=1)
   Book.objects.create(title="金瓶眉",publishDate="2012-12-12",price=665,pageNum=334,publish=publish_obj)
 
方式2:
   Book.objects.create(title="金瓶眉",publishDate="2012-12-12",price=665,pageNum=334,publish_id=1)　　
```

关键点：book_obj.publish是什么？

## 多对多字段

```
book_obj=Book.objects.create(title="追风筝的人",publishDate="2012-11-12",price=69,pageNum=314,publish_id=1)
 
author_yuan=Author.objects.create(name="yuan",age=23,authorDetail_id=1)
author_egon=Author.objects.create(name="egon",age=32,authorDetail_id=2)
 
book_obj.authors.add(author_egon,author_yuan)  # 将某个特定的 model 对象添加到被关联对象集合中。 ======= book_obj.authors.add(*[])
 
book_obj.authors.create()  #创建并保存一个新对象，然后将这个对象加被关联对象的集合中，然后返回这个新对象。

```

关键点：book_obj.authors是什么？　　

解除关系：

```
book_obj.authors.remove()     # 将某个特定的对象从被关联对象集合中去除。====== book_obj.authors.remove(*[])
book_obj.authors.clear()       #清空被关联对象集合。
```

### class RelatedManager

"关联管理器"是在一对多或者多对多的关联上下文中使用的管理器。它存在于下面两种情况：

ForeignKey关系的“另一边”。像这样：

```
from django.db import models
 
class Reporter(models.Model):
    # ...
    pass
 
class Article(models.Model):
    reporter = models.ForeignKey(Reporter)
```

在上面的例子中，管理器reporter.article_set拥有下面的方法。

ManyToManyField关系的两边：

```
class Topping(models.Model):
    # ...
    pass
 
class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)
```

这个例子中，topping.pizza_set 和pizza.toppings都拥有下面的方法。

**add(obj1[, obj2, ...])**

```
把指定的模型对象添加到关联对象集中。

例如：

>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.add(e) # Associates Entry e with Blog b.
在上面的例子中，对于ForeignKey关系，e.save()由关联管理器调用，执行更新操作。然而，在多对多关系中使用add()并不会调用任何 save()方法，而是由QuerySet.bulk_create()创建关系。

延伸：

# 1 *[]的使用
>>> book_obj = Book.objects.get(id=1)
>>> author_list = Author.objects.filter(id__gt=2)
>>> book_obj.authors.add(*author_list)


# 2 直接绑定主键
book_obj.authors.add(*[1,3])  # 将id=1和id=3的作者对象添加到这本书的作者集合中
                              # 应用: 添加或者编辑时,提交作者信息时可以用到.  
```



**create(\**kwargs)**



```
创建一个新的对象，保存对象，并将它添加到关联对象集之中。返回新创建的对象：

>>> b = Blog.objects.get(id=1)
>>> e = b.entry_set.create(
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )

# No need to call e.save() at this point -- it's already been saved.
这完全等价于（不过更加简洁于）：

>>> b = Blog.objects.get(id=1)
>>> e = Entry(
...     blog=b,
...     headline='Hello',
...     body_text='Hi',
...     pub_date=datetime.date(2005, 1, 1)
... )
>>> e.save(force_insert=True)
要注意我们并不需要指定模型中用于定义关系的关键词参数。在上面的例子中，我们并没有传入blog参数给create()。Django会明白新的 Entry对象blog 应该添加到b中。
```



**remove(obj1[, obj2, ...])**

```
从关联对象集中移除执行的模型对象：

>>> b = Blog.objects.get(id=1)
>>> e = Entry.objects.get(id=234)
>>> b.entry_set.remove(e) # Disassociates Entry e from Blog b.
对于ForeignKey对象，这个方法仅在null=True时存在。
```

**clear()**

```
从关联对象集中移除一切对象。

>>> b = Blog.objects.get(id=1)
>>> b.entry_set.clear()
注意这样不会删除对象 —— 只会删除他们之间的关联。

就像 remove() 方法一样，clear()只能在 null=True的ForeignKey上被调用。
```



**set()方法**

先清空，在设置，编辑书籍时即可用到

![img](assets2.0/877318-20171119170926484-683145874-6881349.png)

**注意**

对于所有类型的关联字段，add()、create()、remove()和clear(),set()都会马上更新数据库。换句话说，在关联的任何一端，都不需要再调用save()方法。

**直接赋值：**

通过赋值一个新的可迭代的对象，关联对象集可以被整体替换掉。

```
>>> new_list = [obj1, obj2, obj3]
>>> e.related_set = new_list
```

如果外键关系满足null=True，关联管理器会在添加new_list中的内容之前，首先调用clear()方法来解除关联集中一切已存在对象的关联。否则， new_list中的对象会在已存在的关联的基础上被添加。　　



## 查询表记录

## 查询相关API

```
<1> all():                 查询所有结果
 
<2> filter(**kwargs):      它包含了与所给筛选条件相匹配的对象
 
<3> get(**kwargs):         返回与所给筛选条件相匹配的对象，返回结果有且只有一个，
                           如果符合筛选条件的对象超过一个或者没有都会抛出错误。
 
<5> exclude(**kwargs):     它包含了与所给筛选条件不匹配的对象
 
<4> values(*field):        返回一个ValueQuerySet——一个特殊的QuerySet，运行后得到的并不是一系列
                           model的实例化对象，而是一个可迭代的字典序列
 
<9> values_list(*field):   它与values()非常相似，它返回的是一个元组序列，values返回的是一个字典序列
 
<6> order_by(*field):      对查询结果排序
 
<7> reverse():             对查询结果反向排序
 
<8> distinct():            从返回结果中剔除重复纪录
 
<10> count():              返回数据库中匹配查询(QuerySet)的对象数量。
 
<11> first():              返回第一条记录
 
<12> last():               返回最后一条记录
 
<13> exists():             如果QuerySet包含数据，就返回True，否则返回False
```

注意：一定区分object与querySet的区别 ！！！

## 双下划线之单表查询

```
models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值
 
models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in
 
models.Tb1.objects.filter(name__contains="ven")
models.Tb1.objects.filter(name__icontains="ven") # icontains大小写不敏感
 
models.Tb1.objects.filter(id__range=[1, 2])      # 范围bettwen and
 
startswith，istartswith, endswith, iendswith　
```

## 基于对象的跨表查询 

### 一对多查询（Publish 与 Book）

正向查询(按字段：publish)：

```
# 查询nid=1的书籍的出版社所在的城市<br>
book_obj=Book.objects.get(nid=1)<br>print(book_obj.publish.city) # book_obj.publish 是nid=1的书籍对象关联的出版社对象　　

```

反向查询(按表名：book_set)：

```
# 查询 人民出版社出版过的所有书籍
 
    publish=Publish.objects.get(name="人民出版社")
 
    book_list=publish.book_set.all()  # 与人民出版社关联的所有书籍对象集合
 
    for book_obj in book_list:
        print(book_obj.title)
```

### 一对一查询(Author 与 AuthorDetail)

正向查询(按字段：authorDetail)：

```
# 查询egon作者的手机号
 
    author_egon=Author.objects.get(name="egon")
    print(author_egon.authorDetail.telephone)
```

反向查询(按表名：author)：

```
# 查询所有住址在北京的作者的姓名
 
    authorDetail_list=AuthorDetail.objects.filter(addr="beijing")
 
    for obj in authorDetail_list:
        print(obj.author.name)
```

### 多对多查询 (Author 与 Book)

正向查询(按字段：authors)：

```
# 金瓶眉所有作者的名字以及手机号
 
    book_obj=Book.objects.filter(title="金瓶眉").first()
 
    authors=book_obj.authors.all()
 
    for author_obj in authors:
 
        print(author_obj.name,author_obj.authorDetail.telephone)
```

反向查询(按表名：book_set)：

```
# 查询egon出过的所有书籍的名字
 
    author_obj=Author.objects.get(name="egon")
    book_list=author_obj.book_set.all() #与egon作者相关的所有书籍
 
    for book_obj in book_list:
        print(book_obj.title)
```

**注意：**

你可以通过在 ForeignKey() 和ManyToManyField的定义中设置 related_name 的值来覆写 FOO_set 的名称。例如，如果 Article model 中做一下更改： publish = ForeignKey(Blog, related_name='bookList')，那么接下来就会如我们看到这般：

```
# 查询 人民出版社出版过的所有书籍
 
   publish=Publish.objects.get(name="人民出版社")
 
   book_list=publish.bookList.all()  # 与人民出版社关联的所有书籍对象集合
```

## 基于双下划线的跨表查询 

Django 还提供了一种直观而高效的方式在查询(lookups)中表示关联关系，它能自动确认 SQL JOIN 联系。要做跨关系查询，就使用两个下划线来链接模型(model)间关联字段的名称，直到最终链接到你想要的 model 为止。

关键点：正向查询按字段，反向查询按表明。



```
# 练习1:  查询人民出版社出版过的所有书籍的名字与价格(一对多)

    # 正向查询 按字段:publish

    queryResult=Book.objects　　　　　　　　　　　　.filter(publish__name="人民出版社")　　　　　　　　　　　　.values_list("title","price")

    # 反向查询 按表名:book

    queryResult=Publish.objects　　　　　　　　　　　　　　.filter(name="人民出版社")　　　　　　　　　　　　　　.values_list("book__title","book__price")



# 练习2: 查询egon出过的所有书籍的名字(多对多)

    # 正向查询 按字段:authors:
    queryResult=Book.objects　　　　　　　　　　　　.filter(authors__name="yuan")　　　　　　　　　　　　.values_list("title")

    # 反向查询 按表名:book
    queryResult=Author.objects　　　　　　　　　　　　　　.filter(name="yuan")　　　　　　　　　　　　　　.values_list("book__title","book__price")


# 练习3: 查询人民出版社出版过的所有书籍的名字以及作者的姓名


    # 正向查询
    queryResult=Book.objects　　　　　　　　　　　　.filter(publish__name="人民出版社")　　　　　　　　　　　　.values_list("title","authors__name")
    # 反向查询
    queryResult=Publish.objects　　　　　　　　　　　　　　.filter(name="人民出版社")　　　　　　　　　　　　　　.values_list("book__title","book__authors__age","book__authors__name")


# 练习4: 手机号以151开头的作者出版过的所有书籍名称以及出版社名称

    queryResult=Book.objects　　　　　　　　　　　　.filter(authors__authorDetail__telephone__regex="151")　　　　　　　　　　　　.values_list("title","publish__name")
    
    
```



 注意：

反向查询时，如果定义了related_name ，则用related_name替换表名，例如： publish = ForeignKey(Blog, related_name='bookList')：

```
# 练习1:  查询人民出版社出版过的所有书籍的名字与价格(一对多)
 
    # 反向查询 不再按表名:book,而是related_name:bookList
 
    queryResult=Publish.objects
　　　　　　　　　　　　　　.filter(name="人民出版社")
　　　　　　　　　　　　　　.values_list("bookList__title","bookList__price")
```



## 聚合查询与分组查询

先了解sql中的聚合与分组概念

### `聚合：aggregate`(*args, **kwargs)

```
# 计算所有图书的平均价格
    >>> from django.db.models import Avg
    >>> Book.objects.all().aggregate(Avg('price'))
    {'price__avg': 34.35}
```

`aggregate()`是`QuerySet` 的一个终止子句，意思是说，它返回一个包含一些键值对的字典。键的名称是聚合值的标识符，值是计算出来的聚合值。键的名称是按照字段和聚合函数的名称自动生成出来的。如果你想要为聚合值指定一个名称，可以向聚合子句提供它。

```
>>> Book.objects.aggregate(average_price=Avg('price'))
{'average_price': 34.35}
```

如果你希望生成不止一个聚合，你可以向`aggregate()`子句中添加另一个参数。所以，如果你也想知道所有图书价格的最大值和最小值，可以这样查询：

```
>>> from django.db.models import Avg, Max, Min
>>> Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
{'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}

```

### 分组：annotate()　

为调用的`QuerySet`中每一个对象都生成一个独立的统计值（统计方法用聚合函数）。　

(1) 练习：统计每一本书的作者个数

```
bookList=Book.objects.annotate(authorsNum=Count('authors'))
for book_obj in bookList:
    print(book_obj.title,book_obj.authorsNum)
```



```
SELECT 
"app01_book"."nid", 
"app01_book"."title", 
"app01_book"."publishDate", 
"app01_book"."price", 
"app01_book"."pageNum", 
"app01_book"."publish_id", 
COUNT("app01_book_authors"."author_id") AS "authorsNum" 
FROM "app01_book" LEFT OUTER JOIN "app01_book_authors" 
ON ("app01_book"."nid" = "app01_book_authors"."book_id") 
GROUP BY 
"app01_book"."nid", 
"app01_book"."title", 
"app01_book"."publishDate", 
"app01_book"."price", 
"app01_book"."pageNum", 
"app01_book"."publish_id"


```



解析：

```
'''
Book.objects.annotate(authorsNum=Count('authors'))
拆分解析：
Book.objects等同于Book.objects.all(),翻译成的sql类似于： select id,name,..  from Book
这样得到的对象一定是每一本书对象，有n本书籍记录，就分n个组，不会有重复对象，每一组再由annotate分组统计。'''
```

(2) 如果想对所查询对象的关联对象进行聚合：

练习：统计每一个出版社的最便宜的书

```
publishList=Publish.objects.annotate(MinPrice=Min("book__price"))
 
for publish_obj in publishList:
    print(publish_obj.name,publish_obj.MinPrice)

```

annotate的返回值是querySet，如果不想遍历对象，可以用上valuelist：

```
queryResult= Publish.objects
　　　　　　　　　　　　.annotate(MinPrice=Min("book__price"))
　　　　　　　　　　　　.values_list("name","MinPrice")
print(queryResult)
```

解析同上。

方式2:　

```
queryResult=Book.objects.values("publish__name").annotate(MinPrice=Min('price')) ＃ 思考： if 有一个出版社没有出版过书会怎样？

```

解析：

```
'''
查看 Book.objects.values("publish__name")的结果和对应的sql语句
可以理解为values内的字段即group by的字段'''
```

(3) 统计每一本以py开头的书籍的作者个数：

```
 queryResult=Book.objects
　　　　　　　　　　 .filter(title__startswith="Py")
　　　　　　　　　 　.annotate(num_authors=Count('authors'))
```

(4) 统计不止一个作者的图书：

```
queryResult=Book.objects
　　　　　　　　　　.annotate(num_authors=Count('authors'))
　　　　　　　　　　.filter(num_authors__gt=1)
```

(5) 根据一本图书作者数量的多少对查询集 `QuerySet`进行排序:

```
Book.objects.annotate(num_authors=Count('authors')).order_by('num_authors')

```

(6) 查询各个作者出的书的总价格:



```
# 按author表的所有字段 group by
    queryResult=Author.objects　　　　　　　　　　　　　　.annotate(SumPrice=Sum("book__price"))　　　　　　　　　　　　　　.values_list("name","SumPrice")
    print(queryResult)
    
# 按authors__name group by
    queryResult2=Book.objects.values("authors__name")　　　　　　　　　　　　　　.annotate(SumPrice=Sum("price"))　　　　　　　　　　　　　　.values_list("authors__name","SumPrice")
    print(queryResult2)
```



## F查询与Q查询

### F查询

在上面所有的例子中，我们构造的过滤器都只是将字段值与某个常量做比较。如果我们要对两个字段的值做比较，那该怎么做呢？

Django 提供 F() 来做这样的比较。F() 的实例可以在查询中引用字段，来比较同一个 model 实例中两个不同字段的值。

```
# 查询评论数大于收藏数的书籍
 
   from django.db.models import F
   Book.objects.filter(commnetNum__lt=F('keepNum'))

```

Django 支持 F() 对象之间以及 F() 对象和常数之间的加减乘除和取模的操作。

```
# 查询评论数大于收藏数2倍的书籍
    Book.objects.filter(commnetNum__lt=F('keepNum')*2)

```

修改操作也可以使用F函数,比如将每一本书的价格提高30元：

```
Book.objects.all().update(price=F("price")+30)　

```

### Q查询

`filter()` 等方法中的关键字参数查询都是一起进行“AND” 的。 如果你需要执行更复杂的查询（例如`OR` 语句），你可以使用`Q 对象`。

```
from django.db.models import Q
Q(title__startswith='Py')
```

`Q` 对象可以使用`&` 和`|` 操作符组合起来。当一个操作符在两个`Q` 对象上使用时，它产生一个新的`Q` 对象。

```
bookList=Book.objects.filter(Q(authors__name="yuan")|Q(authors__name="egon"))

```

等同于下面的SQL `WHERE` 子句：

```
WHERE name ="yuan" OR name ="egon"
```

你可以组合`&` 和`|` 操作符以及使用括号进行分组来编写任意复杂的`Q` 对象。同时，`Q` 对象可以使用`~` 操作符取反，这允许组合正常的查询和取反(`NOT`) 查询：

```
bookList=Book.objects.filter(Q(authors__name="yuan") & ~Q(publishDate__year=2017)).values_list("title")

```

查询函数可以混合使用`Q 对象`和关键字参数。所有提供给查询函数的参数（关键字参数或`Q` 对象）都将"AND”在一起。但是，如果出现`Q` 对象，它必须位于所有关键字参数的前面。例如：

```
 bookList=Book.objects.filter(Q(publishDate__year=2016) | Q(publishDate__year=2017),title__icontains="python")
```



# 修改表记录

 ![img](assets2.0/877318-20160727122351763-1427837148.png)

注意：

<1> 第二种方式修改不能用get的原因是：update是QuerySet对象的方法，get返回的是一个model对象，它没有update方法，而filter返回的是一个QuerySet对象(filter里面的条件可能有多个条件符合，比如name＝'alvin',可能有两个name＝'alvin'的行数据)。

<2>在“插入和更新数据”小节中，我们有提到模型的save()方法，这个方法会更新一行里的所有列。 而某些情况下，我们只需要更新行里的某几列。

 

此外，update()方法对于任何结果集（QuerySet）均有效，这意味着你可以同时更新多条记录update()方法会返回一个整型数值，表示受影响的记录条数。

注意，这里因为update返回的是一个整形，所以没法用query属性；对于每次创建一个对象，想显示对应的raw sql，需要在settings加上日志记录部分



# 删除表记录

删除方法就是 delete()。它运行时立即删除对象而不返回任何值。例如：

```
e.delete()
```

你也可以一次性删除多个对象。每个 QuerySet 都有一个 delete() 方法，它一次性删除 QuerySet 中所有的对象。

例如，下面的代码将删除 pub_date 是2005年的 Entry 对象：

```
Entry.objects.filter(pub_date__year=2005).delete()

```

要牢记这一点：无论在什么情况下，QuerySet 中的 delete() 方法都只使用一条 SQL 语句一次性删除所有对象，而并不是分别删除每个对象。如果你想使用在 model 中自定义的 delete() 方法，就要自行调用每个对象的delete 方法。(例如，遍历 QuerySet，在每个对象上调用 delete()方法)，而不是使用 QuerySet 中的 delete()方法。

在 Django 删除对象时，会模仿 SQL 约束 ON DELETE CASCADE 的行为，换句话说，删除一个对象时也会删除与它相关联的外键对象。例如：

```
b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
b.delete()
```

要注意的是： delete() 方法是 QuerySet 上的方法，但并不适用于 Manager 本身。这是一种保护机制，是为了避免意外地调用 Entry.objects.delete() 方法导致 所有的 记录被误删除。如果你确认要删除所有的对象，那么你必须显式地调用：

```
Entry.objects.all().delete()　　

```

如果不想级联删除，可以设置为：

```
pubHouse = models.ForeignKey(to='Publisher', on_delete=models.SET_NULL, blank=True, null=True)
```

 

#  [Django-model进阶](https://www.cnblogs.com/yuanchenqi/articles/7570003.html)



*知识预览*

-   [QuerySet](https://www.cnblogs.com/yuanchenqi/articles/7570003.html#_label0)
-   [中介模型](https://www.cnblogs.com/yuanchenqi/articles/7570003.html#_label1)
-   [查询优化](https://www.cnblogs.com/yuanchenqi/articles/7570003.html#_label2)
-   [extra](https://www.cnblogs.com/yuanchenqi/articles/7570003.html#_label3)
-   [整体插入](https://www.cnblogs.com/yuanchenqi/articles/7570003.html#_label4)



## QuerySet

### 可切片

使用Python 的切片语法来限制`查询集`记录的数目 。它等同于SQL 的`LIMIT` 和`OFFSET` 子句。

```
>>> Entry.objects.all()[:5]      # (LIMIT 5)
>>> Entry.objects.all()[5:10]    # (OFFSET 5 LIMIT 5)
```

不支持负的索引（例如`Entry.objects.all()[-1]`）。通常，`查询集` 的切片返回一个新的`查询集` —— 它不会执行查询。

### 可迭代

```
articleList=models.Article.objects.all()

for article in articleList:
    print(article.title)
```

### 惰性查询

`查询集` 是惰性执行的 —— 创建`查询集`不会带来任何数据库的访问。你可以将过滤器保持一整天，直到`查询集` 需要求值时，Django 才会真正运行这个查询。

```
queryResult=models.Article.objects.all() # not hits database
 
print(queryResult) # hits database
 
for article in queryResult:
    print(article.title)    # hits database

```

 一般来说，只有在“请求”`查询集` 的结果时才会到数据库中去获取它们。当你确实需要结果时，`查询集` 通过访问数据库来*求值*。 关于求值发生的准确时间，参见[*何时计算查询集*](http://python.usyiyi.cn/documents/django_182/ref/models/querysets.html#when-querysets-are-evaluated)。

### 缓存机制

每个`查询集`都包含一个缓存来最小化对数据库的访问。理解它是如何工作的将让你编写最高效的代码。

在一个新创建的`查询集`中，缓存为空。首次对`查询集`进行求值 —— 同时发生数据库查询 ——Django 将保存查询的结果到`查询集`的缓存中并返回明确请求的结果（例如，如果正在迭代`查询集`，则返回下一个结果）。接下来对该`查询集` 的求值将重用缓存的结果。

请牢记这个缓存行为，因为对`查询集`使用不当的话，它会坑你的。例如，下面的语句创建两个`查询集`，对它们求值，然后扔掉它们：

```
print([a.title for a in models.Article.objects.all()])
print([a.create_time for a in models.Article.objects.all()])
```

这意味着相同的数据库查询将执行两次，显然倍增了你的数据库负载。同时，还有可能两个结果列表并不包含相同的数据库记录，因为在两次请求期间有可能有Article被添加进来或删除掉。为了避免这个问题，只需保存`查询集`并重新使用它：

```
queryResult=models.Article.objects.all()
print([a.title for a in queryResult])
print([a.create_time for a in queryResult])
```

#### 何时查询集不会被缓存?

查询集不会永远缓存它们的结果。当只对查询集的部分进行求值时会检查缓存， 如果这个部分不在缓存中，那么接下来查询返回的记录都将不会被缓存。所以，这意味着使用切片或索引来限制查询集将不会填充缓存。

例如，重复获取查询集对象中一个特定的索引将每次都查询数据库：

```
>>> queryset = Entry.objects.all()
>>> print queryset[5] # Queries the database
>>> print queryset[5] # Queries the database again
```

然而，如果已经对全部查询集求值过，则将检查缓存：

```
>>> queryset = Entry.objects.all()
>>> [entry for entry in queryset] # Queries the database
>>> print queryset[5] # Uses cache
>>> print queryset[5] # Uses cache

```

下面是一些其它例子，它们会使得全部的查询集被求值并填充到缓存中：

```
>>> [entry for entry in queryset]
>>> bool(queryset)
>>> entry in queryset
>>> list(queryset)
```

注：简单地打印查询集不会填充缓存。

```
queryResult=models.Article.objects.all()
print(queryResult) #  hits database
print(queryResult) #  hits database
```

### exists()与iterator()方法

#### exists：

简单的使用if语句进行判断也会完全执行整个queryset并且把数据放入cache，虽然你并不需要这些 数据！为了避免这个，可以用exists()方法来检查是否有数据：

```
if queryResult.exists():
    #SELECT (1) AS "a" FROM "blog_article" LIMIT 1; args=()
        print("exists...")
```

#### iterator:

当queryset非常巨大时，cache会成为问题。

处理成千上万的记录时，将它们一次装入内存是很浪费的。更糟糕的是，巨大的queryset可能会锁住系统 进程，让你的程序濒临崩溃。要避免在遍历数据的同时产生queryset cache，可以使用iterator()方法 来获取数据，处理完数据就将其丢弃。



```
objs = Book.objects.all().iterator()
# iterator()可以一次只从数据库获取少量数据，这样可以节省内存
for obj in objs:
    print(obj.title)
#BUT,再次遍历没有打印,因为迭代器已经在上一次遍历(next)到最后一次了,没得遍历了
for obj in objs:
    print(obj.title)
```



当然，使用iterator()方法来防止生成cache，意味着遍历同一个queryset时会重复执行查询。所以使 #用iterator()的时候要当心，确保你的代码在操作一个大的queryset时没有重复执行查询。

总结:

queryset的cache是用于减少程序对数据库的查询，在通常的使用下会保证只有在需要的时候才会查询数据库。 使用exists()和iterator()方法可以优化程序对内存的使用。不过，由于它们并不会生成queryset cache，可能 会造成额外的数据库查询。　



# 中介模型

处理类似搭配 pizza 和 topping 这样简单的多对多关系时，使用标准的`ManyToManyField` 就可以了。但是，有时你可能需要关联数据到两个模型之间的关系上。

例如，有这样一个应用，它记录音乐家所属的音乐小组。我们可以用一个`ManyToManyField` 表示小组和成员之间的多对多关系。但是，有时你可能想知道更多成员关系的细节，比如成员是何时加入小组的。

对于这些情况，Django 允许你指定一个中介模型来定义多对多关系。 你可以将其他字段放在中介模型里面。源模型的`ManyToManyField` 字段将使用`through` 参数指向中介模型。对于上面的音乐小组的例子，代码如下：

```python
from django.db import models
 
class Person(models.Model):
    name = models.CharField(max_length=128)
 
    def __str__(self):              # __unicode__ on Python 2
        return self.name
 
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')
 
    def __str__(self):              # __unicode__ on Python 2
        return self.name
 
class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```

既然你已经设置好`ManyToManyField` 来使用中介模型（在这个例子中就是`Membership`），接下来你要开始创建多对多关系。你要做的就是创建中介模型的实例：

```
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
[<Person: Ringo Starr>]
>>> ringo.group_set.all()
[<Group: The Beatles>]
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
[<Person: Ringo Starr>, <Person: Paul McCartney>]
```

与普通的多对多字段不同，你不能使用`add`、 `create`和赋值语句（比如，`beatles.members = [...]`）来创建关系：

```
# THIS WILL NOT WORK
>>> beatles.members.add(john)
# NEITHER WILL THIS
>>> beatles.members.create(name="George Harrison")
# AND NEITHER WILL THIS
>>> beatles.members = [john, paul, ringo, george]
```

为什么不能这样做？ 这是因为你不能只创建 `Person`和 `Group`之间的关联关系，你还要指定 `Membership`模型中所需要的所有信息；而简单的`add`、`create` 和赋值语句是做不到这一点的。所以它们不能在使用中介模型的多对多关系中使用。此时，唯一的办法就是创建中介模型的实例。

 `remove()`方法被禁用也是出于同样的原因。但是`clear()` 方法却是可用的。它可以清空某个实例所有的多对多关系：

```
>>> # Beatles have broken up
>>> beatles.members.clear()
>>> # Note that this deletes the intermediate model instances
>>> Membership.objects.all()
[]
```



# 查询优化

## 表数据

```
class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    avatar = models.FileField(verbose_name='头像',upload_to = 'avatar/',default="/avatar/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
 
    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))
 
    def __str__(self):
        return self.username
 
class UserFans(models.Model):
    """
    互粉关系表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')
 
class Blog(models.Model):
 
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')
    def __str__(self):
        return self.title
 
class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
 
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
 
class Article(models.Model):
 
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0)
    comment_count= models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True)
    create_time = models.DateField(verbose_name='创建时间')
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
)
 
 
class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )
 
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')
 
 
class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
 
    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
 
    up_count = models.IntegerField(default=0)
 
    def __str__(self):
        return self.content
 
class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)
    models.BooleanField(verbose_name='是否赞')
 
class CommentUp(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    comment = models.ForeignKey("Comment", null=True)
 
 
class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
 
 
 
class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')
```

## select_related

### 简单使用

对于一对一字段（OneToOneField）和外键字段（ForeignKey），可以使用select_related 来对QuerySet进行优化。

select_related 返回一个`QuerySet`，当执行它的查询时它沿着外键关系查询关联的对象的数据。它会生成一个复杂的查询并引起性能的损耗，但是在以后使用外键关系时将不需要数据库查询。

简单说，在对QuerySet使用select_related()函数后，Django会获取相应外键对应的对象，从而在之后需要的时候不必再查询数据库了。

下面的例子解释了普通查询和`select_related()` 查询的区别。

查询id=2的文章的分类名称,下面是一个标准的查询：

```
# Hits the database.
article=models.Article.objects.get(nid=2)
 
# Hits the database again to get the related Blog object.
print(article.category.title)
```



```
'''
 
SELECT
    "blog_article"."nid",
    "blog_article"."title",
    "blog_article"."desc",
    "blog_article"."read_count",
    "blog_article"."comment_count",
    "blog_article"."up_count",
    "blog_article"."down_count",
    "blog_article"."category_id",
    "blog_article"."create_time",
     "blog_article"."blog_id",
     "blog_article"."article_type_id"
             FROM "blog_article"
             WHERE "blog_article"."nid" = 2; args=(2,)
 
SELECT
     "blog_category"."nid",
     "blog_category"."title",
     "blog_category"."blog_id"
              FROM "blog_category"
              WHERE "blog_category"."nid" = 4; args=(4,)
 
 
'''
```



 如果我们使用select_related()函数：

```
articleList=models.Article.objects.select_related("category").all()
 
 
    for article_obj in articleList:
        #  Doesn't hit the database, because article_obj.category
        #  has been prepopulated in the previous query.
        print(article_obj.category.title)
```



```
SELECT
     "blog_article"."nid",
     "blog_article"."title",
     "blog_article"."desc",
     "blog_article"."read_count",
     "blog_article"."comment_count",
     "blog_article"."up_count",
     "blog_article"."down_count",
     "blog_article"."category_id",
     "blog_article"."create_time",
     "blog_article"."blog_id",
     "blog_article"."article_type_id",
 
     "blog_category"."nid",
     "blog_category"."title",
     "blog_category"."blog_id"
 
FROM "blog_article"
LEFT OUTER JOIN "blog_category" ON ("blog_article"."category_id" = "blog_category"."nid");
```



### 多外键查询

这是针对category的外键查询，如果是另外一个外键呢？让我们一起看下：

```
article=models.Article.objects.select_related("category").get(nid=1)
print(article.articledetail)
```

 观察logging结果，发现依然需要查询两次，所以需要改为：

```
article=models.Article.objects.select_related("category","articledetail").get(nid=1)
print(article.articledetail)

```

 或者：

```
article=models.Article.objects
　　　　　　　　　　　　　.select_related("category")
　　　　　　　　　　　　　.select_related("articledetail")
　　　　　　　　　　　　　.get(nid=1)  # django 1.7 支持链式操作
print(article.articledetail)

```

 

```
SELECT
 
    "blog_article"."nid",
    "blog_article"."title",
    ......
 
    "blog_category"."nid",
    "blog_category"."title",
    "blog_category"."blog_id",
 
    "blog_articledetail"."nid",
    "blog_articledetail"."content",
    "blog_articledetail"."article_id"
 
   FROM "blog_article"
   LEFT OUTER JOIN "blog_category" ON ("blog_article"."category_id" = "blog_category"."nid")
   LEFT OUTER JOIN "blog_articledetail" ON ("blog_article"."nid" = "blog_articledetail"."article_id")
   WHERE "blog_article"."nid" = 1; args=(1,)
```

### 深层查询

```
# 查询id=1的文章的用户姓名
 
    article=models.Article.objects.select_related("blog").get(nid=1)
    print(article.blog.user.username)
```

 依然需要查询两次：

```
SELECT
    "blog_article"."nid",
    "blog_article"."title",
    ......
 
     "blog_blog"."nid",
     "blog_blog"."title",
 
   FROM "blog_article" INNER JOIN "blog_blog" ON ("blog_article"."blog_id" = "blog_blog"."nid")
   WHERE "blog_article"."nid" = 1;
 
 
 
 
SELECT
    "blog_userinfo"."password",
    "blog_userinfo"."last_login",
    ......
 
FROM "blog_userinfo"
WHERE "blog_userinfo"."nid" = 1;
```

 这是因为第一次查询没有query到userInfo表，所以，修改如下：

```
article=models.Article.objects.select_related("blog__user").get(nid=1)
print(article.blog.user.username)
```

```
SELECT
 
"blog_article"."nid", "blog_article"."title",
......
 
 "blog_blog"."nid", "blog_blog"."title",
......
 
 "blog_userinfo"."password", "blog_userinfo"."last_login",
......
 
FROM "blog_article"
 
INNER JOIN "blog_blog" ON ("blog_article"."blog_id" = "blog_blog"."nid")
 
INNER JOIN "blog_userinfo" ON ("blog_blog"."user_id" = "blog_userinfo"."nid")
WHERE "blog_article"."nid" = 1;
```



### 总结

1.  select_related主要针一对一和多对一关系进行优化。
2.  select_related使用SQL的JOIN语句进行优化，通过减少SQL查询的次数来进行优化、提高性能。
3.  可以通过可变长参数指定需要select_related的字段名。也可以通过使用双下划线“__”连接字段名来实现指定的递归查询。
4.  没有指定的字段不会缓存，没有指定的深度不会缓存，如果要访问的话Django会再次进行SQL查询。
5.  也可以通过depth参数指定递归的深度，Django会自动缓存指定深度内所有的字段。如果要访问指定深度外的字段，Django会再次进行SQL查询。
6.  也接受无参数的调用，Django会尽可能深的递归查询所有的字段。但注意有Django递归的限制和性能的浪费。
7.  Django >= 1.7，链式调用的select_related相当于使用可变长参数。Django < 1.7，链式调用会导致前边的select_related失效，只保留最后一个。

## prefetch_related()

对于多对多字段（ManyToManyField）和一对多字段，可以使用prefetch_related()来进行优化。

prefetch_related()和select_related()的设计目的很相似，都是为了减少SQL查询的数量，但是实现的方式不一样。后者是通过JOIN语句，在SQL查询内解决问题。但是对于多对多关系，使用SQL语句解决就显得有些不太明智，因为JOIN得到的表将会很长，会导致SQL语句运行时间的增加和内存占用的增加。若有n个对象，每个对象的多对多字段对应Mi条，就会生成Σ(n)Mi 行的结果表。

prefetch_related()的解决方法是，分别查询每个表，然后用Python处理他们之间的关系。

```
# 查询所有文章关联的所有标签
    article_obj=models.Article.objects.all()
    for i in article_obj:
 
        print(i.tags.all())  #4篇文章: hits database 5
```

改为prefetch_related：

```
# 查询所有文章关联的所有标签
    article_obj=models.Article.objects.prefetch_related("tags").all()
    for i in article_obj:
 
        print(i.tags.all())  #4篇文章: hits database 2
```



```
SELECT "blog_article"."nid",
               "blog_article"."title",
               ......
 
FROM "blog_article";
 
 
 
SELECT
  ("blog_article2tag"."article_id") AS "_prefetch_related_val_article_id",
  "blog_tag"."nid",
  "blog_tag"."title",
  "blog_tag"."blog_id"
   FROM "blog_tag"
  INNER JOIN "blog_article2tag" ON ("blog_tag"."nid" = "blog_article2tag"."tag_id")
  WHERE "blog_article2tag"."article_id" IN (1, 2, 3, 4);

```



# extra

```
extra(select=None, where=None, params=None, 
      tables=None, order_by=None, select_params=None)
```

有些情况下，Django的查询语法难以简单的表达复杂的 `WHERE` 子句，对于这种情况, Django 提供了 `extra()` `QuerySet`修改机制 — 它能在 `QuerySet`生成的SQL从句中注入新子句

extra可以指定一个或多个 `参数`,例如 `select`, `where` or `tables`. 这些参数都不是必须的，但是你至少要使用一个!要注意这些额外的方式对不同的数据库引擎可能存在移植性问题.(因为你在显式的书写SQL语句),除非万不得已,尽量避免这样做

### 参数之select

The `select` 参数可以让你在 `SELECT` 从句中添加其他字段信息，它应该是一个字典，存放着属性名到 SQL 从句的映射。

```
queryResult=models.Article
　　　　　　　　　　　.objects.extra(select={'is_recent': "create_time > '2017-09-05'"})
```

结果集中每个 Entry 对象都有一个额外的属性is_recent, 它是一个布尔值，表示 Article对象的create_time 是否晚于2017-09-05.

练习：



```
# in sqlite:
    article_obj=models.Article.objects.filter(nid=1).extra(select={"standard_time":"strftime('%%Y-%%m-%%d',create_time)"}).values("standard_time","nid","title")
    print(article_obj)
    # <QuerySet [{'title': 'MongoDb 入门教程', 'standard_time': '2017-09-03', 'nid': 1}]>
    
```



### 参数之`where` / `tables`

您可以使用`where`定义显式SQL `WHERE`子句 - 也许执行非显式连接。您可以使用`tables`手动将表添加到SQL `FROM`子句。

`where`和`tables`都接受字符串列表。所有`where`参数均为“与”任何其他搜索条件。

举例来讲：

```
queryResult=models.Article
　　　　　　　　　　　.objects.extra(where=['nid in (1,3) OR title like "py%" ','nid>2'])
```



# 整体插入

创建对象时，尽可能使用bulk_create()来减少SQL查询的数量。例如：

```
Entry.objects.bulk_create([
    Entry(headline="Python 3.0 Released"),
    Entry(headline="Python 3.1 Planned")
])
```

...更优于：

```
Entry.objects.create(headline="Python 3.0 Released")
Entry.objects.create(headline="Python 3.1 Planned")
```

注意该方法有很多注意事项，所以确保它适用于你的情况。

这也可以用在ManyToManyFields中，所以：

```
my_band.members.add(me, my_friend)
```

...更优于：

```
my_band.members.add(me)
my_band.members.add(my_friend)
```

...其中Bands和Artists具有多对多关联。



# [Django-admin管理工具](https://www.cnblogs.com/yuanchenqi/articles/8323452.html)



*知识预览*

-   [admin组件使用](https://www.cnblogs.com/yuanchenqi/articles/8323452.html#_label0)
-   [admin源码解析](https://www.cnblogs.com/yuanchenqi/articles/8323452.html#_label1)



# admin组件使用

Django 提供了基于 web 的管理工具。

Django 自动管理工具是 django.contrib 的一部分。你可以在项目的 settings.py 中的 INSTALLED_APPS 看到它：



```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "app01"
]
```



django.contrib是一套庞大的功能集，它是Django基本代码的组成部分。

## 激活管理工具

通常我们在生成项目时会在 urls.py 中自动设置好，



```
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

]
```



当这一切都配置好后，Django 管理工具就可以运行了。

## 使用管理工具

启动开发服务器，然后在浏览器中访问 http://127.0.0.1:8000/admin/，得到登陆界面，

你可以通过命令 **python manage.py createsuperuser** 来创建超级用户。

为了让 admin 界面管理某个数据模型，我们需要先注册该数据模型到 admin



```
from django.db import models

# Create your models here.

class Author(models.Model):

    name=models.CharField( max_length=32)
    age=models.IntegerField()

    def __str__(self):
        return self.name

class Publish(models.Model):

    name=models.CharField( max_length=32)
    email=models.EmailField()

    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)

    publisher=models.ForeignKey(to="Publish")
    authors=models.ManyToManyField(to='Author')

    def __str__(self):
        return self.title
```



## admin的定制

在admin.py中只需要讲Mode中的某个类注册，即可在Admin中实现增删改查的功能，如：

```
admin.site.register(models.UserInfo)
```

但是，这种方式比较简单，如果想要进行更多的定制操作，需要利用ModelAdmin进行操作，如：



```
方式一：
    class UserAdmin(admin.ModelAdmin):
        list_display = ('user', 'pwd',)
 
    admin.site.register(models.UserInfo, UserAdmin) # 第一个参数可以是列表
     
 
方式二：
    @admin.register(models.UserInfo)                # 第一个参数可以是列表
    class UserAdmin(admin.ModelAdmin):
        list_display = ('user', 'pwd',)
```



ModelAdmin中提供了大量的可定制功能，如

1.   list_display，列表时，定制显示的列。

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'pwd', 'xxxxx')
 
    def xxxxx(self, obj):
        return "xxxxx"
```

2.   list_display_links，列表时，定制列可以点击跳转。

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'pwd', 'xxxxx')
    list_display_links = ('pwd',)
```

3.   list_filter，列表时，定制右侧快速筛选。

4.   list_select_related，列表时，连表查询是否自动select_related

5.   list_editable，列表时，可以编辑的列 

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'pwd','ug',)
    list_editable = ('ug',)
```

6.   search_fields，列表时，模糊搜索的功能

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
     
    search_fields = ('user', 'pwd')
```

7.   date_hierarchy，列表时，对Date和DateTime类型进行搜索

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
 
    date_hierarchy = 'ctime'
```

8 inlines，详细页面，如果有其他表和当前表做FK，那么详细页面可以进行动态增加和删除

```
class UserInfoInline(admin.StackedInline): # TabularInline
    extra = 0
    model = models.UserInfo
 
 
class GroupAdminMode(admin.ModelAdmin):
    list_display = ('id', 'title',)
    inlines = [UserInfoInline, ]
```



9 action，列表时，定制action中的操作

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
 
    # 定制Action行为具体方法
    def func(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))
 
    func.short_description = "中文显示自定义Actions"
    actions = [func, ]
 
    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False
 
    # 是否显示选择个数
    actions_selection_counter = True
```



10 定制HTML模板

```
add_form_template = None
change_form_template = None
change_list_template = None
delete_confirmation_template = None
delete_selected_confirmation_template = None
object_history_template = None
```

11 raw_id_fields，详细页面，针对FK和M2M字段变成以Input框形式

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
 
    raw_id_fields = ('FK字段', 'M2M字段',)
```

12 fields，详细页面时，显示字段的字段

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    fields = ('user',)
```

13 exclude，详细页面时，排除的字段

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    exclude = ('user',)
```

14 readonly_fields，详细页面时，只读字段

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
```

15 fieldsets，详细页面时，使用fieldsets标签对数据进行分割显示

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('基本数据', {
            'fields': ('user', 'pwd', 'ctime',)
        }),
        ('其他', {
            'classes': ('collapse', 'wide', 'extrapretty'),  # 'collapse','wide', 'extrapretty'
            'fields': ('user', 'pwd'),
        }),
    )
```



16 详细页面时，M2M显示时，数据移动选择（方向：上下和左右）

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    filter_vertical = ("m2m字段",) # 或filter_horizontal = ("m2m字段",)
```

17 ordering，列表时，数据排序规则

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    或
    def get_ordering(self, request):
        return ['-id', ]
```

18.   radio_fields，详细页面时，使用radio显示选项（FK默认使用select）

```
radio_fields = {"ug": admin.VERTICAL} # 或admin.HORIZONTAL
```

19 form = ModelForm，用于定制用户请求时候表单验证

```
from app01 import models
from django.forms import ModelForm
from django.forms import fields
 
 
class MyForm(ModelForm):
    others = fields.CharField()
 
    class Meta:
        model = models = models.UserInfo
        fields = "__all__"
 
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
 
    form = MyForm
```



20 empty_value_display = "列数据为空时，显示默认值"

```
@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = "列数据为空时，默认显示"
 
    list_display = ('user','pwd','up')
 
    def up(self,obj):
        return obj.user
    up.empty_value_display = "指定列数据为空时，默认显示"
```







```
from django.contrib import admin

# Register your models here.

from .models import *

class BookInline(admin.StackedInline): # TabularInline
    extra = 0
    model = Book

class BookAdmin(admin.ModelAdmin):

    list_display = ("title",'publishDate', 'price',"foo","publisher")
    list_display_links = ('publishDate',"price")
    list_filter = ('price',)
    list_editable=("title","publisher")
    search_fields = ('title',)
    date_hierarchy = 'publishDate'
    preserve_filters=False

    def foo(self,obj):

        return obj.title+str(obj.price)

    # 定制Action行为具体方法
    def func(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))

    func.short_description = "中文显示自定义Actions"
    actions = [func, ]
    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    actions_selection_counter = True

    change_list_template="my_change_list_template.html"


class PublishAdmin(admin.ModelAdmin):
     list_display = ('name', 'email',)
     inlines = [BookInline, ]


admin.site.register(Book, BookAdmin) # 第一个参数可以是列表
admin.site.register(Publish,PublishAdmin)
admin.site.register(Author)
```





# admin源码解析

## 单例模式

**单例模式（Singleton Pattern）**是一种常用的软件设计模式，该模式的主要目的是确保**某一个类只有一个实例存在**。当你希望在整个系统中，某个类只能出现一个实例时，单例对象就能派上用场。

比如，某个服务器程序的配置信息存放在一个文件中，客户端通过一个 AppConfig 的类来读取配置文件的信息。如果在程序运行期间，有很多地方都需要使用配置文件的内容，也就是说，很多地方都需要创建 AppConfig 对象的实例，这就导致系统中存在多个 AppConfig 的实例对象，而这样会严重浪费内存资源，尤其是在配置文件内容很多的情况下。事实上，类似 AppConfig 这样的类，我们希望在程序运行期间只存在一个实例对象。

在 Python 中，我们可以用多种方法来实现单例模式：

-   使用模块
-   使用 `__new__`
-   使用装饰器（decorator）
-   使用元类（metaclass）

### （1）使用 `__new__`

为了使类只能出现一个实例，我们可以使用 `__new__` 来控制实例的创建过程，代码如下：

```
class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)  
        return cls._instance  

class MyClass(Singleton):  
    a = 1
```



在上面的代码中，我们将类的实例和一个类变量 `_instance` 关联起来，如果 `cls._instance` 为 None 则创建实例，否则直接返回 `cls._instance`。

执行情况如下：

```
>>> one = MyClass()
>>> two = MyClass()
>>> one == two
True
>>> one is two
True
>>> id(one), id(two)
(4303862608, 4303862608)
```



### （2）使用模块

其实，**Python 的模块就是天然的单例模式**，因为模块在第一次导入时，会生成 `.pyc` 文件，当第二次导入时，就会直接加载 `.pyc` 文件，而不会再次执行模块代码。因此，我们只需把相关的函数和数据定义在一个模块中，就可以获得一个单例对象了。如果我们真的想要一个单例类，可以考虑这样做：

```
# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass
 
my_singleton = My_Singleton()
```

将上面的代码保存在文件 `mysingleton.py` 中，然后这样使用：

```
from mysingleton import my_singleton
 
my_singleton.foo()
```

## admin执行流程

<1> 循环加载执行所有已经注册的app中的admin.py文件

```
def autodiscover():
    autodiscover_modules('admin', register_to=site)
```

<2> 执行代码

```
＃admin.py

class BookAdmin(admin.ModelAdmin):
    list_display = ("title",'publishDate', 'price')

admin.site.register(Book, BookAdmin) 
admin.site.register(Publish)
```



<3> admin.site 

![img](assets2.0/877318-20180123092346881-320111203.png)

这里应用的是一个单例模式，对于AdminSite类的一个单例模式，执行的每一个app中的每一个admin.site都是一个对象

<4> 执行register方法

```
admin.site.register(Book, BookAdmin) 
admin.site.register(Publish)
```



```
class ModelAdmin(BaseModelAdmin):pass

def register(self, model_or_iterable, admin_class=None, **options):
    if not admin_class:
            admin_class = ModelAdmin
    # Instantiate the admin class to save in the registry
    self._registry[model] = admin_class(model, self)
```



思考：在每一个app的admin .py中加上

```
print(admin.site._registry)   ＃ 执行结果？
```

到这里，注册结束！

<5> admin的URL配置

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```



```
class AdminSite(object):
    
     def get_urls(self):
        from django.conf.urls import url, include
      
        urlpatterns = []

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

      
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'admin', self.name
        
```



<6> url()方法的扩展应用



```
from django.shortcuts import HttpResponse
def test01(request):
    return HttpResponse("test01")

def test02(request):
    return HttpResponse("test02")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^yuan/', ([
                    url(r'^test01/', test01),
                    url(r'^test02/', test02),

                    ],None,None)),

]
```



扩展优化



```
from django.conf.urls import url,include
from django.contrib import admin

from django.shortcuts import HttpResponse

def change_list_view(request):
    return HttpResponse("change_list_view")
def add_view(request):
    return HttpResponse("add_view")
def delete_view(request):
    return HttpResponse("delete_view")
def change_view(request):
    return HttpResponse("change_view")

def get_urls():

    temp=[
        url(r"^$".format(app_name,model_name),change_list_view),
        url(r"^add/$".format(app_name,model_name),add_view),
        url(r"^\d+/del/$".format(app_name,model_name),delete_view),
        url(r"^\d+/change/$".format(app_name,model_name),change_view),
    ]

    return temp


url_list=[]

for model_class,obj in admin.site._registry.items():

    model_name=model_class._meta.model_name
    app_name=model_class._meta.app_label

    # temp=url(r"{0}/{1}/".format(app_name,model_name),(get_urls(),None,None))
    temp=url(r"{0}/{1}/".format(app_name,model_name),include(get_urls()))
    url_list.append(temp)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^yuan/', (url_list,None,None)),
]
```



 

# [Django-进阶](https://www.cnblogs.com/yuanchenqi/articles/7652353.html)



*知识预览*

-   [分页](https://www.cnblogs.com/yuanchenqi/articles/7652353.html#_label0)
-   [中间件](https://www.cnblogs.com/yuanchenqi/articles/7652353.html#_label1)



# 分页

## Django的分页器（paginator）

### view

```
from django.shortcuts import render,HttpResponse

# Create your views here.
from app01.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    '''
    批量导入数据:

    Booklist=[]
    for i in range(100):
        Booklist.append(Book(title="book"+str(i),price=30+i*i))
    Book.objects.bulk_create(Booklist)
    '''

    '''
分页器的使用:

    book_list=Book.objects.all()

    paginator = Paginator(book_list, 10)

    print("count:",paginator.count)           #数据总数
    print("num_pages",paginator.num_pages)    #总页数
    print("page_range",paginator.page_range)  #页码的列表



    page1=paginator.page(1) #第1页的page对象
    for i in page1:         #遍历第1页的所有数据对象
        print(i)

    print(page1.object_list) #第1页的所有数据


    page2=paginator.page(2)

    print(page2.has_next())            #是否有下一页
    print(page2.next_page_number())    #下一页的页码
    print(page2.has_previous())        #是否有上一页
    print(page2.previous_page_number()) #上一页的页码



    # 抛错
    #page=paginator.page(12)   # error:EmptyPage

    #page=paginator.page("z")   # error:PageNotAnInteger

    '''


    book_list=Book.objects.all()

    paginator = Paginator(book_list, 10)
    page = request.GET.get('page',1)
    currentPage=int(page)

    try:
        print(page)
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    return render(request,"index.html",{"book_list":book_list,"paginator":paginator,"currentPage":currentPage})
    
```



### index.html:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" 
    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>

<div class="container">

    <h4>分页器</h4>
    <ul>

        {% for book in book_list %}
             <li>{{ book.title }} -----{{ book.price }}</li>
        {% endfor %}

     </ul>


    <ul class="pagination" id="pager">

                 {% if book_list.has_previous %}
                    <li class="previous"><a href="/index/?page={{ book_list.previous_page_number }}">上一页</a></li>
                 {% else %}
                    <li class="previous disabled"><a href="#">上一页</a></li>
                 {% endif %}


                 {% for num in paginator.page_range %}

                     {% if num == currentPage %}
                       <li class="item active"><a href="/index/?page={{ num }}">{{ num }}</a></li>
                     {% else %}
                       <li class="item"><a href="/index/?page={{ num }}">{{ num }}</a></li>

                     {% endif %}
                 {% endfor %}



                 {% if book_list.has_next %}
                    <li class="next"><a href="/index/?page={{ book_list.next_page_number }}">下一页</a></li>
                 {% else %}
                    <li class="next disabled"><a href="#">下一页</a></li>
                 {% endif %}

            </ul>
</div>

</body>
</html>

```



## 扩展

```python
def index(request):


    book_list=Book.objects.all()

    paginator = Paginator(book_list, 15)
    page = request.GET.get('page',1)
    currentPage=int(page)

    #  如果页数十分多时，换另外一种显示方式
    if paginator.num_pages>30:

        if currentPage-5<1:
            pageRange=range(1,11)
        elif currentPage+5>paginator.num_pages:
            pageRange=range(currentPage-5,paginator.num_pages+1)

        else:
            pageRange=range(currentPage-5,currentPage+5)

    else:
        pageRange=paginator.page_range


    try:
        print(page)
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)

    return render(request,"index.html",locals())
```



## 自定义分页器



```python
"""
分页组件使用示例：

    obj = Pagination(request.GET.get('page',1),len(USER_LIST),request.path_info)
    page_user_list = USER_LIST[obj.start:obj.end]
    page_html = obj.page_html()

    return render(request,'index.html',{'users':page_user_list,'page_html':page_html})


"""

class Pagination(object):

    def __init__(self,current_page,all_count,base_url,per_page_num=2,pager_count=11):
        """
        封装分页相关数据
        :param current_page: 当前页
        :param all_count:    数据库中的数据总条数
        :param per_page_num: 每页显示的数据条数
        :param base_url: 分页中显示的URL前缀
        :param pager_count:  最多显示的页码个数
        """

        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page <1:
            current_page = 1

        self.current_page = current_page

        self.all_count = all_count
        self.per_page_num = per_page_num

        self.base_url = base_url

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager


        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []

        first_page = '<li><a href="%s?page=%s">首页</a></li>' % (self.base_url,1,)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="%s?page=%s">上一页</a></li>' % (self.base_url,self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?page=%s">%s</a></li>' % (self.base_url,i, i,)
            else:
                temp = '<li><a href="%s?page=%s">%s</a></li>' % (self.base_url,i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="%s?page=%s">下一页</a></li>' % (self.base_url,self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="%s?page=%s">尾页</a></li>' % (self.base_url,self.all_pager,)
        page_html_list.append(last_page)

        return ''.join(page_html_list)
```





# 中间件

![img](assets2.0/101822420536468.png)

## 中间件的概念

中间件顾名思义，是介于request与response处理之间的一道处理过程，相对比较轻量级，并且在全局上改变django的输入与输出。因为改变的是全局，所以需要谨慎实用，用不好会影响到性能。

Django的中间件的定义：

```
Middleware is a framework of hooks into Django’s request/response processing. <br>It’s a light, low-level “plugin” system for globally altering Django’s input or output.

```

如果你想修改请求，例如被传送到view中的**HttpRequest**对象。 或者你想修改view返回的**HttpResponse**对象，这些都可以通过中间件来实现。

可能你还想在view执行之前做一些操作，这种情况就可以用 middleware来实现。

大家可能频繁在view使用`request.user`吧。 Django想在每个view执行之前把user设置为request的属性，于是就用了一个中间件来实现这个目标。所以Django提供了可以修改request 对象的中间件 `AuthenticationMiddleware`。

Django默认的`Middleware`：



```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```



每一个中间件都有具体的功能。

## 自定义中间件

中间件中一共有四个方法：

```
process_request

process_view

process_exception

process_response
```



### process_request，process_response

当用户发起请求的时候会依次经过所有的的中间件，这个时候的请求时process_request,最后到达views的函数中，views函数处理后，在依次穿过中间件，这个时候是process_response,最后返回给请求者。

![img](assets2.0/877318-20171012212952512-1143032176-6885135.png)

上述截图中的中间件都是django中的，我们也可以自己定义一个中间件，我们可以自己写一个类，但是必须继承MiddlewareMixin

需要导入

```
from django.utils.deprecation import MiddlewareMixin

```

 ![img](assets2.0/877318-20171012215322324-2079210800-6885136.png)

**in views:**

```
def index(request):

    print("view函数...")
    return HttpResponse("OK")
```

**in Mymiddlewares.py：**



```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
 
    def process_response(self,request,response):
        print("Md1返回")
        return response

class Md2(MiddlewareMixin):

    def process_request(self,request):
        print("Md2请求")
        #return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response
```



**结果：**

```
Md1请求
Md2请求
view函数...
Md2返回
Md1返回
```

**注意：**如果当请求到达请求2的时候直接不符合条件返回，即return HttpResponse("Md2中断")，程序将把请求直接发给中间件2返回，然后依次返回到请求者，结果如下：

返回Md2中断的页面，后台打印如下：

```
Md1请求
Md2请求
Md2返回
Md1返回
```

**流程图如下：**

**![img](assets2.0/877318-20171012223730527-1366794845.png)** 

### process_view

```
process_view(self, request, callback, callback_args, callback_kwargs)
```

 **Mymiddlewares.py**修改如下



```
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Md1view")

class Md2(MiddlewareMixin):

    def process_request(self,request):
        print("Md2请求")
        return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("Md2view")
```



结果如下：



```
Md1请求
Md2请求
Md1view
Md2view
view函数...
Md2返回
Md1返回
```



下图进行分析上面的过程：

![img](assets2.0/997599-20170113093429385-1950865037.png)

当最后一个中间的process_request到达路由关系映射之后，返回到中间件1的process_view，然后依次往下，到达views函数，最后通过process_response依次返回到达用户。

process_view可以用来调用视图函数：

```
class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):

        # return HttpResponse("hello")

        response=callback(request,*callback_args,**callback_kwargs)
        return response
```



结果如下：

```
Md1请求
Md2请求
view函数...
Md2返回
Md1返回
```

注意：process_view如果有返回值，会越过其他的process_view以及视图函数，但是所有的process_response都还会执行。

### process_exception

```
process_exception(self, request, exception)

```

示例修改如下：



```
class Md1(MiddlewareMixin):

    def process_request(self,request):
        print("Md1请求")
        #return HttpResponse("Md1中断")
    def process_response(self,request,response):
        print("Md1返回")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):

        # return HttpResponse("hello")

        # response=callback(request,*callback_args,**callback_kwargs)
        # return response
        print("md1 process_view...")

    def process_exception(self):
        print("md1 process_exception...")



class Md2(MiddlewareMixin):

    def process_request(self,request):
        print("Md2请求")
        # return HttpResponse("Md2中断")
    def process_response(self,request,response):
        print("Md2返回")
        return response
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("md2 process_view...")

    def process_exception(self):
        print("md1 process_exception...")
```



结果如下：



```
Md1请求
Md2请求
md1 process_view...
md2 process_view...
view函数...

Md2返回
Md1返回
```



流程图如下：

当views出现错误时：

![img](assets2.0/877318-20171012235627512-66918024.png)

 将md2的process_exception修改如下：

```
  def process_exception(self,request,exception):

        print("md2 process_exception...")
        return HttpResponse("error")
```

结果如下：

```
Md1请求
Md2请求
md1 process_view...
md2 process_view...
view函数...
md2 process_exception...
Md2返回
Md1返回
```



 







  

　　

　　

　　

 

　

  

 

