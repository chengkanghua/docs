# 用户的登陆认证

接下来，因为是新开发一个功能模块，那么我们可以在新的分支下进行开发，将来方便对这部分代码进行单独管理，等开发完成了以后再合并分支到develop也是可以的。

```bash
cd ~/Desktop/luffycity
git checkout -b feature/user
```



## 前端显示登陆页面

### 登录页组件

components/Login.vue

```vue
<template>
  <div class="title">
    <span :class="{active:state.login_type==0}" @click="state.login_type=0">密码登录</span>
    <span :class="{active:state.login_type==1}" @click="state.login_type=1">短信登录</span>
  </div>
  <div class="inp" v-if="state.login_type==0">
    <input v-model="state.username" type="text" placeholder="用户名 / 手机号码" class="user">
    <input v-model="state.password" type="password" class="pwd" placeholder="密码">
    <div id="geetest1"></div>
    <div class="rember">
      <label>
        <input type="checkbox" class="no" name="a"/>
        <span>记住密码</span>
      </label>
      <p>忘记密码</p>
    </div>
    <button class="login_btn">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
  <div class="inp" v-show="state.login_type==1">
    <input v-model="state.username" type="text" placeholder="手机号码" class="user">
    <input v-model="state.password"  type="text" class="code" placeholder="短信验证码">
    <el-button id="get_code" type="primary">获取验证码</el-button>
    <button class="login_btn">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
</template>

<script setup>
import {reactive} from "vue";

const state = reactive({
  login_type: 0,
  username:"",
  password:"",
})
</script>

<style scoped>
.title{
    font-size: 20px;
    color: #9b9b9b;
    letter-spacing: .32px;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    justify-content: space-around;
    padding: 0px 60px 0 60px;
    margin-bottom: 20px;
    cursor: pointer;
}
.title span.active{
	color: #4a4a4a;
    border-bottom: 2px solid #84cc39;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
    width: 220px;
    margin-right: 16px;
}
#get_code{
   margin-top: 6px;
}
.inp input{
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
    vertical-align: middle;
    margin-right: 4px;
}

.inp .rember p span{
    display: inline-block;
    font-size: 12px;
    width: 100px;
}
.login_btn{
    cursor: pointer;
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
    border: none;
    outline: none;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>
```

components/Header.vue，代码：

```vue
<template>
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo">
            <router-link to="/"><img src="../assets/logo.svg" alt=""></router-link>
          </div>
          <ul class="nav">
              <li v-for="item in nav.header_nav_list">
                <a :href="item.link" v-if="item.is_http">{{item.name}}</a>
                <router-link :to="item.link" v-else>{{item.name}}</router-link>
              </li>
          </ul>
          <div class="search-warp">
            <div class="search-area">
              <input class="search-input" placeholder="请输入关键字..." type="text" autocomplete="off">
              <div class="hotTags">
                <router-link to="/search/?words=Vue" target="_blank" class="">Vue</router-link>
                <router-link to="/search/?words=Python" target="_blank" class="last">Python</router-link>
              </div>
            </div>
            <div class="showhide-search" data-show="no"><img class="imv2-search2" src="../assets/search.svg" /></div>
          </div>
          <div class="login-bar">
            <div class="shop-cart full-left">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <span @click="state.show_login=true">登录</span>
              &nbsp;/&nbsp;
              <span>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog :width="600" v-model="state.show_login">
      <Login></Login>
    </el-dialog>
</template>
```

```vue
<script setup>
import Login from "./Login.vue"
import {reactive} from "vue";
import nav from "../api/nav";

const state = reactive({
  show_login: false,
})

// 获取头部导航
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data;
}).catch(error=>{
  console.log(error);
});

</script>
```

```css
<style scoped>
.header-box{
  height: 72px;
}
.header{
  width: 100%;
  height: 72px;
  box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
  position: fixed;
  top:0;
  left: 0;
  right:0;
  margin: auto;
  z-index: 99;
  background: #fff;
}
.header .content{
  max-width: 1366px;
  width: 100%;
  margin: 0 auto;
}
.header .content .logo a{
  width: 150px;
  height: auto;
  margin-right: 50px;

  cursor: pointer;

}
.header .content .logo{
  height: 72px;
  line-height: 72px;
  margin: 0 20px;
  float: left;
  cursor: pointer; /* 设置光标的形状为爪子 */
}
.header .content .logo img{
  width: 150px;
  vertical-align: middle;
  margin: -40px;
}
.header .nav li{
  float: left;
  height: 80px;
  line-height: 80px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
}
.header .nav li span{
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}
.header .nav li span a{
  display: inline-block;
}
.header .nav li .this{
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}
.header .nav li:hover span{
  color: #000;
}

/*首页导航全局搜索*/
.search-warp {
  position: relative;
  float: left;
  margin-left: 24px;
}
.search-warp .showhide-search {
  width: 20px;
  height: 24px;
  text-align: right;
  position: absolute;
  display: inline-block;
  right: 0;
  bottom: 24px;
  padding: 0 8px;
  border-radius: 18px;
}
.search-warp .showhide-search i {
  display: block;
  height: 24px;
  color: #545C63;
  cursor: pointer;
  font-size: 18px;
  line-height: 24px;
  width: 20px;
}
.search-area {
  float: right;
  position: relative;
  height: 40px;
  padding-right: 36px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
  zoom: 1;
  background: #F3F5F6;
  border-radius: 4px;
  margin: 16px 0;
  width: 324px;
  box-sizing: border-box;
  font-size: 0;
  -webkit-transition: width 0.3s;
  -moz-transition: width 0.3s;
  transition: width 0.3s;
}
.search-area .search-input {
  padding: 8px 12px;
  font-size: 14px;
  color: #9199A1;
  line-height: 24px;
  height: 40px;
  width: 100%;
  float: left;
  border: 0;
  -webkit-transition: background-color 0.3s;
  -moz-transition: background-color 0.3s;
  transition: background-color 0.3s;
  background-color: transparent;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  -ms-box-sizing: border-box;
  box-sizing: border-box;
}
.search-area .search-input.w100 {
  width: 100%;
}
.search-area .hotTags {
  display: inline-block;
  position: absolute;
  top: 0;
  right: 32px;
}
.search-area .hotTags a {
  display: inline-block;
  padding: 4px 8px;
  height: 16px;
  font-size: 14px;
  color: #9199A1;
  line-height: 16px;
  margin-top: 8px;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.search-area .hotTags a:hover {
  color: #F21F1F;
}
.search-area input::-webkit-input-placeholder {
  color: #A6A6A6;
}
.search-area input::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  color: #A6A6A6;
}
.search-area input:-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  color: #A6A6A6;
}
.search-area input:-ms-input-placeholder {
  /* Internet Explorer 10-11 */
  color: #A6A6A6;
}
.search-area .btn_search {
  float: left;
  cursor: pointer;
  width: 30px;
  height: 38px;
  text-align: center;
  -webkit-transition: background-color 0.3s;
  -moz-transition: background-color 0.3s;
  transition: background-color 0.3s;
}
.search-area .search-area-result {
  position: absolute;
  left: 0;
  top: 57px;
  width: 300px;
  margin-bottom: 20px;
  border-top: none;
  background-color: #fff;
  box-shadow: 0 8px 16px 0 rgba(7, 17, 27, 0.2);
  font-size: 12px;
  overflow: hidden;
  display: none;
  z-index: 800;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
}
.search-area .search-area-result.hot-hide {
  top: 47px;
}
.search-area .search-area-result.hot-hide .hot {
  display: none;
}
.search-area .search-area-result.hot-hide .history {
  border-top: 0;
}
.search-area .search-area-result h2 {
  font-size: 12px;
  color: #1c1f21;
  line-height: 12px;
  margin-bottom: 8px;
  font-weight: 700;
}
.search-area .search-area-result .hot {
  padding: 12px 0 8px 12px;
  box-sizing: border-box;
}
.search-area .search-area-result .hot .hot-item {
  background: rgba(84, 92, 99, 0.1);
  border-radius: 12px;
  padding: 4px 12px;
  line-height: 16px;
  margin-right: 4px;
  margin-bottom: 4px;
  display: inline-block;
  cursor: pointer;
  font-size: 12px;
  color: #545c63;
}
.search-area .search-area-result .history {
  border-top: 1px solid rgba(28, 31, 33, 0.1);
  box-sizing: border-box;
}
.search-area .search-area-result .history li {
  height: 40px;
  line-height: 40px;
  padding: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #787d82;
  cursor: pointer;
}
.search-area .search-area-result .history li:hover,
.search-area .search-area-result .history li .light {
  color: #1c1f21;
  background-color: #edf0f2;
}


.header .login-bar{
  margin-top: 20px;
  height: 80px;
  float: right;
}
.header .login-bar .shop-cart{
  float: left;
  margin-right: 20px;
  border-radius: 17px;
  background: #f7f7f7;
  cursor: pointer;
  font-size: 14px;
  height: 28px;
  width: 88px;
  line-height: 32px;
  text-align: center;
}
.header .login-bar .shop-cart:hover{
  background: #f0f0f0;
}
.header .login-bar .shop-cart img{
  width: 15px;
  margin-right: 4px;
  margin-left: 6px;
}
.header .login-bar .shop-cart span{
  margin-right: 6px;
}
.header .login-bar .login-box{
  float: left;
  height: 28px;
  line-height: 30px;
}
.header .login-bar .login-box span{
  color: #4a4a4a;
  cursor: pointer;
}
.header .login-bar .login-box span:hover{
  color: #000000;
}
</style>
```



views/Login.vue，代码：

```vue
<template>
	<div class="login box">
		<img src="../assets/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../assets/logo.svg" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <Login></Login>
      </div>
		</div>
	</div>
</template>

<script setup>
import Login from "../components/Login.vue"

</script>

<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .login {
	position: absolute;
	width: 500px;
	height: 400px;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -438px;
}

.login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
    padding-top: 50px;
}
</style>
```



### 绑定登陆页面路由地址

src/router/index.js，代码：

```javascript
import {createRouter,createWebHistory} from 'vue-router'

// 路由列表
const routes = [
  {
    meta:{
      title:"luffy2.0-站点首页",
      keepalive:true
    },
    path:'/', //url访问地址
    name:"Home",
    component: ()=> import("../views/Home.vue")
  },
  {
    meta:{
      title:"luffy2.0-用户登录",
      keepalive: true
    },
    path:'/login',
    name:"Login",
    component:()=>import("../views/Login.vue")
  }
]

// 路由对象实例化
const router = createRouter({
  // history, 指定路由的模式
  history: createWebHistory(),
  // 路由列表
  routes,
});


// 暴露路由对象
export default router
```

```bash
git add .
git commit -m "feature:自定义用户模型"
# 执行 git push 以后会提示如下，跟着执行提示的命令即可。
git push --set-upstream origin feature/user  
# 这句命令表示提交的时候，同步创建线上分支
```



## 后端实现登陆认证

![image-20220410030657922](assets/image-20220410030657922.png)

Django默认已经提供了认证系统Auth模块。认证系统包含：

- 用户管理
- 权限管理[RBAC]
- 用户组管理（就是权限里面的角色）
- 密码哈希系统（就是密码加密和验证密码）
- 用户登录或内容显示的表单和视图
- 一个可插拔的后台系统(admin站点)

Django默认用户的认证机制依赖Session机制，但是session认证机制在前后端分离项目中具有一定的局限性。

1. session默认会把session_id 作为cookie保存到客户端。有些客户端的是默认禁用cookie/或者没法使用cookie的。
2. session的数据默认是保存到服务端的，带来一定的存储要求。

所以，基于session的这种现状，我们一般在前后端分离的项目中，一般引入JWT认证机制来实现用户的登录和鉴权（鉴别身份，识别权限），jwt可以将用户的身份凭据存放在一个Token（认证令牌，本质上就是一个经过处理的字符串）中，然后把token发送给客户端，客户端可以选择采用自己的技术来保存这个token。

在django中如果要实现jwt认证，有一个常用的第三方jwt模块，我们可以很方便的去通过jwt对接Django的认证系统，帮助我们来快速实现：

- 用户的数据模型
- 用户密码的加密与验证
- 用户的权限系统



### Django用户模型类

```python
from django.contrib.auth.models import User
```

Django的Auth认证系统中提供了用户模型类User保存用户的数据，默认的User包含以下常见的基本字段：

| 字段名             | 字段描述                                                     |
| ------------------ | ------------------------------------------------------------ |
| `username`         | 必选。150个字符以内。 用户名可能包含字母数字，`_`，`@`，`+` `.` 和`-`个字符。 |
| `first_name`       | 可选（`blank=True`）。 少于等于30个字符。                    |
| `last_name`        | 可选（`blank=True`）。 少于等于30个字符。                    |
| `email`            | 可选（`blank=True`）。 邮箱地址。                            |
| `password`         | 必选。 密码的哈希加密串。 （Django 不保存原始密码）。 原始密码可以无限长而且可以包含任意字符。 |
| `groups`           | 与`Group` 之间的多对多关系。对接权限功能的。                 |
| `user_permissions` | 与`Permission` 之间的多对多关系。对接权限功能的。            |
| `is_staff`         | 布尔值。 设置用户是否可以访问Admin 站点。                    |
| `is_active`        | 布尔值。 指示用户的账号是否激活。 它不是用来控制用户是否能够登录，而是描述一种帐号的使用状态。值为False的时候，是无法登录的。 |
| `is_superuser`     | 是否是超级用户。超级用户具有所有权限。                       |
| `last_login`       | 用户最后一次登录的时间。                                     |
| `date_joined`      | 账户创建的时间。 当账号创建时，默认设置为当前的date/time。   |



##### 模型提供的常用方法：

模型常用方法可以通过`user实例对象.方法名`来进行调用。

- `set_password`(*raw_password*)

    设置用户的密码为给定的原始字符串，并负责密码的。 不会保存`User` 对象。当`None`为`raw_password` 时，密码将设置为一个不可用的密码。

- `check_password`(*raw_password*)

    如果给定的raw_password是用户的真实密码，则返回True，可以在校验用户密码时使用。

##### 管理器的常用方法：

管理器方法可以通过`User.objects.` 进行调用。

- `create_user`(*username*, *email=None*, *password=None*, **\*extra_fields*)

    创建、保存并返回一个`User`对象。

- `create_superuser`(*username*, *email*, *password*, **\*extra_fields*)

    与`create_user()` 相同，但是设置`is_staff` 和`is_superuser` 为`True`。

虽然上面的User模型看起来很多的属性和方法了，但是我们当前要实现的项目是一个在线教育商城，所以我们还需要记录用户的手机号，或者头像等等一系列信息。所以我们需要在原有模型的基础上对这个模型进行改造。

所以我们需要自定义一个新的users子应用并在django原有功能的基础上，完善用户的登录注册功能。



### 创建用户模块的子应用

```shell
cd luffycityapi/apps/
python ../../manage.py startapp users
```

在settings/dev.py文件中注册子应用。

```python
INSTALLED_APPS = [
    ...
  	'users',
]
```

创建users/urls.py子路由并在总路由中进行注册。

users/urls.py，代码：

```python
from django.urls import path
from . import views
urlpatterns = [

]
```



luffycityapi/urls.py，总路由，代码：

```python
from django.contrib import admin
from django.urls import path,re_path,include

from django.conf import settings
from django.views.static import serve # 静态文件代理访问模块

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'uploads/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path("home/", include("home.urls")),
    path("users/", include("users.urls")),
]
```



### 创建自定义的用户模型类

Django认证系统中提供的用户模型类及方法很方便，我们可以使用这个模型类，但是字段有些无法满足项目需求，如本项目中需要保存用户的手机号，需要给模型类添加额外的字段。

Django提供了`django.contrib.auth.models.AbstractUser`用户抽象模型类允许我们继承，扩展字段来使用Django认证系统的用户模型类。

**我们可以在apps中创建Django应用users，并在配置文件中注册users应用。**

在创建好的应用models.py中定义用户的用户模型类。

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    money = models.DecimalField(max_digits=9, default=0.0, decimal_places=2, verbose_name="钱包余额")
    credit = models.IntegerField(default=0, verbose_name="积分")
    avatar = models.ImageField(upload_to="avatar/%Y", null=True, default="", verbose_name="个人头像")
    nickname = models.CharField(max_length=50, default="", null=True, verbose_name="用户昵称")

    class Meta:
        db_table = 'lf_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
```

我们自定义的用户模型类还不能直接被Django的认证系统所识别，需要在配置文件中告知Django认证系统使用我们自定义的模型类。

在settings/dev.py配置文件中进行设置

```python
AUTH_USER_MODEL = 'users.User'
```

`AUTH_USER_MODEL` 参数的设置以`点.`来分隔，表示`应用名.模型类名`。

**注意：Django建议我们对于AUTH_USER_MODEL参数的设置一定要在第一次数据库迁移之前就设置好，否则后续使用可能出现未知错误。**

![image-20220410043300396](assets/image-20220410043300396.png)

这是表示有一个叫admin的子应用使用了原来的废弃的auth.User模型，但是目前数据库已经设置了默认的子应用为`users`的模型了，所以产生了冲突。那么这种冲突，我们需要重置下原来的auth模块的迁移操作，再次迁移就可以解决了。

```
解决步骤：
1. 备份数据库[如果刚开始开发，无需备份。]
   cd /home/moluo/Desktop/luffycity/docs
   mysqldump -uroot -p123 luffycity > 03_20_luffycity.sql

​````
mysqldump: [Warning] Using a password on the command line interface can be insecure.
(base) kanghua@ubuntu:~/Desktop/luffycity/docs$ mysqldump -uroot -p luffycity > 03_20_luffycity.sql
Enter password: 
​````
2. 注释掉users.User代码以及AUTH_USER_MODEL配置项，然后执行数据迁移回滚操作，把冲突的所有表迁移记录全部归零
   cd ~/Desktop/luffycity/luffycityapi
   # python manage.py migrate <子应用目录> zero
   python manage.py migrate auth zero

3. 恢复users.User代码以及AUTH_USER_MODEL配置项，执行数据迁移。
   python manage.py makemigrations
   python manage.py migrate
4. 创建管理员查看auth功能是否能正常使用。
   python manage.py createsuperuser
```

提交版本

```bash
cd ~/Desktop/luffycity/luffycityapi
git add .
git commit -m "feature:自定义用户模型"
git push origin feature/user
```



### 实现jwt认证分布式认证流程

在用户注册或登录后，我们想记录用户的登录状态，或者为用户创建身份认证的凭证。我们不再使用Session认证机制，而使用Json Web Token认证机制。

```
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者（客户端）和服务提供者（服务端）间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于身份认证，也可被数据加密传输。
```



### JWT的构成

JWT就一段字符串，由三段信息构成的，将这三段信息文本用`.`拼接一起就构成了Jwt token字符串。就像这样:

```
eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAiMTUwMTIzNDU1IiwgImlhdCI6ICIxNTAxMDM0NTUiLCAibmFtZSI6ICJ3YW5neGlhb21pbmciLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ==.815ce0e4e15fff813c5c9b66cfc3791c35745349f68530bc862f7f63c9553f4b
```

第一部分我们称它为头部（header)，第二部分我们称其为载荷（payload, 类似于飞机上承载的物品)，第三部分是签证（signature).



### header

jwt的头部承载两部分信息：

- typ: 声明token类型，这里是jwt ，typ的值也可以是：Bear
- alg: 声明签证的加密的算法 通常直接使用 HMAC SHA256

完整的头部就像下面这样的JSON：

```
{
  'typ': 'JWT',
  'alg': 'HS256'
}
```

然后将头部进行base64编码，构成了jwt的第一部分头部

python代码举例：

```python
import base64, json
header_data = {"typ": "jwt", "alg": "HS256"}
# json.dumps先序列化成json字符串 , encode()将 str 类型转换成 bytes 类型
header = base64.b64encode( json.dumps(header_data).encode() ).decode()  
print(header) # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9
```



### payload

载荷就是存放有效信息的地方。这个名字像是特指飞机上承载的货仓，这些有效信息包含三个部分:

- 标准声明
- 公共声明
- 私有声明

**标准声明**指定jwt实现规范中要求的属性。 (官方建议但不强制使用) ：

- iss: jwt签发者
- sub: jwt所面向的用户
- **aud**: 接收jwt的一方
- **exp**: jwt的过期时间，这个过期时间必须要大于签发时间
- **nbf**: 定义在什么时间之后，该jwt才可以使用
- **iat**: jwt的签发时间
- **jti**: jwt的唯一身份标识，主要用来作为一次性token, 从而回避重放攻击。

**公共声明** ： 公共的声明可以添加任何的公开信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可直接读取.

**私有声明** ： 私有声明是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，里面存放的是一些可以在服务端或者客户端通过秘钥进行加密和解密的加密信息。往往采用的RSA非对称加密算法。

举例，定义一个payload载荷信息，demo/jwtdemo.py：

```python
import base64, json, time

if __name__ == '__main__':
    # 载荷
    iat = int(time.time())
    payload_data = {
        "sub": "root",
        "exp": iat + 3600,  # 假设一小时过期
        "iat": iat,
        "name": "wangxiaoming",
        "avatar": "1.png",
        "user_id": 1,
        "admin": True,
        "acc_pwd": "QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9",
    }
    # 将其进行base64编码，得到JWT的第二部分。
    payload = base64.b64encode(json.dumps(payload_data).encode()).decode()
    print(payload)
    # eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjQ3Nzc0Mjk1LCAiaWF0IjogMTY0Nzc3MDY5NSwgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImF2YXRhciI6ICIxLnBuZyIsICJ1c2VyX2lkIjogMSwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0=

```

Js console

```js
payload = "eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjQ3Nzc0Mjk1LCAiaWF0IjogMTY0Nzc3MDY5NSwgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImF2YXRhciI6ICIxLnBuZyIsICJ1c2VyX2lkIjogMSwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0="
'eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjQ3Nzc0Mjk1LCAiaWF0IjogMTY0Nzc3MDY5NSwgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImF2YXRhciI6ICIxLnBuZyIsICJ1c2VyX2lkIjogMSwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0='
JSON.parse(atob(payload))
{sub: 'root', exp: 1647774295, iat: 1647770695, name: 'wangxiaoming', avatar: '1.png', …}
JSON.parse(atob(payload)).avatar
'1.png'
```





### signature

JWT的第三部分是一个签证信息，用于辨真伪，防篡改。这个签证信息由三部分组成：

- header (base64后的头部)
- payload (base64后的载荷)
- secret（保存在服务端的秘钥字符串，不会提供给客户端的，这样可以保证客户端没有签发token的能力）

举例，定义一个完整的jwt token，demo/jwtdemo.py：

```python
import base64, json, hashlib

if __name__ == '__main__':
    """jwt 头部的生成"""
    header_data = {"typ": "jwt", "alg": "HS256"}
    header = base64.b64encode( json.dumps(header_data).encode() ).decode()
    print(header) # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9

    """jwt 载荷的生成"""
    payload_data = {
        "sub": "root",
        "exp": "150123455",
        "iat": "150103455",
        "name": "wangxiaoming",
        "admin": True,
        "acc_pwd": "QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9",
    }
    # 将其进行base64编码，得到JWT的第二部分。
    payload = base64.b64encode(json.dumps(payload_data).encode()).decode()
    print(payload) # eyJzdWIiOiAicm9vdCIsICJleHAiOiAiMTUwMTIzNDU1IiwgImlhdCI6ICIxNTAxMDM0NTUiLCAibmFtZSI6ICJ3YW5neGlhb21pbmciLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ==

    # from django.conf import settings
    # secret = settings.SECRET_KEY
    secret = 'django-insecure-hbcv-y9ux0&8qhtkgmh1skvw#v7ru%t(z-#chw#9g5x1r3z=$p'
    data = header + payload + secret  # 秘钥绝对不能提供给客户端。
    HS256 = hashlib.sha256()
    HS256.update(data.encode('utf-8'))
    signature = HS256.hexdigest()
    print(signature) # 815ce0e4e15fff813c5c9b66cfc3791c35745349f68530bc862f7f63c9553f4b

    # jwt 最终的生成
    token = f"{header}.{payload}.{signature}"
    print(token)
    # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAiMTUwMTIzNDU1IiwgImlhdCI6ICIxNTAxMDM0NTUiLCAibmFtZSI6ICJ3YW5neGlhb21pbmciLCAiYWRtaW4iOiB0cnVlLCAiYWNjX3B3ZCI6ICJRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjkifQ==.815ce0e4e15fff813c5c9b66cfc3791c35745349f68530bc862f7f63c9553f4b
```

**注意：secret是保存在服务器端的，jwt的签发生成也是在服务器端的，secret就是用来进行jwt的签发和jwt的验证，所以，它就是你服务端的私钥，在任何场景都不应该流露出去。一旦客户端得知这个secret, 那就意味着客户端是可以自我签发jwt了。**

![image-20210716111517771](assets/image-20210716111517771.png)

举例，定义一个完整的jwt token，并认证token，demo/jwtdemo.py：

```python
import base64, json, hashlib
from datetime import datetime

if __name__ == '__main__':
    # 头部生成原理
    header_data = {
        "typ": "jwt",
        "alg": "HS256"
    }
    # print( json.dumps(header_data).encode() )
    # json转成字符串，接着base64编码处理
    header = base64.b64encode(json.dumps(header_data).encode()).decode()
    print(header)  # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9


    # 载荷生成原理
    iat = int(datetime.now().timestamp()) # 签发时间
    payload_data = {
        "sub": "root",
        "exp": iat + 3600,  # 假设一小时过期
        "iat": iat,
        "name": "wangxiaoming",
        "admin": True,
        "acc_pwd": "QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9QiLCJhbGciOiJIUzI1NiJ9",
    }

    payload = base64.b64encode(json.dumps(payload_data).encode()).decode()
    print(payload)
    # eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjM2NTk3OTAzLCAiaWF0IjogMTYzNjU5NDMwMywgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0=

    # from django.conf import settings
    # secret = settings.SECRET_KEY
    secret = 'django-insecure-hbcv-y9ux0&8qhtkgmh1skvw#v7ru%t(z-#chw#9g5x1r3z=$p'

    data = header + payload + secret  # 秘钥绝对不能提供给客户端。

    HS256 = hashlib.sha256()
    HS256.update(data.encode('utf-8'))
    signature = HS256.hexdigest()
    print(signature) # ce46f9d350be6b72287beb4f5f9b1bc4c42fc1a1f8c8db006e9e99fd46961156

    # jwt 最终的生成
    token = f"{header}.{payload}.{signature}"
    print(token)
    # eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjM2NTk3OTAzLCAiaWF0IjogMTYzNjU5NDMwMywgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0=.ce46f9d350be6b72287beb4f5f9b1bc4c42fc1a1f8c8db006e9e99fd46961156


    # 认证环节
    token = "eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiAicm9vdCIsICJleHAiOiAxNjM2NTk3OTAzLCAiaWF0IjogMTYzNjU5NDMwMywgIm5hbWUiOiAid2FuZ3hpYW9taW5nIiwgImFkbWluIjogdHJ1ZSwgImFjY19wd2QiOiAiUWlMQ0poYkdjaU9pSklVekkxTmlKOVFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5In0=.ce46f9d350be6b72287beb4f5f9b1bc4c42fc1a1f8c8db006e9e99fd46961156"
    # token = "eyJ0eXAiOiAiand0IiwgImFsZyI6ICJIUzI1NiJ9.eyJzdWIiOiJyb290IiwiZXhwIjoxNjMxNTI5MDg4LCJpYXQiOjE2MzE1MjU0ODgsIm5hbWUiOiJ3YW5neGlhb2hvbmciLCJhZG1pbiI6dHJ1ZSwiYWNjX3B3ZCI6IlFpTENKaGJHY2lPaUpJVXpJMU5pSjlRaUxDSmhiR2NpT2lKSVV6STFOaUo5UWlMQ0poYkdjaU9pSklVekkxTmlKOSJ9.b533c5515444c51058557017e433d411379862d91640c8beed6f2617b1da2feb"
    header, payload, signature = token.split(".")

    # 验证是否过期了
    # 先基于base64，接着使用json解码
    payload_data = json.loads( base64.b64decode(payload.encode()) )
    print(payload_data)
    exp = payload_data.get("exp", None)
    if exp is not None and int(exp) < int(datetime.now().timestamp()):
        print("token过期！！！")
    else:
        print("没有过期")

    # 验证token是否有效，是否被篡改
    # from django.conf import settings
    # secret = settings.SECRET_KEY
    secret = 'django-insecure-hbcv-y9ux0&8qhtkgmh1skvw#v7ru%t(z-#chw#9g5x1r3z=$p'
    data = header + payload + secret  # 秘钥绝对不能提供给客户端。
    HS256 = hashlib.sha256()
    HS256.update(data.encode('utf-8'))
    new_signature = HS256.hexdigest()

    if new_signature != signature:
        print("认证失败")
    else:
        print("认证通过")

```

提交版本

```bash
cd ~/Desktop/luffycity/luffycityapi
git add .
git commit -m "test:jwt构成原理、jwt签发和验证流程"
git push origin feature/user
```



关于签发和核验JWT，python中提供了一个PyJWT模块帮我们实现jwt的整体流程。我们可以使用Django REST framework JWT扩展来完成。

文档网站：https://jpadilla.github.io/django-rest-framework-jwt/



### 安装配置JWT

安装

```shell
pip install djangorestframework-jwt
```

settings/dev.py，配置jwt

```python
# drf配置
REST_FRAMEWORK = {
    # 自定义异常处理
    'EXCEPTION_HANDLER': 'luffycityapi.utils.exceptions.exception_handler',
    # 自定义认证
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt认证
        'rest_framework.authentication.SessionAuthentication',           # session认证
        'rest_framework.authentication.BasicAuthentication',
    ),
}

import datetime
# jwt认证相关配置项
JWT_AUTH = {
    # 设置jwt的有效期
    # 如果内部站点，例如：运维开发系统，OA，往往配置的access_token有效期基本就是15分钟，30分钟，1~2个小时
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=1), # 一周有效，
}
```

- JWT_EXPIRATION_DELTA 指明token的有效期



### 生成jwt

Django REST framework JWT 扩展的说明文档中提供了手动签发JWT的方法

官方文档：https://jpadilla.github.io/django-rest-framework-jwt/#creating-a-new-token-manually

```python
# 可以进入到django的终端下测试生成token的逻辑
python manage.py shell

# 引入jwt配置
from rest_framework_jwt.settings import api_settings
# 获取载荷生成函数
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# 获取token生成函数
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# 生成载荷需要的字典数据
# 此处，拿数据库中的用户信息进行测试
from users.models import User
user = User.objects.first()
payload = jwt_payload_handler(user)  # user用户模型对象
# 生成token
token = jwt_encode_handler(payload)
```

在用户注册或登录成功后，在序列化器中返回用户信息以后同时返回token即可。



### 后端实现登陆认证接口

Django REST framework-JWT为了方便开发者使用jwt提供了登录获取token的视图，开发者可以直接使用它绑定一个url地址即可。

在users/urls.py中绑定登陆视图

```python
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path("login/", obtain_jwt_token, name="login"),
]

# obtain_jwt_token实际上就是 rest_framework_jwt.views.ObtainJSONWebToken.as_view()

# 登录视图，获取access_token
# obtain_jwt_token = ObtainJSONWebToken.as_view()
# 刷新token视图，依靠旧的access_token生成新的access_token
# refresh_jwt_token = RefreshJSONWebToken.as_view()
# 验证现有的access_token是否有效
# verify_jwt_token = VerifyJSONWebToken.as_view()

```

接下来，我们可以通过postman来测试下功能，可以发送form表单，也可以发送json，username和password是必填字段

![image-20220410091633460](assets/image-20220410091633460.png)





## 前端实现登陆功能

在登陆组件中找到登陆按钮，绑定点击事件，调用登录处理方法loginhandle。

components/Login.vue

```html
<template>
  <div class="title">
    <span :class="{active:user.login_type==0}" @click="user.login_type=0">密码登录</span>
    <span :class="{active:user.login_type==1}" @click="user.login_type=1">短信登录</span>
  </div>
  <div class="inp" v-if="user.login_type==0">
    <input v-model="user.account" type="text" placeholder="用户名 / 手机号码" class="user">
    <input v-model="user.password" type="password" class="pwd" placeholder="密码">
    <div id="geetest1"></div>
    <div class="rember">
      <label>
        <input type="checkbox" class="no" v-model="user.remember"/>
        <span>记住密码</span>
      </label>
      <p>忘记密码</p>
    </div>
    <button class="login_btn" @click="loginhandler">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
  <div class="inp" v-show="user.login_type==1">
    <input v-model="user.mobile" type="text" placeholder="手机号码" class="user">
    <input v-model="user.code"  type="text" class="code" placeholder="短信验证码">
    <el-button id="get_code" type="primary">获取验证码</el-button>
    <button class="login_btn">登录</button>
    <p class="go_login" >没有账号 <span>立即注册</span></p>
  </div>
</template>
```

```vue
<script setup>
import user from "../api/user";
import { ElMessage } from 'element-plus'

// 登录处理
const loginhandler = ()=>{
  // 验证数据
  if(user.account.length<1 || user.password.length<1){
    // 错误提示
    console.log("错了哦，用户名或密码不能为空！");
    ElMessage.error("错了哦，用户名或密码不能为空！");
    return ;
  }

  // 登录请求处理
  user.login().then(response=>{
    console.log(response.data);
    ElMessage.success("登录成功！");
  }).catch(error=>{
    ElMessage.error("登录失败！");
  })
}

</script>
```

在api中请求后端，api/user.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const user = reactive({
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    account: "",  // 登录账号/手机号/邮箱
    password: "", // 登录密码
    remember: false, // 是否记住登录状态
    mobile: "",      // 登录手机号码
    code: "",        // 短信验证码
    login(){
        // 用户登录
        return http.post("/users/login/", {
            "username": this.account,
            "password": this.password,
        })
    }
})

export default user;
```

解决elementplus显示错误提示框没有样式的问题。src/main.js，代码：

```javascript
import { createApp } from 'vue'
import App from './App.vue'

import 'element-plus/dist/index.css';

import router from "./router/index.js";

createApp(App).use(router).mount('#app')
```

提交版本

```bash
cd ~/Desktop/luffycity/luffycityapi
git add .
git commit -m "feature:客户端请求登陆功能基本实现"
git push origin feature/user
```



### 前端保存jwt

我们保存在浏览器的HTML5提供的本地存储对象中。

浏览器的本地存储提供了2个全局的js对象，给我们用于保存数据的，分别是sessionStorage 和 localStorage ：

- **sessionStorage** 会话存储，浏览器关闭即数据丢失。
- **localStorage** 永久存储，长期有效，浏览器关闭了也不会丢失。

我们可以通过浏览器提供的Application调试选项中的界面查看到保存在本地存储的数据。

![image-20210716121858268](assets/image-20210716121858268.png)

注意：不同的域名或IP下的数据，互不干扰的，相互独立，也调用或访问不了其他域名下的数据。

sessionStorage和localStorage提供的操作一模一样，基本使用：

```js
// 添加/修改数据
sessionStorage.setItem("变量名","变量值")
// 简写：sessionStorage.变量名 = 变量值

// 读取数据
sessionStorage.getItem("变量名")
// 简写：sessionStorage.变量名

// 删除一条数据
sessionStorage.removeItem("变量名")
// 清空所有数据
sessionStorage.clear()  // 慎用，会清空当前域名下所有的存储在本地的数据



// 添加/修改数据
localStorage.setItem("变量名","变量值")
// 简写：localStorage.变量名 = 变量值

// 读取数据
localStorage.getItem("变量名")
// 简写：localStorage.变量名

// 删除数据
localStorage.removeItem("变量名")
// 清空数据
localStorage.clear()  // 慎用，会清空当前域名下所有的存储在本地的数据
```



登陆子组件，components/Login.vue，代码：

```vue
<script setup>
import user from "../api/user";
import { ElMessage } from 'element-plus'

// 登录处理
const loginhandler = ()=>{
  if(user.account.length<1 || user.password.length<1){
    // 错误提示
    console.log("错了哦，用户名或密码不能为空！");
    ElMessage.error('错了哦，用户名或密码不能为空！');
    return;  // 在函数/方法中，可以阻止代码继续往下执行
  }

  // 登录请求处理
  user.login().then(response=>{
     // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    console.log(response.data.token);
    if(user.remember){ // 判断是否记住登录状态
      // 记住登录
      localStorage.token = response.data.token
    }else{
      // 不记住登录，关闭浏览器以后就删除状态
      sessionStorage.token = response.data.token;
    }
    // 保存token，并根据用户的选择，是否记住密码
    // 成功提示
    ElMessage.success("登录成功！");
    console.log("登录成功！");
    // 关闭登录弹窗

  }).catch(error=>{
    ElMessage.error("登录失败！");
    console.log(error);
  })
}

</script>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端使用本地存储保存token"
git push origin feature/user
```



### 首页登录成功以后关闭登录弹窗

在components/Login.vue中，基于emit发送自定义事件通知父组件关闭当前登录窗口。components/Login.vue，代码：

```vue
<script setup>
import user from "../api/user"
import { ElMessage } from 'element-plus'
const emit = defineEmits(["successhandle",])

const loginhandler = ()=>{
  // 登录处理
  if(user.username.length<1 || user.password.length<1){
    // 错误提示
    ElMessage.error('错了哦，用户名或密码不能为空！');
    return false // 在函数/方法中，可以阻止代码继续往下执行
  }

   // 登录请求处理
  user.login().then(response=>{
     // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    console.log(response.data.token);
    if(user.remember){ // 判断是否记住登录状态
      // 记住登录
      localStorage.token = response.data.token
    }else{
      // 不记住登录，关闭浏览器以后就删除状态
      sessionStorage.token = response.data.token;
    }
    // 保存token，并根据用户的选择，是否记住密码
    // 成功提示
    ElMessage.success("登录成功！");
    console.log("登录成功！");
     // 关闭登录弹窗，对外发送一个登录成功的信息
    user.account = ""
    user.password = ""
    user.mobile = ""
    user.code = ""
    user.remember = false
    emit("successhandle")

  }).catch(error=>{
    ElMessage.error("登录失败！");
    console.log(error);
  })
}

</script>
```

在首页中是通过Header子组件调用的component/Login.vue，所以我们需要在Header子组件中监听自定义事件login_success并关闭登陆弹窗即可。components/Header.vue，代码：

```vue
<el-dialog :width="600" v-model="state.show_login">
    <Login @successhandle="login_success"></Login>
</el-dialog>
```

```vue
<script setup>
import Login from "./Login.vue"

import nav from "../api/nav"
import {reactive} from "vue";

const state = reactive({
  show_login: false,
})

// 获取头部导航
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data;
})

// 用户登录成功以后的处理
const login_success = (token)=>{
  state.show_login = false
}

</script>
```

views/Login.vue登陆页面中，则监听Login子组件登陆成功的自定义事件以后直接路由跳转到首页即可。`views/Login.vue`，代码：

```vue
<template>
	<div class="login box">
		<img src="../assets/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../assets/logo.png" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <Login @successhandle="login_success"></Login>
      </div>
		</div>
	</div>
</template>
```

```vue
<script setup>
import Login from "../components/Login.vue"
import router from "../router";

// 用户登录成功以后的处理
const login_success = ()=>{
  // 跳转到首页
  router.push("/");
}

</script>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端登陆成功以后关闭窗口或登陆页面"
git push origin feature/user
```



### 自定义载荷

默认返回值的token只有username和user_id以及email，我们如果还需在客户端页面中显示当前登陆用户的其他信息(例如：头像)，则可以把额外的用户信息添加到jwt的返回结果中。通过修改该视图的返回值可以完成我们的需求。

在utils/authenticate.py 中，创建jwt_payload_handler函数重写返回值。

```python
from rest_framework_jwt.utils import jwt_payload_handler as payload_handler


def jwt_payload_handler(user):
    """
    自定义载荷信息
    :params user  用户模型实例对象
    """
    # 先让jwt模块生成自己的载荷信息
    payload = payload_handler(user)
    # 追加自己要返回的内容
    if hasattr(user, 'avatar'):
        payload['avatar'] = user.avatar.url if user.avatar else ""
    if hasattr(user, 'nickname'):
        payload['nickname'] = user.nickname

    if hasattr(user, 'money'):
        payload['money'] = float(user.money)
    if hasattr(user, 'credit'):
        payload['credit'] = user.credit

    return payload

```

修改settings/dev.py配置文件

```python
import datetime
# jwt认证相关配置项
JWT_AUTH = {
    # 设置jwt的有效期
    # 如果内部站点，例如：运维开发系统，OA，往往配置的access_token有效期基本就是15分钟，30分钟，1~2个小时
    'JWT_EXPIRATION_DELTA': datetime.timedelta(weeks=1), # 一周有效，
    # 自定义载荷
    'JWT_PAYLOAD_HANDLER': 'luffycityapi.utils.authenticate.jwt_payload_handler',
}

```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:服务端重写jwt的自定义载荷生成函数增加token载荷信息"
git push origin feature/user
```



### 多条件登录

JWT扩展的登录视图，在收到用户名与密码时，也是调用Django的认证系统中提供的**authenticate()**来检查用户名与密码是否正确。

我们可以通过修改Django认证系统的认证后端（主要是authenticate方法）来支持登录账号既可以是用户名也可以是手机号。

**修改Django认证系统的认证后端需要继承django.contrib.auth.backends.ModelBackend，并重写authenticate方法。**

`authenticate(self, request, username=None, password=None, **kwargs)`方法的参数说明：

- request 本次认证的请求对象
- username 本次认证提供的用户账号
- password 本次认证提供的密码

**我们想要让用户既可以以用户名登录，也可以以手机号登录，那么对于authenticate方法而言，username参数即表示用户名或者手机号。**

重写authenticate方法的思路：

1. 根据username参数查找用户User对象，username参数可能是用户名，也可能是手机号
2. 若查找到User对象，调用User对象的check_password方法检查密码是否正确

在utils/authenticate.py中编写：

```python
from rest_framework_jwt.utils import jwt_payload_handler as payload_handler
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q


def jwt_payload_handler(user):
    """
    自定义载荷信息
    :params user  用户模型实例对象
    """
    # 先让jwt模块生成自己的载荷信息
    payload = payload_handler(user)
    # 追加自己要返回的字段内容
    if hasattr(user, 'avatar'):
        payload['avatar'] = user.avatar.url if user.avatar else ""
    if hasattr(user, 'nickname'):
        payload['nickname'] = user.nickname
    if hasattr(user, 'money'):
        payload['money'] = float(user.money)
    if hasattr(user, 'credit'):
        payload['credit'] = user.credit

    return payload


def get_user_by_account(account):

    """
    根据帐号信息获取user模型实例对象
    :param account: 账号信息，可以是用户名，也可以是手机号，甚至其他的可用于识别用户身份的字段信息
    :return: User对象 或者 None
    """
    user = UserModel.objects.filter(Q(mobile=account) | Q(username=account) | Q(email=account)).first()
    return user


class CustomAuthBackend(ModelBackend):
    """
    自定义用户认证类[实现多条件登录]
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        多条件认证方法
        :param request: 本次客户端的http请求对象
        :param username:  本次客户端提交的用户信息，可以是user，也可以mobile或其他唯一字段
        :param password: 本次客户端提交的用户密码
        :param kwargs: 额外参数
        :return:
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return
        # 根据用户名信息useranme获取账户信息
        user = get_user_by_account(username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
```

在配置文件settings/dev.py中告知Django使用我们自定义的认证后端，注意不是给drf添加设置。

```python
# django自定义认证
AUTHENTICATION_BACKENDS = ['luffycityapi.utils.authenticate.CustomAuthBackend', ]
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:服务端实现jwt多条件登陆认证"
git push origin feature/user
```



## 客户端实现用户登陆状态的判断

components/Header.vue，子组件代码：

```vue
<template>
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo">
            <router-link to="/"><img src="../assets/logo.svg" alt=""></router-link>
          </div>
          <ul class="nav">
              <li v-for="nav in nav.header_nav_list">
                <a :href="nav.link" v-if="nav.is_http">{{nav.name}}</a>
                <router-link :to="nav.link" v-else>{{nav.name}}</router-link>
              </li>
          </ul>
          <div class="search-warp">
            <div class="search-area">
              <input class="search-input" placeholder="请输入关键字..." type="text" autocomplete="off">
              <div class="hotTags">
                <router-link to="/search/?words=Vue" target="_blank" class="">Vue</router-link>
                <router-link to="/search/?words=Python" target="_blank" class="last">Python</router-link>
              </div>
            </div>
            <div class="showhide-search" data-show="no"><img class="imv2-search2" src="../assets/search.svg" /></div>
          </div>
          <div class="login-bar logined-bar" v-show="state.is_login">
            <div class="shop-cart ">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box ">
              <router-link to="">我的课堂</router-link>
              <el-dropdown>
                <span class="el-dropdown-link">
                  <el-avatar class="avatar" size="50" src="https://fuguangapi.oss-cn-beijing.aliyuncs.com/avatar.jpg"></el-avatar>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="UserFilled">学习中心</el-dropdown-item>
                    <el-dropdown-item :icon="List">订单列表</el-dropdown-item>
                    <el-dropdown-item :icon="Setting">个人设置</el-dropdown-item>
                    <el-dropdown-item :icon="Position">注销登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          <div class="login-bar" v-show="!state.is_login">
            <div class="shop-cart full-left">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <span @click="state.show_login=true">登录</span>
              &nbsp;/&nbsp;
              <span>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog :width="600" v-model="state.show_login">
      <Login @successhandle="login_success"></Login>
    </el-dialog>
</template>
```

```vue
<script setup>
import {UserFilled, List, Setting, Position} from '@element-plus/icons-vue'
import Login from "./Login.vue"
import nav from "../api/nav";
import {reactive} from "vue";

const state = reactive({
  is_login: true,  // 登录状态
  show_login: false,
})

// 请求头部导航列表
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data
})

// 用户登录成功以后的处理
const login_success = ()=>{
  state.show_login = false
}

</script>
```

```vue
<style scoped>
/* 登陆后状态栏 */
.logined-bar{
  margin-top: 0;
  height: 72px;
  line-height: 72px;
}
.header .logined-bar .shop-cart{
  height: 32px;
  line-height: 32px;
}
.logined-bar .login-box{
  height: 72px;
  line-height: 72px;
  position: relative;
}
.logined-bar .el-avatar{
  float: right;
  width: 50px;
  height: 50px;
  position: absolute;
  top: -10px;
  left: 10px;
  transition: transform .5s ease-in .1s;
}
.logined-bar .el-avatar:hover{
  transform: scale(1.3);
}
</style>
```

如果图标没有显示，可以采用安装以下组件：

```bash
yarn add @element-plus/icons-vue
```



### 使用Vuex保存用户登录状态并判断是否在登陆栏显示用户信息

Vuex是Vue框架生态的一环，用于实现全局数据状态的统一管理。

官方地址：https://next.vuex.vuejs.org/zh/index.html

```bash
cd ~/Desktop/luffycity/luffycityweb
# 在客户端项目根目录下执行安装命令
yarn add vuex@next
```

Vuex初始化，是在src目录下创建store目录，store目录下创建index.js文件对vuex进行初始化：

```javascript
import {createStore} from "vuex"

// 实例化一个vuex存储库
export default createStore({
    state () {  // 数据存储位置，相当于组件中的data
        return {
          user: {

          }
        }
    },
    mutations: { // 操作数据的方法，相当于methods
        login (state, user) {  // state 就是上面的state   state.user 就是上面的数据
          state.user = user
        }
    }
})
```

main.js中注册vuex，代码：

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from "./router";
import store from "./store"

import 'element-plus/theme-chalk/index.css'

createApp(App).use(router).use(store).mount('#app')

```

在components/Login.vue子组件中登录成功以后，记录用户信息到vuex中。

```vue
<script setup>
import {reactive} from "vue";
import { ElMessage } from 'element-plus'
import user from "../api/user";
const emit = defineEmits(["successhandle",])

import {useStore} from "vuex"
const store = useStore()

const state = reactive({
  login_type: 0,
  username:"",
  password:"",
})

// 登录处理
const loginhandler = ()=>{
  // 验证数据
  if(user.account.length<1 || user.password.length<1){
    // 错误提示
    console.log("错了哦，用户名或密码不能为空！");
    ElMessage.error("错了哦，用户名或密码不能为空！");
    return ;
  }

  // 登录请求处理
  user.login().then(response=>{
     // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    console.log(response.data.token);
    if(user.remember){ // 判断是否记住登录状态
      // 记住登录
      localStorage.token = response.data.token
    }else{
      // 不记住登录，关闭浏览器以后就删除状态
      sessionStorage.token = response.data.token;
    }

    // vuex存储用户登录信息，保存token，并根据用户的选择，是否记住密码
    let payload = response.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    console.log(payload_data)
    store.commit("login", payload_data)

    // 保存token，并根据用户的选择，是否记住密码
    // 成功提示
    ElMessage.success("登录成功！");
    console.log("登录成功！");
     // 关闭登录弹窗，对外发送一个登录成功的信息
    user.account = ""
    user.password = ""
    user.mobile = ""
    user.code = ""
    user.remember = false
    emit("successhandle")

  }).catch(error=>{
    ElMessage.error("登录失败！");
    console.log(error);
  })
}
</script>
```

记录下来了以后，我们就可以直接components/Header.vue中读取Vuex中的用户信息。

```vue
<template>
    <div class="header-box">
      <div class="header">
        <div class="content">
          <div class="logo">
            <router-link to="/"><img src="../assets/logo.png" alt=""></router-link>
          </div>
          <ul class="nav">
              <li v-for="item in nav.header_nav_list">
                <a v-if="item.is_http" :href="item.link">{{item.name}}</a>
                <router-link v-else :to="item.link">{{item.name}}</router-link>
              </li>
          </ul>
          <div class="search-warp">
            <div class="search-area">
              <input class="search-input" placeholder="请输入关键字..." type="text" autocomplete="off">
              <div class="hotTags">
                <router-link to="/search/?words=Vue" target="_blank" class="">Vue</router-link>
                <router-link to="/search/?words=Python" target="_blank" class="last">Python</router-link>
              </div>
            </div>
            <div class="showhide-search" data-show="no"><img class="imv2-search2" src="../assets/search.svg" /></div>
          </div>
          <div class="login-bar logined-bar" v-if="store.state.user.user_id">
            <div class="shop-cart ">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box ">
              <router-link to="">我的课堂</router-link>
              <el-dropdown>
                <span class="el-dropdown-link">
                  <el-avatar class="avatar" size="50" src="https://luffycityapi.oss-cn-beijing.aliyuncs.com/avatar.jpg"></el-avatar>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item icon="el-icon-user">学习中心</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-edit-outline">订单列表</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-setting">个人设置</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-position">注销登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          <div class="login-bar" v-else>
            <div class="shop-cart full-left">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <span @click="state.show_login=true">登录</span>
              &nbsp;/&nbsp;
              <span>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog :width="600" v-model="state.show_login">
    <Login @login_success="login_success"></Login>
    </el-dialog>
</template>
```

```vue
<script setup>
import {UserFilled, List, Setting, Position} from '@element-plus/icons-vue'
import Login from "./Login.vue"
import {reactive} from "vue";
import nav from "../api/nav";
import {useStore} from "vuex"
const store = useStore()

const state = reactive({
  // is_login: true,  // 登录状态
  show_login: false,
})

// 获取头部导航
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data;
}).catch(error=>{
  console.log(error);
});


// 用户登录成功以后的处理
const login_success = (token)=>{
  state.show_login = false
}
</script>
```

因为vuex默认是保存数据在内存中的，所以基于浏览器开发的网页，如果在F5刷新网页时会存在数据丢失的情况。所以我们可以把store数据永久存储到localStorage中。这里就需要使用插件vuex-persistedstate来实现。 

在前端项目的根目录下执行安装命令

```bash
cd ~/Desktop/luffycity/luffycityweb
yarn add vuex-persistedstate
```

在vuex的store/index.js文件中导入此插件。

```javascript
import {createStore} from "vuex"
import createPersistedState from "vuex-persistedstate"

// 实例化一个vuex存储库
export default createStore({
    // 调用永久存储vuex数据的插件，localstorage里会多一个名叫vuex的Key，里面就是vuex的数据
    plugins: [createPersistedState()],
    state(){  // 相当于组件中的data，用于保存全局状态数据
        return {
            user: {}
        }
    },
    getters: {
        getUserInfo(state){
            // 从jwt的载荷中提取用户信息
            let now = parseInt( (new Date() - 0) / 1000 );
            if(state.user.exp === undefined) {
                // 没登录
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }

            if(parseInt(state.user.exp) < now) {
                // 过期处理
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }
            return state.user;
        }
    },
    mutations: { // 相当于组件中的methods，用于操作state全局数据
        login(state, payload){
            state.user = payload; // state.user 就是上面声明的user
        }
    }
})
```

完成了登录功能以后，我们要防止用户翻墙访问需要认证身份的页面时，可以基于vue-router的导航守卫来完成。

src/router/index.js，代码：

```javascript
import {createRouter, createWebHistory} from 'vue-router'
import store from "../store";
// 路由列表
const routes = [
  {
    meta:{
        title: "首页",
        keepAlive: true
    },
    path: '/',         // uri访问地址
    name: "Home",
    component: ()=> import("../views/Home.vue")
  },
  {
    meta:{
        title: "用户登录",
        keepAlive: true
    },
    path:'/login',      // uri访问地址
    name: "Login",
    component: ()=> import("../views/Login.vue")
  },{
    meta:{
        title: "luffy2.0-个人中心",
        keepAlive: true,
      	authorization:true,
    },
    path: '/user',
    name: "User",
    component: ()=> import("../views/User.vue"),
  },
]

// 路由对象实例化
const router = createRouter({
  // history, 指定路由的模式
  history: createWebHistory(),
  // 路由列表
  routes,
});



// 导航守卫
router.beforeEach((to, from, next)=>{
  document.title=to.meta.title
  // 登录状态验证
  if (to.meta.authorization && !store.getters.getUserInfo) {
    next({"name": "Login"})
  }else{
    next()
  }
})

// 暴露路由对象
export default router
```

src/views/User.vue，代码：

```vue
<template>
用户中心
</template>

<script>
export default {
  name: "User"
}
</script>

<style scoped>

</style>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端基于vuex存储本地全局数据并判断登陆状态"
git push origin feature/user
```





## 退出登录功能

在vuex的store/index.js中编写一个登录注销的方法logout，代码：

```javascript
import {createStore} from "vuex"
import createPersistedState from "vuex-persistedstate"

// 实例化一个vuex存储库
export default createStore({
    // 调用永久存储vuex数据的插件，localstorage里会多一个名叫vuex的Key，里面就是vuex的数据
    plugins: [createPersistedState()],
    state(){  // 相当于组件中的data，用于保存全局状态数据
        return {
            user: {}
        }
    },
    getters: {
        getUserInfo(state){
            let now = parseInt( (new Date() - 0) / 1000 );
            if(state.user.exp === undefined) {
                // 没登录
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }

            if(parseInt(state.user.exp) < now) {
                // 过期处理
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }
            return state.user;
        }
    },
    mutations: { // 相当于组件中的methods，用于操作state全局数据
        login(state, payload){
            state.user = payload; // state.user 就是上面声明的user
        },
        logout(state){ // 退出登录
            state.user = {}
            localStorage.token = null;
            sessionStorage.token = null;
        }
    }
})
```

在用户点击头部登录栏的注销登录时绑定登录注销操作。`components/Header.vue`，代码：

```vue
<el-dropdown-item :icon="Position" @click="logout">注销登录</el-dropdown-item>
```

```vue
<script setup>
import {UserFilled, List, Setting, Position} from '@element-plus/icons-vue'
import Login from "./Login.vue"
import nav from "../api/nav";
import {reactive} from "vue";

import {useStore} from "vuex"
const store = useStore()

const state = reactive({
  show_login: false,
})

// 请求头部导航列表
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data
})

// 用户登录成功以后的处理
const login_success = ()=>{
  state.show_login = false
}

// 登录注销的处理
const logout = ()=>{
  store.commit("logout");
}


</script>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "客户端注销登录状态"
git push origin feature/user
```



## 在登录认证中接入防水墙验证码

```bash
验证码:
1. 图形验证码 ---> 一张图片，图片是服务端基于pillow模块生成的，里面的内容就是验证码信息，会生成验证码增加一些雪花，干扰线，采用特殊字体写入图片，内容同时会保存一份到redis中。

2. 滑块验证码 ---> 通过js互动的方式，让用户旋转、拖动图片到达一定的随机的位置。

3. 短信验证码 ---> 通过绑定手机的方式，发送随机验证码到用户手机中，确认用户是真人。
   邮件验证码
   微信验证码[消息模板, 关注公众号]
   谷歌验证码[Authenticator，二段验证]
```



使用腾讯提供的防水墙验证码

官网： https://007.qq.com/

登录腾讯云：https://cloud.tencent.com/login

![image-20210719122241679](assets/image-20210719122241679.png)

![image-20210719122255018](assets/image-20210719122255018.png)

点击立即选购，使用微信扫码登录以后，选择右上角"控制台"。

![image-20210719122442827](assets/image-20210719122442827.png)

云产品中，搜索 验证码即可。

![image-20210719122544114](assets/image-20210719122544114.png)

![image-20210719122645991](assets/image-20210719122645991.png)

![image-20211112093248262](assets/image-20211112093248262.png)

创建验证的应用。

![image-20210719122902385](assets/image-20210719122902385.png)

在验证应用的基本配置中记录下我们接下来需要使用的2个重要配置信息.

```python
应用ID   CaptchaAppId    2029921598
应用秘钥  AppSecretKey   0TpKDSegIcNJ8lunxvGGY_w**             (*号也为Key值，请不要忽略或者删除)
```

![image-20211112102218700](assets/image-20211112102218700.png)

因为后面要python对接腾讯云服务器，所以通过访问管理，API秘钥管理提取当前腾讯云账号的SecretId和SecretKey。

```bash
SecretId: AKIDxhEUU6TZT6TaQzIK8gkZ7YjeJhpgGZc0
SecretKey: YzEG4cuyyrWx85mDLIyOXR5RXP0LRHrB
```

接下来在应用中心点击右边的系统代码集成，把验证码集成到项目中就可以。

![image-20220505022120912](assets/image-20220505022120912.png)

web前端接入文件地址：https://cloud.tencent.com/document/product/1110/36841

python接入文档地址：https://cloud.tencent.com/document/sdk/Python

### 前端获取显示并校验验证码

```javascript
// 需要下载官方提供的核心js文件并在项目导入使用。
https://ssl.captcha.qq.com/TCaptcha.js
```

![image-20210719125049015](assets/image-20210719125049015.png)

components/Login.vue，代码：

```vue
<button class="login_btn" @click="show_captcha">登录</button>
```

```vue
<script setup>
import user from "../api/user";
import { ElMessage } from 'element-plus'
import "../utils/TCaptcha"
const emit = defineEmits(["successhandle",])

import {useStore} from "vuex"
const store = useStore()

// 显示验证码
const show_captcha = ()=>{
  var captcha1 = new TencentCaptcha('2029921598', (res)=>{
      // 接收验证结果的回调函数
      /* res（验证成功） = {ret: 0, ticket: "String", randstr: "String"}
         res（客户端出现异常错误 仍返回可用票据） = {ret: 0, ticket: "String", randstr: "String", errorCode: Number, errorMessage: "String"}
         res（用户主动关闭验证码）= {ret: 2}
      */
      console.log(res);
      // 调用登录处理
      loginhandler(res);
  });
  captcha1.show(); // 显示验证码
}

// 登录处理
const loginhandler = (res)=>{
  // 验证数据
  if(user.account.length<1 || user.password.length<1){
    // 错误提示
    console.log("错了哦，用户名或密码不能为空！");
    ElMessage.error("错了哦，用户名或密码不能为空！");
    return ;
  }

  // 登录请求处理
  user.login({
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 先删除之前存留的状态
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    // 根据用户选择是否记住登录密码，保存token到不同的本地存储中
    if(user.remember){
      // 记录登录状态
      localStorage.token = response.data.token
    }else{
      // 不记录登录状态
      sessionStorage.token = response.data.token
    }
    ElMessage.success("登录成功！");
    // 登录后续处理，通知父组件，当前用户已经登录成功
    user.account = ""
    user.password = ""
    user.mobile = ""
    user.code = ""
    user.remember = false

    // vuex存储用户登录信息，保存token，并根据用户的选择，是否记住密码
    let payload = response.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    console.log("payload_data=", payload_data)
    store.commit("login", payload_data)

    emit("successhandle")
  }).catch(error=>{
    ElMessage.error("登录失败！");
  })
}

</script>
```

src/api/user.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const user = reactive({
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    account: "",  // 登录账号/手机号/邮箱
    password: "", // 登录密码
    remember: false, // 是否记住登录状态
    mobile: "",      // 登录手机号码
    code: "",        // 短信验证码
    login(res){
        // 用户登录
        return http.post("/users/login/", {
            "ticket": res.ticket,
            "randstr": res.randstr,
            "username": this.account,
            "password": this.password,
        })
    }
})

export default user;
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "客户端集成腾讯云验证码"
git push origin feature/user

```



### 服务端登录功能中校验验证码结果

python接入文档地址：https://cloud.tencent.com/document/sdk/Python

安装腾讯云PythonSKD扩展模块到项目中

```bash
pip install --upgrade tencentcloud-sdk-python
```

生成代码的API操作界面：https://console.cloud.tencent.com/api/explorer?Product=captcha&Version=2019-07-22&Action=DescribeCaptchaResult&SignVersion=

utils/tencentcloudapi.py，封装一个操作腾讯云SDK的API工具类，代码：

```python
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.captcha.v20190722 import captcha_client, models
from django.conf import settings


class TencentCloudAPI(object):
    """腾讯云API操作工具类"""

    def __init__(self):
        self.cred = credential.Credential(settings.TENCENTCLOUD["SecretId"], settings.TENCENTCLOUD["SecretKey"])

    def captcha(self, ticket, randstr, user_ip):
        """
        验证码校验工具方法
        :ticket  客户端验证码操作成功以后得到的临时验证票据
        :randstr 客户端验证码操作成功以后得到的随机字符串
        :user_ip 客户端的IP地址
        """
        try:
            Captcha = settings.TENCENTCLOUD["Captcha"]

            # 实例化http请求工具类
            httpProfile = HttpProfile()
            # 设置API所在服务器域名
            httpProfile.endpoint = Captcha["endpoint"]
            # 实例化客户端工具类
            clientProfile = ClientProfile()
            # 给客户端绑定请求的服务端域名
            clientProfile.httpProfile = httpProfile
            # 实例化验证码服务端请求工具的客户端对象
            client = captcha_client.CaptchaClient(self.cred, "", clientProfile)
            # 客户端请求对象参数的初始化
            req = models.DescribeCaptchaResultRequest()

            params = {
                # 验证码类型固定为9
                "CaptchaType": Captcha["CaptchaType"],
                # 客户端提交的临时票据
                "Ticket": ticket,
                # 客户端ip地址
                "UserIp": user_ip,
                # 随机字符串
                "Randstr": randstr,
                # 验证码应用ID
                "CaptchaAppId": Captcha["CaptchaAppId"],
                # 验证码应用key
                "AppSecretKey": Captcha["AppSecretKey"],
            }
            # 发送请求
            req.from_json_string(json.dumps(params))
            # 获取腾讯云的响应结果
            resp = client.DescribeCaptchaResult(req)
            # 把响应结果转换成json格式数据
            result = json.loads( resp.to_json_string() )
            return result and result.get("CaptchaCode") == 1

        except Exception as err:
            raise TencentCloudSDKException
```





settings/dev.py，保存腾讯云验证码的配置信息，保存代码：

```python
# 腾讯云API接口配置
TENCENTCLOUD = {
    # 腾讯云访问秘钥ID
    "SecretId": "AKIDxhEUU6TZT6TaQzIK8gkZ7YjeJhpgGZc0",
    # 腾讯云访问秘钥key
    "SecretKey": "YzEG4cuyyrWx85mDLIyOXR5RXP0LRHrB",
    # 验证码API配置
    "Captcha": {
        "endpoint": "captcha.tencentcloudapi.com", # 验证码校验服务端域名
        "CaptchaType": 9,  # 验证码类型，固定为9
        "CaptchaAppId": 2029921598,  # 验证码应用ID
        "AppSecretKey": "0TpKDSegIcNJ8lunxvGGY_w**", # 验证码应用key
    },
}
```

users/views.py，重写登陆视图，先校验验证码，接着再调用jwt原来提供的视图来校验用户账号信息，代码：

```python
from rest_framework_jwt.views import ObtainJSONWebToken
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI,TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class LoginAPIView(ObtainJSONWebToken):
    """用户登录视图"""
    def post(self, request, *args, **kwargs):
        # 校验用户操作验证码成功以后的ticket临时票据
        try:
            api = TencentCloudAPI()
            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
                request._request.META.get("REMOTE_ADDR"),
            )
            if result:
                # 验证通过
                print("验证通过")
                # 登录实现代码，调用父类实现的登录视图方法
                return super().post(request, *args, **kwargs)
            else:
                # 如果返回值不是True，则表示验证失败
                raise TencentCloudSDKException
        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)
```

users/urls.py，代码：

```python
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
]
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "服务端重写登录视图实现验证码的操作结果验证"
git push origin feature/user

```



# 用户的注册认证

前端显示注册页面并调整首页头部和登陆页面的注册按钮的链接。

创建一个注册页面views/Register.vue，主要是通过登录窗口组件进行改成而成，组件代码：

```vue
<template>
	<div class="login box">
		<img src="../assets/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../assets/logo.svg" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <div class="title">
            <span class="active">用户注册</span>
          </div>
          <div class="inp">
            <input v-model="state.mobile" type="text" placeholder="手机号码" class="user">
            <input v-model="state.password" type="password" placeholder="登录密码" class="user">
            <input v-model="state.re_password" type="password" placeholder="确认密码" class="user">
            <input v-model="state.code"  type="text" class="code" placeholder="短信验证码">
            <el-button id="get_code" type="primary">获取验证码</el-button>
            <button class="login_btn">注册</button>
            <p class="go_login" >已有账号 <router-link to="/login">立即登录</router-link></p>
          </div>
      </div>
		</div>
	</div>
</template>

<script setup>
import {reactive, defineEmits} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import "../utils/TCaptcha"

const store = useStore()

const state = reactive({
  password:"",    // 密码
  re_password: "",// 确认密码
  mobile: "",     // 手机号
  code: "",       // 验证码
})
</script>

<style scoped>
.box{
	width: 100%;
  height: 100%;
	position: relative;
  overflow: hidden;
}
.box img{
	width: 100%;
  min-height: 100%;
}
.box .login {
	position: absolute;
	width: 500px;
	height: 400px;
	left: 0;
  margin: auto;
  right: 0;
  bottom: 0;
  top: -438px;
}

.login-title{
     width: 100%;
    text-align: center;
}
.login-title img{
    width: 190px;
    height: auto;
}
.login-title p{
    font-size: 18px;
    color: #fff;
    letter-spacing: .29px;
    padding-top: 10px;
    padding-bottom: 50px;
}
.login_box{
    width: 400px;
    height: auto;
    background: #fff;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
    border-radius: 4px;
    margin: 0 auto;
    padding-bottom: 40px;
    padding-top: 50px;
}
.title{
	font-size: 20px;
	color: #9b9b9b;
	letter-spacing: .32px;
	border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 0px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.title span.active{
	color: #4a4a4a;
}

.inp{
	width: 350px;
	margin: 0 auto;
}
.inp .code{
  width: 190px;
  margin-right: 16px;
}
#get_code{
 margin-top: 6px;
}
.inp input{
    outline: 0;
    width: 100%;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
}
.inp input.user{
    margin-bottom: 16px;
}
.inp .rember{
     display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    margin-top: 10px;
}
.inp .rember p:first-of-type{
    font-size: 12px;
    color: #4a4a4a;
    letter-spacing: .19px;
    margin-left: 22px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    /*position: relative;*/
}
.inp .rember p:nth-of-type(2){
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .19px;
    cursor: pointer;
}

.inp .rember input{
    outline: 0;
    width: 30px;
    height: 45px;
    border-radius: 4px;
    border: 1px solid #d9d9d9;
    text-indent: 20px;
    font-size: 14px;
    background: #fff !important;
    vertical-align: middle;
    margin-right: 4px;
}

.inp .rember p span{
    display: inline-block;
  font-size: 12px;
  width: 100px;
}
.login_btn{
    cursor: pointer;
    width: 100%;
    height: 45px;
    background: #84cc39;
    border-radius: 5px;
    font-size: 16px;
    color: #fff;
    letter-spacing: .26px;
    margin-top: 30px;
    border: none;
    outline: none;
}
.inp .go_login{
    text-align: center;
    font-size: 14px;
    color: #9b9b9b;
    letter-spacing: .26px;
    padding-top: 20px;
}
.inp .go_login span{
    color: #84cc39;
    cursor: pointer;
}
</style>
```

客户端注册路由，src/router/index.js，代码：

```javascript
import {createRouter, createWebHistory, createWebHashHistory} from 'vue-router'
import store from "../store";

// 路由列表
const routes = [
  {
    meta:{
        title: "luffy2.0-站点首页",
        keepAlive: true
    },
    path: '/',         // uri访问地址
    name: "Home",
    component: ()=> import("../views/Home.vue")
  },
  {
    meta:{
        title: "luffy2.0-用户登录",
        keepAlive: true
    },
    path:'/login',      // uri访问地址
    name: "Login",
    component: ()=> import("../views/Login.vue")
  },
  {
      meta:{
        title: "luffy2.0-用户注册",
        keepAlive: true
      },
      path: '/register',
      name: "Register",            // 路由名称
      component: ()=> import("../views/Register.vue"),         // uri绑定的组件页面
  },
  {
    meta:{
        title: "luffy2.0-个人中心",
        keepAlive: true,
        authorization: true,
    },
    path: '/user',
    name: "User",
    component: ()=> import("../views/User.vue"),
  },
]


// 路由对象实例化
const router = createRouter({
  // history, 指定路由的模式
  history: createWebHistory(),
  // 路由列表
  routes,
});

// 导航守卫
router.beforeEach((to, from, next)=>{
  document.title=to.meta.title
  // 登录状态验证
  if (to.meta.authorization && !store.getters.getUserInfo) {
    next({"name": "Login"})
  }else{
    next()
  }
})


// 暴露路由对象
export default router
```

修改首页头部的连接和登录窗口中登录和注册的链接。代码：

```html
# components/Header.vue
<router-link to="/register">注册</router-link>
#components/Login.vue
<p class="go_login" >没有账号 <router-link to="/register">立即注册</router-link></p>
```



## 注册功能的实现流程

![image-20210720102658402](assets/image-20210720102658402-1651693161553.png)

综合上图所示，我们需要在服务端完成3个接口：

```python
1. 验证手机号是否注册了
2. 发送验证码
3. 校验验证码，并保存用户提交的注册信息
```

所以，除了短信发送功能以外，其他2个接口功能，我们完全不需要依赖第三方，直接可以先实现了。

## 用户手机号码的校验

用户填写手机号的时候，我们可以监听手机号格式正确的情况下，通过ajax提前告诉用户手机号是否已经被注册了。

### 客户端监听手机号格式是否正确

views/Register.vue

```vue
<script setup>
import {reactive, defineEmits,watch} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import "../utils/TCaptcha"

const store = useStore()

const state = reactive({
  password:"",    // 密码
  re_password: "",// 确认密码
  mobile: "",     // 手机号
  code: "",       // 验证码
})

watch(() => state.mobile, (mobile, prevMobile) => {
  if(/1[3-9]\d{9}/.test(state.mobile)){
    // 发送ajax验证手机号是否已经注册
  }
})

</script>
```

#### 服务端提供验证手机号的api接口

users/views，视图代码：

```python
from rest_framework.views import APIView
from .models import User


class MobileAPIView(APIView):
    def get(self, request, mobile):
        """
        校验手机号是否已注册
        :param request:
        :param mobile: 手机号
        :return:
        """
        try:
            User.objects.get(mobile=mobile)
            return Response({"errmsg": "当前手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # 如果查不到该手机号的注册记录，则证明手机号可以注册使用
            return Response({"errmsg": "OK"}, status=status.HTTP_200_OK)
```

路由，代码：

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    re_path(r"^mobile/(?P<mobile>1[3-9]\d{9})/$", views.MobileAPIView.as_view()),
]
```



### 客户端发送ajax请求验证手机号是否已注册

src/api/user.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const user = reactive({
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    account: "",  // 登录账号/手机号/邮箱
    password: "", // 登录密码
    remember: false, // 是否记住登录状态
    re_password: "",// 确认密码
    login(res){
        // 用户登录
        return http.post("/users/login/", {
            "ticket": res.ticket,
            "randstr": res.randstr,
            "username": this.account,
            "password": this.password,
        })
    },
    check_mobile(){
        // 验证手机号
        return http.get(`/users/mobile/${this.mobile}/`)
    }
})

export default user;
```



views/Register.vue，代码：

```vue
<template>
	<div class="login box">
		<img src="../assets/Loginbg.3377d0c.jpg" alt="">
		<div class="login">
			<div class="login-title">
				<img src="../assets/logo.svg" alt="">
				<p>帮助有志向的年轻人通过努力学习获得体面的工作和生活!</p>
			</div>
      <div class="login_box">
          <div class="title">
            <span class="active">用户注册</span>
          </div>
          <div class="inp">
            <input v-model="user.mobile" type="text" placeholder="手机号码" class="user">
            <input v-model="user.password" type="password" placeholder="登录密码" class="user">
            <input v-model="user.re_password" type="password" placeholder="确认密码" class="user">
            <input v-model="user.code"  type="text" class="code" placeholder="短信验证码">
            <el-button id="get_code" type="primary">获取验证码</el-button>
            <button class="login_btn">注册</button>
            <p class="go_login" >已有账号 <router-link to="/login">立即登录</router-link></p>
          </div>
      </div>
		</div>
	</div>
</template>
```

```vue
<script setup>
import {reactive, defineEmits, watch} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import "../utils/TCaptcha"
import user from "../api/user";

const store = useStore()

// 监听数据mobile是否发生变化
watch(()=>user.mobile, (mobile, prevMobile) => {
  if(/1[3-9]\d{9}/.test(user.mobile)){
    // 发送ajax验证手机号是否已经注册
    user.check_mobile().catch(error=>{
      ElMessage.error(error.response.data.errmsg);
    })
  }
})

</script>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "注册功能实现流程-验证手机号是否已经注册!"
git push origin feature/user
```





## 注册功能的基本实现

### 服务端实现用户注册的api接口

序列化器，`users/serializers`，代码：

```python
import re, constants
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import User


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["mobile", "password", "re_password", "sms_code", "token"]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16,
            },
        }

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("mobile", None)
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError(detail="手机号格式不正确！",code="mobile")

        # 密码和确认密码
        password = data.get("password")
        re_password = data.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

        # 手机号是否已注册
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError(detail="手机号已注册！")
        except User.DoesNotExist:
            pass

        # todo 验证短信验证码

        return data

    def create(self, validated_data):
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        # 注册成功以后，免登陆
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
```

默认头像配置，`settings.constants`，utils/constants.py代码：

```python
# 默认头像
DEFAULT_USER_AVATAR = "avatar/2021/avatar.jpg"
# 手动在uploads下创建avatar/2021/并把客户端的头像保存到该目录下。
```

视图，`users.views`，代码，

```python
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterModelSerializer


class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer

```

路由，`users/urls`，代码：

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    re_path("^mobile/(?P<mobile>1[3-9]\d{9})/$", views.MobileAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
]
```



### 客户端提交用户注册信息

`views/views/Register.vue`，代码：

```vue
<button class="login_btn" @click="show_captcha">注册</button>
```

```vue
<script setup>
import {reactive, defineEmits, watch} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import "../utils/TCaptcha"
import user from "../api/user";
import settings from "../settings";
import router from "../router";  // 实测最后一步跳转首页提示router未定义 加上这句
const store = useStore()

// 监听数据mobile是否发生变化
watch(()=>user.mobile, (mobile, prevMobile) => {
  if(/1[3-9]\d{9}/.test(user.mobile)){
    // 发送ajax验证手机号是否已经注册
    user.check_mobile().catch(error=>{
      ElMessage.error(error.response.data.errmsg);
    })
  }
})


// 显示登录验证码
const show_captcha = ()=>{
  // 直接生成一个验证码对象
  let  captcha1 = new TencentCaptcha(settings.captcha_app_id, (res)=>{
    // 验证码通过验证以后的回调方法
    if(res && res.ret === 0){
      // 验证通过，发送登录请求
      registerhandler(res)
    }
  });

  // 显示验证码
  captcha1.show();
}


const registerhandler = (res)=> {
  // 注册处理
  if (!/^1[3-9]\d{9}$/.test(user.mobile)) {
    // 错误提示
    ElMessage.error('错了哦，手机号格式不正确！');
    return false // 阻止代码继续往下执行
  }
  if (user.password.length < 6 || user.password.length > 16) {
    ElMessage.error('错了哦，密码必须在6~16个字符之间！');
    return false
  }

  if (user.password !== user.re_password) {
    ElMessage.error('错了哦，密码和确认密码不一致！');
    return false
  }

    // 发送请求
  user.register({
    // 验证码通过的票据信息
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");

    // 默认不需要记住登录
    sessionStorage.token = response.data.token;

    // vuex存储用户登录信息
    let payload = response.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    store.commit("login", payload_data)
    // 清空表单信息
    user.mobile = ""
    user.password = ""
    user.code = ""
    user.remember = false
    //  成功提示
    ElMessage.success("注册成功！");
    // 路由跳转到首页
    router.push("/");


  })
}


</script>
```

src/api/user.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const user = reactive({
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    account: "",  // 登录账号/手机号/邮箱
    password: "", // 登录密码
    remember: false, // 是否记住登录状态
    re_password: "",// 确认密码
    code: "", // 短信验证码
    login(res){
        // 用户登录
        return http.post("/users/login/", {
            "ticket": res.ticket,
            "randstr": res.randstr,
            "username": this.account,
            "password": this.password,
        })
    },
    check_mobile(){
        // 验证手机号
        return http.get(`/users/mobile/${this.mobile}/`)
    },
    register(data){
        data.mobile = this.mobile
        data.re_password = this.re_password
        data.password = this.password
        data.sms_code = this.code
        // 用户注册请求
        return http.post("/users/register/", data)
    }
})

export default user;
```

把防水墙验证码的`app_id`保存到配置文件src/settings.js中.

src/settings.js，代码：

```javascript
export default {
    // api服务端所在地址
    host: "http://api.luffycity.cn:8000", // ajax服务度地址
    // 防水墙验证码的应用ID
    captcha_app_id: "2029921598",  // IP应用ID
}
```

components/Login.vue，登录组件中，把app_id改成settings提供的变量，代码：

```vue
<script setup>
import user from "../api/user";
import { ElMessage } from 'element-plus'
import "../utils/TCaptcha"
const emit = defineEmits(["successhandle",])
import settings from "../settings";
import {useStore} from "vuex"
const store = useStore()

// 显示验证码
const show_captcha = ()=>{
  var captcha1 = new TencentCaptcha(settings.captcha_app_id, (res)=>{
      // 接收验证结果的回调函数
      /* res（验证成功） = {ret: 0, ticket: "String", randstr: "String"}
         res（客户端出现异常错误 仍返回可用票据） = {ret: 0, ticket: "String", randstr: "String", errorCode: Number, errorMessage: "String"}
         res（用户主动关闭验证码）= {ret: 2}
      */
      console.log(res);
      // 调用登录处理
      loginhandler(res);
  });
  captcha1.show(); // 显示验证码
}

// 登录处理
const loginhandler = (res)=>{
  // 验证数据
  if(user.account.length<1 || user.password.length<1){
    // 错误提示
    console.log("错了哦，用户名或密码不能为空！");
    ElMessage.error("错了哦，用户名或密码不能为空！");
    return ;
  }

  // 登录请求处理
  user.login({
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 先删除之前存留的状态
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");
    // 根据用户选择是否记住登录密码，保存token到不同的本地存储中
    if(user.remember){
      // 记录登录状态
      localStorage.token = response.data.token
    }else{
      // 不记录登录状态
      sessionStorage.token = response.data.token
    }
    ElMessage.success("登录成功！");
    // 登录后续处理，通知父组件，当前用户已经登录成功
    user.account = ""
    user.password = ""
    user.mobile = ""
    user.code = ""
    user.remember = false

    // vuex存储用户登录信息，保存token，并根据用户的选择，是否记住密码
    let payload = response.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    console.log("payload_data=", payload_data)
    store.commit("login", payload_data)

    emit("successhandle")
  }).catch(error=>{
    ElMessage.error("登录失败！");
  })
}

</script>
```

服务端的注册功能中，添加验证腾讯云的验证码ticket和randstr。users/serializers.py

```python
import re, constants
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException

class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True, help_text="确认密码")
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(read_only=True)
    ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        fields = ["mobile", "password", "re_password", "sms_code", "token", "ticket", "randstr"]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16,
            },
        }

        def validate(self, data):
            """验证客户端数据"""
            # 手机号格式验证
            mobile = data.get("mobile", None)
            if not re.match("^1[3-9]\d{9}$", mobile):
                raise serializers.ValidationError(detail="手机号格式不正确！", code="mobile")

            # 密码和确认密码
            password = data.get("password")
            re_password = data.get("re_password")
            if password != re_password:
                raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

            # 手机号是否已注册
            try:
                User.objects.get(mobile=mobile)
                raise serializers.ValidationError(detail="手机号已注册！")
            except User.DoesNotExist:
                pass

            # todo 验证防水墙验证码
            api = TencentCloudAPI()
            result = api.captcha(
                data.get("ticket"),
                data.get("randstr"),
                self.context['request']._request.META.get("REMOTE_ADDR"), # 客户端IP
            )

            if not result:
                raise serializers.ValidationError(detail="滑块验证码校验失败！")

            # todo 验证短信验证码

            return data

    def create(self, validated_data):
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        # 注册成功以后，免登陆
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)

        user.token = jwt_encode_handler(payload)

        return user
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "注册功能实现流程-保存用户注册信息!"
git push origin feature/user

```



## 注册功能添加短信验证码

接下来，我们把注册过程中一些注册信息（例如：短信验证码）缓存到redis数据库中。

在django集成redis缓存功能的文档：https://django-redis-chs.readthedocs.io/zh_CN/latest/#

确认settings.dev.py配置中添加了存储短信验证码的配置项，代码：

```python
# redis configration
# 设置redis缓存
CACHES = {
    # 默认缓存
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # 项目上线时,需要调整这里的路径
        # "LOCATION": "redis://:密码@IP地址:端口/库编号",
        "LOCATION": "redis://:@127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},  # 连接池
        }
    },
    # 提供给admin运营站点的session存储
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
        }
    },
    # 提供存储短信验证码
    "sms_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 10},
        }
    }
}

# 设置用户登录admin站点时,记录登录状态的session保存到redis缓存中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 设置session保存的位置对应的缓存配置项
SESSION_CACHE_ALIAS = "session"

```



### 使用云通讯发送短信

官网：https://www.yuntongxun.com/

在登录后的平台控制台下获取以下信息：

```
ACCOUNT SID：8a216da881ad97540181d8e645e20809
AUTH TOKEN : e9aacc7819774ca39916f472c6083684
AppID(默认)：8a216da881ad97540181d8e646e70810
Rest URL(生产)： https://app.cloopen.com:8883

```

![image-20220505153622072](assets/image-20220505153622072.png)

在开发过程中,为了节约发送短信的成本,可以把自己的或者同事的手机加入到测试号码中.

![1553678528811](assets/1553678528811-1651693161553.png)

查看发送短信的api接口文档。

![image-20210720122011602](assets/image-20210720122011602-1651693161554.png)



#### 后端生成短信验证码

安装云通讯的短信SDK扩展模块，终端执行命令：

```bash
pip install ronglian_sms_sdk
```

封装容联云的短信发送功能，`luffycityapi/utils/ronglianyunapi`，代码：

```python
import json
from ronglian_sms_sdk import SmsSDK
from django.conf import settings
def send_sms(tid, mobile, datas):
    """
    发送短信
    @params tid: 模板ID，默认测试使用1
    @params mobile: 接收短信的手机号，多个手机号使用都逗号隔开
            单个号码： mobile="13312345678"
            多个号码： mobile="13312345678,13312345679,...."
    @params datas: 短信模板的参数列表
            例如短信模板为： 【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。
            则datas=("123456",5,)
    """
    ronglianyun = settings.RONGLIANYUN
    sdk = SmsSDK(ronglianyun.get("accId"), ronglianyun.get("accToken"), ronglianyun.get("appId"))
    resp = sdk.sendMessage(tid, mobile, datas)
    response = json.loads(resp)
    print(response, type(response))
    return response.get("statusCode") == "000000"
```

把容联云的配置信息，填写到配置文件中，`settings.dev`，代码：

```python
# 容联云短信
RONGLIANYUN = {
    "accId": '8a216da881ad97540181d8e645e20809',
    "accToken": 'e9aacc7819774ca39916f472c6083684',
    "appId": '8a216da881ad97540181d8e646e70810',
    "reg_tid": 1,      # 注册短信验证码的模板ID
    "sms_expire": 300, # 短信有效期，单位：秒(s)
    "sms_interval": 60,# 短信发送的冷却时间，单位：秒(s)
}
```



视图，`users/views.py`，代码：

```python
from rest_framework_jwt.views import ObtainJSONWebToken
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status


class LoginAPIView(ObtainJSONWebToken):
    """用户登录视图"""
    def post(self, request, *args, **kwargs):
        # 校验用户操作验证码成功以后的ticket临时票据
        try:
            api = TencentCloudAPI()
            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
                request._request.META.get("REMOTE_ADDR"), # 客户端IP
            )

            if result:
                # 验证通过
                print("验证通过")
                # 登录实现代码，调用父类实现的登录视图方法
                return super().post(request, *args, **kwargs)

            else:
                # 如果返回值不是True，则表示验证失败
                raise TencentCloudSDKException

        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from .models import User


class MobileAPIView(APIView):
    def get(self, request, mobile):
        """
        校验手机号是否已注册
        :param request:
        :param mobile: 手机号
        :return:
        """
        try:
            User.objects.get(mobile=mobile)
            return Response({"errmsg": "当前手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # 如果查不到该手机号的注册记录，则证明手机号可以注册使用
            return Response({"errmsg": "OK"}, status=status.HTTP_200_OK)


from .serializers import UserRegisterModelSerializer
from rest_framework.generics import CreateAPIView


class UserAPIView(CreateAPIView):
    """用户视图"""
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer



import random
from django_redis import get_redis_connection
from django.conf import settings
from ronglianyunapi import send_sms
"""
/users/sms/(?P<mobile>1[3-9]\d{9})
"""
class SMSAPIView(APIView):
    """
    SMS短信接口视图
    """
    def get(self, request, mobile):
        """发送短信验证码"""
        redis = get_redis_connection("sms_code")
        # 判断手机短信是否处于发送冷却中[60秒只能发送一条]
        interval = redis.ttl(f"interval_{mobile}")  # 通过ttl方法可以获取保存在redis中的变量的剩余有效期
        if interval != -2:
            return Response(
                {"errmsg": f"短信发送过于频繁，请{interval}秒后再次点击获取!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 基于随机数生成短信验证码
        # code = "%06d" % random.randint(0, 999999)
        code = f"{random.randint(0, 999999):06d}"
        # 获取短信有效期的时间
        time = settings.RONGLIANYUN.get("sms_expire")
        # 短信发送间隔时间
        sms_interval = settings.RONGLIANYUN["sms_interval"]
        # 调用第三方sdk发送短信
        send_sms(settings.RONGLIANYUN.get("reg_tid"), mobile, datas=(code, time // 60))

        # 记录code到redis中，并以time作为有效期
        # 使用redis提供的管道对象pipeline来优化redis的写入操作[添加/修改/删除]
        pipe = redis.pipeline()
        pipe.multi()  # 开启事务
        pipe.setex(f"sms_{mobile}", time, code)
        pipe.setex(f"interval_{mobile}", sms_interval, "_")
        pipe.execute()  # 提交事务，同时把暂存在pipeline的数据一次性提交给redis

        return Response({"errmsg": "OK"}, status=status.HTTP_200_OK)
```

路由，`users/urls.py`，代码：

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    re_path(r"^mobile/(?P<mobile>1[3-9]\d{9})/$", views.MobileAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
    re_path(r"^sms/(?P<mobile>1[3-9]\d{9})/$", views.SMSAPIView.as_view()),
]
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "注册功能实现流程-服务端提供短信发送API接口!"
git push origin feature/user

```



### 客户端请求发送短信

views/Register.vue，注册页面绑定点击发送短信的方法，代码：

```vue
<el-button id="get_code" type="primary" @click="send_sms">{{user.sms_btn_text}}</el-button>
```

```vue
<script setup>
import {reactive, defineEmits, watch} from "vue"
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"
import {useRouter} from "vue-router"
import "../utils/TCaptcha"
import user from "../api/user";
import settings from "../settings";
const store = useStore()
const router = useRouter()

// 监听数据mobile是否发生变化
watch(()=>user.mobile, (mobile, prevMobile) => {
  if(/1[3-9]\d{9}/.test(user.mobile)){
    // 发送ajax验证手机号是否已经注册
    user.check_mobile().catch(error=>{
      ElMessage.error(error.response.data.errmsg);
    })
  }
})


// 显示登录验证码
const show_captcha = ()=>{
  // 直接生成一个验证码对象
  let  captcha1 = new TencentCaptcha(settings.captcha_app_id, (res)=>{
    // 验证码通过验证以后的回调方法
    if(res && res.ret === 0){
      // 验证通过，发送登录请求
      registerhandler(res)
    }
  });

  // 显示验证码
  captcha1.show();
}


const registerhandler = (res)=> {
  // 注册处理
  if (!/^1[3-9]\d{9}$/.test(user.mobile)) {
    // 错误提示
    ElMessage.error('错了哦，手机号格式不正确！');
    return false // 阻止代码继续往下执行
  }
  if (user.password.length < 6 || user.password.length > 16) {
    ElMessage.error('错了哦，密码必须在6~16个字符之间！');
    return false
  }

  if (user.password !== user.re_password) {
    ElMessage.error('错了哦，密码和确认密码不一致！');
    return false
  }

    // 发送请求
  user.register({
    // 验证码通过的票据信息
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(response=>{
    // 保存token，并根据用户的选择，是否记住密码
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");

    // 默认不需要记住登录
    sessionStorage.token = response.data.token;

    // vuex存储用户登录信息
    let payload = response.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    store.commit("login", payload_data)
    // 清空表单信息
    user.mobile = ""
    user.password = ""
    user.code = ""
    user.remember = false
    //  成功提示
    ElMessage.success("注册成功！");
    // 路由跳转到首页
    router.push("/");


  })
}


// 发送短信
const send_sms = ()=> {
  if (!/1[3-9]\d{9}/.test(user.mobile)) {
    ElMessage.error("手机号格式有误！")
    return false
  }

  // 判断是否处于短信发送的冷却状态
  if (user.is_send) {
    ElMessage.error("短信发送过于频繁！")
    return false
  }

  let time = user.sms_interval;
  // 发送短信请求
  user.get_sms_code().then(response=>{
    ElMessage.success("短信发送中，请留意您的手机！");
    // 发送短信后进入冷却状态
    user.is_send = true;
    // 冷却倒计时
    clearInterval(user.interval);
    user.interval = setInterval(()=> {
      if (time < 1) {
        // 退出短信发送的冷却状态
        user.is_send = false
        user.sms_btn_text = "点击获取验证码"
      } else {
        time -= 1;
        user.sms_btn_text = `${time}秒后重新获取`;
      }
    }, 1000)
  }).catch(error=>{
    ElMessage.error(error?.response?.data?.errmsg);
    time = error?.response?.data?.interval;
    // 冷却倒计时
    clearInterval(user.interval);
    user.interval = setInterval(()=>{
      if(time<1){
        // 退出短信发送的冷却状态
        user.is_send = false
        user.sms_btn_text = "点击获取验证码"
      }else{
        time-=1;
        user.sms_btn_text = `${time}秒后重新获取`;
      }
    }, 1000)

  })
}


</script>
```

src/api/user.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const user = reactive({
    login_type: 0, // 登录方式，0，密码登录，1，短信登录
    account: "",  // 登录账号/手机号/邮箱
    password: "", // 登录密码
    remember: false, // 是否记住登录状态
    re_password: "",// 确认密码
    code: "", // 短信验证码
    sms_btn_text: "点击获取验证码", // 短信按钮提示
    is_send: false,  // 短信发送的标记
    sms_interval: 60,// 间隔时间
    interval: null,  // 定时器的标记
    login(res){
        // 用户登录
        return http.post("/users/login/", {
            "ticket": res.ticket,
            "randstr": res.randstr,
            "username": this.account,
            "password": this.password,
        })
    },
    check_mobile(){
        // 验证手机号
        return http.get(`/users/mobile/${this.mobile}/`)
    },
    register(data){
        data.mobile = this.mobile
        data.re_password = this.re_password
        data.password = this.password
        data.sms_code = this.code
        // 用户注册请求
        return http.post("/users/register/", data)
    },
    get_sms_code(){
        return http.get(`/users/sms/${this.mobile}/`)
    }
})

export default user;
```

提交版本

```bash
cd ~/Desktop/luffycity/
git add .
git commit -m "注册功能实现流程-客户端请求发送短信并实现短信倒计时冷却提示!"
git push origin feature/user

```



### 服务端校验客户端提交的验证码

`users/serializers.py`，代码：

```python
import re, constants
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import User
from luffycityapi.utils.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException
from django_redis import get_redis_connection


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True, help_text="确认密码")
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(read_only=True)
    ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        fields = ["mobile", "password", "re_password", "sms_code", "token", "ticket", "randstr"]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16,
            },
        }

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("mobile", None)
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError(detail="手机号格式不正确！", code="mobile")

        # 密码和确认密码
        password = data.get("password")
        re_password = data.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

        # 手机号是否已注册
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError(detail="手机号已注册！")
        except User.DoesNotExist:
            pass

        # 验证防水墙验证码
        api = TencentCloudAPI()
        result = api.captcha(
            data.get("ticket"),
            data.get("randstr"),
            self.context['request']._request.META.get("REMOTE_ADDR"), # 客户端IP
        )

        if not result:
            raise serializers.ValidationError(detail="滑块验证码校验失败！")

        # 验证短信验证码
        # 从redis中提取短信
        redis = get_redis_connection("sms_code")
        code = redis.get(f"sms_{mobile}")
        if code is None:
            """获取不到验证码，则表示验证码已经过期了"""
            raise serializers.ValidationError(detail="验证码失效或已过期！", code="sms_code")

        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误！", code="sms_code")
        print(f"code={code.decode()}, sms_code={data.get('sms_code')}")
        # 删除掉redis中的短信，后续不管用户是否注册成功，至少当前这条短信验证码已经没有用处了
        redis.delete(f"sms_{mobile}")

        return data

    def create(self, validated_data):
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        # 注册成功以后，免登陆
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)

        user.token = jwt_encode_handler(payload)

        return user
```

对于生成jwt token的这段代码，我们也可以封装成一个工具函数，方便后面其他地方如果还有使用，可以复用代码、

users/serializers.py，代码：

```python
import re, constants
from rest_framework import serializers
from django_redis import get_redis_connection

from tencentcloudapi import TencentCloudAPI
from .models import User
from authenticate import generate_jwt_token


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True)
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True)
    token = serializers.CharField(read_only=True)
    ticket = serializers.CharField(write_only=True)
    randstr = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["mobile", "password", "re_password", "sms_code", "token", "ticket", "randstr"]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16,
            },
        }

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("mobile", None)
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError(detail="手机号格式不正确！",code="mobile")

        # 密码和确认密码
        password = data.get("password")
        re_password = data.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

        # 手机号是否已注册
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError(detail="手机号已注册！", code="mobile")
        except User.DoesNotExist:
            pass

        # 验证腾讯云的滑动验证码
        api = TencentCloudAPI()
        # 视图中的request对象，在序列化器中使用 self.context["request"]
        result = api.captcha(
            data.get("ticket"),
            data.get("randstr"),
            self.context["request"]._request.META.get("REMOTE_ADDR"),
        )

        if not result:
            raise serializers.ValidationError(detail="滑动验证码校验失败！", code="verify")

        # 验证短信验证码
        redis = get_redis_connection("sms_code")
        code = redis.get(f"sms_{mobile}")
        if code is None:
            """获取不多验证码，则表示验证码已经过期了"""
            raise serializers.ValidationError(detail="验证码失效或已过期！", code="sms_code")

        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误！", code="sms_code")

        # 删除掉redis中的短信，后续不管用户是否注册成功，至少当前这条短信验证码已经没有用处了
        redis.delete(f"sms_{mobile}")

        return data

    def create(self, validated_data):
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        # 注册成功以后，免登陆, 生成 jwt token
        user.token = generate_jwt_token(user)
        return user
```

luffycityapi/utils/authenticate.py，代码：

```python
from rest_framework_jwt.settings import api_settings

def generate_jwt_token(user):
    """
    生成jwt token
    @params user: 用户模型实例对象
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
```

提交版本

```bash
cd ~/Desktop/luffycity/
git add .
git commit -m "注册功能实现流程-服务端校验短信验证码!"
git push origin feature/user
```



