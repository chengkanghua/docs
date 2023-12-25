## day11 前端基础

- day11，前端基础 & 认识
- day12，前端进阶



课程目标：前端基础 & 认识

- 前端行业的认知 & 课程设计的相关内容
- 实战案例 & 面试（3个）
- HTML、CSS、JS相关内容，案例：加载、模态框、菜单、TAB切换、返回顶部。





## 1. 行业认知

专业的前端开发：

- 基础入门：HTML、CSS、JavaScript、jQuery、BootStrap【类比python函数、数据类型、模块等】
- 前端分离框架：
  - vue.js
  - react.js
  - angular.js
- 学习app开发：
  - react-native，开发ios和安卓app
  - uni-app，开发ios和安卓app
- 微信小程序开发
  - 微信自己的框架，与vue.js极其相似
- 学习一门后端语言
  - node.js，最简单的。
  - Python
  - Go
  - Java

想往全栈方向发展，侧重点：前端。



对于咱们《Python全栈开发》，侧重点：后端。

- 基础入门：HTML、CSS、JavaScript、jQuery、BootStrap。【第5模块 Web前端开发】 + Django框架 =》 ”简单“的项目。
- vue.js 框架：路飞学城项目。【第9模块 路飞项目】   =》 ”复杂“的项目。
  - vue.js 框架-前端
  - django + drf框架-python
  - 路飞业务（项目）
- 微信小程序开发  【第12模块】

自己就具备自学能力，去搞定 uni-app（建议） 和 react-native。





我给大家的定位：

- 去公司做Python开发

  - 稍微有规模公司，不会让你写前端代码。 

    ```
    前端开发，vue.js
    后端开发，python
    ```

  - 初创型公司

    ```
    vue.js代码
    python后端
    
    - 最开始：前端 + 后端
    -   后来：全能（维护&bug修改）   目前：前端 + 后端 => 3年工作经验
    -   后期：前端 + 后端
    ```

- 接私活赚钱

  - 前端 + 后端：5k、2w、10w
  - app + 前端 + 后端
  - 微信小程序 + 后端



关于直播课：

- day11，前端基础，HTML、CSS、JavaScript、jQuery、BootStrap。
- day12，前端进阶，vue.js、微信小程序



## 2. 快速来一遍

https://pythonav.com/wiki/

- [学前必备](https://pythonav.com/wiki/detail/5/61/) 
- [第一章 HTML](https://pythonav.com/wiki/detail/5/60/) 
- [第二章 CSS（一）](https://pythonav.com/wiki/detail/5/62/) 
- [第三章 CSS（二）](https://pythonav.com/wiki/detail/5/65/) 
- [第四章 JavaScript](https://pythonav.com/wiki/detail/5/63/) 
- [第五章 jQuery](https://pythonav.com/wiki/detail/5/64/) （js的类库，模块：动态功能100行，jQuery=10行 -》 动态效果）
- [第六章 BootStrap](https://pythonav.com/wiki/detail/5/66/) （类库：好看样式 + 现成的功能）



我的学习经历：

- 最开始：HTML、CSS、jQuery（多、杂）
- 独立开发平台：找了一个网站模仿（实现功能为主）  -->  美乐乐 



标准：看到任何网站，利用前端知识就可以开发出一个跟他长得一样的东西。



## 3. 知识点 & 案例



### 3.1 函数

```javascript
// 定义函数
function f1(){
	
}

// 执行函数
f1()
```

```javascript
// 定义函数
var f1 = function(){
    
}

// 执行函数
f1()
```

需求，定义一个函数并且立即去执行这个函数。

```javascript
(function(arg){
    // 函数体
    console.log(arg);
})(123)
```



另外的作用，作用域的划分：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script type="text/javascript">
    (function () {
        var v1 = 123;
        var v2 = 456;

        function f1() {
            console.log(v1);
        }
    })()

    (function () {
        var v1 = 666;
        var v2 = 999;

        function f1() {
            console.log(v1);
        }
    })()

</script>
</body>
</html>
```



### 3.2 js中的作用域

注意：我给你讲的以下知识点不涵盖es6的语法。

1. “JavaScript中无块级作用域”

   ```javascript
   function Main(){
       if(1==1){
           var name = 'seven';
       }
       console.log(name);
   }
   
   Main();
   
   // 输出： seven （Python）
   ```

2. ”JavaScript采用函数作用域“

   ```javascript
   function Main(){
       var innerValue = 'seven';
   }
    
   Main();
    
   console.log(innerValue); // 报错
   ```

3. 关于作用域链

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Title</title>
   </head>
   <body>
   <script type="text/javascript">
       xo = 'alex';
   
       function Func() {
           // var xo = "seven";
   
           function inner() {
               // var xo = 'alvin';
               console.log(xo);
           }
   
           inner();
       }
   
   	
       Func();
   
   </script>
   </body>
   </html>
   ```

   ```javascript
   xo = 'alex';
    
   function Func(){
       var xo = "seven";
       function inner(){
           console.log(xo);
       }
       return inner;
   }
   var ret = Func();
   ret();
   ```

4. JavaScript的作用域链执行前已创建

   ```javascript
   xo = 'alex';
    
   function Func(){
       var xo = "seven";
       function inner(){
           console.log(xo);
       }
       return inner;
   }
   
   var ret = Func();
   ret();
   ```

   ```javascript
   xo = 'alex';
    
   function Func(){
       var xo = "eirc";
       function inner(){
           console.log(xo);
       }
       xo = 'seven';
       return inner;
   }
    
   var ret = Func();
   ret();
   ```

   ```javascript
   xo = 'alex';
   function Bar(){
       console.log(xo);
   }
    
   function Func(){
       var xo = "seven";
        
       return Bar;
   }
    
   var ret = Func();
   ret();
   ```

5. 声明提前

   ```
   var v1 = 123;
   console.log(v1);
   ```

   ```javascript
   console.log(v1);
   var v1 = 123;
   ```

   ```javascript
   function func(){
       // var v1;
       console.log(v1); // undefined
   	var v1 = 123;
   }
   
   func();
   ```

   

### 3.3 this到底是个啥？

```
function f1(){
	console.log(this); // window
}

f1();
window.f1();
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<script type="text/javascript">
    v1 = "alex"
    function f1() {
        var v1 = "eric";
        console.log(this.v1); // alex
        console.log(v1); // eric
    }
    // window.v1    window.f1
    window.f1();

</script>
</body>
</html>
```

```javascript
(function(){
    console.log(this);
})()
```



```javascript
name = "alex";

info = {
    name:"eric",
    age:123,
    func:function(){
        console.log(this);      // info
        console.log(this.name); // info.name => eric
    }
}

info.func()
```



```javascript
name = "alex";

info = {
    name:"eric",
    age:123,
    func:function(){
        // 作用域，this=info
        console.log(this.name); // info.name => eric
        function f1(){
            // 作用域 this=window
            console.log(this.name); // window.name => alex
        }
        f1(); // window.f1()
    }
}

info.func()

// 函数在执行 window
```

```javascript
name = "alex";

info = {
    name:"eric",
    age:123,
    func:function(){
        // 作用域，this=info
        console.log(this.name); // info.name => eric
        (function(){
	        // 作用域，this=window
            console.log(this.name);  // alex
        })();
    }
}

info.func()

// 函数在执行 window
```

```javascript
name = "alex";

info = {
    name:"eric",
    age:123,
    func:function(){
        // 作用域，this=info;  that = info;
        var that = this;
        (function(){
            // this=window
            console.log(that.name);  // info.name => eric
        })();
    }
}

info.func()

// 函数在执行 window
```

注意：es6语法， let & 箭头函数



### 3.4 闭包

需求来了，假设我给你一个数组。

```
imageList = [
    "https://hcdn2.luffycity.com/media/frontend/public_class/web1@2x(1)_1566529822.6339395.png",
    "https://hcdn2.luffycity.com/media/frontend/public_class/PY1@2x_1566529821.1110113.png",
    "https://hcdn2.luffycity.com/media/frontend/course/小程序列表图.png",
];
```

请读取三个URL并创建3个img标签，将img图片添加到页面中。

```html
<div id='container'>
    <img src="https://hcdn2.luffycity.com/media/frontend/public_class/web1@2x(1)_1566529822.6339395.png" />
    ...
</div>
```

并且为 img标签绑定点击事件， 点击显示这个URL在列表中的索引位置。



#### 示例1

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #container img{
            width: 400px;
            margin-left: 20px;
        }
    </style>
</head>
<body>
<div id="container">

</div>

<script type="text/javascript">
    imageList = [
        "https://hcdn2.luffycity.com/media/frontend/public_class/web1@2x(1)_1566529822.6339395.png",
        "https://hcdn2.luffycity.com/media/frontend/public_class/PY1@2x_1566529821.1110113.png",
        "https://hcdn2.luffycity.com/media/frontend/course/小程序列表图.png",
    ];

    function init() {
        for (var i = 0; i < imageList.length; i++) {
            console.log(i); // 0  1   2
            var tag = document.createElement("img"); // <img />
            tag.src = imageList[i];   // <img src="https://hcdn2.luffycity.com/..."/>

            tag.onclick = function(){  // <img src="https://hcdn2.luffycity.com/..." onclick=函数/>
                alert(i);
            }

            document.getElementById("container").appendChild(tag);
        }
    }

    init();

</script>
</body>
</html>
```



问题就是：如果定义了函数，函数不执行，函数内容内部代码。





#### 示例2

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #container img{
            width: 400px;
            margin-left: 20px;
        }
    </style>
</head>
<body>
<div id="container">

</div>

<script type="text/javascript">
    imageList = [
        "https://hcdn2.luffycity.com/media/frontend/public_class/web1@2x(1)_1566529822.6339395.png",
        "https://hcdn2.luffycity.com/media/frontend/public_class/PY1@2x_1566529821.1110113.png",
        "https://hcdn2.luffycity.com/media/frontend/course/小程序列表图.png",
    ];

    function init() {
        for (var i = 0; i < imageList.length; i++) {
            console.log(i); // 0  1   2
            var tag = document.createElement("img"); // <img />
            tag.src = imageList[i];   // <img src="https://hcdn2.luffycity.com/..."/>

            // <img src="https://hcdn2.luffycity.com/..." onclick=函数/>
            tag.onclick = (function (arg) {
                return function () {
                    alert(arg);
                }
            })(i);
            document.getElementById("container").appendChild(tag);
        }
    }

    init();

</script>
</body>
</html>
```



#### 示例3

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        #container img {
            width: 400px;
            margin-left: 20px;
        }
    </style>
</head>
<body>
<div id="container">

</div>

<script type="text/javascript">
    imageList = [
        "https://hcdn2.luffycity.com/media/frontend/public_class/web1@2x(1)_1566529822.6339395.png",
        "https://hcdn2.luffycity.com/media/frontend/public_class/PY1@2x_1566529821.1110113.png",
        "https://hcdn2.luffycity.com/media/frontend/course/小程序列表图.png",
    ];

    function init() {
        for (var i = 0; i < imageList.length; i++) {
            console.log(i); // 0  1   2
            var tag = document.createElement("img"); // <img />
            tag.src = imageList[i];   // <img src="https://hcdn2.luffycity.com/..."/>
            tag.setAttribute('xx', i);
            tag.onclick = function () {
                // 找到当前点击的标签，获取xx属性。
            }

            document.getElementById("container").appendChild(tag);
        }
    }

    init();

</script>
</body>
</html>
```









### 案例：加载、模态框、菜单、TAB切换、返回顶部（手写）



# 下午 13：50 上课



































