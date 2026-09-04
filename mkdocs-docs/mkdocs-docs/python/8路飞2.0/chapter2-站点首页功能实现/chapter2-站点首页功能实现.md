# 1. 导航功能实现

导航数据的存储，必须要找出导航数据的结构，也就是有哪些属性？

导航位置、导航名称、导航链接、导航序号、是否显示、是否外链、添加时间、更新时间、是否删除

E-R图，如下：

![image-20220402021856478](assets/image-20220402021856478.png)

### 1.1 创建模型

![image-20220402022526081](assets/image-20220402022526081.png)

home/models.py，代码：

```python
from luffycityapi.utils.models import models, BaseModel


# Create your models here.


class Nav(BaseModel):
    """导航菜单"""
    # 字段选项
    # 模型对象.<字段名>  ---> 实际数据
    # 模型对象.get_<字段名>_display()  --> 文本提示
    POSITION_CHOICES = (
        # (实际数据, "文本提示"),
        (0, "顶部导航"),
        (1, "脚部导航"),
    )
    link = models.CharField(max_length=255, verbose_name="导航连接")
    is_http = models.BooleanField(default=False, verbose_name="是否站外连接地址")
    position = models.IntegerField(choices=POSITION_CHOICES, default=0, verbose_name="导航位置")

    class Meta:
        db_table = "fg_nav"
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name

```

公共模型【抽象模型，不会在数据迁移的时候为它创建表】，保存项目的公共代码库目录下luffycityapi/utils.py文件中。

`luffycityapi/utils/models.py`，代码：

```python
from django.db import models


class BaseModel(models.Model):
    """
    公共模型
    保存项目中的所有模型的公共属性和公共方法的声明
    """
    name = models.CharField(max_length=255, default="", verbose_name="名称/标题")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    orders = models.IntegerField(default=0, verbose_name="序号")
    is_show = models.BooleanField(default=True, verbose_name="是否显示")
    # auto_now_add=True 当数据被创建时，以当前时间作为默认值写入当前字段
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    # auto_now=True 当数据被更新时，以当前时间作为值写入当前字段
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        # 设置当前模型类并非真正的模型，而是一种保存公共代码的抽象模型类
        # 这种模型在数据迁移中不会被当做数据模型来创建数据表
        abstract = True
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self)

```

settings/dev.py，中配置导包路径，代码：

```python
# 因为项目中子应用已经换了存储目录，所以需要把apps设置为系统导包路径，方便我们后面开发时可以简写子应用相关的导包路径。
import sys
sys.path.insert(0, str( BASE_DIR / "apps") )
sys.path.insert(0, str( BASE_DIR / "utils") )
```

home/models.py，代码调整如下：

```python
from models import BaseModel, models

# Create your models here.


class Nav(BaseModel):
    """导航菜单"""
    # 字段选项
    # 模型对象.<字段名>  ---> 实际数据
    # 模型对象.get_<字段名>_display()  --> 文本提示
    POSITION_CHOICES = (
        # (实际数据, "文本提示"),
        (0, "顶部导航"),
        (1, "脚部导航"),
    )

    link = models.CharField(max_length=255, verbose_name="导航连接")
    is_http = models.BooleanField(default=False, verbose_name="是否站外连接地址")
    position = models.SmallIntegerField(default=0, choices=POSITION_CHOICES, verbose_name="导航位置")

    class Meta:
        db_table = "fg_nav"
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name

```

实际工作中，有些大厂企业不需要我们使用django的数据迁移操作的，如果公司有DBA的话，那就直接DBA已经提前设计数据表结构了，我们只需要根据表结构声明模型代码，保证模型代码的表名和字段与数据库中的表结构对应上，就可以在django中直接调用ORM模型对象操作数据库中的数据了。当然，我们现在在学习阶段，所以并没有DBA，所以老老实实执行数据迁移命令吧。

```bash
cd ~/Desktop/luffycity/luffycityapi
python manage.py makemigrations
python manage.py migrate
```

刚上面仅仅创建的是数据表结构而已，所以接下来我们如果要实现客户端展示导航功能，则还需要在admin后台手动添加测试数据，或者MySQL交互终端下添加测试数据才可以。

```sql
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (1, '免费课', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 0);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (2, '项目课', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/project', 0, 0);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (3, '学位课', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/position', 0, 0);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (4, '习题库', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/exam', 0, 0);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (5, '路飞学城', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', 'https://www.luffycity.com', 1, 0);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (6, '企业服务', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (7, '关于我们', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (8, '联系我们', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (9, '商务合作', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (10, '帮助中心', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (11, '意见反馈', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
INSERT INTO luffycity.fg_nav (id, name, orders, is_show, is_deleted, created_time, updated_time, link, is_http, position) VALUES (12, '新手指南', 1, 1, 0, '2021-07-15 01:27:27.350000', '2021-07-15 01:27:28.690000', '/free', 0, 1);
```



### 1.2 序列化器

home.serializers， home/serializers.pyf代码：

```python
from rest_framework import serializers
from .models import Nav


class NavModelSerializer(serializers.ModelSerializer):
    """
    导航菜单的序列化器
    """
    class Meta:
        model = Nav
        fields = ["name", "link", "is_http"]

```



### 1.3 视图代码

home/views.py

```python
import constants
from rest_framework.generics import ListAPIView
from .models import Nav
from .serializers import NavModelSerializer
#NAV_HEADER_POSITION = 0
#NAV_HEADER_SIZE = 5
#NAV_FOOTER_POSITION = 1
#NAV_FOOTER_SIZE = 10

class NavHeaderListAPIView(ListAPIView):
    """顶部导航视图"""
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.NAV_HEADER_SIZE]
    serializer_class = NavModelSerializer


class NavFooterListAPIView(ListAPIView):
    """脚部导航视图"""
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavModelSerializer
```



#### 1.3.1 常量配置

utils/constants.py，代码：

```python
"""常量配置文件"""
# 导航的位置 --> 顶部
NAV_HEADER_POSITION = 0
# 导航的位置 --> 脚部
NAV_FOOTER_POSITION = 1
# 顶部导航显示的最大数量
NAV_HEADER_SIZE = 5
# 脚部导航显示的最大数量
NAV_FOOTER_SIZE = 10
```



### 1.4 路由代码

home/urls.py

```python
from django.urls import path
from . import views
urlpatterns = [
    path("nav/header/", views.NavHeaderListAPIView.as_view()),
    path("nav/footer/", views.NavFooterListAPIView.as_view()),
]
```

完成了上面操作以后，可以直接访问url地址或者postman来请求测试接口数据是否正确。

![image-20220407004245180](assets/image-20220407004245180.png)

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:服务端提供导航api接口"
git push origin develop
```



### 1.5 客户端获取导航数据

所有与api服务端进行交互的操作代码，可以单独保存api目录下，根据数据表单独创建js文件，方便将来代码复用。

src/api/nav.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const nav = reactive({
    header_nav_list: [], // 头部导航列表
    footer_nav_list: [], // 脚部导航列表
    get_header_nav(){
        // 获取头部导航
        return http.get("/home/nav/header/")
    },
    get_footer_nav(){
        // 获取脚部导航
        return http.get("/home/nav/footer/")
    },

})

export default nav;
```



components/Header.vue代码：

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
          <div class="login-bar">
            <div class="shop-cart full-left">
              <img src="../assets/cart.svg" alt="" />
              <span><router-link to="/cart">购物车</router-link></span>
            </div>
            <div class="login-box full-left">
              <span>登录</span>
              &nbsp;/&nbsp;
              <span>注册</span>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
```

```vue
<script setup>
import nav from "../api/nav";

// 请求头部导航列表
nav.get_header_nav().then(response=>{
  nav.header_nav_list = response.data
})


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



components/Footer.vue代码：

```vue
<template>
    <div class="footer">
      <ul>
        <li v-for="nav in nav.footer_nav_list">
          <a :href="nav.link" v-if="nav.is_http">{{nav.name}}</a>
          <router-link :to="nav.link" v-else>{{nav.name}}</router-link>
        </li>
      </ul>
      <p>Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p>
    </div>
</template>
```

```vue
<script setup>
import nav from "../api/nav";

// 获取脚部导航列表
nav.get_footer_nav().then(response=>{
  nav.footer_nav_list = response.data
})

</script>
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端实现导航信息展示"
git push origin develop
```

# 2. 轮播图功能实现

compoents/Banner.vue，代码：

```vue
<template>
   <div class="bk"></div>
   <div class="bgfff banner-box">
    <div class="g-banner pr" @mouseleave="state.current_menu=-1">
     <!-- 商品课程分类信息 -->
     <div class="submenu" v-if="state.current_menu==0">
      <div class="inner-box">
       <h2 class="type">前端开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix"><a target="_blank" href="">Vue.js</a>
          <a target="_blank" href="">Typescript</a>
          <a target="_blank" href="">React.JS</a>
          <a target="_blank" href="">HTML/CSS</a>
          <a target="_blank" href="">JavaScript</a>
          <a target="_blank" href="">Angular</a>
          <a target="_blank" href="">Node.js</a>
          <a target="_blank" href="">jQuery</a>
          <a target="_blank" href="">Bootstrap</a>
          <a target="_blank" href="">Sass/Less</a>
          <a target="_blank" href="">WebApp</a>
          <a target="_blank" href="">小程序</a>
          <a target="_blank" href="">前端工具</a>
          <a target="_blank" href="">CSS</a>
          <a target="_blank" href="">Html5</a>
          <a target="_blank" href="">CSS3</a>
        </p>
       </div>
      </div>
      <div class="recomment clearfix">
        <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a7779909e3fc1206960344.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">前端工程师2021</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4599.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 19322</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="前端框架及项目面试 聚焦Vue3/React/Webpack" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5e3cfea008e9a61b06000338-360-202.jpg')"></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">前端框架及项目面试 聚焦Vue3/React/Webpack</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">399.00</span> &middot;
          <span class="difficulty"> 中级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 2946</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="从0打造微前端框架，实战汽车资讯平台，系统掌握微前端架构设计与落地能力" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60d44ec8084b799712000676-360-202.jpg')"></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"><span class="text">从0打造微前端框架，实战汽车资讯平台，系统掌握微前端架构设计与落地能力</span><span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">限时优惠</span>
          <span class="price">￥328.00</span> &middot;
          <span class="difficulty"> 高级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 109</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2bab0952610803240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Vue.js 从入门到精通</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">4步骤</span> &middot;
          <span class="difficulty">4门课</span> &middot;
          <span class="num">19697人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="submenu" v-if="state.current_menu==1">
      <div class="inner-box">
       <h2 class="type">后端开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix">
          <a target="_blank" href="">Java</a>
          <a target="_blank" href="">SpringBoot</a>
          <a target="_blank" href="">Spring Cloud</a>
          <a target="_blank" href="">SSM</a>
          <a target="_blank" href="">PHP</a>
          <a target="_blank" href="">.net</a>
          <a target="_blank" href="">Python</a>
          <a target="_blank" href="">爬虫</a>
          <a target="_blank" href="">Django</a>
          <a target="_blank" href="">Flask</a>
          <a target="_blank" href="">Tornado</a>
          <a target="_blank" href="">Go</a>
          <a target="_blank" href="">C</a>
          <a target="_blank" href="">C++</a>
          <a target="_blank" href="">C#</a>
          <a target="_blank" href="">Ruby</a></p>
       </div>
      </div>
      <div class="recomment clearfix">
        <a href="" target="_blank" title="Java工程师2021" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a777ef0942d7bf06960344.png'); background-size: 100%; "></div>
        <div class="details">
         <div class="title-box">
          <p class="title"> <span class="text">Java工程师2021</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4399.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 15052</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Python工程师（全能型）" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a77721093df37606960344.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Python工程师（全能型）</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4366.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 10786</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Java全栈工程师" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5dd6567b09d9d01c06000338.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Java全栈工程师</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥3380.00</span> &middot;
          <span class="difficulty"> 进阶 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 1853</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2bb6099d6a8803240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">SpringBoot从入门到精通</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">3步骤</span> &middot;
          <span class="difficulty">5门课</span> &middot;
          <span class="num">11092人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="submenu" v-if="state.current_menu==2">
      <div class="inner-box">
       <h2 class="type">移动开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix"></p>
       </div>
      </div>
      <div class="recomment clearfix">
       <a href="" target="_blank" title="移动端架构师成长体系课" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5ec5ddf209cd2c8606000338.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">移动端架构师成长体系课</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4888.00</span> &middot;
          <span class="difficulty"> 进阶 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 402</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Flutter高级进阶实战  仿哔哩哔哩APP 一次性深度掌握Flutter高阶技能" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60497caf0971842912000676-360-202.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Flutter高级进阶实战 仿哔哩哔哩APP 一次性深度掌握Flutter高阶技能</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">368.00</span> &middot;
          <span class="difficulty"> 高级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 646</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="音视频基础+ffmpeg原理+项目实战 一课完成音视频技术开发入门" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5e5621d0092c054612000676-360-202.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">音视频基础+ffmpeg原理+项目实战 一课完成音视频技术开发入门</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">288.00</span> &middot;
          <span class="difficulty"> 入门 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 1303</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2b52090de67603240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Android工程师高薪面试突破路线</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">3步骤</span> &middot;
          <span class="difficulty">3门课</span> &middot;
          <span class="num">1471人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="menuContent">
      <div class="item" :class="{'js-menu-item-on': state.current_menu==0}" @mouseover="state.current_menu=0">
       <span class="title">前端开发：</span>
       <span class="sub-title">HTML5 / Vue.js / Node.js</span>
       <i class="imv2-arrow1_r"></i>
      </div>
      <div class="item" :class="{'js-menu-item-on': state.current_menu==1}" @mouseover="state.current_menu=1">
       <span class="title">后端开发：</span>
       <span class="sub-title">Java / Python / Go</span>
       <i class="imv2-arrow1_r"></i>
      </div>
      <div class="item" :class="{'js-menu-item-on': state.current_menu==2}" @mouseover="state.current_menu=2">
       <span class="title">移动开发：</span>
       <span class="sub-title">Flutter / Android / iOS </span>
       <i class="imv2-arrow1_r"></i>
      </div>
     </div>
      <!-- 轮播图-->
      <div class="g-banner-content"  @mouseover="state.current_menu=-1">
        <el-carousel :interval="5000" arrow="always" height="482px">
          <el-carousel-item>
            <img src="http://fuguangapi.oss-cn-beijing.aliyuncs.com/1.jpg" alt="" style="width: 100%;height: 100%;">
          </el-carousel-item>
          <el-carousel-item>
            <img src="http://fuguangapi.oss-cn-beijing.aliyuncs.com/2.jpg" alt="" style="width: 100%;height: 100%;">
          </el-carousel-item>
          <el-carousel-item>
            <img src="http://fuguangapi.oss-cn-beijing.aliyuncs.com/3.jpg" alt="" style="width: 100%;height: 100%;">
          </el-carousel-item>
          <el-carousel-item>
            <img src="http://fuguangapi.oss-cn-beijing.aliyuncs.com/4.jpg" alt="" style="width: 100%;height: 100%;">
          </el-carousel-item>
          <el-carousel-item>
            <img src="http://fuguangapi.oss-cn-beijing.aliyuncs.com/5.jpg" alt="" style="width: 100%;height: 100%;">
          </el-carousel-item>
        </el-carousel>
     </div>
    </div>
   </div>
</template>

<script setup>
import {reactive} from "vue"
const state = reactive({
  current_menu: -1,
})
</script>

<style scoped>
.banner-box {
  padding: 32px 0;
}
.system-class-show {
  width: 1152px;
  height: 100px;
  margin: 0 auto;
  background: #FFFFFF;
  box-shadow: 0 5px 20px 0 rgba(0, 0, 0, 0.3);
  border-radius: 0 0 8px 8px;
}
.system-class-show .show-box {
  display: block;
  width: 192px;
  height: 45px;
  float: left;
  margin: 28px 0 0 16px;
  cursor: pointer;
}
.system-class-show .show-box .system-class-icon {
  float: left;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background-size: cover;
  margin-right: 8px;
  transition: all .2s;
}
.system-class-show .show-box .describe {
  float: left;
}
.system-class-show .show-box .describe h4 {
  width: 139px;
  font-family: PingFangSC-Medium;
  font-size: 16px;
  color: #1C1F21;
  letter-spacing: 0.76px;
  line-height: 22px;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
}
.system-class-show .show-box .describe p {
  width: 139px;
  font-family: PingFangSC-Regular;
  font-size: 12px;
  color: #545C63;
  line-height: 18px;
  white-space: nowrap;
  overflow: hidden;
}
.system-class-show .show-box:hover .system-class-icon {
  transform: translateY(-2px);
}
.system-class-show .show-box:hover .describe h4 {
  color: #F01414;
}
.system-class-show .line {
  float: left;
  height: 36px;
  border: 1px solid #E8E8E8;
  margin-left: 16px;
  margin-top: 33px;
}
.system-class-show .all-btn {
  position: relative;
  display: block;
  height: 100%;
  cursor: pointer;
  overflow: hidden;
}
.system-class-show .all-btn .mini-title {
  font-family: PingFangSC-Medium;
  font-size: 12px;
  color: #1C1F21;
  text-align: center;
  line-height: 14px;
  margin-top: 40px;
}
.system-class-show .all-btn .more-btn {
  font-family: PingFangSC-Regular;
  font-size: 12px;
  color: #545C63;
  line-height: 12px;
  margin-left: 30px;
  position: relative;
}
.system-class-show .all-btn .more-btn .icon-right2 {
  position: absolute;
  top: 1px;
  left: 28px;
  transition: all .2s;
}
.system-class-show .all-btn:hover .more-btn {
  color: #1C1F21;
}
.system-class-show .all-btn:hover .more-btn .icon-right2 {
  transform: translateX(3px);
}
.g-banner {
  position: relative;
  overflow: hidden;
  width: 1400px;
  margin: auto;
  border-radius: 8px 8px 0 0;
}
.g-banner .g-banner-content {
  position: relative;
  float: left;
  width: 1142px;
}
.g-banner .g-banner-content .g-banner-box {
  position: relative;
  height: 316px;
}
.g-banner .g-banner-content .notice {
  position: absolute;
  top: 8px;
  left: 0;
  background: #FF9900;
  box-shadow: 0 2px 4px 0 rgba(7, 17, 27, 0.2);
  padding: 6px 12px 6px 8px;
  z-index: 1;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}
.g-banner .g-banner-content .notice .imv2-vol_up {
  font-size: 16px;
  color: #FFFFFF;
  display: inline-block;
  line-height: 20px;
  margin-top: 1px;
  margin-right: 4px;
  vertical-align: sub;
}
.g-banner .g-banner-content .notice .notice-txt {
  display: inline-block;
  width: auto;
  font-size: 12px;
  color: #FFFFFF;
  line-height: 20px;
  z-index: 1;
  white-space: nowrap;
}
.g-banner .g-banner-content .notice .notice-close {
  font-size: 16px;
  margin: 6px 0 6px 12px;
  color: rgba(255, 255, 255, 0.6);
  line-height: 20px;
}
.g-banner .g-banner-content .notice .notice-close:hover {
  color: #fff;
}
.g-banner .g-banner-content .notice.closed {
  transition: all .3s;
  background: rgba(255, 153, 0, 0.6);
  box-shadow: 0 2px 4px 0 rgba(7, 17, 27, 0.2);
}
.g-banner .g-banner-content .notice.closed .notice-txt {
  overflow: hidden;
}
.g-banner .g-banner-content .notice.closed .notice-close {
  display: none;
}
.g-banner .banner-anchor {
  position: absolute;
  top: 50%;
  margin-top: -24px;
  width: 48px;
  height: 48px;
  background: rgba(28, 31, 33, 0.1) url(/src/assets/icon-left-small.png) no-repeat center / 16px auto;
  border-radius: 50%;
  color: #FFFFFF;
  transition: all .2s;
}
.g-banner .banner-anchor:hover {
  background-color: rgba(28, 31, 33, 0.5);
}
.g-banner .next {
  right: 16px;
  transform: rotate(180deg);
}
.g-banner .prev {
  left: 16px;
}
.g-banner .g-banner-box > a:first-child .banner-slide {
  display: block;
}
.g-banner .banner-slide {
  position: absolute;
  display: none;
  width: 896px;
  height: 316px;
  /*margin: auto;*/
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-repeat: no-repeat;
  background-position: center 0;
}
.g-banner .banner-slide .festival {
  position: absolute;
  top: 450px;
  right: 75px;
}
.g-banner .banner-slide .festival a {
  display: block;
  width: 190px;
  height: 120px;
}
.g-banner .banner-slide .festival a:hover {
  background-position: 0 0;
}
.g-banner .banner-slide img {
  width: 100%;
  height: 100%;
}
.g-banner .inner {
  position: relative;
  width: 1200px;
  margin: 0 auto;
}
.g-banner .banner-dots {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: right;
  padding-right: 24px;
  line-height: 12px;
}
.g-banner .banner-dots span {
  display: inline-block;
  *display: inline;
  *zoom: 1;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  margin-left: 8px;
  background: rgba(255, 255, 255, 0.75);
  transition: all .2s;
  cursor: pointer;
}
.g-banner .banner-dots span.active {
  width: 20px;
}

.submenu {
  position: absolute;
  left: 256px;
  width: 776px;
  height: 482px;
  background: #FFFFFF;
  box-shadow: 0 4px 8px 0 rgba(7, 17, 27, 0.1);
  border-radius: 0 12px 12px 0;
  z-index: 33;
  box-sizing: border-box;
}
.submenu .inner-box {
  height: 188px;
  padding: 28px 36px 0;
  box-sizing: border-box;
}
.submenu .inner-box .type {
  margin-bottom: 10px;
  font-size: 16px;
  color: #1C1F21;
  line-height: 22px;
  font-weight: bold;
}
.submenu .inner-box .tag {
  margin-bottom: 12px;
}
.submenu .inner-box .tag a {
  float: left;
  font-size: 12px;
  line-height: 1;
  color: #E02020;
  border-radius: 100px;
  border: 1px solid #E02020;
  padding: 5px 10px;
  margin-right: 10px;
}
.submenu .inner-box .tag a:last-child {
  margin-right: 0;
}
.submenu .inner-box .lore {
  font-size: 12px;
  line-height: 24px;
  color: #6D7278;
  margin-bottom: 8px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
}
.submenu .inner-box .lore .title {
  color: #1C1F21;
  font-weight: bold;
}
.submenu .inner-box .lore .lores {
  width: 0;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  -webkit-flex: 1;
  flex: 1;
}
.submenu .inner-box .lore .lores a {
  float: left;
  color: #6D7278;
  margin-right: 24px;
}
.submenu .inner-box .lore .lores a:last-child {
  margin-right: 0;
}
.submenu .recomment {
  padding: 35px 36px;
  height: 204px;
  background-color: #F3F5F6;
  box-sizing: border-box;
}
.submenu .recomment .recomment-item {
  width: 329px;
  float: left;
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
}
.submenu .recomment .recomment-item:nth-child(2n) {
  margin-left: 30px;
}
.submenu .recomment .recomment-item:nth-child(-n+2) {
  margin-bottom: 30px;
}
.submenu .recomment .recomment-item .img {
  width: 90px;
  height: 50px;
  margin-right: 11px;
  border-radius: 4px;
  background-position: center;
  image-rendering: -moz-crisp-edges;
  /* Firefox */
  image-rendering: -o-crisp-edges;
  /* Opera */
  image-rendering: -webkit-optimize-contrast;
  /*Webkit (non-standard naming) */
  image-rendering: crisp-edges;
  -ms-interpolation-mode: nearest-neighbor;
  /* IE (non-standard property) */
  box-shadow: 0 6px 10px 0 rgba(95, 101, 105, 0.15);
}
.submenu .recomment .recomment-item .details {
  height: 50px;
  font-size: 12px;
  width: 0;
  -webkit-box-flex: 1;
  -ms-flex: 1;
  -webkit-flex: 1;
  flex: 1;
}
.submenu .recomment .recomment-item .details .title-box {
  margin-bottom: 10px;
  display: -webkit-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  -webkit-align-items: center;
  align-items: center;
}
.submenu .recomment .recomment-item .details .title-box .title {
  display: flex;
  align-items: center;
  color: #1C1F21;
  width: 228px;
}
.submenu .recomment .recomment-item .details .title-box .title .text {
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 4em);
}
.submenu .recomment .recomment-item .details .title-box .title .tag {
  display: inline-block;
  width: 2em;
  color: #fff;
  opacity: .6;
  border-radius: 2px;
  line-height: 1;
  padding: 2px 4px;
  margin-left: 5px;
}
.submenu .recomment .recomment-item .details .title-box .title .tag.shizhan {
  background-color: #FA6400;
}
.submenu .recomment .recomment-item .details .title-box .title .tag.tixi {
  background-color: #E02020;
}
.submenu .recomment .recomment-item .details .title-box .title .tag.lujing {
  background-color: #0091FF;
}
.submenu .recomment .recomment-item .details .bottom {
  color: #9199A1;
  line-height: 18px;
}
.submenu .recomment .recomment-item .details .bottom .discount-name,
.submenu .recomment .recomment-item .details .bottom .tag {
  display: inline-block;
  color: #fff;
  background-color: rgba(242, 13, 13, 0.6);
  border-radius: 2px;
  padding: 2px 4px;
  line-height: 1;
}
.submenu .recomment .recomment-item .details .bottom .discount-name {
  background: rgba(242, 13, 13, 0.6);
}
.submenu .recomment .recomment-item .details .bottom .price:not(.free) {
  font-weight: bold;
  color: #F01414;
}
.menuContent {
  position: relative;
  float: left;
  width: 256px;
  height: 482px;
  z-index: 2;
  padding-top: 17px;
  box-sizing: border-box;
  background: #39364d;
  border-bottom-left-radius: 4px;
  font-weight: 400;
}
.menuContent .item {
  line-height: 50px;
  cursor: pointer;
  position: relative;
  color: #fff;
  padding: 0 14px;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
  height: 50px;
  transition: all .1s;
  font-size: 14px;
}
.menuContent .item .sub-title {
  font-size: 12px;
}
.menuContent .item i {
  position: absolute;
  right: 4px;
  top: 16px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 16px;
}
.menuContent .item.js-menu-item-on {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
```



Home.vue，代码：

```vue
<template>
<div class="home">
    <Header></Header>
    <div id="main">
      <Banner></Banner>
    </div>
    <Footer></Footer>
</div>
</template>

<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import Banner from "../components/Banner.vue"

</script>

<style scoped>

</style>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端展示轮播图界面效果"
git push origin develop
```



### 2.1 安装依赖模块和配置

安装图片处理模块，前面已经安装了，如果没有安装则需要安装

```shell
pip install pillow
```

填写上传文件的相关配置，settings/dev.py

```python
# 访问静态文件的url地址前缀
STATIC_URL = '/static/'
# 设置django的静态文件目录[手动创建]
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 项目中存储上传文件的根目录[手动创建]，注意，uploads目录需要手动创建否则上传文件时报错
MEDIA_ROOT = BASE_DIR / "uploads"
# 访问上传文件的url地址前缀
MEDIA_URL = "/uploads/"
```

总路由luffycityapi.urls.py新增代码：

```python
from django.contrib import admin
from django.urls import path,re_path,include

from django.conf import settings
from django.views.static import serve # 静态文件代理访问模块

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'uploads/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path("home/", include("home.urls")),
]
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:服务端提供访问静态文件（static和uploads）的url配置"
git push origin develop
```



### 2.2 创建轮播图的模型

home/models.py，代码：

```python
from models import BaseModel,models
# Create your models here.

class Banner(BaseModel):
    image = models.ImageField(upload_to="banner/%Y/", verbose_name="图片地址")
    link = models.CharField(max_length=500, verbose_name="链接地址")
    note = models.CharField(max_length=150, verbose_name='备注信息')
    is_http = models.BooleanField(default=False, verbose_name="是否外链地址", help_text="站点链接地址：http://www.baidu.com/book<br>站点链接地址：/book/")

    class Meta:
        db_table = "lf_banner"
        verbose_name = "轮播广告"
        verbose_name_plural = verbose_name
```

数据迁移

```python
cd luffycityapi
python manage.py makemigrations
python manage.py migrate
```

把课件中素材目录下的图片保存到项目上传文件存储目录下`luffycityapi/uploads/banner/2021/`，并添加测试数据到MySQL。

```sql
INSERT INTO luffycity.lf_banner (id, name, orders, is_show, is_deleted, created_time, updated_time, image, note, link, is_http) VALUES (1, '1', 1, 1, 0, '2021-07-15 03:39:49.859000', '2021-07-15 03:39:51.437000', 'banner/2022/1.jpg', '暂无', '/project', 0);
INSERT INTO luffycity.lf_banner (id, name, orders, is_show, is_deleted, created_time, updated_time, image, note, link, is_http) VALUES (2, '2', 1, 1, 0, '2021-07-15 03:39:49.859000', '2021-07-15 03:39:51.437000', 'banner/2022/2.jpg', '暂无', '/project', 0);
INSERT INTO luffycity.lf_banner (id, name, orders, is_show, is_deleted, created_time, updated_time, image, note, link, is_http) VALUES (3, '3', 1, 1, 0, '2021-07-15 03:39:49.859000', '2021-07-15 03:39:51.437000', 'banner/2022/3.jpg', '暂无', '/project', 0);
INSERT INTO luffycity.lf_banner (id, name, orders, is_show, is_deleted, created_time, updated_time, image, note, link, is_http) VALUES (4, '4', 1, 1, 0, '2021-07-15 03:39:49.859000', '2021-07-15 03:39:51.437000', 'banner/2022/4.jpg', '暂无', '/project', 0);
INSERT INTO luffycity.lf_banner (id, name, orders, is_show, is_deleted, created_time, updated_time, image, note, link, is_http) VALUES (5, '5', 1, 1, 0, '2021-07-15 03:39:49.859000', '2021-07-15 03:39:51.437000', 'banner/2022/5.jpg', '暂无', '/project', 0);
```



### 2.3 序列化器

home/serializers.py

```python
class BannerModelSerializer(serializers.ModelSerializer):
    """
    轮播广告的序列化器
    """
    class Meta:
        model = Banner
        fields = ["image", "name", "link", "is_http"]
```

### 2.4 视图代码

home/views.py

```python
import constants
from rest_framework.generics import ListAPIView
from .models import Nav, Banner
from .serializers import NavModelSerializer, BannerModelSerializer

# 中间代码省略

class BannerListAPIView(ListAPIView):
    """轮播广告视图"""
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.BANNER_SIZE]
    serializer_class = BannerModelSerializer
```



### 2.5 路由代码

home/urls.py，代码：

```python
from django.urls import path
from . import views
urlpatterns = [
    path("nav/header/", views.NavHeaderListAPIView.as_view()),
    path("nav/footer/", views.NavFooterListAPIView.as_view()),
    path("banner/", views.BannerListAPIView.as_view()),
]
```

`utils/constants.py`，常量文件:

```python
# 轮播广告显示的最大数量
BANNER_SIZE = 10
```

提交git版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:api服务端实现轮播广告接口"
git push origin develop
```



### 2.6 客户端获取轮播广告的数据

src/api/banner.js，代码：

```javascript
import http from "../utils/http"
import {reactive, ref} from "vue"

const banner = reactive({
    banner_list: [], // 轮播广告列表
    get_banner_list(){
        // 获取轮播广告
        return http.get("/home/banner/")
    },

})

export default banner;
```



src/components/Banner.vue，代码：

```vue
<template>
   <div class="bk"></div>
   <div class="bgfff banner-box">
    <div class="g-banner pr" @mouseleave="state.current_menu=-1">
     <!-- 商品课程分类信息 -->
     <div class="submenu" v-if="state.current_menu==0">
      <div class="inner-box">
       <h2 class="type">前端开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix"><a target="_blank" href="">Vue.js</a>
          <a target="_blank" href="">Typescript</a>
          <a target="_blank" href="">React.JS</a>
          <a target="_blank" href="">HTML/CSS</a>
          <a target="_blank" href="">JavaScript</a>
          <a target="_blank" href="">Angular</a>
          <a target="_blank" href="">Node.js</a>
          <a target="_blank" href="">jQuery</a>
          <a target="_blank" href="">Bootstrap</a>
          <a target="_blank" href="">Sass/Less</a>
          <a target="_blank" href="">WebApp</a>
          <a target="_blank" href="">小程序</a>
          <a target="_blank" href="">前端工具</a>
          <a target="_blank" href="">CSS</a>
          <a target="_blank" href="">Html5</a>
          <a target="_blank" href="">CSS3</a>
        </p>
       </div>
      </div>
      <div class="recomment clearfix">
        <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a7779909e3fc1206960344.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">前端工程师2021</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4599.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 19322</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="前端框架及项目面试 聚焦Vue3/React/Webpack" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5e3cfea008e9a61b06000338-360-202.jpg')"></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">前端框架及项目面试 聚焦Vue3/React/Webpack</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">399.00</span> &middot;
          <span class="difficulty"> 中级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 2946</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="从0打造微前端框架，实战汽车资讯平台，系统掌握微前端架构设计与落地能力" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60d44ec8084b799712000676-360-202.jpg')"></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"><span class="text">从0打造微前端框架，实战汽车资讯平台，系统掌握微前端架构设计与落地能力</span><span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">限时优惠</span>
          <span class="price">￥328.00</span> &middot;
          <span class="difficulty"> 高级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 109</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2bab0952610803240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Vue.js 从入门到精通</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">4步骤</span> &middot;
          <span class="difficulty">4门课</span> &middot;
          <span class="num">19697人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="submenu" v-if="state.current_menu==1">
      <div class="inner-box">
       <h2 class="type">后端开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix">
          <a target="_blank" href="">Java</a>
          <a target="_blank" href="">SpringBoot</a>
          <a target="_blank" href="">Spring Cloud</a>
          <a target="_blank" href="">SSM</a>
          <a target="_blank" href="">PHP</a>
          <a target="_blank" href="">.net</a>
          <a target="_blank" href="">Python</a>
          <a target="_blank" href="">爬虫</a>
          <a target="_blank" href="">Django</a>
          <a target="_blank" href="">Flask</a>
          <a target="_blank" href="">Tornado</a>
          <a target="_blank" href="">Go</a>
          <a target="_blank" href="">C</a>
          <a target="_blank" href="">C++</a>
          <a target="_blank" href="">C#</a>
          <a target="_blank" href="">Ruby</a></p>
       </div>
      </div>
      <div class="recomment clearfix">
        <a href="" target="_blank" title="Java工程师2021" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a777ef0942d7bf06960344.png'); background-size: 100%; "></div>
        <div class="details">
         <div class="title-box">
          <p class="title"> <span class="text">Java工程师2021</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4399.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 15052</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Python工程师（全能型）" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60a77721093df37606960344.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Python工程师（全能型）</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4366.00</span> &middot;
          <span class="difficulty"> 零基础 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 10786</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Java全栈工程师" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5dd6567b09d9d01c06000338.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Java全栈工程师</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥3380.00</span> &middot;
          <span class="difficulty"> 进阶 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 1853</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2bb6099d6a8803240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">SpringBoot从入门到精通</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">3步骤</span> &middot;
          <span class="difficulty">5门课</span> &middot;
          <span class="num">11092人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="submenu" v-if="state.current_menu==2">
      <div class="inner-box">
       <h2 class="type">移动开发</h2>
       <div class="tag clearfix">
       </div>
       <div class="lore">
        <span class="title">知识点：</span>
        <p class="lores clearfix"></p>
       </div>
      </div>
      <div class="recomment clearfix">
       <a href="" target="_blank" title="移动端架构师成长体系课" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5ec5ddf209cd2c8606000338.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">移动端架构师成长体系课</span> <span class="tag tixi">体系</span> </p>
         </div>
         <div class="bottom">
          <span class="discount-name">优惠价</span>
          <span class="price">￥4888.00</span> &middot;
          <span class="difficulty"> 进阶 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 402</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="Flutter高级进阶实战  仿哔哩哔哩APP 一次性深度掌握Flutter高阶技能" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/60497caf0971842912000676-360-202.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Flutter高级进阶实战 仿哔哩哔哩APP 一次性深度掌握Flutter高阶技能</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">368.00</span> &middot;
          <span class="difficulty"> 高级 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 646</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="音视频基础+ffmpeg原理+项目实战 一课完成音视频技术开发入门" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/5e5621d0092c054612000676-360-202.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">音视频基础+ffmpeg原理+项目实战 一课完成音视频技术开发入门</span> <span class="tag shizhan">实战</span> </p>
         </div>
         <div class="bottom">
          <span class="price">288.00</span> &middot;
          <span class="difficulty"> 入门 </span> &middot;
          <span class="num"><i class="imv2-set-sns"></i> 1303</span>
         </div>
        </div> </a>
       <a href="" target="_blank" title="" class="recomment-item">
        <div class="img" style="background-image: url('/src/assets/604f2b52090de67603240324-140-140.png'); background-size: 100%; "></div>
        <div class="details">
         <!--路径单独写-->
         <div class="title-box">
          <p class="title"> <span class="text">Android工程师高薪面试突破路线</span> <span class="tag lujing">路线</span> </p>
         </div>
         <div class="bottom">
          <span class="difficulty">3步骤</span> &middot;
          <span class="difficulty">3门课</span> &middot;
          <span class="num">1471人收藏</span>
         </div>
        </div> </a>
      </div>
     </div>
     <div class="menuContent">
      <div class="item" :class="{'js-menu-item-on': state.current_menu==0}" @mouseover="state.current_menu=0">
       <span class="title">前端开发：</span>
       <span class="sub-title">HTML5 / Vue.js / Node.js</span>
       <i class="imv2-arrow1_r"></i>
      </div>
      <div class="item" :class="{'js-menu-item-on': state.current_menu==1}" @mouseover="state.current_menu=1">
       <span class="title">后端开发：</span>
       <span class="sub-title">Java / Python / Go</span>
       <i class="imv2-arrow1_r"></i>
      </div>
      <div class="item" :class="{'js-menu-item-on': state.current_menu==2}" @mouseover="state.current_menu=2">
       <span class="title">移动开发：</span>
       <span class="sub-title">Flutter / Android / iOS </span>
       <i class="imv2-arrow1_r"></i>
      </div>
     </div>
      <!-- 轮播图-->
      <div class="g-banner-content"  @mouseover="state.current_menu=-1">
        <el-carousel :interval="5000" arrow="always" height="482px" v-if="banner.banner_list[0]">
          <el-carousel-item v-for="item,key in banner.banner_list" :key="key">
            <a :href="item.link" v-if="item.is_http"><img :src="item.image" alt="" style="width: 100%;height: 100%;"></a>
            <router-link :to="item.link" v-else><img :src="item.image" alt="" style="width: 100%;height: 100%;"></router-link>
          </el-carousel-item>
        </el-carousel>
     </div>
    </div>
   </div>
</template>

<script setup>
import {reactive} from "vue"
import banner from "../api/banner";

// 获取轮播广告列表
banner.get_banner_list().then(response=>{
  banner.banner_list = response.data
})

const state = reactive({
  current_menu: -1,
})
</script>
```

提交git版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature:客户端展示轮播广告数据"
git push origin develop
```



# 3. 缓存导航与轮播图数据

因为导航菜单或轮播广告在项目中每一个页面都会被用户访问到，所以我们可以实现缓存，减少MySQL数据库的查询压力，使用内存缓存可以加快数据查询速度。

视图缓存：https://docs.djangoproject.com/zh-hans/3.2/topics/cache/#the-per-view-cache

装饰类视图：https://docs.djangoproject.com/zh-hans/3.2/topics/class-based-views/intro/#decorating-the-class

utils/views.py，代码：

```python
import constants
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CacheListAPIView(ListAPIView):
    """列表缓存视图"""
    @method_decorator(cache_page(constants.LIST_PAGE_CACHE_TIME))
    def get(self,request, *args, **kwargs):
        # 重写ListAPIView的get方法，但是不改动源代码。仅仅装饰而已
        return super().get(request, *args, **kwargs)
```

utils/constants.py，代码：

```python
# 列表页数据的缓存周期，单位：秒
LIST_PAGE_CACHE_TIME = 24 * 60 * 60
```

home/views.py，代码：

```python
import constants
from views import CacheListAPIView
from .models import Nav, Banner
from .serializers import NavModelSerializer, BannerModelSerializer



class NavHeaderListAPIView(CacheListAPIView):
    """顶部导航视图"""
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.NAV_HEADER_SIZE]
    serializer_class = NavModelSerializer


class NavFooterListAPIView(CacheListAPIView):
    """脚部导航视图"""
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.NAV_FOOTER_SIZE]
    serializer_class = NavModelSerializer


class BannerListAPIView(CacheListAPIView):
    """轮播广告视图"""
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")[:constants.BANNER_SIZE]
    serializer_class = BannerModelSerializer

```

注意：此处数据使用了缓存，那么将来admin站点在修改此处相关的数据库的数据时，admin站点中我们就需要在更新数据时对缓存进行删除，这块业务逻辑等我们后面登陆注册功能以后搭建admin后面时会带着小伙伴们完成。

提交git版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "perf:服务端实现导航和轮播的数据缓存"
git push origin develop
```

