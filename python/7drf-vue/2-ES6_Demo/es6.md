es6

## 为什么学习ES6

- es5语言的先天性不足。比如变量提升、内置对象的方法不灵活、模块化实现不完善等等

- 为了后面的vue、尤其是react框架做好了准备

- 目前大部分公司的项目都在使用es6

ECMAScript6.0（简称ES6）是 javascript 语言的下一代标准，已经在2015年6月正式发布了， 它的目标
是使得javascript 语言可以用来编写复杂的大型应用程序，成为企业级开发语言

ES6即是一个历史名词，也是一个泛指，含义是5.1以后的jabascript的下一代标准，涵盖了ES2016 、ES2016、ES2017
等等，而是ES2015则是正式名称，特指该年发布的正式版本的语言标准

ES6新特性
- let 和 const命令
- es6的模板字符串
- 增强的函数
- 扩展的字符串、对象、数组功能
- 解构赋值
- Symbol
- Map和Set
- 迭代器和生成器
- Promise对象
- async 的用法
- 类 class
- 模块化实现

浏览器支持
查看 http://kangax.github.io/compat-table/es6/

强大的babel
- 被称为下一代的javascript编译器。可以将es6的代码转换成es5的代码，从而让浏览器获得支持

参考文献
ES6阮一峰教程：
http://es6.ruanyifeng.com
mdn教程：
https://developer.mozilla.org/zh-CN/docs/Web/JavaScript



## let和const

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>let和const</title>
</head>

<body>
    <script>
        // var a;
        // // var
        // console.log(a);
        // a = 2;
        // 1.let声明变量，没有变量提升
        // console.log(a);
        // let a = 10;
        // console.log(b);

        // 2.是一个块作用域
        // if(1===1){
        //     let b = 10;
        // }
        // console.log(b);

        // var a = 2;
        // var a = 4;
        // 3.不能重复声明
        // let a = 1;
        // let a = 3;
        // console.log(a);
        // const  声明常量  一旦被声明 无法修改
        // console.log(max);
        // if(1===1){
        //     const max = 30;
        // }
        //  const max = 30;
        //  const max = 40;

        // max = 40;
        // console.log(max);

        /*
        const person = {
            name:'小马哥'
        }
        // person.name = 'alex';
        person = {
            age:20
        }
        console.log(person);
        */

        //作用1： for循环是个经典例子
         const arr = [];

        for (let i = 0; i < 10; i++) {
            arr[i] = function() {
                return i;
            }
        }
        console.log(arr[5]()); 

        // 作用2:不会污染全局变量
        let RegExp = 10;
        console.log(RegExp);
        console.log(window.RegExp);

        // 建议：在默认情况下用const,而只有在你知道变量值需要被修改的情况使用let
        
        
        

    </script>

</body>

</html>
```



## 模版字符串

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>模板字符串</title>
</head>

<body>
    <div class="box">
       
    </div>
    <script>

        // 模板字符串：使用tab键上面的反引号``,插入变量时使用${变量名}
        const oBox = document.querySelector('.box');
        let id = 1,
            name = '小马哥';
        let htmlStr = `<ul>
            <li>
                <p id=${id}>${name}</p>
            </li>
        </ul>`;
        // oBox.innerHTML = "<ul><li><p id=" + id + ">" + name + "</p></li></ul>";
        oBox.innerHTML = htmlStr;
    </script>

</body>

</html>
```



## 强大的函数

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>

<body>
    <script>
        // 1.带参数默认值的函数
        // es5的写法
        /* function add(a, b) {
            a = a || 10;
            b = b || 20;
            return a + b;
        }
        console.log(add()); */

        // function add(a, b = 20) {
        //     return a + b;
        // }
        // console.log(add(30));

        // 2.默认的表达式也可以是一个函数
        // function add(a, b = getVal(5)) {
        //     return a + b;
        // }

        // function getVal(val) {
        //     return val + 5;
        // }
        // console.log(add(10));

        // es5写法   //vs code 多行注释快捷键 alt + shift + a
          /* function pick(obj) {
             let result = Object.create(null);
             console.log(arguments.length) //4
             for(let i = 1;i < arguments.length;i++){
                 result[arguments[i]] = obj[arguments[i]]
             }
             return result;
         }
         let book = {
             title:'es6的教程',
             author:'小马哥',
             year:2019
         }
         let bookData = pick(book,'title','year','author');
         console.log(bookData);  */ //{title: 'es6的教程', year: 2019, author: '小马哥'}

        // 3.剩余参数：由三个点...和一个紧跟着的具名参数指定 ...keys

     /*    function pick(obj, ...keys) {
            // ...keys 解决了arguments 的问题
            let result = Object.create(null);
            for (let i = 0; i < keys.length; i++) {
                result[keys[i]] = obj[keys[i]];
            }
            return result;
        }

        let book = {
            title: 'es6的教程',
            author: '小马哥',
            year: 2019
        }
        let bookData = pick(book, 'year', 'author');
        console.log(bookData); //{year: 2019, author: '小马哥'}

        function checkArgs(...args) {
            console.log(args);   //(3) ['a', 'b', 'c']
            console.log(arguments); //Arguments(3) ['a', 'b', 'c', callee: (...), Symbol(Symbol.iterator): ƒ]
        }
        checkArgs('a', 'b', 'c'); */

        // 4.扩展运算符...
        // 剩余运算符：把多个独立的合并到一个数组中
        // 扩展运算法：将一个数组分割，并将各个项作为分离的参数传给函数
/*         const maxNum = Math.max(20,30);
        console.log(maxNum); //30

        // 处理数组中的最大值，使用apply
        const arr = [10, 20, 50, 30, 90, 100, 40];
        console.log(Math.max.apply(null,arr)); //100

        // es6 扩展运算法更方便
        console.log(Math.max(...arr));//100 */


        //******** es6的箭头函数 ********
        // 使用=>来定义  function(){}等于与 ()=>{}

        // let add = function (a, b) {
        //     return a + b;
        // }

        // let add = (a, b) => {
        //     return a + b;
        // }

        // let add = (val1, val2) => val1 + val2;
        // console.log(add(10, 20));

        // let fn = ()=> 'hello world' + 123;
        // console.log(fn());

        /* let getObj = id => {
            return {
                id: id,
                name:'小马哥'
            }
        } */
        // let getObj = id => ({id:id,name:"小马哥"});
        // let obj = getObj(1);
        // console.log(obj);  //{id: 1, name: '小马哥'}

        // let fn = (function() {
        //     return function() {
        //         console.log('hello es6');
        //     }
        // })();  // 返回了内部函数
        // fn()

        
        //  let fn = (() => {
        //      return () => {
        //          console.log('hello es6 2');
        //      }
        //  })();
        //  fn();

        // 没有this绑定
        // es5中this指向：取决于调用该函数的上下文对象
        // let PageHandle = {
        //     id: 123,
        //     init: function () {
        //           //文档添加点击事件
        //         document.addEventListener('click',function(event) {
        //             // this.doSomeThings is not a function  //点击文档触发
        //             // console.log(this);
        //             this.doSomeThings(event.type);
        //         })
        //     },
        //     doSomeThings:function(type){
        //         console.log(`事件类型:${type},当前id:${this.id}`);
                
        //     }
        // }
        // PageHandle.init();  

        let PageHandle = {
            id: 123,
            init: function () {
                // 箭头函数没有this指向，箭头函数内部this值只能通过查找作用域链来确定,一旦使用箭头函数，当前就不存在作用域链
                // 作用域链在init函数 向上找属于PageHandle对象，所以this指向了PageHandle对象
                document.addEventListener('click', (event) => {
                    // this.doSomeThings is not a function
                    console.log('::'+this); //::[object Object]
                    this.doSomeThings(event.type);
                }, false)
            },
            doSomeThings: function (type) {
                console.log(`事件类型:${type},当前id:${this.id}`); //事件类型:click,当前id:123

            }
        }
        PageHandle.init();  

        // 使用箭头函数的注意事项1:使用箭头函数 函数内部没有arguments
        // let getVal = (a, b) => {
        //     console.log(arguments); // ReferenceError: arguments is not defined
        //     return a + b;
        // }
        // console.log(getVal(1, 3)); //4

        // 2.箭头函数不能使用new关键字来实例化对象
        // let Person = ()=>{
            
        // };
        // // function函数 也是一个对象，但是箭头函数不是一个对象，它其实就是一个语法糖
        // console.log(Person); //()=>{   }
        
        // let p = new Person(); //TypeError: Person is not a constructor
        
    </script>
</body>

</html>
```



## 解构赋值

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>解构赋值</title>
</head>

<body>
    <script>
        // 解构赋值是对赋值运算符的一种扩展
        // 它针对数组和对象来进行操作
        // 优点：代码书写上简洁易读
        let node = {
            type:'iden',
            name:'foo'
        }
        // let type = node.type;
        // let name = node.name;
        
        // 完全解构
        let {type,name} = node;
        console.log(type,name);  //iden foo

        let obj = {
            a:{
                name:"张三"
            },
            b:[],
            c:'hello,world'
        }

        // 不完全解构 可忽略
        // let {a} = obj;
        // console.log(a);  //{name: '张三'}
        // 剩余运算符
        let {a,...res} = obj;
        console.log(a,res); //{name: '张三'} {b: Array(0), c: 'hello,world'}

        // 默认值
        // let {a,b = 30} = {a:20};
        // console.log(a,b) // 20 30

        // 对数组解构
        // let arr = [1,2,3];
        // let [a,b] = arr;
        // console.log(a,b); // 1 2
        // 可嵌套
        // let [a,[b],c] = [1,[2],3];
        // console.log(a,b,c) // 1 2 3

    </script>

</body>

</html>
```



## 扩展的对象功能

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>扩展的对象的功能</title>
</head>

<body>
    <script>
        // es6直接写入变量和函数，作为对象的属性和方法
        // const name = '小马哥',age = 20;
        // const person = {
        //     name,//等价于name:name
        //     age,
        //     sayName(){
        //         console.log(this.name);
        //     }
        // }
        // person.sayName(); //小马哥

        // function fn(x,y) {
        //     return {x,y};
        // }
        // console.log(fn(10,20));  //Object x: 10 y: 20  [[Prototype]]: Object


        // let cart = {
        //     wheel:4,
        //     set(newVal){
        //         if(newVal < this.wheel){
        //             throw new Error('轮子数太少了')
        //         }
        //         this.wheel = newVal;
        //     },
        //     get(){
        //         return this.wheel;
        //     }
        // }
        // console.log(cart.get()); //4
        // cart.set(6);
        // console.log(cart.get()) //6

        // const obj = {};
        // obj.isShow = true;
        // const name = 'a';
        // obj[name+'bc'] = 123;
        // console.log(obj); //{isShow: true, abc: 123}
        // obj['f'+'bc'] = function () {
        //     console.log(this);
        // }
        // console.log(obj);  //{isShow: true, abc: 123, fbc: ƒ}
    
        // const name = 'a';
        // const obj = {
        //     isShow:true,
        //     [name+'bc']:123,
        //     ['f'+name](){
        //         console.log(this);
                
        //     }
        // }
        // console.log(obj); //{isShow: true, abc: 123, fa: ƒ}

        // 对象的方法

        // is() ===
        // 比较两个值是否严格相等
        console.log(NaN === NaN);         // false ES5缺点
        console.log(Object.is(NaN,NaN));  // true 与严格比较运算符（===）的行为基本一致。
        // ***** assign() ***
        // 对象的合并
        // Object.assign(target,obj1,obj2....)
        
        // 返回合并之后的新对象
        let newObj = Object.assign({},{a:1},{b:2});
        console.log(newObj); //{a: 1, b: 2}
        
        
        

        
        
        
    </script>

</body>

</html>
```

## Symbol

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Symbol</title>
</head>

<body>
    <script>
        // 原始数据类型Symbol ,它表示是独一无二的值
        // 最大的用途：用来定义对象的私有变量
        const name = Symbol('name');
        const name2 = Symbol('name');
        console.log(name === name2); //false

        let s1 = Symbol('s1');
        console.log(s1);  //Symbol(s1)
        let obj = {
            [s1]:'小马哥'
        };
        // obj[s1] = '小马哥';

        // 如果用Symbol定义的对象中的变量，取值时一定要用[变量名]
        console.log(obj[s1]); //小马哥
        // console.log(obj.s1); //undefined

        for(let key in obj){
            console.log(key); //空
        }
        console.log(Object.keys(obj)); //[]
        
        // 获取Symbol声明的属性名（作为对象的key）
        let s = Object.getOwnPropertySymbols(obj);
        console.log(s[0]);  //Symbol(s1)
        
        // Reflect翻译反射
        let m = Reflect.ownKeys(obj);
        console.log(m);  //[Symbol(s1)]
       

    </script>

</body>

</html>
```



## Map和Set

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>

<body>
    <script>
        //  集合：表示无重复值的有序列表
        let set = new Set();
        // console.log(set);  //Set(1)

        // 添加元素
        set.add(2);
        set.add('4');
        set.add('4');
        // set.add(['hello','world',3]);
        // 删除元素
        set.delete(2);
        // 校验某个值是否在set中
        console.log(set.has('4'));  //true
        console.log(set.size);      //1

        /* set.forEach((val,key)=>{
            console.log(val);
            console.log(key);
        }) */

        // 将set转换成数组
        let set2 = new Set([1, 2, 3, 3, 3, 4]);
        // 扩展运算符
        let arr = [...set2]
        console.log(arr);  //(4) [1, 2, 3, 4]


        // 1.set中对象的引用无法被释放
        // let set3 = new Set(),obj = {};
        // set3.add(obj);
        // // 释放当前的资源
        // obj = null;
        // console.log(set3);  //Set(1) {{…}}

        let set4 = new WeakSet(),
            obj = {};
        set4.add(obj);
        // 释放当前的资源
        obj = null;
        console.log(set4);  //WeakSet {{…}}

        // WeakSet
        // 1.不能传入非对象类型的参数
        // 2.不可迭代
        // 3.没有forEach()
        // 4.没有size属性


        // Map类型是键值对的有序列表，键和值是任意类型

         let map = new Map();
         map.set('name','张三');
         map.set('age',20);
         console.log(map.get('name'));  //张三
         console.log(map);   //Map(2) {'name' => '张三', 'age' => 20}
         map.has('name');//true
         map.delete('name');
         map.clear();
         console.log(map);  //Map(0) {size: 0}
         map.set(['a',[1,2,3]],'hello');
         console.log(map);  //Map(1) {Array(2) => 'hello'}

        let m = new Map([
            ['a', 1],
            ['c', 2]
        ]);
        console.log(m);   //Map(2) {'a' => 1, 'c' => 2}
        
    </script>

</body>

</html>
```

## 数组的扩展功能

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>

<body>
    <ul>
        <li>1</li>
        <li>2</li>
        <li>3</li>
        <li>4</li>
    </ul>
    <script>
        // 数组的方法  from()  of()
        // 1.from() 将伪数组转换成真正的数组
        function add() {
            console.log(arguments);
            // es5转换
            // let arr = [].slice.call(arguments);
            // console.log(arr);
            // es6写法
            let arr = Array.from(arguments);
            console.log(arr); //(3) [1, 2, 3]
        }
        add(1, 2, 3);

        let lis = document.querySelectorAll('li')
        console.log(lis); //NodeList(4) [li, li, li, li]

        console.log(Array.from(lis)); //(4) [li, li, li, li]
        // 扩展运算符 将伪数组转换成真正的数组
        console.log([...lis]);  //(4) [li, li, li, li]

        // from() 还可以接受第二个参数，用来对每个元素进行处理

        let liContents = Array.from(lis, ele => ele.textContent);
        console.log(liContents);   //(4) ['1', '2', '3', '4']

        // 2.of() 将任意的数据类型，转换成数组
        console.log(Array.of(3, 11, 20, [1, 2, 3], {
            id: 1
        }));   //(5) [3, 11, 20, Array(3), {…}]


        // 3.copywithin() 数组内部将制定位置的元素复制到其它的位置，返回当前数组
        // 从3位置往后的所有数值去替换从0位置往后的三个数值
        console.log([1, 2, 3, 8, 9, 10].copyWithin(0, 3));  //[8,9,10,8,9,10]

        //  4.find() findIndex()
        // find()找出第一个符合条件的数组成员
        let num = [1, 2, -10, -20, 9, 2].find(n => n < 0)
        console.log(num);  // -10

        // findIndex()找出第一个符合条件的数组成员的索引
        // 条件是值小于0，返回索引号
        let numIndex = [1, 2, -10, -20, 9, 2].findIndex(n => n < 0)
        console.log(numIndex); // 2


        // 5.entries() keys() values() 返回一个遍历器  可以使用for...of循环进行遍历
        
        // keys() 对键名遍历
        // values() 对值遍历
        // entries() 对键值对遍历
        console.log(['a','b'].keys());  //Array Iterator {}

        for (let index of ['a', 'b'].keys()) {
            console.log(index);  // 0 1
        }

        for (let ele of ['a', 'b'].values()) {
            console.log(ele);  // a b
        }

        for(let [index,ele] of ['a','b'].entries()){
            console.log(index,ele); // 0 'a' 1 'b'
        }

        let letter = ['a','b','c'];
        let it = letter.entries();
        console.log(it.next().value);  //(2) [0, 'a']
        console.log(it.next().value);  //(2) [1, 'b']
        console.log(it.next().value);  //(2) [2, 'c']
        console.log(it.next().value);  //undefined

        // 6.includes() 返回一个布尔值，表示某个数组是否包含给定的值
        console.log([1,2,3].includes(2));   // true
        console.log([1,2,3].includes('4')); // false

        // 之前 indexof()
        // console.log([1,2,3].indexOf('2'));  // -1


        
        
        
    </script>

</body>

</html>
```

## 迭代器

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>迭代器</title>
</head>

<body>

<script>
    //   Iterator
    //   是一种新的遍历机制，两个核心
    // 1.迭代器是一个接口，能快捷的访问数据，通过Symbol.iterator来创建迭代器 通过迭代器的next()获取迭代之后的结果
    // 2.迭代器是用于遍历数据结构的指针(数据库的游标)

    // 使用迭代
    const items = ['one', 'two', 'three'];
    // 1.创建新的迭代器
    const ite = items[Symbol.iterator]();
    console.log(ite.next()); //{value: "one", done: false} done如果为false表示遍历继续 如果为true表示遍历完成
    console.log(ite.next());
    console.log(ite.next());
    console.log(ite.next());
</script>
</body>

</html>
```

##  生成器

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>生成器 Generator</title>
</head>

<body>
    <script>
        // generator函数 可以通过yield关键字，将函数挂起，为了改变执行流提供了可能，同时为了做异步编程提供了方案
        // 它普通函数的区别
        // 1.function后面 函数名之前有个*
        // 2.只能在函数内部使用yield表达式，让函数挂起

        // function* func() {
        //     console.log('one');
        //     yield 2;
        //     console.log('two');
        //     yield 3;
        //     console.log('end');   
        // }
        // // 返回一个遍历器对象 可以调用next()
        // let fn = func();
        // console.log(fn)  // func {<suspended>}
        // console.log(fn.next()); //{value: 2, done: false}
        // console.log(fn.next());
        // console.log(fn.next()); //{value: undefined, done: true}

        // 总结：generator函数是分段执行的，yield语句是暂停执行  而next()恢复执行
        

        function* add() {
            console.log('start');
            // x 可真的不是yield '2'的返回值，它是next()调用 恢复当前yield()执行传入的实参
            let x = yield '2';
            console.log('one:'+x); // one:20
            let y = yield '3';
            console.log('two:'+y);
            return x+y;  
        }
        const fn = add();
        console.log(fn.next()); //{value:'2',done:false}
        console.log(fn.next(20)); //{value:'3',done:false} // 20赋值给了x
        console.log(fn.next(30)); //{value:50,done:true}   //30赋值给了y

        // 使用场景1：为不具备Interator接口的对象提供了遍历操作
        function* objectEntries(obj) {
            // 获取对象的所有的key保存到数组 [name,age]
            const propKeys = Object.keys(obj);
            for(const propkey of propKeys){
                yield [propkey,obj[propkey]]
            }
        }
        

        const obj = {
            name:'小马哥',
            age:18
        }
        // obj[Symbol.iterator] = objectEntries;
        // console.log(obj); //{name: '小马哥', age: 18, Symbol(Symbol.iterator): ƒ}

        for(let [key,value] of objectEntries(obj)){
            console.log(`${key}:${value}`);  
        }
        // name:小马哥
        // age:18
        
    </script>
</body>

</html>
```



## Generator的应用

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>11 Generator的应用</title>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
</head>

<body>
    <script>

        // Generator 部署ajax操作，让异步代码同步化
        // 回调地狱  参考https://blog.csdn.net/qq_42698326/article/details/111075519
        /* $.ajax({
            url: 'https://free-api.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976',
            method: 'get',
            success(res) {
                console.log(res);

                // 继续发送请求
                $.ajax({
                    url: '',
                    method: 'get',
                    success(res1) {
                        // 发送ajax
                        $.ajax({
                            url: '',
                            method: 'get',
                            success(res2) {

                                // 发送ajax
                                $
                            }
                        })
                    }
                })

            }
        }) */

        function* main() {
            console.log('main');

            let res = yield request(
                'https://free-api.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976'
            )
            console.log(res);

            // 执行后面的操作
            console.log('数据请求完成，可以继续操作');

        }
        const ite = main();
        ite.next();

        function request(url) {
            $.ajax({
                url,
                method: 'get',
                success(res) {
                    ite.next(res);
                }
            })
        }

        // 加载loading...页面
        // 数据加载完成...（异步操作）
        // loading关闭掉

        function* load() {
            loadUI();
            yield showData();
            hideUI();
        }

        let itLoad = load();
        itLoad.next();

        function loadUI() {
            console.log('加载loading...页面');
        }
        function showData() {
            // 模拟异步操作
            setTimeout(() => {
                console.log('数据加载完成');
                itLoad.next();
                
            }, 1000);
        }
        function hideUI() {
            console.log('隐藏loading...页面');
            
        }
        
    </script>

</body>

</html>
```



## Promise对象

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title></title>
</head>

<body>

    <script>
        // Promise 承诺
        // 相当于一个容器，保存着未来才会结束的事件(异步操作)的一个结果
        // 各种异步操作都可以用同样的方法进行处理 axios

        // 特点：
        // 1.对象的状态不受外界影响  处理异步操作 三个状态  Pending(进行)  Resolved(成功) Rejected(失败)
        // 2.一旦状态改变，就不会再变，任何时候都可以得到这个结果

        
        /* let pro = new Promise(function(resolved,rejected) {
            //模拟执行异步操作 得到的结果
            let res = {
                code: 201,
                data:{
                    name:'小马哥'
                },
                error:'失败了'
            }
            setTimeout(() => {
                if(res.code === 200){
                    resolved(res.data);
                }else{
                    rejected(res.error);
                }
            }, 1000);
        })
        console.log(pro); //Promise
        pro.then((val)=>{
            console.log(val);  
        },(err)=>{
            console.log(err); //失败了
        }); */
       

        /* function timeOut(ms) {
            return new Promise((resolved,rejected)=>{
                setTimeout(() => {
                    resolved('hello promise success!!')
                }, ms);
            })
        }
        timeOut(2000).then((val)=>{  // 两秒之后返回
            console.log(val);        //hello promise success!!
        }) */

        // https://free-api.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976
        /* const getJSON = function (url) {
            return new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('GET', url);
                xhr.onreadystatechange = handler;
                xhr.responseType = 'json';
                xhr.setRequestHeader('Accept', 'application/json');
                // 发送
                xhr.send();

                function handler() {
                    if (this.readyState === 4) { // 4表示成功回调
                        if (this.status === 200) {
                            resolve(this.response.HeWeather6);
                        } else {
                            reject(new Error(this.statusText));
                        }
                    }

                }
            })
        }
        let a = getJSON(
                'https://free-api.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976')
            .then((data) => {
                // console.log(data);   
                return data[0]
            }).then((obj)=>{
                console.log(obj);  //Promise {<pending>}
            })
        console.log(a);  //{status: 'invalid key'}
 */
        /* 
        catch(err=>{

        })

         // then(null,err=>{

         // })
        
        */

        // getJSON('https://free-ap.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976')
        //     .then(data => {
        //         console.log(data);
        //     }).catch(err => {
        //         console.log(err);
        //     })


        // then()方法 
        // then() 第一个参数是relove回调函数，第二个参数是可选的 是reject状态回调的函数
        // then()返回一个新的promise实例，可以采用链式编程 


        // resolve()  reject() all() race()  done() finally()

        // resolve()能将现有的任何对象转换成promise对象
        // let p = Promise.resolve('foo');
        /*  let p = new Promise(resolve=>resolve('foo'));
         p.then((data)=>{
             console.log(data);
             
         }) */

        // 应用：一些游戏类的素材比较多，等待图片、flash、静态资源文件 都加载完成 才进行页面的初始化
        // 伪代码
        /* let promise1 = new Promise((resolve, reject) => {});
        let promise2 = new Promise((resolve, reject) => {});
        let promise3 = new Promise((resolve, reject) => {});

        let p4 = Promise.all([promise1, promise2, promise3])

        p4.then(()=>{
            // 三个都成功  才成功
        }).catch(err=>{
            // 如果有一个失败 则失败
        }) */

        // race() 某个异步请求设置超时时间，并且在超时后执行相应的操作
        // 1 请求图片资源
        // function requestImg(imgSrc) {
        //     return new Promise((resolve, reject) => {
        //         const img = new Image();
        //         img.onload = function () {  //onload 当图像装载完毕时调用的事件句柄。	
        //             resolve(img);  //Promise.resolve(value)方法返回一个以给定值解析后的Promise 对象
        //         }
        //         img.src = imgSrc;
        //     });
        // }

        // function timeout() {
        //     return new Promise((resolve, reject) => {
        //         setTimeout(() => {
        //             reject(new Error('图片请求超时'));
        //         }, 3000);
        //     })
        // }
        // Promise.race([requestImg('https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fblog%2F202102%2F18%2F20210218112720_25189.thumb.1000_0.jpg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1646595131&t=12acaf9c7b1e00ac6a874e1b0945c3af'),
        //             timeout()]).then(data=>{
        //     console.log(data);
        //     document.body.appendChild(data);
            
        // }).catch(err=>{
        //     console.log(err);
            
        // }); 

        /* 
        server.listen(3000).then(()=>{

        }).finally(server.stop());  //finally不管前面执行是否成功，最后都会执行
        */


    </script>
</body>

</html>
```



## async用法

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>async异步操作</title>
</head>

<body>
    <script>

        //Generator  Promise  async  1.解决回调地域  2.使得异步操作显得更加方便
        
        // 作用：使得异步操作更加方便
        // 基本操作 async它会返回一个Promise对象  then catch
        // async是Generator的一个语法糖
        async function f() {
            // return await 'hello async';
            let s = await 'hello world';
            let data = await s.split('');
            return data;
        }
        // 如果async函数中有多个await 那么then函数会等待所有的await指令 运行完的结果 才去执行
        f().then(v => {
            console.log(v)  //Array(11)
        }).catch(e => console.log(e));

        async function f2() {
            // throw new Error('出错了');
            try {
                await Promise.reject('出错了');
            } catch (error) {

            }
            return await Promise.resolve('hello');
        }
        f2().then(v => console.log(v)).catch(e => console.log(e));  //hello




        // 需求： 想获取和风天气 现在now的数据
        const getJSON = function (url) {
            return new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();
                xhr.open('GET', url);
                xhr.onreadystatechange = handler;
                xhr.responseType = 'json';
                xhr.setRequestHeader('Accept', 'application/json');
                // 发送
                xhr.send();

                function handler() {
                    if (this.readyState === 4) {
                        if (this.status === 200) {
                            resolve(this.response);
                        } else {
                            reject(new Error(this.statusText));
                        }
                    }

                }
            })
        }

        async function getNowWeather(url) {
            // 发送ajax 获取实况天气
            let res = await getJSON(url);
            console.log(res);  //object
            // 获取HeWeather6的数据   获取未来3~7天的天气状况
            let arr = await res.HeWeather6;
            return arr[0].now;
        }
              //https://www.qweather.com/  api失效
        getNowWeather(
                'https://free-api.heweather.net/s6/weather/now?location=beijing&key=4693ff5ea653469f8bb0c29638035976')
            .then(now => {
                console.log(now);
            })
    </script>

</body>

</html>
```

## class 类

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>

<body>
    <script>
        // es5造类
        /* function Person(name,age) {
            this.name = name;
            this.age = age;
        }
        Person.prototype.sayName = function() {
            return this.name;
        }
        let p1 = new Person('小马哥',28);
        console.log(p1);
         */
        class Person {
            // 实例化的时候会立即被调用
            constructor(name, age) {
                this.name = name;
                this.age = age;
            }

        }
        // 通过Object.assign()方法一次性向类中添加多个方法
        Object.assign(Person.prototype, {
            sayName() {
                return this.name
            },
            sayAge() {
                return this.age
            }
        })
        let p1 = new Person('小马哥', 28);
        console.log(p1);
    </script>

</body>

</html>
```



## 类的继承 extends

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>类的继承</title>
</head>

<body>
    <script>
        // 使用关键字 extends
        class Animal{
            constructor(name,age) {
                this.name = name;
                this.age = age;
            }
            sayName(){
                return this.name;
            }
            sayAge(){
                return this.age;
            }
        }

        class Dog extends Animal{
            constructor(name,age,color) {
                super(name,age);
                // Animal.call(this,name,age);
                this.color = color;
            }
            // 子类自己的方法
            sayColor(){
                return `${this.name}是${this.age}岁了,它的颜色是${this.color}`
            }
            // 重写父类的方法
            sayName(){
                return this.name + super.sayAge() + this.color;
            }
            
        }
        let d1 = new Dog('小黄',28,'red');
        console.log(d1.sayColor());
        console.log(d1.sayName());


        // 思考：如何让多个类 混入到一个类中？？？？
        
    </script>

</body>

</html>
```



## module模块的使用

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>

<body>
    <script type='module'>
        /*
            运行模块导入 需要用服务器启动，vscode插件 Live Server
        */
        // CommonJS和AMD
        // ES6 module 
        import Person,{name,age,sayName} from './modules/index.js'
        // import * as f from './modules/index.js'
        // console.log(Person);
        const p = new Person();
        p.sayAge();
        // console.log(f.default);
        // console.log(name,age,sayName());
    </script>
</body>

</html>
```

./modules/index.js

```js
// es6模块功能主要有两个命令构成：export和import
// export用于规定模块的对外接口 import用于输入其它模块提供的功能
// 一个模块就是独立的文件

/* export const name = '张三';
export const age = 18;
export function sayName(){
    return 'my name is 小马哥';
} */
// export {sayName}

const name = '张三';
const age = 18;
function sayName() {
    return 'my name is 小马哥';
}
export {
    name,age,sayName
}
/* const obj = {
    foo:'foo'
} */
class Person{
    constructor(){

    }
    sayAge(){
        console.log('16');
        
    }
}

export default Person;

```





