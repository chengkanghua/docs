# day08 模块和面向对象等

今日概要：

- 模块
- 面向对象，目的：看的懂代码。（重点 & 不简单）
- 异常处理（重点 & 简单）
- 反射（重点 & 近期用不到 & 理解）
- 网络编程
- 并发编程
  - 爬虫&脚本：自己写线程&进程。（重点）
  - 平台&网站：框架上进行配置。



## 上节作业

1. 关于main主函数

   ```python
   def run():
       pass
   
   
   if __name__ == '__main__':
       run()
   ```

2. 全局变量问题

   ```python
   import requests
   
   
   def func():
       print(res.text)
   
   
   def xxx():
       print(res.text)
   
   
   if __name__ == '__main__':
       res = requests.get("...")
   ```

3. 导入模块

   ```python
   """
   对文件的注释可以写在这里。
   此脚本是用于连接服务器并上传文件的功能....
   """
   import time
   import json
   import datetime
   
   import json
   import openpyxl
   
   import xx
   
   def func():
       pass
   
   
   
   if __name__ == '__main__':
       func()
   ```

4. 关于注释

   ```python
   def func(a1, a2, a3):
       """ 实现下载视频的功能 """
       pass
   
   
   def do(a1, a2, a3):
       """
       函数的功能的注释
       :param a1: 文件路径
       :param a2: 文件路径
       :param a3: 文件路径
       :return xxx
       """
       pass
   ```

5. 输出

   ```python
   import time
   
   for i in range(100):
       message = "\r{}%".format(i)
       print(message, end="")
       time.sleep(0.2)
   ```

6. 关于单元格对象

   ```python
   cell_object = sheet.cell(1,5)
   cell_object.value = "你好"
   cele_object.border = 边框..
   cele_object.border = 边框..
   ```

   ```python
   sheet.cell(1,5).value = "你好"
   
   c = sheet.cell(1,5)
   c1.border = ?
   c1.border = ?
   ```

7. 写Excel的提示

   ```python
   sheet.cell(1,1).value = "ID"
   sheet.cell(1,2).value = "名称"
   sheet.cell(1,3).value = "URL"
   ```

   ```python
   data_list = ["ID","名称","URL"]
   for item in data_list:
       sheet.cell(1,1).value = item
   ```

8. 关于eval

   ```
   - 学习知识点，没问题。
   - 建议不要通篇去用。
   ```

9. 在作业中，比较小的功能写了一个函数来实现。



## 1.模块

### 1.1 bs

针对爬虫取爬取哪些前后端不分离的网站。

```
pip install BeautifulSoup4
```

- 关于HTML格式

  ```html
  <h3> 超级播报：蔚来靠ET5撬动更大市场？ </h3>
  <p>[汽车之家 新能源]  超级播报，每周都有料。本周车圈的大事件不少，新车也非常多，前有丰田连发15款电动车，后有大家期盼已久的蔚来ET5登场，在202...</p>
  <a href="www.baidu.com">百度</a>
  <img src="图片地址" x1="123" x3 ="123" />
  
  image_object.attrs    # {"src":"图片地址","x1":"123","x3":"123"}
  ```

  ```html
  <div id="x1" class='c1'>
      <a href="www.baidu.com">百度</a>
  	<img src="图片地址" />
  </div>
  <div class='c1' >
      <a href="www.baidu.com">百度</a>
  	<img src="图片地址" />
  </div>
  <div class='c1' >
      <a href="www.baidu.com" class='c1'>百度</a>
  	<img src="图片地址" />
  </div>
  ```

- 谷歌浏览器查看元素

  

```python
import requests
from bs4 import BeautifulSoup

# 1.请求并获取结构
res = requests.get("https://www.autohome.com.cn/news/")
text = res.content.decode('gbk')

# 2.获取我们想要的数据
#   - 正则表达式，费劲
#   - bs4，简单
soup = BeautifulSoup(text, features='html.parser')

# 2.1 获取新闻的区域 对象
area_object = soup.find(name='div', attrs={"id": "auto-channel-lazyload-article"})

# 2.2 在之前的基础上找所有的li标签，得到的是列表 [对象,对象,对象]
li_object_list = area_object.find_all(name='li')

# 2.3 循环所有的li_object_list对象
for obj in li_object_list:
    # 2.4 每个li中寻找h3标签
    # 标题
    h3_object = obj.find(name='h3')
    if not h3_object:
        continue
    title = h3_object.text  # <h3>吉利特别股东大会通过增持极氪股份议案</h3>

    # 简介
    p_object = obj.find(name='p')
    summary = p_object.text

    # 图片
    img_object = obj.find(name='img')
    src = img_object.attrs['src']

    # 链接
    a_object = obj.find(name='a')
    url = a_object.attrs['href']
    url_string = "https:{}".format(url)
    
    print(title)
    print(summary)
    print(src)
    print(url_string)
    print('-' * 30)
```



### 小结

```
# 1.创建bs对象
soup = BeautifulSoup(文本, features='html.parser')

# 2.基于对象，根据特点去找标签
标签对象 = soup.find(name="标签名字",attrs={'id':"xx1"})
[标签对象,标签对象] = soup.find_all(name="标签名字",attrs={'id':"xx1",'class':"c1"})

# 3.获取标签对象中的值
标签对象.text
标签对象.attrs
```



### 需求

1. 获取编辑姓名

   ![image-20211219113700518](assets/image-20211219113700518.png)

   ```python
   import requests
   from bs4 import BeautifulSoup
   
   res = requests.get("https://www.autohome.com.cn/news/")
   text = res.content.decode('gbk')
   soup = BeautifulSoup(text, features='html.parser')
   
   area_object = soup.find(name='ul', attrs={"id": "tagInfo"})
   
   li_object_list = area_object.find_all(name='li')
   for obj in li_object_list:
       div_object = obj.find(name='div',attrs={'class':"editorname"})
       # print(div_object.text)
       a_object = div_object.find(name='a')
       print(a_object.text)
   ```

2. 上节作业，提供的案例。

   ```python
   import re
   import requests
   from bs4 import BeautifulSoup
   
   res = requests.get(url="http://s.10010.com/hebei/mobilelist-0-0-0-0-0-0-0-0-177-0-0-p2/")
   
   soup_object = BeautifulSoup(res.text, 'html.parser')
   
   goods_object_list = soup_object.find_all(name='li', attrs={"class": "goodsLi"})
   
   for goods in goods_object_list:
       # 商品ID
       # goods_id = goods.get("goodsid")
       goods_id = goods.attrs['goodsid']
   
       # 商品标题
       title = goods.find(name='p', attrs={"class": "mobileGoodsName"}).find(name='a').text
   
       # 需求1：补充代码实现提取价格中的数字，例如：￥59，则想办法只获取数字部分。
       price_string = goods.find(name="label", attrs={'class': "priceD"}).text
   
       # 需求2：提取评论数量，例如：已有5人评价，想办法只获取数字部分。
       comment_string = goods.find(name="p", attrs={'class': "evalNum"}).text
   
       # 需求3：将已处理好的商品ID、价格、评论数量、商品标题写入到Excel文件中。
       print(goods_id, price_string, comment_string, title)
   
   ```



### 1.2 paramiko

> 代码远程连接的服务器并进行操作。

```
pip install paramiko
```



#### 1.2.1 执行命令

基于用户名和密码：

```python
import paramiko

# 创建SSH对象
ssh = paramiko.SSHClient()

# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname='10.211.55.6', port=22, username='root', password='123')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')

# 获取命令结果
result = stdout.read()

# 关闭连接
ssh.close()
stdout.close()
```



基于公钥和私钥：

> 提前请执行ssh-copy-id。
>
> ```
> ssh-copy-id -i 公钥 root@10.211.55.6
> ```
>
> ```
> ssh root@10.211.55.6
> ```

```python
import paramiko

# 私钥的地址
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')

# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='c1.salt.com', port=22, username='wupeiqi', pkey=private_key)

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
# 获取命令结果
result = stdout.read()

# 关闭连接
ssh.close()

print(result)

```



#### 1.2.2 上传和下载文件

基于用户名和密码 ：

```python
import paramiko
 
transport = paramiko.Transport(('hostname',22))
transport.connect(username='wupeiqi',password='123')
 
sftp = paramiko.SFTPClient.from_transport(transport)
# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/tmp/location.py', '/tmp/test.py')
# 将remove_path 下载到本地 local_path
sftp.get('remove_path', 'local_path')
 
transport.close()
```



基于公钥和私钥：

```python
import paramiko
 
private_key = paramiko.RSAKey.from_private_key_file('/home/auto/.ssh/id_rsa')
 
transport = paramiko.Transport(('hostname', 22))
transport.connect(username='root', pkey=private_key )
 
sftp = paramiko.SFTPClient.from_transport(transport)
# 将location.py 上传至服务器 /tmp/test.py
sftp.put('/tmp/location.py', '/tmp/test.py')

# 将remove_path 下载到本地 local_path
sftp.get('remove_path', 'local_path')
 
transport.close()
```



#### 1.2.3 字符串形式的私钥

```python
import paramiko
from io import StringIO

key_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIB37Le5SbLDddwCNxGlBzbpBa0=
-----END RSA PRIVATE KEY-----"""

private_key = paramiko.RSAKey(file_obj=StringIO(key_str))

print(result)
```



## 2.面向对象

- 有些编程语言：只支持函数式编程。（函数）
- 有些远程语言：只支持面向对象编程。



### 2.1 初识oop

> 实现一个发送邮件的功能。

```python
def send_email(to):
    msg = "给{}发送一个邮件".format(to)
    print(msg)
    
send_email("欧阳")
send_email("王平安")
```

```python
class Info:
    def send_email(self, to):
        msg = "给{}发送一个邮件".format(to)
        print(msg)
        
x = Info()
x.send_email("小魏")
```

- 创建类

  ```python
  class 类名:
  	pass
  ```

- 在类中定义方法

  ```python
  class Info:
      def send_email(self, to):
          ...
  ```

- 先实例化对象

  ```python
  obj = 类名()
  ```

- 调用类中的方法

  ```python
  obj.方法名()
  ```

  

### 2.2 到底什么是对象？

示例1：

![image-20211219155806562](assets/image-20211219155806562.png)

```python
class Info:
    def send_email(self, to):
        msg = "给{}发送一个邮件".format(to)
        print(msg)

# 实例化一个对象
x = Info()
x.v1 = 123
print(x.v1) # 123
x.send_email("陈聪")

y = Info()
y.v1 = 999
y.send_email("王建伟")
```





示例2：

![image-20211219160918666](assets/image-20211219160918666.png)

```python
class Info:
    
    # 实例化对象时，方法会被自动调用。
    def __init__(self,a1):
        self.name = a1
        self.age = 19
        
	def send_email(self):
        msg = "给{}发送一个邮件".format(self.name)
        print(msg)
    
# 实例化对象时，自动执行类中的__init__方法。
x = Info("展翔")  # x.__init__()
y = Info("陈宣良")


x.send_email()
y.send_email()
```



示例3：

```python
def send_email(to,content):
	msg = "给{}发送一个邮件，内容是：{}".format(xto,content)
    print(msg)
    
def send_sms(to,content):
	msg = "给{}发送一个短信，内容是：{}".format(to,content)
    print(msg)
    
def send_wechat(to,content):
	msg = "给{}发送一个微信，内容是：{}".format(to,content)
    print(msg)

    
send_email("陈聪","大帅比")
send_sms("陈聪","大帅比")
send_wechat("陈聪","大帅比")
```



![image-20211219162033564](assets/image-20211219162033564.png)

```python
class Message:
    
	def __init__(self,to,content):
        self.to = to
        self.content = content
        
    def send_email(self):
        msg = "给{}发送邮件，内容：{}".format(self.to,self.content)
        print(msg)

    def send_sms(self):
        msg = "给{}发送短信，内容：{}".format(self.to,self.content)
        print(msg)

    def send_wechat(self):
        msg = "给{}发送微信，内容：{}".format(self.to,self.content)
        print(msg)
        
obj = Message("陈聪","大帅比")
obj.send_emal()
obj.send_sms()
obj.send_wechat()
```



### 2.3 常见的应用场景



#### 2.3.1 数据的封装

```python
user_list = []

while True:
    user = input(">>>")
    pwd = input(">>>")
    info = {"username":user,'password':pwd}
    user_list.append(info)
    
for item in user_list:
    info["username"]
    info["password"]
```

```python
class UserInfo:
    def __init__(self.name,pwd):
        self.username = name
        self.password = pwd

# [对象(username,password),对象,对象,对象,对象,]
user_list = []

while True:
    user = input(">>>")
    pwd = input(">>>")
    # info = {"username":user,'password':pwd}
	obj = UserInfo(user,pwd)
    user_list.append(info)
    
for item in user_list:
    item.username
    item.password
```



案例：

```python
import configparser


def load_config():
    # 读取ini文件
    config = configparser.ConfigParser()
    config.read('settings.ini', encoding='utf-8')
    result = {}
    items = ['wx_url', "min_inventory", 'pool_size', 'max_error_count']
    for key in items:
        value = config.get("settings", key)
        result[key] = value
    return result


def run():
    # 加载配置文件
    data_dict = load_config()
    print(data_dict)
    print("很多其他的功能")
    data_dict['min_inventory']
    data_dict['wx_url']


if __name__ == '__main__':
    run()
```



```python
import configparser


class ConfigContext:
    def __init__(self):
        self.wx_url = str
        self.min_inventory = float
        self.pool_size = int
        self.max_error_count = int


def load_config():
    # 读取ini文件
    config = configparser.ConfigParser()
    config.read('settings.ini', encoding='utf-8')

    obj = ConfigContext()
    for k, convert in obj.__dict__.items():
        value = config.get('settings', k)
        target_type_value = convert(value)
        setattr(obj, k, target_type_value)
    return obj


def run():
    # 加载配置文件
    data_object = load_config()
    print(data_object.wx_url)
    print(data_object.pool_size, type(data_object.pool_size))


if __name__ == '__main__':
    run()
```



#### 2.3.2 很多函数用相同的参数

当函数函数的参数都相同，且反复传递。

```python
class Message:
    
	def __init__(self,to,content):
        self.to = to
        self.content = content
        
    def send_email(self):
        msg = "给{}发送邮件，内容：{}".format(self.to,self.content)
        print(msg)

    def send_sms(self):
        msg = "给{}发送短信，内容：{}".format(self.to,self.content)
        print(msg)

    def send_wechat(self):
        msg = "给{}发送微信，内容：{}".format(self.to,self.content)
        print(msg)
        
obj = Message("陈聪","大帅比")
obj.send_emal()
obj.send_sms()
obj.send_wechat()
```

```python
def send_email(to,content):
	msg = "给{}发送一个邮件，内容是：{}".format(xto,content)
    print(msg)
    
def send_sms(to,content):
	msg = "给{}发送一个短信，内容是：{}".format(to,content)
    print(msg)
    
def send_wechat(to,content):
	msg = "给{}发送一个微信，内容是：{}".format(to,content)
    print(msg)

    
send_email("陈聪","大帅比")
send_sms("陈聪","大帅比")
send_wechat("陈聪","大帅比")
```



#### 2.3.3 创建一类东西

```python
class Police:
    
    def __init__(self,name):
        self.name = name
        self.role = "警察"
	
    def 抓小偷(self):
        pass
    
    def 缉毒(self):
        pass
    
    def 扫黄(self):
        pass
    
v1 = Police("小魏")
v2 = Police("xx")
v3 = Police("xxxx")
```

学习ORM框架：

- 类，对应表。

  ```class
  class UserInfo:
  	def __init__(self,a1,a2,a3):
  		self.id = a1
  		self.name =a2
  		self.age = a3
  ```

- 对象，数据行。

  ```python
  obj1 = UserInfo(1,"xx","xx")
  obj1 = UserInfo(1,"xx","xx")
  obj1 = UserInfo(1,"xx","xx")
  obj1 = UserInfo(1,"xx","xx")
  ```

  

### 2.4 三大特性

三大特性：封装、继承、多态。



#### 2.4.1 封装

```python
class UserInfo:
    def __init__(self,name,pwd):
        self.username = name
        self.password = pwd
        
obj = UserInfo("王建伟","123")


obj.username
obj.password
```



#### 2.4.2 继承

```python
class Base:
	def v1(self):
        pass

class F1(Base):
    def v2(self):
        pass
    
class H1(Base):
    def v3(self):
		pass
```

```
父类、子类
基类、派生类
```



示例1：

![image-20211219175739100](assets/image-20211219175739100.png)

```python
class Base(object):
	def v1(self):
        print("Base.v1")

class Foo(Base):
    def v2(self):
        print("F1.v2")
        
obj = Foo()
obj.v2() # F1.v2
obj.v1() # Base.v1
```



示例2：

```python
class Base(object):
	def v1(self):
        print("Base.v1")

class Foo(Base):
    def v2(self):
        print("F1.v2")
        
	def v1(self):
        print("F1.v1")
        
obj = Foo()
obj.v2() # F1.v2
obj.v1() # F1.v1
```



示例3：

![image-20211219180214214](assets/image-20211219180214214.png)

```python
class Base(object):
	def v1(self):
        print("Base.v1")

class Foo(Base):
    def v2(self):
        print("F1.v2")
        
	def v1(self):
        print("F1.v1")
obj = Base()
obj.v1()
obj.v2()
```

注意：对象.方法时，要找到对象是由那个类创建的，就要从这个类开始找。





示例4：

```python
class Base(object):
	def v1(self):
        print("Base.v1")

class Foo(Base):
    def v2(self):
        print("F1.v2")
        self.v1()

	def v1(self):
        print("F1.v1")
        
obj = Foo()
obj.v2()

>>>F1.v2
>>>F1.v1
```



示例5：

```python
class Base(object):
	def v1(self):
        print("Base.v1")
        
    def v2(self):
        print("F1.v2")
        self.v1()
        
class Foo(Base):
	def v1(self):
        print("F1.v1")
        
obj = Foo()
obj.v2()

>>>F1.v2
>>>F1.v1
```



示例6：

```python
class BaseServer(object):
    def run_server(self):
        self.process_request()
	
    def process_request(self):
        print("BaseServer")
        
class TCPServer(BaseServer):
    pass

class ThreadingTCPServer(TCPServer):
	def process_request(self):
        print("ThreadingTCPServer")

t = ThreadingTCPServer()
t.run_server() # ThreadingTCPServer

t = TCPServer()
t.run_server() # BaseServer

t = BaseServer()
t.run_server() # BaseServer
```



提醒：确保self到底是那个类的对象。



扩展：Python中支持多继承（先去左边再去右边）【c3算法】。

```python
class Base:
    pass

class Foo:
    pass

class Bar(Base,Foo):
    pass
```



#### 2.4.3 多态

- 在Java中

  ```python
  public void send(Foo arg){
      
  }
  
  class Foo:
      pass
  
  arg = Foo()
  send(arg)
  ```

  ```python
  在Java中的多态：
  class Base:
  	pass
  
  class Foo(Base):
      pass
  
  class Bar(Base):
      pass
  
  # 传入arg参数时，可以使：Base类的对象、也可以是Base子类的对象。
  public void send(Base arg){
  }
  
  v1 = Bar()
  send(v1)
  
  v2 = Foo()
  send(v2)
  
  v3 = Base()
  send(v3)
  ```

- 在Python中，天生支持多态（鸭子模型）

  ```python
  def func(a1):
      pass
  ```

  ```python
  def func(a1):
      a1.xx()
  ```



## 3.异常处理

```python
try:
    print(66)
    int("沙河")
    print(999)
except Exception as e:
    print("出现错误了")
```

```python
try:
    print(66)
    int("adafs")
    print(999)
except ValueError as e:
    print("出现错误了")
except Exception as e:
    print("出现错误了")
```

```python
try:
    print(66)
    int("adafs")
    print(999)
except Exception as e:
    print("出现错误了", str(e))
```



```python
try:
    print(66)
    int("adafs")
    print(999)
except Exception as e:
    print("出现错误了", str(e))
finally:
    print("无论如何都会执行")
```



特殊的东西：

```python
def download():
    try:
        return True
    except Exception as e:
        return False
    finally:
        print("结束")
download()
```



特别的东西：

```python
try:
    print(666)
    raise Exception("我错误了") # 主动抛出异常
    print(999)
except Exception as e:
    print("异常了", str(e))
```

































