# 下单结算

## 客户端展示下单结算界面展示

`views/Cart.vue`，代码：

```vue
<div class="li-3"><router-link to="/order" class="btn">去结算</router-link></div>
```

`router/index.js`，代码：

```javascript
// 路由列表
const routes = [
    {
      meta:{
        title: "luffy2.0-首页",
        keepAlive: true
      },
      path:'/',         // uri访问地址
      component: ()=> import("../views/Home.vue")
    },{
      meta:{
        title: "登录",
        keepAlive: true
      },
      path: '/login',
      name: "Login",            // 路由名称
      component: ()=> import("../views/Login.vue"),         // uri绑定的组件页面
    },{
      meta:{
        title: "注册",
        keepAlive: true
      },
      path: '/register',
      name: "Register",            // 路由名称
      component: ()=> import("../views/Register.vue"),         // uri绑定的组件页面
    },{
      meta:{
        title: "项目课",
        keepAlive: true
      },
      path: '/project',
      name: "Course",            // 路由名称
      component: ()=> import("../views/Course.vue"),         // uri绑定的组件页面
    },{
      meta:{
        title: "项目课",
        keepAlive: true
      },
      path: '/project/:id',
      name: "Info",
      component: ()=> import("../views/Info.vue"),
    },{
      meta:{
        title: "购物车",
        keepAlive: true
      },
      path: '/cart',
      name: "Cart",
      component: ()=> import("../views/Cart.vue"),
    },{
      meta:{
        title: "确认下单",
        keepAlive: true
      },
      path: '/order',
      name: "Order",
      component: ()=> import("../views/Order.vue"),
    }
]
```

`views/Order.vue`，代码：

```vue
<template>
  <div class="cart">
    <Header/>
    <div class="cart-main">
      <div class="cart-header">
        <div class="cart-header-warp">
          <div class="cart-title left">
            <h1 class="left">确认订单</h1>
          </div>
          <div class="right">
            <div class="">
              <span class="left"><router-link class="myorder-history" to="/cart">返回购物车</router-link></span>
            </div>
          </div>
        </div>
      </div>
      <div class="cart-body" id="cartBody">
        <div class="cart-body-title"><p class="item-1 l">课程信息</p></div>
        <div class="cart-body-table">
          <div class="item">
              <div class="item-2">
                  <a href="" class="img-box l"><img src="../assets/course-9.png"></a>
                  <dl class="l has-package">
                    <dt>【实战课程】3天Typescript精修 </dt>
                    <p class="package-item">减免价</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price"><em>￥</em><span>998.00</span></p>
                      <p class="original-price"><em>￥</em><span>800.00</span></p>
                  </div>
              </div>
          </div>
          <div class="item">
              <div class="item-2">
                  <a href="" class="img-box l"><img src="../assets/course-9.png"></a>
                  <dl class="l has-package">
                    <dt>【实战课程】3天Typescript精修 </dt>
                    <p class="package-item">减免价</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price"><em>￥</em><span>998.00</span></p>
                      <p class="original-price"><em>￥</em><span>800.00</span></p>
                  </div>
              </div>
          </div>
          <div class="item">
              <div class="item-2">
                  <a href="" class="img-box l"><img src="../assets/course-9.png"></a>
                  <dl class="l has-package">
                    <dt>【实战课程】3天Typescript精修 </dt>
                    <p class="package-item">减免价</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price"><em>￥</em><span>998.00</span></p>
                      <p class="original-price"><em>￥</em><span>800.00</span></p>
                  </div>
              </div>
          </div>
          <div class="item">
              <div class="item-2">
                  <a href="" class="img-box l"><img src="../assets/course-9.png"></a>
                  <dl class="l has-package">
                    <dt>【实战课程】3天Typescript精修 </dt>
                    <p class="package-item">减免价</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price"><em>￥</em><span>998.00</span></p>
                      <p class="original-price"><em>￥</em><span>800.00</span></p>
                  </div>
              </div>
          </div>
          <div class="item">
              <div class="item-2">
                  <a href="" class="img-box l"><img src="../assets/course-9.png"></a>
                  <dl class="l has-package">
                    <dt>【实战课程】3天Typescript精修 </dt>
                    <p class="package-item">减免价</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price"><em>￥</em><span>998.00</span></p>
                      <p class="original-price"><em>￥</em><span>800.00</span></p>
                  </div>
              </div>
          </div>
        </div>
        <div class="coupons-box">
          <div class="coupon-title-box">
            <p class="coupon-title">
              使用优惠券/积分
                <span v-if="state.use_coupon" @click="state.use_coupon=!state.use_coupon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-394d1fd8=""><path fill="currentColor" d="M831.872 340.864 512 652.672 192.128 340.864a30.592 30.592 0 0 0-42.752 0 29.12 29.12 0 0 0 0 41.6L489.664 714.24a32 32 0 0 0 44.672 0l340.288-331.712a29.12 29.12 0 0 0 0-41.728 30.592 30.592 0 0 0-42.752 0z"></path></svg></span>
                <span v-else @click="state.use_coupon=!state.use_coupon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-394d1fd8=""><path fill="currentColor" d="m488.832 344.32-339.84 356.672a32 32 0 0 0 0 44.16l.384.384a29.44 29.44 0 0 0 42.688 0l320-335.872 319.872 335.872a29.44 29.44 0 0 0 42.688 0l.384-.384a32 32 0 0 0 0-44.16L535.168 344.32a32 32 0 0 0-46.336 0z"></path></svg></span>
<!--                <i :class="state.use_coupon?'el-icon-arrow-up':'el-icon-arrow-down'" @click="state.use_coupon=!state.use_coupon"></i>-->
            </p>
          </div>
          <transition name="el-zoom-in-top">
          <div class="coupon-del-box" v-if="state.use_coupon">
            <div class="coupon-switch-box">
              <div class="switch-btn ticket" :class="{'checked': state.discount_type===0}" @click="state.discount_type=0">优惠券 (4)<em><i class="imv2-check"></i></em></div>
              <div class="switch-btn code" :class="{'checked': state.discount_type===1}" @click="state.discount_type=1">积分<em><i class="imv2-check"></i></em></div>
            </div>
            <div class="coupon-content ticket" v-if="state.discount_type===0">
              <p class="no-coupons" v-if="state.coupon_list.length<1">暂无可用优惠券</p>
              <div class="coupons-box" v-else>
               <div class="content-box">
                <ul class="nouse-box">
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l select">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l wait-use">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l wait-use">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
                <ul class="use-box">
                 <li class="l useing">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
                <ul class="overdue-box">
                 <li class="l useing">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
               </div>
              </div>
            </div>
            <div class="coupon-content code" v-else>
                <div class="input-box">
                  <el-input-number placeholder="10积分=1元" v-model="state.credit" :step="1" :min="0" :max="1000"></el-input-number>
                  <a class="convert-btn">兑换</a>
                </div>
                <div class="converted-box">
                  <p>使用积分:<span class="code-num">200</span></p>
                  <p class="course-title">课程:<span class="c_name">3天JavaScript入门</span>
                    <span class="discount-cash">100积分抵扣:<em>10</em>元</span>
                  </p>
                  <p class="course-title">课程:<span class="c_name">3天JavaScript入门</span>
                    <span class="discount-cash">100积分抵扣:<em>10</em>元</span>
                  </p>
                </div>
                <p class="error-msg">本次订单最多可以使用1000积分，您当前拥有200积分。(10积分=1元)</p>
                <p class="tip">说明：每笔订单只能使用一次积分，并只有在部分允许使用积分兑换的课程中才能使用。</p>
              </div>
          </div>
          </transition>
        </div>
        <div class="pay-type">
          <p class="title">选择支付方式</p>
          <div class="list">
            <img :src="state.pay_type==0?'/src/assets/alipay2.png':'/src/assets/alipay1.png'" @click="state.pay_type=0" alt="支付宝">
            <img :src="state.pay_type==1?'/src/assets/wechat2.png':'/src/assets/wechat1.png'" @click="state.pay_type=1" alt="微信">
            <img :src="state.pay_type==2?'/src/assets/yue2.png':'/src/assets/yue1.png'"  @click="state.pay_type=2" alt="余额">
          </div>
        </div>
        <div class="pay-box" :class="{fixed:state.fixed}">
				  <div class="row-bottom">
            <div class="row">
              <div class="goods-total-price-box">
                <p class="r rw price-num"><em>￥</em><span>1811.00</span></p>
                <p class="r price-text"><span>共<span>5</span>件商品，</span>商品总金额：</p>
              </div>
            </div>
            <div class="coupons-discount-box">
              <p class="r rw price-num">-<em>￥</em><span>60.00</span></p>
              <p class="r price-text">优惠券/积分抵扣：</p>
            </div>
            <div class="pay-price-box clearfix">
              <p class="r rw price"><em>￥</em><span id="js-pay-price">1751.00</span></p>
              <p class="r price-text">应付：</p>
            </div>
            <span class="r btn btn-red submit-btn">提交订单</span>
					</div>
          <div class="pay-add-sign">
            <ul class="clearfix">
              <li>支持花呗</li>
              <li>可开发票</li>
              <li class="drawback">7天可退款</li>
            </ul>
          </div>
	      </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script setup>
import {reactive,watch} from "vue"
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {useStore} from "vuex";

let store = useStore()

let state = reactive({
  course_list: [],     // 购物车中的商品课程列表
  total_price: 0,      // 勾选商品的总价格
  use_coupon: false,   // 用户是否使用优惠
  discount_type: 0,    // 0表示优惠券，1表示积分
  coupon_list:[1,2,3], // 用户拥有的可用优惠券列表
  select: -1,          // 当前用户选中的优惠券
  credit: 0,           // 当前用户选择抵扣的积分
  fixed: true,         // 底部订单总价是否固定浮动
  pay_type: 0,         // 支付方式
})

// 监听用户选择的支付方式
watch(
    ()=>state.pay_type,
    ()=>{
      console.log(state.pay_type)
    }
)

// 底部订单总价信息固定浮动效果
window.onscroll = ()=>{
  let cart_body_table = document.querySelector(".cart-body-table")
  let offsetY = window.scrollY
  let maxY = cart_body_table.offsetTop+cart_body_table.offsetHeight
  state.fixed = offsetY < maxY
}
</script>

<style scoped>
.cart-header {
	height: 160px;
	background-color: #e3e6e9;
	background: url("/src/assets/cart-header-bg.jpeg") repeat-x;
	background-size: 38%;
}

.cart-header .cart-header-warp {
	width: 1500px;
	height: 120px;
	line-height: 120px;
	margin-left: auto;
	margin-right: auto;
	font-size: 14px
}

.cart-header .cart-header-warp .myorder-history {
	font-weight: 200
}

.cart-header .left {
	float: left
}

.cart-header .right {
	float: right
}

.cart-header .cart-title {
	color: #4d555d;
	font-weight: 200;
	font-size: 14px
}

.cart-header .cart-title h1 {
	font-size: 32px;
	line-height: 115px;
	margin-right: 25px;
	color: #07111b;
	font-weight: 200
}

.cart-header .cart-title span {
	margin: 0 4px
}

.l {
  float: left;
}
.r {
  float: right;
}
.cart-body {
	width: 1500px;
	padding: 0 36px 32px;
	background-color: #fff;
	margin-top: -40px;
	margin-left: auto;
	margin-right: auto;
	box-shadow: 0 8px 16px 0 rgba(7,17,27, .1);
	border-radius: 8px;
	box-sizing: border-box
}

.cart-body .left {
	float: left!important
}

.cart-body .right {
	float: right!important
}

.cart-body .cart-body-title {
	min-height: 88px;
	line-height: 88px;
	border-bottom: 1px solid #b7bbbf;
	box-sizing: border-box
}

body {
	background: #f8fafc
}

.cart-body .cart-body-title span {
	font-size: 14px
}

.cart-body .cart-body-title .item-1>span,
.cart-body .cart-body-title .item-2>span,
.cart-body .cart-body-title .item-3>span{
	display: inline-block;
	font-size: 14px;
	line-height: 24px;
	color: #4d555d
}

.cart-body .cart-body-title .item-1>span {
	color: #93999f
}

.cart-body .cart-body-title .item-2>span {
	margin-left: 40px
}

.cart-body .item {
	height: 88px;
	padding: 24px 0;
	background: #f3f5f7;
}
.cart-body .cart-body-table {
    padding-bottom: 36px;
    border-bottom: 1px solid #d9dde1;
}
.cart-body .item>div {
	float: left
}

.cart-body .item .item-1 {
	padding-top: 34px;
	position: relative;
	z-index: 1
}

.cart-body .item:last-child>.item-1::after {
	display: none
}

.cart-body .item-1 {
	width: 120px
}

.cart-body .item-1 i {
	margin-left: 12px;
	margin-right: 8px;
	font-size: 24px
}

.cart-body .item-2 {
	width: 1020px;
  position:relative;
}
.cart-body .item-2>span{
  line-height: 88px;
}
.cart-body .item-2 dl {
	width: 464px;
	margin-left: 24px;
	padding-top: 12px
}

.cart-body .item-2 dl a {
	display: block;
}

.cart-body .item-2 dl.has-package {
	padding-top: 4px;
}

.cart-body .item-2 dl.has-package .package-item {
	display: inline-block;
	padding: 0 12px;
	margin-top: 4px;
	font-size: 12px;
	color: rgba(240,20,20, .6);
	line-height: 24px;
	background: rgba(240,20,20, .08);
	border-radius: 12px;
	cursor: pointer
}

.cart-body .item-2 dl.has-package .package-item:hover {
	color: #fff;
	background: rgba(240,20,20, .2)
}

.cart-body .item-2 dt {
	font-size: 16px;
	color: #07111b;
	line-height: 24px;
	margin-bottom: 4px
}

.cart-body .item-2 .img-box {
	display: block;
  margin-left: 42px;
}
.cart-body .item-2 .img-box img{
  height: 94px;
}
.cart-body .item-2 dd {
	font-size: 12px;
	color: #93999f;
	line-height: 24px;
	font-weight: 200
}

.cart-body .item-2 dd a {
	display: inline-block;
	margin-left: 12px;
	color: rgba(240,20,20, .4)
}

.cart-body .item-2 dd a:hover {
	color: #f01414
}

.cart-body .item-3 {
	width: 280px;
	margin-left: 48px;
  position: relative;
}

.cart-body .item-3 .price {
	display: inline-block;
	height: 46px;
	width: 96px;
  padding-top: 24px;
  padding-bottom: 24px;
  color: #f01414;
}
.cart-body .item-3 .price em,
.cart-body .item-3 .price span{
  font-size: 18px;
}
.cart-body .item-3 .price .original-price em,
.cart-body .item-3 .price .original-price span{
  font-size: 15px;
  color: #aaa;
  text-decoration: line-through;
}

.cart-body .cart-body-bot li {
	float: left
}

.cart-body .cart-body-bot .li-1 em,
.cart-body .cart-body-bot .li-3 em {
	font-style: normal;
	color: red
}

.cart-body .cart-body-bot .li-2 .price {
	font-size: 16px;
	color: #f01414;
	line-height: 24px;
	font-weight: 700
}

.coupons-box::after{
  display: block;
  content: "";
  overflow: hidden;
  clear: both;
}
.coupons-box .coupon-title-box {
	margin: 27px 0 0 12px
}

.coupons-box .coupon-title-box .coupon-title {
	color: #07111b;
	font-size: 16px;
	line-height: 34px
}

.coupons-box .coupon-title-box .coupon-title svg {
	position: relative;
    width: 26px;
    height: 26px;
	top: 5px;
	margin-left: 12px;
	font-size: 24px;
	color: #999;
	cursor: pointer
}


.coupons-box .coupon-del-box {
	width: 100%;
	padding-top: 24px;
	box-sizing: border-box
}

.coupons-box .coupon-del-box .coupon-switch-box {
	margin-bottom: 16px
}

.coupons-box .coupon-del-box .coupon-switch-box .switch-btn {
	position: relative;
	display: inline-block;
	width: 138px;
	height: 58px;
	line-height: 20px;
	border: 1px solid #d9dde1;
	border-radius: 8px;
	padding: 18px 0;
	color: #1c1f21;
	text-align: center;
	font-size: 16px;
	margin-right: 16px;
	box-sizing: border-box;
	cursor: pointer
}

.coupons-box .coupon-del-box .coupon-switch-box .switch-btn em {
	display: none;
	position: absolute;
	bottom: 0;
	right: 0;
	width: 0;
	height: 0;
	line-height: 54px;
	border-left-width: 20px;
	border-left-style: solid;
	border-left-color: transparent;
	border-bottom-width: 20px;
	border-bottom-style: solid;
	border-bottom-color: #f01414
}

.coupons-box .coupon-del-box .coupon-switch-box .switch-btn em i {
	color: #fff;
	position: absolute;
	bottom: -20px;
	right: 0;
	font-size: 12px
}

.coupons-box .coupon-del-box .coupon-switch-box .switch-btn.checked {
	border: 2px solid #f01414
}

.coupons-box .coupon-del-box .coupon-switch-box .switch-btn.checked em {
	display: block
}

.coupons-box .coupon-del-box .coupon-content {
	position: relative;
	background: #f3f5f7;
	border-radius: 8px;
	padding: 24px
}

.coupons-box .coupon-del-box .coupon-content:before {
	content: "";
	display: block;
	position: absolute;
	top: -7px;
	left: 62px;
	border-left: 12px solid transparent;
	border-right: 12px solid transparent;
	border-bottom: 7px solid #f3f5f7
}

.coupons-box .coupon-del-box .coupon-content.ticket li {
	padding-top: 8px;
	box-sizing: border-box;
	width: 320px;
	background-color: #fff6f0;
	cursor: pointer;
	margin: 12px
}

.coupons-box .coupon-del-box .coupon-content.ticket li .more-del-box {
	padding: 16px 22px 24px 22px;
	width: 100%;
	box-sizing: border-box;
	background-repeat: no-repeat
}

.coupons-box .coupon-del-box .coupon-content.ticket li .price-box {
	height: 32px;
	line-height: 32px
}

.coupons-box .coupon-del-box .coupon-content.ticket li .price-box .price {
	font-size: 30px;
	margin-right: 4px
}

.coupons-box .coupon-del-box .coupon-content.ticket li .price-box .price sub {
	font-size: 24px;
	letter-spacing: -5px
}

.coupons-box .coupon-del-box .coupon-content.ticket li .price-box .use-inst {
	font-size: 12px;
	margin-top: 5px;
}

.coupons-box .coupon-del-box .coupon-content.ticket .active .price,
.coupons-box .coupon-del-box .coupon-content.ticket .active .use-inst {
	color: #fff
}

.coupons-box .coupon-del-box .coupon-content.ticket .active i {
	position: absolute;
	top: 12px;
	right: 12px;
	color: #fff;
	font-size: 24px
}

.coupons-box .coupon-del-box .coupon-content.ticket .no-coupons {
	font-size: 14px;
	color: #4d555d;
	line-height: 14px
}

.coupons-box .coupon-del-box .coupon-content.code {
	padding-left: 38px
}

.coupons-box .coupon-del-box .coupon-content.code:before {
	left: 216px
}

.coupons-box .coupon-del-box .coupon-content.code .input-box {
	position: relative;
	left: -12px;
	margin-top: 12px
}

.coupons-box .coupon-del-box .coupon-content.code .input-box .convert-input {
	background: #fff;
	border: 1px solid #9199a1;
	width: 356px;
	height: 48px;
	border-radius: 8px;
	font-size: 16px;
	font-weight: 600;
	color: #07111b;
	letter-spacing: 2px;
	line-height: 24px;
	padding: 12px 16px;
	box-sizing: border-box;
	vertical-align: middle
}

.coupons-box .coupon-del-box .coupon-content.code .input-box .convert-btn {
	display: inline-block;
	width: 124px;
	height: 48px;
	line-height: 22px;
	font-size: 16px;
	color: #fff;
	padding: 12px;
	background: #f01414;
	border-radius: 8px;
	margin-left: 24px;
	box-sizing: border-box;
	text-align: center;
	cursor: pointer
}

.coupons-box .coupon-del-box .coupon-content.code .converted-box p {
	line-height: 24px;
	font-size: 16px;
	color: #07111b;
  margin-top: 10px;
}

.coupons-box .coupon-del-box .coupon-content.code .converted-box .c_name,
.coupons-box .coupon-del-box .coupon-content.code .converted-box .code-num {
	padding-left: 8px
}

.coupons-box .coupon-del-box .coupon-content.code .converted-box .cancel-btn {
	background: #fff;
	border: 1px solid #d9dde1;
	line-height: 20px;
	padding: 2px 12px;
	text-align: center;
	border-radius: 4px;
	color: #f01414;
	font-size: 14px;
	margin-left: 16px;
	cursor: pointer
}

.coupons-box .coupon-del-box .coupon-content.code .converted-box .course-title {
	font-size: 14px;
	color: #07111b;
	font-weight: 600;
	margin-top: 12px
}

.coupons-box .coupon-del-box .coupon-content.code .converted-box .course-title .discount-cash {
	margin-left: 12px;
	color: #f01414
}

.coupons-box .coupon-del-box .coupon-content.code .error-msg {
	font-size: 14px;
	color: #f01414;
	margin-top: 8px;
	line-height: 20px;
	height: 20px
}

.coupons-box .coupon-del-box .coupon-content.code .tip {
	font-size: 14px;
	color: #93999f;
	margin-top: 8px;
	line-height: 20px
}


.coupons-box .content-box ul {
	width: 100%
}
.coupons-box .content-box .nouse-box::after,
.coupons-box .content-box .overdue-box::after,
.coupons-box .content-box .use-box::after {
  display: block;
  content: "";
  overflow: hidden;
  clear: both;
}
.coupons-box .content-box .nouse-box li,
.coupons-box .content-box .overdue-box li,
.coupons-box .content-box .use-box li {
	position: relative;
	padding: 24px 32px;
	margin-right: 16px;
	margin-bottom: 16px;
	width: 320px;
	height: 144px;
	border-radius: 8px;
	box-sizing: border-box;
	background-color: #fff;
	box-shadow: 0 8px 16px 0 rgba(7,17,27, .2);
	background-repeat: no-repeat;
	background-size: 320px 144px;
}
.coupons-box .content-box .nouse-box li.select{
  background-color: orangered;
}
.coupons-box .content-box .nouse-box li .detail-box,
.coupons-box .content-box .overdue-box li .detail-box,
.coupons-box .content-box .use-box li .detail-box {
	width: 100%;
	height: 100%
}

.coupons-box .content-box .nouse-box li .detail-box .price-box,
.coupons-box .content-box .overdue-box li .detail-box .price-box,
.coupons-box .content-box .use-box li .detail-box .price-box {
	margin-bottom: 8px;
	height: 40px;
	color: #93999f;
	line-height: 40px;
	font-weight: 700
}

.coupons-box .content-box .nouse-box li .detail-box .price-box .coupon-price,
.coupons-box .content-box .overdue-box li .detail-box .price-box .coupon-price,
.coupons-box .content-box .use-box li .detail-box .price-box .coupon-price {
	margin-right: 12px;
	font-size: 36px;
  margin-top: 5px;
}

.coupons-box .content-box .nouse-box li .detail-box .price-box .use-inst,
.coupons-box .content-box .overdue-box li .detail-box .price-box .use-inst,
.coupons-box .content-box .use-box li .detail-box .price-box .use-inst {
	font-size: 14px
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box,
.coupons-box .content-box .use-box li .detail-box .use-detail-box {
	font-size: 12px;
	color: #93999f;
	line-height: 24px
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box .use-ajust-box,
.coupons-box .content-box .use-box li .detail-box .use-detail-box .use-ajust-box {
	position: relative
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box i,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box .use-ajust-box i,
.coupons-box .content-box .use-box li .detail-box .use-detail-box .use-ajust-box i {
	position: relative;
	top: 3px;
	left: 0;
	font-size: 16px;
	color: #93999f;
	line-height: 24px;
	cursor: pointer
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box .use-course a,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box .use-ajust-box .use-course a,
.coupons-box .content-box .use-box li .detail-box .use-detail-box .use-ajust-box .use-course a {
	padding: 16px 0;
	width: 100%;
	display: block;
	font-size: 12px;
	color: #4d555d;
	line-height: 20px;
	border-bottom: 1px solid #d9dde1;
	box-sizing: border-box
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box .use-course a:hover,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box .use-ajust-box .use-course a:hover,
.coupons-box .content-box .use-box li .detail-box .use-detail-box .use-ajust-box .use-course a:hover {
	color: #07111b
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box .use-course a:last-child,
.coupons-box .content-box .overdue-box li .detail-box .use-detail-box .use-ajust-box .use-course a:last-child,
.coupons-box .content-box .use-box li .detail-box .use-detail-box .use-ajust-box .use-course a:last-child {
	border-bottom: none
}

.coupons-box .content-box li {
	background-image: url(/src/assets/coupons_bg.png)
}

.coupons-box .content-box .nouse-box li .detail-box .price-box .coupon-price {
	color: #f01414
}

.coupons-box .content-box .nouse-box li .detail-box .price-box .use-inst {
	color: #f01414
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box {
	color: #07111b
}

.coupons-box .content-box .nouse-box li .detail-box .use-detail-box .use-ajust-box i {
	color: #4d555d
}

.coupons-box .content-box .nouse-box li.wait-use {
	background-image: url(/src/assets/coupon_start_bg.png)
}

.coupons-box .content-box .use-box li {
	background-image: url(/src/assets/coupons_used_bg.png)
}

.coupons-box .content-box .use-box li.useing {
	background-image: url(/src/assets/coupon_useing_bg.png)
}

.coupons-box .content-box .overdue-box li {
	background-image: url(/src/assets/coupons_overdue.png)
}

.tip-box ol {
	margin-top: 16px;
	width: 100%;
	list-style: decimal;
	margin-left: 14px;
	box-sizing: border-box
}

.tip-box ol li {
	font-size: 12px
}

.pay-box {
	margin-top: 36px;
	position: relative
}

.pay-box::after,
.goods-total-price-box::after,
.package-discount-box::after,
.pay-price-box::after,
.coupons-discount-box::after{
  display: block;
  content: "";
  clear: both;
  overflow: hidden;
}

.pay-box .rw {
	width: 140px;
	box-sizing: border-box;
	text-align: right
}

.pay-box .bargain-discount-box,.pay-box .coupons-discount-box,.pay-box .goods-total-price-box,.pay-box .package-discount-box,.pay-box .redpackage-discount-box,.pay-box .student-discount-box {
	margin-bottom: 12px;
	line-height: 26px
}

.pay-box .bargain-discount-box .price-num,.pay-box .coupons-discount-box .price-num,.pay-box .goods-total-price-box .price-num,.pay-box .package-discount-box .price-num,.pay-box .redpackage-discount-box .price-num,.pay-box .student-discount-box .price-num {
	position: relative;
	font-size: 14px;
	color: #07111b
}

.pay-box .bargain-discount-box .price-text,.pay-box .coupons-discount-box .price-text,.pay-box .goods-total-price-box .price-text,.pay-box .package-discount-box .price-text,.pay-box .redpackage-discount-box .price-text,.pay-box .student-discount-box .price-text {
	text-align: right;
	font-size: 14px;
	color: #07111b
}

.pay-box .bargain-discount-box .price-text span,.pay-box .coupons-discount-box .price-text span,.pay-box .goods-total-price-box .price-text span,.pay-box .package-discount-box .price-text span,.pay-box .redpackage-discount-box .price-text span,.pay-box .student-discount-box .price-text span {
	margin-left: 4px;
	margin-right: 4px
}

.pay-box .pay-add-sign {
	text-align: right;
	position: absolute;
	top: -10px
}

.pay-box .pay-add-sign li {
	float: left;
	padding: 0 12px;
	height: 26px;
	line-height: 26px;
	border: 1px solid #f01414;
	border-radius: 18px;
	font-size: 12px;
	color: #f01414;
	margin-right: 15px
}

.pay-box .pay-add-sign li.drawback {
	position: relative
}

.pay-box .pay-add-sign li.drawback .imv2-ques {
	position: absolute;
	top: -4px;
	right: -2px;
	background: #fff;
	color: #d7dbdf;
	font-size: 14px;
	display: inline-block;
	width: 14px;
	height: 14px;
	cursor: pointer
}

.pay-box .pay-add-sign li.drawback .imv2-ques:hover {
	color: #f20d0d
}

.pay-box .pay-add-sign a.checkbackbtn {
	display: none;
	color: #fff;
	font-size: 12px;
	text-align: center;
	border-radius: 8px;
	vertical-align: top;
	position: absolute;
	left: 100%;
	top: -12px;
	background: rgba(28,31,33,.25);
	width: 100px;
	height: 26px;
	line-height: 26px;
	margin-left: 8px
}

.pay-box .pay-add-sign a.checkbackbtn i.arrow {
	width: 0;
	height: 0;
	border-top: 5px solid transparent;
	border-right: 5px solid;
	border-bottom: 5px solid transparent;
	position: absolute;
	left: -5px;
	top: 8px;
	border-right-color: rgba(28,31,33,.25)
}

.pay-box .pay-price-box {
	color: #07111b
}

.pay-box .pay-price-box .price {
	position: relative;
	color: #f01414;
	font-size: 24px;
	font-weight: 700;
  line-height: 36px;
  height: 36px;
}
.pay-box .pay-price-box .price-text{
  line-height: 36px;
  height: 36px;
}
.pay-box .pay-price-box .price span {
	float: none;
	font-weight: 700
}

.pay-box .pay-account {
	font-size: 12px;
	color: #93999f;
	line-height: 24px;
	margin-bottom: 20px;
	margin-top: 15px
}

.pay-box .submit-btn {
	padding: 0;
	width: 140px;
	height: 40px;
	margin-top: 12px;
	text-align: center;
	font-size: 14px;
	line-height: 40px;
	border-radius: 24px
}

.pay-box .disabled {
	background: #ccc;
	cursor: not-allowed;
	border: none
}

.pay-box .presale-wrap {
	text-align: right
}

.pay-box .presale-wrap .submit-btn {
	margin-top: 24px
}

.pay-box .presale-box {
	display: inline-block;
	font-size: 0;
	text-align: left
}

.pay-box .presale-box .step {
	width: 213px;
	padding-bottom: 10px;
	position: relative
}

.pay-box .presale-box .step .title {
	font-size: 14px;
	color: #07111b;
	line-height: 26px
}

.pay-box .presale-box .step .title .price {
	color: #93999f;
	float: right
}

.pay-box .presale-box .step .title .price.active {
	color: #f01414
}

.pay-box .presale-box .step .desc {
	font-size: 12px;
	color: #93999f;
	line-height: 16px
}

.pay-box .presale-box .step:nth-child(3) .price {
	color: #f01414;
	font-size: 24px;
	font-weight: 700
}

.pay-box .presale-box .step .step-line {
	position: absolute;
	top: 8px;
	left: -16px;
	width: 9px;
	display: flex;
	flex-direction: column;
	align-items: center
}

.pay-box .presale-box .step .step-line .circle {
	width: 9px;
	height: 9px;
	border-radius: 50%;
	background: rgba(147,153,159,.3)
}

.pay-box .presale-box .step .step-line .circle.active {
	background: #f01414
}

.pay-box .presale-box .step .step-line .line {
	height: 43px;
	border-left: 1px dashed rgba(147,153,159,.3)
}

.pay-box .presale-box .step .step-line .line.short {
	height: 27px
}

.pay-box.fixed {
	position: fixed;
	bottom: 0;
	left: 0;
	width: 100%;
	height: 80px;
	line-height: 80px;
	background-color: #fff;
	z-index: 300;
	box-shadow: 10px -2px 12px rgba(7,17,27,.2);
  padding-top: 10px;
}

.pay-box.fixed .row-bottom {
	max-width: 1500px;
	position: relative;
	margin: 0 auto;
}

.pay-box.fixed .row-bottom .row {
	float: left
}

.pay-box.fixed .row-bottom .bargain-discount-box,.pay-box.fixed .row-bottom .coupons-discount-box,.pay-box.fixed .row-bottom .js-total-hide,.pay-box.fixed .row-bottom .package-discount-box {
	display: none
}

.pay-box.fixed .bargain-discount-box,.pay-box.fixed .coupons-discount-box,.pay-box.fixed .goods-total-price-box,.pay-box.fixed .package-discount-box,.pay-box.fixed .pay-add-sign,.pay-box.fixed .pay-price-box,.pay-box.fixed .redpackage-discount-box {
	float: left;
	margin-bottom: 0
}

.pay-box.fixed .coupons-discount-box,.pay-box.fixed .package-discount-box,.pay-box.fixed .redpackage-discount-box {
	margin-left: 20px
}

.pay-box.fixed .goods-total-price-box {
	width: auto
}

.pay-box.fixed .rw {
	text-align: left;
	width: auto
}

.pay-box.fixed .price,.pay-box.fixed .price-num,.pay-box.fixed .price-text {
	line-height: 80px
}

.pay-box.fixed .pay-add-sign {
	position: static!important;
	margin-left: 20px
}

.pay-box.fixed .pay-add-sign li {
	float: left;
	padding: 0 12px;
	height: 26px;
	line-height: 26px;
	border: 1px solid #f01414;
	border-radius: 18px;
	font-size: 12px;
	color: #f01414;
	margin: 27px 20px 27px 0
}

.pay-box.fixed .pay-price-box {
	width: auto;
	margin-left: 20px
}

.pay-box.fixed .submit-btn {
	margin-top: 16px;
	width: 148px;
	height: 48px;
	line-height: 48px;
	font-size: 16px;
	border-radius: 24px
}

.pay-box.fixed .presale-wrap {
	float: left;
	text-align: left
}

.pay-box.fixed .presale-wrap .presale-box {
	height: 80px;
	display: flex;
	align-items: center
}

.pay-box.fixed .presale-wrap .presale-box .step {
	padding-right: 38px;
	padding-bottom: 0;
	width: auto;
	min-width: 118px;
	height: 45px
}

.pay-box.fixed .presale-wrap .presale-box .step:nth-child(3) {
	height: auto
}

.pay-box.fixed .presale-wrap .presale-box .step .title {
	float: none;
	background: #fff
}

.pay-box.fixed .presale-wrap .presale-box .step .title .price {
	line-height: 26px;
	float: none
}

.pay-box.fixed .presale-wrap .presale-box .step .step-line {
	flex-direction: row;
	width: 100%;
	left: -14px
}

.pay-box.fixed .presale-wrap .presale-box .step .step-line .line {
	border-left: none;
	border-top: 1px dashed rgba(147,153,159,.3);
	width: 30px;
	height: 1px;
	position: absolute;
	right: 5px
}

.pay-box.fixed .presale-wrap .presale-box .step .step-line .circle:nth-child(3) {
	position: absolute;
	right: -10px
}

.btn {
  position: relative;
  display: inline-block;
  margin-bottom: 0;
  text-align: center;
  vertical-align: middle;
  touch-action: manipulation;
  text-decoration: none;
  box-sizing: border-box;
  background-image: none;
  -webkit-appearance: none;
  white-space: nowrap;
  outline: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  border-style: solid;
  border-width: 1px;
  cursor: pointer;
  transition: all .3s;
  color: #545c63;
  background-color: transparent;
  border-color: #9199a1;
  opacity: 1;
  padding: 7px 16px;
  font-size: 14px;
  line-height: 1.42857143;
  border-radius: 18px;
}

.btn-red {
  border-style: solid;
  border-width: 1px;
  cursor: pointer;
  -moz-transition: all .3s;
  transition: all .3s;
  color: #fff;
  background-color: #f20d0d;
  border-color: #f20d0d;
  opacity: 1;
}
.btn-red:hover {
  color: #fff;
  border-color: #c20a0a;
  background: #c20a0a;
  opacity: 1;
}
.pay-type {
  margin-top: 28px;
  margin-left: 12px;
}
.pay-type .title {
  margin-top: 28px;
}
.pay-type .list {
  padding-top: 20px;
}

.pay-type .list img {
  margin-right: 10px;
}
</style>
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 客户端展示下单结算页面"
git push
```



## 展示购物车勾选商品列表

### 服务端实现购物车勾选商品列表的api接口

`cart/views`，视图，代码：

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course


# .... 中间代码省略

class CartOrderAPIView(APIView):
    """购物车确认下单接口"""
    # 保证用户必须是登录状态才能调用当前视图
    permission_classes = [IsAuthenticated]

    def get(self,request):
        """获取勾选商品列表"""
        # 查询购物车中的商品课程ID列表
        user_id = request.user.id
        redis = get_redis_connection("cart")
        cart_hash = redis.hgetall(f"cart_{user_id}")
        """
        cart_hash = {
            # b'商品课程ID': b'勾选状态', 
            b'2': b'1', 
            b'4': b'1', 
            b'5': b'1'
        }
        """
        if len(cart_hash) < 1:
            return Response({"errmsg": "购物车没有任何商品。"}, status=status.HTTP_204_NO_CONTENT)

        # 把redis中的购物车勾选课程ID信息转换成普通列表
        cart_list = [int(course_id.decode()) for course_id, selected in cart_hash.items() if selected == b'1']

        course_list = Course.objects.filter(pk__in=cart_list, is_deleted=False, is_show=True).all()

        # 把course_list进行遍历，提取课程中的信息组成列表
        data = []
        for course in course_list:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_cover": course.course_cover.url,
                "price": float(course.price),
                "discount": course.discount,
                "course_type": course.get_course_type_display(),
            })

        # 返回客户端
        return Response({"errmsg": "ok！", "cart": data})

```

`cart/urls.py`，路由，代码：

```python
from django.urls import path
from . import views
urlpatterns = [
    path("", views.CartAPIView.as_view()),
    path("order/", views.CartOrderAPIView.as_view()),
]

```



### 客户端获取购物车勾选商品的数据

`api/cart.js`，代码：

```javascript
import http from "../utils/http";
import {reactive, ref} from "vue"

const cart = reactive({
    // ... 中间代码省略
    select_course_list: [], // 购物车中被勾选的商品磕碜列表
    // ... 中间代码省略
    get_select_course(token){
        // 获取购物车中被勾选的商品列表
        return http.get("/cart/order/", {
            headers:{
                Authorization: "jwt " + token,
            }
        })
    }
})

export default cart;
```

`api/order.js`，代码：

```javascript
import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
  total_price: 0,      // 勾选商品的总价格
  use_coupon: false,   // 用户是否使用优惠
  discount_type: 0,    // 0表示优惠券，1表示积分
  coupon_list:[1,2,3], // 用户拥有的可用优惠券列表
  select: -1,          // 当前用户选中的优惠券下标，-1表示没有选择
  credit: 0,           // 当前用户选择抵扣的积分，0表示没有使用积分
  fixed: true,         // 底部订单总价是否固定浮动
  pay_type: 0,         // 支付方式
})

export default order;
```

`views/Order.vue`，代码：

```vue
<template>
  <div class="cart">
    <Header/>
    <div class="cart-main">
      <div class="cart-header">
        <div class="cart-header-warp">
          <div class="cart-title left">
            <h1 class="left">确认订单</h1>
          </div>
          <div class="right">
            <div class="">
              <span class="left"><router-link class="myorder-history" to="/cart">返回购物车</router-link></span>
            </div>
          </div>
        </div>
      </div>
      <div class="cart-body" id="cartBody">
        <div class="cart-body-title"><p class="item-1 l">课程信息</p></div>
        <div class="cart-body-table">
          <div class="item" v-for="course_info in cart.select_course_list">
              <div class="item-2">
                  <router-link :to="`/project/${course_info.id}`" class="img-box l"><img :src="course_info.course_cover"></router-link>
                  <dl class="l has-package">
                    <dt>【{{course_info.course_type}}】{{course_info.name}} </dt>
                    <p class="package-item" v-if="course_info.discount.type">{{course_info.discount.type}}</p>
                  </dl>
              </div>
              <div class="item-3">
                  <div class="price">
                      <p class="discount-price" v-if="course_info.discount.price>=0"><em>￥</em><span>{{course_info.discount.price.toFixed(2)}}</span></p>
                      <p :class="{'original-price': course_info.discount.price>=0}"><em>￥</em><span>{{course_info.price.toFixed(2)}}</span></p>
                  </div>
              </div>
          </div>
        </div>
        <div class="coupons-box">
          <div class="coupon-title-box">
            <p class="coupon-title">
              使用优惠券/积分
                <span v-if="order.use_coupon" @click="order.use_coupon=!order.use_coupon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-394d1fd8=""><path fill="currentColor" d="M831.872 340.864 512 652.672 192.128 340.864a30.592 30.592 0 0 0-42.752 0 29.12 29.12 0 0 0 0 41.6L489.664 714.24a32 32 0 0 0 44.672 0l340.288-331.712a29.12 29.12 0 0 0 0-41.728 30.592 30.592 0 0 0-42.752 0z"></path></svg></span>
                <span v-else @click="order.use_coupon=!order.use_coupon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-394d1fd8=""><path fill="currentColor" d="m488.832 344.32-339.84 356.672a32 32 0 0 0 0 44.16l.384.384a29.44 29.44 0 0 0 42.688 0l320-335.872 319.872 335.872a29.44 29.44 0 0 0 42.688 0l.384-.384a32 32 0 0 0 0-44.16L535.168 344.32a32 32 0 0 0-46.336 0z"></path></svg></span>
<!--                <i :class="order.use_coupon?'el-icon-arrow-up':'el-icon-arrow-down'" @click="order.use_coupon=!order.use_coupon"></i>-->
            </p>
          </div>
          <transition name="el-zoom-in-top">
          <div class="coupon-del-box" v-if="order.use_coupon">
            <div class="coupon-switch-box">
              <div class="switch-btn ticket" :class="{'checked': order.discount_type===0}" @click="order.discount_type=0">优惠券 (4)<em><i class="imv2-check"></i></em></div>
              <div class="switch-btn code" :class="{'checked': order.discount_type===1}" @click="order.discount_type=1">积分<em><i class="imv2-check"></i></em></div>
            </div>
            <div class="coupon-content ticket" v-if="order.discount_type===0">
              <p class="no-coupons" v-if="order.coupon_list.length<1">暂无可用优惠券</p>
              <div class="coupons-box" v-else>
               <div class="content-box">
                <ul class="nouse-box">
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l select">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l wait-use">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l wait-use">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
                <ul class="use-box">
                 <li class="l useing">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
                <ul class="overdue-box">
                 <li class="l useing">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥100 </p>
                    <p class="use-inst l">满499可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                 <li class="l">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l"> ￥248 </p>
                    <p class="use-inst l">满999可用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：全部实战课程</div>
                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>
                   </div>
                  </div>
                 </li>
                </ul>
               </div>
              </div>
            </div>
            <div class="coupon-content code" v-else>
                <div class="input-box">
                  <el-input-number placeholder="10积分=1元" v-model="order.credit" :step="1" :min="0" :max="1000"></el-input-number>
                  <a class="convert-btn">兑换</a>
                </div>
                <div class="converted-box">
                  <p>使用积分:<span class="code-num">200</span></p>
                  <p class="course-title">课程:<span class="c_name">3天JavaScript入门</span>
                    <span class="discount-cash">100积分抵扣:<em>10</em>元</span>
                  </p>
                  <p class="course-title">课程:<span class="c_name">3天JavaScript入门</span>
                    <span class="discount-cash">100积分抵扣:<em>10</em>元</span>
                  </p>
                </div>
                <p class="error-msg">本次订单最多可以使用1000积分，您当前拥有200积分。(10积分=1元)</p>
                <p class="tip">说明：每笔订单只能使用一次积分，并只有在部分允许使用积分兑换的课程中才能使用。</p>
              </div>
          </div>
          </transition>
        </div>
        <div class="pay-type">
          <p class="title">选择支付方式</p>
          <div class="list">
            <img :src="order.pay_type==0?'/src/assets/alipay2.png':'/src/assets/alipay1.png'" @click="order.pay_type=0" alt="支付宝">
            <img :src="order.pay_type==1?'/src/assets/wechat2.png':'/src/assets/wechat1.png'" @click="order.pay_type=1" alt="微信">
            <img :src="order.pay_type==2?'/src/assets/yue2.png':'/src/assets/yue1.png'"  @click="order.pay_type=2" alt="余额">
          </div>
        </div>
        <div class="pay-box" :class="{fixed:order.fixed}">
				  <div class="row-bottom">
            <div class="row">
              <div class="goods-total-price-box">
                <p class="r rw price-num"><em>￥</em><span>1811.00</span></p>
                <p class="r price-text"><span>共<span>5</span>件商品，</span>商品总金额：</p>
              </div>
            </div>
            <div class="coupons-discount-box">
              <p class="r rw price-num">-<em>￥</em><span>60.00</span></p>
              <p class="r price-text">优惠券/积分抵扣：</p>
            </div>
            <div class="pay-price-box clearfix">
              <p class="r rw price"><em>￥</em><span id="js-pay-price">1751.00</span></p>
              <p class="r price-text">应付：</p>
            </div>
            <span class="r btn btn-red submit-btn">提交订单</span>
					</div>
          <div class="pay-add-sign">
            <ul class="clearfix">
              <li>支持花呗</li>
              <li>可开发票</li>
              <li class="drawback">7天可退款</li>
            </ul>
          </div>
	      </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>
```

```vue
<script setup>
import {reactive,watch} from "vue"
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {useStore} from "vuex";
import cart from "../api/cart"
import order from "../api/order";

// let store = useStore()

const get_select_course = ()=>{
    // 获取购物车中的勾选商品列表
    let token = sessionStorage.token || localStorage.token;
    cart.get_select_course(token).then(response=>{
        cart.select_course_list = response.data.cart
    })
}

get_select_course();


// 监听用户选择的支付方式
watch(
    ()=>order.pay_type,
    ()=>{
      console.log(order.pay_type)
    }
)

// 底部订单总价信息固定浮动效果
window.onscroll = ()=>{
  let cart_body_table = document.querySelector(".cart-body-table")
  let offsetY = window.scrollY
  let maxY = cart_body_table.offsetTop+cart_body_table.offsetHeight
  order.fixed = offsetY < maxY
}
</script>
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 确认下单页面中展示购物车勾选商品列表"
git push
```



## 订单生成

### 创建订单子应用

完成了勾选商品列表展示以后，因为优惠券或积分属于增值业务，所以可以先把优惠券功能和积分功能延后处理，先完成主流程中的订单生成功能。同时，为了方便以后项目的代码管理和维护，我们再次创建子应用orders来完成接下来的订单功能。

```bash
# 确认前面功能已经开发完整，review代码结束，向公司申请合并分支，开发合并分支
git checkout master
git merge feature/cart
# 查看线上本地所有的分支列表，可以看到本地的feature/user分支已经删除，但是线上的依然存在。
git branch --all
git branch -d feature/cart
# 本地删除了分支以后，线上分支也要同步一下。
git push origin --delete feature/cart
# 因为属于一个较大功能的开发合并，往往项目中都会打一个标签
git tag v0.0.4
# 提交标签版本
git push --tag
# git push origin v0.0.4

# 后续的功能属于购物流程里面的订单生成部分了
git checkout -b feature/order

# 创建订单子应用
python ../../manage.py startapp orders
```

注册子应用，`settings/dev.py`，代码：

```python
INSTALLED_APPS = [
    # 子应用
	。。。
    
    'orders',
]
```

子路由，`orders/urls.py`，代码：

```python
from django.urls import path
from . import views
urlpatterns = [
    
]
```

总路由，`luffycityapi/urls.py`，代码：

```python
    path("orders/", include("orders.urls")),
```



### 订单模型

订单相关的模型分析：

```python
订单基本信息：订单ID，支付方式，订单状态，支付时间，订单总价格，实付价格，订单标题，订单号，用户ID等等
订单项详情(订单与商品的关系）：商品ID，商品原价、商品实价，优惠方式，订单ID等等

用户课程（用户与课程的关系）：用户ID，课程ID，学习总时长等等
用户学习课程的进度跟踪记录（用户与课时的关系）：用户ID，课时ID，课程ID，章节ID，学习进度（视频进度），学习时间等等

优惠券：优惠券标题、优惠券面额、优惠券优惠方式、优惠类型、领取方式（用户领取，系统发放）、起用时间、过期时间等等
用户的优惠券（用户与优惠券的关系）:  用户ID，优惠券ID，领取时间等等。（我们采用redis来记录）
优惠券的使用记录（用户的优惠券与订单的关系）：用户ID，优惠券ID、使用状态、订单ID等等。
积分流水：操作方式、积分面值、用户ID、订单ID等等。
余额流水：操作方式、货币面值、用户ID、订单ID等等。
```

为什么有订单号？

```python
原因是支付平台需要记录每一个商家的资金流水，所以需要我们这边提供一个足够复杂的流水号和支付平台保持一致。
所以订单号是支付平台那边强制要求在支付时提供给平台的。用于对账。
```

`orders/models.py`，订单模型，代码：

```python
from model import BaseModel,models
from users.models import User
from courses.models import Course
# Create your models here.


class Order(BaseModel):
    """订单基本信息模型"""
    status_choices = (
        # 模型对象.<字段名>                   获取元组的第一个成员
        # 模型对象.get_<字段名>_display()     获取元组的第二个成员
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '超时取消'),
    )
    pay_choices = (
        (0, '支付宝'),
        (1, '微信'),
        (2, '余额'),
    )

    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="订单总价")
    real_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="实付金额")
    order_number = models.CharField(max_length=64, verbose_name="订单号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    pay_type = models.SmallIntegerField(choices=pay_choices, default=1, verbose_name="支付方式")
    order_desc = models.TextField(null=True, blank=True, max_length=500, verbose_name="订单描述")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="下单用户")

    class Meta:
        db_table = "ly_order"
        verbose_name = "订单记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.name, self.total_price, self.real_price)


class OrderDetail(BaseModel):
    """
    订单详情
    """
    order = models.ForeignKey(Order, related_name='order_courses', on_delete=models.CASCADE, db_constraint=False, verbose_name="订单")
    course = models.ForeignKey(Course, related_name='course_orders', on_delete=models.CASCADE, db_constraint=False, verbose_name="课程")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="课程原价")
    real_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="课程实价")
    discount_name = models.CharField(max_length=120,default="",verbose_name="优惠类型")

    class Meta:
        db_table = "ly_order_course"
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.course.name

```

数据迁移：

```python
cd ../../
python manage.py makemigrations
python manage.py migrate
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature：订单子应用创建以及订单信息和订单项模型的创建"
git push --set-upstream origin feature/order
```





### 把订单子应用相关的模型注册到admin管理站点

`orders/admin.py`，代码：

```python
from django.contrib import admin
from .models import Order, OrderDetail


# class OrderDetailInLine(admin.StackedInline):
class OrderDetailInLine(admin.TabularInline):
    """订单项的内嵌类"""
    model = OrderDetail
    fields = ["course", "price", "real_price", "discount_name"]
    # readonly_fields = ["discount_name"]


class OrderModelAdmin(admin.ModelAdmin):
    """订单信息的模型管理器"""
    list_display = ["id","order_number","user","total_price","total_price","order_status"]
    inlines = [OrderDetailInLine, ]


admin.site.register(Order, OrderModelAdmin)

```

`orders/apps.py`，代码：

```python
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = "订单管理"
    verbose_name_plural = verbose_name
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature：把订单子应用相关的模型注册到admin管理站点"
git push origin feature/order
```



### 服务端提供创建订单的api接口

`orders/views.py`，代码：

```python
from rest_framework.generics import CreateAPIView
from .models import Order
from .serializers import OrderModelSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class OrderCreateAPIView(CreateAPIView):
    """创建订单"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer

```

子路由，`orders/urls.py`，代码：

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrderCreateAPIView.as_view()),
]
```

序列化器，`orders/serializers.py`，代码：

```python
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from .models import Order, OrderDetail, Course


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user_id = self.context["request"].user.id  # 1

        # 创建订单记录
        order = Order.objects.create(
            name="购买课程",  # 订单标题
            user_id=user_id,  # 当前下单的用户ID
            # order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%08d" % user_id) + "%08d" % random.randint(1,99999999) # 基于随机数生成唯一订单号
            order_number=datetime.now().strftime("%Y%m%d") + ("%08d" % user_id) + "%08d" % redis.incr("order_number"), # 基于redis生成分布式唯一订单号
            pay_type=validated_data.get("pay_type"),  # 支付方式
        )

        # 记录本次下单的商品列表
        cart_hash = redis.hgetall(f"cart_{user_id}")
        if len(cart_hash) < 1:
            raise serializers.ValidationError(detail="购物车没有要下单的商品")

        # 提取购物车中所有勾选状态为b'1'的商品
        course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

        # 添加订单与课程的关系
        course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
        detail_list = []
        total_price = 0 # 本次订单的总价格
        real_price = 0  # 本次订单的实付总价

        for course in course_list:
            discount_price = float(course.discount.get("price", 0)) # 获取课程原价
            discount_name = course.discount.get("type", "")
            detail_list.append(OrderDetail(
                order=order,
                course=course,
                name=course.name,
                price=course.price,
                real_price=discount_price,
                discount_name=discount_name,
            ))

            # 统计订单的总价和实付总价
            total_price += float(course.price)
            real_price += discount_price if discount_price > 0 else float(course.price)

        # 一次性批量添加本次下单的商品记录
        OrderDetail.objects.bulk_create(detail_list)

        # 保存订单的总价格和实付价格
        order.total_price = total_price
        order.real_price = real_price
        order.save()

        # todo 支付链接地址[后面实现支付功能的时候，再做]
        order.pay_link = ""
        return order

```

生成订单时,在序列化器中要接收客户端用户的user_id

```python
用户ID在序列化器中接收到视图中的数据,那么在序列化器初始化的时候,其实有3个参数可以填写:
   1. instance 模型对象,数据模型,
   2. data     字典,客户端提交数据,
   3. context  字典,额外参数[执行上下文],如果要自定义参数,可以直接通过字典格式声明,然后到context
   
   OrderModerSerializer(instance="模型对象",data="客户端数据", context={})
    
利用序列化器初始化时提供的第三个参数就可以调用到视图类的
   context的属性          描述                       序列化器中的调用代码
       request    本次客户端的请求对象			self.context["request"]
       format     本次服务器响应的数据格式		   self.context["format"]
       view       调用当前序列化器的视图类          self.context["view"]
   
因此,我们要在序列化器中提取用户的id,代码如下:
   user_id = self.context["request"].user.id
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature：服务端提供创建订单的API接口"
git push
```



上面我们完成了订单信息的添加，但是下单不是一个数据记录而已，而是多张表记录的同时添加操作。所以针对这种多个记录或者多张表连贯进行的操作，为了保证数据的完整性和一致性以及原子性，我们要使用数据库的事务（Transaction）来完成，当然我们这个项目中不需要使用到数据库原生的事务语句，而是使用django的ORM提供的事务模块即可。

```python
事务（Transaction），是以功能或业务作为逻辑单位，把一条或多条SQL语句组成一个不可分割的操作序列来执行的数据库特性。
在完成一个整体功能时，操作到了多个表数据，或者同一个表的多条记录，如果要保证这些SQL语句操作作为一个整体保存到数据库中，那么可以使用事务(transaction)，保证这些操作作为不可分割的整体，要么一起成功，要么一起失败。

事务具有4个特性（ACID），5个隔离等级
  
  四个特性：一致性，原子性，隔离性，持久性
  # 隔离性:两个事务的隔离性，隔离性的修改可以通过数据库的配置文件mysqld.cnf进行修改，默认mysql是属于可重复级别
  五个隔离级别（从高到低）： 串行隔离，可重复读，已提交读，未提交读，没有隔离
    原子性（Atomicity）
    一致性（Consistency）
    隔离性（Isolation）[事务隔离级别->幻读，脏读, 不可重复读]
    持久性（Durability）

  在mysql中有专门的SQl语句来完成事务的操作，事务的代码操作一般有3个步骤：
     设置事务开始  begin;
	 事务的处理[mysql:增删改]
         redis.sadd()
         事务的处理[mysql:增删改]
     设置事务的回滚或者提交 rollback / commit;  # 这个事务过程中，事务无法对mysql数据库以外的其他类型的数据库操作进行管理和回滚
mysql中底层的事务是如何实现事务的回滚操作：undo.log重做日志
在ORM框架一般都会实现了事务操作封装，所以我们可以直接使用ORM框架即可完成事务的操作
```



django框架本身就提供了2种事务操作的写法，主要都是通过 django.db.transaction模块完成的。

启用事务写法1：基于**装饰器**对函数或方法进行事务管理：

```python
from django.db import transaction
from rest_framework.views import APIView
class OrderAPIView(APIView):
    @transaction.atomic          # 开启事务，当函数/方法执行完成以后，自动提交事务
    def post(self,request):      # 不一定是视图方法，也可以是其他函数方法。
        ....  # 在整个函数或者方法中，进行的所有SQL数据写操作[增删改]，都属于同一个事务操作
```

启用事务写法2，基于**with上下文管理器**进行事务管理：

```python
from django.db import transaction
from rest_framework.views import APIView
class OrderAPIView(APIView):
    def post(self,request):
        .... # 事务以外的，其他的SQL数据操作
        with transation.atomic(): # 开启事务，当with语句执行完成以后，自动提交事务
            # 数据库操作【DML增删改】
            
        .... # with语句以外的其他的SQL数据操作，无法被上面事务管理
```

在使用事务过程中， 有时候会出现异常，当出现异常时我们需要回滚事务。

```python
from django.db import transaction
from rest_framework.generics import CreateAPIView
class OrderCreateAPIView(CreateAPIView):
    def post(self,request):
        ....
        with transaction.atomic():
            # 1、设置事务回滚的标记点【一个事物中可以设置多个回滚标记】
            sid1 = transaction.savepoint()
            try:
                .... # 增删改等数据库操作
                ....
            except:
                transaction.savepoint_rallback(sid1)

        .... # 数据库操作，注意，如果这里被执行，因为没有在with里面，所以是不会被上面的事务操作影响。
```

django的事务操作是支持嵌套事务的，但是mysql本身不支持嵌套事务。

```python
from django.db import transaction
from rest_framework.generics import CreateAPIView
class OrderCreateAPIView(CreateAPIView):
    def post(self,request):
        ....
        with transaction.atomic():
            # 1、设置事务回滚的标记点【一个事物中可以设置多个回滚标记】
            sid1 = transaction.savepoint()

            try:
                .... # 增删改等数据库操作
                ....
                with transaction.atomic():
                    # 2. 设置回滚点
                    sid2 = transaction.savepoint()
                    try:
                        .... # 其他内部数据库处理
                        ....
                    except:
                        transaction.savepoint_rallback(sid2)
            except:
                transaction.savepoint_rallback(sid1)
            
        .... # 数据库操作，注意，如果这里被执行，因为没有在with里面，所以是不会被上面的事务操作影响。
```



### 使用Django的ORM提供的mysql事务操作保证下单过程中的数据原子性

`orders/serializers.py`，代码：

```python
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from django.db import transaction
from .models import Order, OrderDetail, Course
import logging

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user_id = self.context["request"].user.id  # 1

        # 开启事务操作，保证下单过程中的所有数据库的原子性
        with transaction.atomic():
            # 设置事务的回滚点标记
            t1 = transaction.savepoint()
            try:
                # 创建订单记录
                order = Order.objects.create(
                    name="购买课程",  # 订单标题
                    user_id=user_id,  # 当前下单的用户ID
                    # order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%08d" % user_id) + "%08d" % random.randint(1,99999999) # 基于随机数生成唯一订单号
                    order_number=datetime.now().strftime("%Y%m%d") + ("%08d" % user_id) + "%08d" % redis.incr("order_number"), # 基于redis生成分布式唯一订单号
                    pay_type=validated_data.get("pay_type"),  # 支付方式
                )

                # 记录本次下单的商品列表
                cart_hash = redis.hgetall(f"cart_{user_id}")
                if len(cart_hash) < 1:
                    raise serializers.ValidationError(detail="购物车没有要下单的商品")

                # 提取购物车中所有勾选状态为b'1'的商品
                course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

                # 添加订单与课程的关系
                course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
                detail_list = []
                total_price = 0 # 本次订单的总价格
                real_price = 0  # 本次订单的实付总价

                for course in course_list:
                    discount_price = float(course.discount.get("price", 0)) # 获取课程原价
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += discount_price if discount_price > 0 else float(course.price)

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = total_price
                order.real_price = real_price
                order.save()

                # todo 支付链接地址[后面实现支付功能的时候，再做]
                order.pay_link = ""
                return order
            except Exception as e:
                # 1. 记录日志
                logger.error(f"订单创建失败：{e}")
                # 2. 事务回滚
                transaction.savepoint_rollback(t1)
                # 3. 抛出异常，通知视图返回错误提示
                raise serializers.ValidationError(detail="订单创建失败！")

```

购物车中选中的商品被记录到了订单中，那么购物车中原来的勾选商品是否要删除？

如果不删除，那么订单中的商品与购物车中就重复了，所以要删除，购物车中只需要保留没有勾选过的商品。

`orders/serializers.py`，代码：

```python
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from django.db import transaction
from .models import Order, OrderDetail, Course
import logging

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user_id = self.context["request"].user.id  # 1

        # 开启事务操作，保证下单过程中的所有数据库的原子性
        with transaction.atomic():
            # 设置事务的回滚点标记
            t1 = transaction.savepoint()
            try:
                # 创建订单记录
                order = Order.objects.create(
                    name="购买课程",  # 订单标题
                    user_id=user_id,  # 当前下单的用户ID
                    # order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%08d" % user_id) + "%08d" % random.randint(1,99999999) # 基于随机数生成唯一订单号
                    order_number=datetime.now().strftime("%Y%m%d") + ("%08d" % user_id) + "%08d" % redis.incr("order_number"), # 基于redis生成分布式唯一订单号
                    pay_type=validated_data.get("pay_type"),  # 支付方式
                )

                # 记录本次下单的商品列表
                cart_hash = redis.hgetall(f"cart_{user_id}")
                if len(cart_hash) < 1:
                    raise serializers.ValidationError(detail="购物车没有要下单的商品")

                # 提取购物车中所有勾选状态为b'1'的商品
                course_id_list = [int(key.decode()) for key, value in cart_hash.items() if value == b'1']

                # 添加订单与课程的关系
                course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
                detail_list = []
                total_price = 0 # 本次订单的总价格
                real_price = 0  # 本次订单的实付总价

                for course in course_list:
                    discount_price = float(course.discount.get("price", 0)) # 获取课程原价
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += discount_price if discount_price > 0 else float(course.price)

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = total_price
                order.real_price = real_price
                order.save()

                # todo 支付链接地址[后面实现支付功能的时候，再做]
                order.pay_link = ""

                # 删除购物车中被勾选的商品，保留没有被勾选的商品信息
                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                # 删除原来的购物车
                pipe.delete(f"cart_{user_id}")
                # 重新把未勾选的商品记录到购物车中
                pipe.hmset(f"cart_{user_id}", cart)  # hset 在新版本的redis中实际上hmset已经被废弃了，改用hset替代hmset
                pipe.execute()

                return order
            except Exception as e:
                # 1. 记录日志
                logger.error(f"订单创建失败：{e}")
                # 2. 事务回滚
                transaction.savepoint_rollback(t1)
                # 3. 抛出异常，通知视图返回错误提示
                raise serializers.ValidationError(detail="订单创建失败！")

```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature：服务端基于事务保证订单生成操作的原子性"
git push
```



### 客户端请求生成订单

`api/order.js`，代码：

```javascript
import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
  total_price: 0,      // 勾选商品的总价格
  use_coupon: false,   // 用户是否使用优惠
  discount_type: 0,    // 0表示优惠券，1表示积分
  coupon_list:[1,2,3], // 用户拥有的可用优惠券列表
  select: -1,          // 当前用户选中的优惠券下标，-1表示没有选择
  credit: 0,           // 当前用户选择抵扣的积分，0表示没有使用积分
  fixed: true,         // 底部订单总价是否固定浮动
  pay_type: 0,         // 支付方式
  create_order(token){
    // 生成订单
    return http.post("/orders/",{
        pay_type: this.pay_type
    },{
        headers:{
            Authorization: "jwt " + token,
        }
    })
  }
})

export default order;
```

`views/Order.vue`，代码：

```vue
<span class="r btn btn-red submit-btn" @click="commit_order">提交订单</span>
```

```vue
<script setup>
import {reactive,watch} from "vue"
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {useStore} from "vuex";
import cart from "../api/cart"
import order from "../api/order";
import {ElMessage} from "element-plus";
import router from "../router";

// let store = useStore()

const get_select_course = ()=>{
    // 获取购物车中的勾选商品列表
    let token = sessionStorage.token || localStorage.token;
    cart.get_select_course(token).then(response=>{
        cart.select_course_list = response.data.cart
        if(response.data.cart.length === 0){
          ElMessage.error("当前购物车中没有下单的商品！请重新重新选择购物车中要购买的商品~");
          router.back();
        }
    }).catch(error=>{
    if(error?.response?.status===400){
      ElMessage.error("登录超时！请重新登录后再继续操作~");
    }
  })
}

get_select_course();


const commit_order = ()=>{
    // 生成订单
    let token = sessionStorage.token || localStorage.token;
    order.create_order(token).then(response=>{
    console.log(response.data.order_number)  // todo 订单号
    console.log(response.data.pay_link)      // todo 支付链接
    // 成功提示
    ElMessage.success("下单成功！马上跳转到支付页面，请稍候~")
    // 扣除掉被下单的商品数量，更新购物车中的商品数量
    store.commit("set_cart_total", store.state.cart_total - cart.select_course_list.length);
  }).catch(error=>{
    if(error?.response?.status===400){
          ElMessage.success("登录超时！请重新登录后再继续操作~");
    }
  })
}


// 监听用户选择的支付方式
watch(
    ()=>order.pay_type,
    ()=>{
      console.log(order.pay_type)
    }
)

// 底部订单总价信息固定浮动效果
window.onscroll = ()=>{
  let cart_body_table = document.querySelector(".cart-body-table")
  let offsetY = window.scrollY
  let maxY = cart_body_table.offsetTop+cart_body_table.offsetHeight
  order.fixed = offsetY < maxY
}
</script>
```

提交版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature：客户端请求生成订单"
git push
```

