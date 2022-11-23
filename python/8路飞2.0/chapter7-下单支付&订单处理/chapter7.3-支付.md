支付的实现一般我们开发中都是通过第三方支付平台来实现的！ 

目前国内外比较常见的第三方支付平台：

```
小额支付
1. 国内
   微信支付，支付宝，京东支付，百度钱包，贝宝[paypal中文版]
2. 国外
   apple pay，paypal[贝宝国际版]，万事达信用卡
   
大额支付
   银联支付
```



## 支付宝

### 支付宝开发平台登录

官网：https://open.alipay.com/platform/home.htm

公司以企业账号进行支付签约：https://b.alipay.com/signing/productDetailV2.htm?productId=I1011000290000001000

目前我们是作为开发者给项目测试支付功能，所以我们先采用支付平台提供的测试服务端使用测试账号进行功能测试。将来等企业账号申请支付签约通过以后，则可以直接修改代码中的配置信息，就可以在线上运营使用了。

![image-20210809091621044](assets/image-20210809091621044.png)

### 沙箱环境

- 是支付宝提供给开发者的模拟支付的环境，提供了一个测试服务器。
- 沙箱环境跟真实环境是分开的，项目上线时必须切换对应的配置服务器地址和开发者ID和密钥。
- **沙箱文档**：https://opendocs.alipay.com/support/01razc
- **沙箱接口**：[https://opendocs.alipay.com/open/200/105311#沙箱支持产品](https://opendocs.alipay.com/open/200/105311#沙箱支持产品)
- **沙箱账号**：https://openhome.alipay.com/platform/appDaily.htm?tab=info

```
真实的支付宝网关: https://openapi.alipay.com/gateway.do
沙箱的支付宝网关: https://openapi.alipaydev.com/gateway.do  
```



### 支付宝开发者文档

**电脑网站支付产品介绍**：https://opendocs.alipay.com/open/270

**电脑网站支付流程**的时序图：

![电脑网站支付流程图](assets/电脑网站支付流程图.png)

![](assets/支付流程时序图.png)



### 开发支付功能

终端下创建新的git分支，并创建新的子应用。

```bash
cd ~/Desktop/luffycity
git checkout -b feature/payments

cd luffycityapi/luffycityapi/apps
python ../../manage.py startapp payments
```

注册子应用，`settings/dev.py`，代码：

```python
INSTALLED_APPS = [
	。。。。
    'payments',
]
```

子应用路由，`payments/urls.py`，代码：

```python
from django.urls import path,re_path
from . import views
urlpatterns = [

]
```

总路由，`luffycityapi/urls.py`，代码：

```python
    path("payments/", include("payments.urls")),
```



### 配置秘钥

```
RSA2算法：非对称加密算法。一般加密的密钥是成对出现的。
私钥用于解密，自己保存，
公钥用于加密，提供给别人。
目前所有的第三方支付基本都是使用RSA2算法加密。所以要开发支付宝这种第三方支付平台的支付接口基本都有2对密钥。
支付宝密钥对：支付宝公钥，支付宝密钥。
商户（应用）密钥对：应用公钥，应用私钥。

往往我们需要从支付宝的官网上获取支付宝的公钥，把自己的应用公钥填写到支付宝官网。
```



#### 1. 生成应用的私钥和公钥

##### 支付宝公钥

获取支付宝公钥：https://openhome.alipay.com/platform/appDaily.htm?tab=info

第一次需要启用RSA2秘钥( 公钥模式 )

![image-20210928173730216](assets/image-20210928173730216.png)

点击**启用**了以后，就可以新窗口下看到支付宝提供的公钥。

![image-20210928173916579](assets/image-20210928173916579.png)

得到了公钥以后，复制保存到luffycityapi/apps/payments/keys/alipay_public_key.pem，这个pem文件一般就直接保存到当前子应用目录下的keys目录下。

内容格式如下：

```
-----BEGIN PUBLIC KEY-----
支付宝公钥信息[不能手动调整，复制下来就原样不动]
-----END PUBLIC KEY-----
```

效果如下：

![image-20210928174342691](assets/image-20210928174342691.png)



##### 应用私钥

应用的公钥和私钥，支付宝本身已经提供了。所以，我们直接复制到本地保存起来即可。

注意：我们使用的是非java语言，所以不要选错了！

![image-20220712113817599](assets/image-20220712113817599.png)

luffycityapi/apps/payments/keys/app_private_key.pem，代码：

```bash
-----BEGIN RSA PRIVATE KEY-----
应用私钥信息[不能手动调整，复制下来就原样不动]
-----END RSA PRIVATE KEY-----
```

效果如下：

![image-20210928180618251](assets/image-20210928180618251.png)

如果要保留公钥到本地将来作为备份，或者用着其他的支付方式，可以保存，但是不推荐。

luffycityapi/apps/payments/keys/app_public_key.pem，代码：

```
-----BEGIN PUBLIC KEY-----
应用公钥信息[不能手动调整，复制下来就原样不动]
-----END PUBLIC KEY-----
```

效果：

![image-20210928180832892](assets/image-20210928180832892.png)



#### 4. 使用支付宝的sdk开发支付接口

SDK：https://opendocs.alipay.com/open/54/103419

python版本的支付宝SDK文档：https://github.com/fzlee/alipay/blob/master/README.zh-hans.md

安装命令：

```
pip install python-alipay-sdk --upgrade
```

使用文档：https://github.com/fzlee/alipay/blob/master/docs/apis_new.zh-hans.md

调整原来下单的序列化器，不在序列化器中返回支付信息，而是由客户端根据订单号请求服务端生成支付信息。

`orders/serializers.py`，代码：

```python
import logging
import constants

from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from django.db import transaction
from .models import Order, OrderDetail, Course
from coupon.models import CouponLog

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "user_coupon_id", "credit"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
            "credit": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user = self.context["request"].user
        user_id = user.id

        # 判断用户如果使用了优惠券，则优惠券需要判断验证
        user_coupon_id = validated_data.get("user_coupon_id")
        # 本次下单时，用户使用的优惠券
        user_coupon = None
        if user_coupon_id != -1:
            user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user_id).first()

        # 本次下单时使用的积分数量
        use_credit = validated_data.get("credit", 0)
        if use_credit > 0 and use_credit > user.credit:
            raise serializers.ValidationError(detail="您拥有的积分不足以抵扣本次下单的积分，请重新下单！")

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

                # 用户使用优惠券或积分以后，需要在服务端计算本次使用优惠券或积分的最大优惠额度
                total_discount_price = 0    # 总优惠价格
                max_discount_course = None  # 享受最大优惠的课程

                # 本次下单最多可以抵扣的积分
                max_use_credit = 0

                for course in course_list:
                    discount_price = course.discount.get("price", None)  # 获取课程原价
                    if discount_price is not None:
                        discount_price = float(discount_price)
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=course.price if discount_price is None else discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += float(course.price if discount_price is None else discount_price)

                    # 在用户使用了优惠券，并且当前课程没有参与其他优惠活动时，找到最佳优惠课程
                    if user_coupon and discount_price is None:
                        if max_discount_course is None:
                            max_discount_course = course
                        else:
                            if course.price >= max_discount_course.price:
                                max_discount_course = course

                    # 添加每个课程的可用积分
                    if use_credit > 0 and course.credit > 0:
                        max_use_credit += course.credit

                # 在用户使用了优惠券以后，根据循环中得到的最佳优惠课程进行计算最终抵扣金额
                if user_coupon:
                    # 优惠公式
                    sale = float(user_coupon.coupon.sale[1:])
                    if user_coupon.coupon.discount == 1:
                        """减免优惠券"""
                        total_discount_price = sale
                    elif user_coupon.coupon.discount == 2:
                        """折扣优惠券"""
                        total_discount_price = float(max_discount_course.price) * (1 - sale)

                if use_credit > 0:
                    if max_use_credit < use_credit:
                        raise serializers.ValidationError(detail="本次使用的抵扣积分数额超过了限制！")

                    # 当前订单添加积分抵扣的数量
                    order.credit = use_credit
                    total_discount_price = float(use_credit / constants.CREDIT_TO_MONEY)

                    # todo 扣除用户拥有的积分，后续在订单超时未支付，则返还订单中对应数量的积分给用户。如果订单成功支付，则添加一个积分流水记录。
                    user.credit = user.credit - use_credit
                    user.save()

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = real_price
                order.real_price =  float(real_price - total_discount_price)
                order.save()

                # 删除购物车中被勾选的商品，保留没有被勾选的商品信息
                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                # 删除原来的购物车
                pipe.delete(f"cart_{user_id}")
                # 重新把未勾选的商品记录到购物车中
                if cart:
                    pipe.hmset(f"cart_{user_id}", cart)
                pipe.execute()

                # 如果有使用了优惠券，则把优惠券和当前订单进行绑定
                if user_coupon:
                    user_coupon.order = order
                    user_coupon.save()
                    # 把优惠券从redis中移除
                    redis = get_redis_connection("coupon")
                    redis.delete(f"{user_id}:{user_coupon_id}")

                return order
            except Exception as e:
                # 1. 记录日志
                logger.error(f"订单创建失败：{e}")
                # 2. 事务回滚
                transaction.savepoint_rollback(t1)
                # 3. 抛出异常，通知视图返回错误提示
                raise serializers.ValidationError(detail="订单创建失败！")

```



### 后端提供发起支付的api接口

`payments/views.py`，代码:

```python
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from orders.models import Order
from alipay import AliPay
from alipay.utils import AliPayConfig


# Create your views here.
class AlipayAPIViewSet(ViewSet):
    """支付宝接口"""

    def link(self, request, order_number):
        """生成支付宝支付链接信息"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 0:
                return Response({"message": "对不起，当前订单不能重复支付或订单已超时！"})
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在！"})

        # 读取支付宝公钥与商户私钥
        app_private_key_string = open(settings.ALIPAY["app_private_key_path"]).read()
        alipay_public_key_string = open(settings.ALIPAY["alipay_public_key_path"]).read()

        # 创建alipay SDK操作对象
        alipay = AliPay(
            appid=settings.ALIPAY["appid"],
            app_notify_url=settings.ALIPAY["notify_url"],  # 默认全局回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIPAY["sign_type"],  # RSA2
            debug=settings.ALIPAY["debug"],  # 默认 False，沙箱模式下必须设置为True
            verbose=settings.ALIPAY["verbose"],  # 输出调试数据
            config=AliPayConfig(timeout=settings.ALIPAY["timeout"])  # 可选，请求超时时间，单位：秒
        )

        # 生成支付信息
        order_string = alipay.client_api(
            "alipay.trade.page.pay",  # 接口名称
            biz_content={
                "out_trade_no": order_number,  # 订单号
                "total_amount": float(order.real_price),  # 订单金额 单位：元
                "subject": order.name,  # 订单标题
                "product_code": "FAST_INSTANT_TRADE_PAY",  # 产品码，目前只能支持 FAST_INSTANT_TRADE_PAY
            },
            return_url=settings.ALIPAY["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
            notify_url=settings.ALIPAY["notify_url"]   # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        )

        # 拼接完整的支付链接
        link = f"{settings.ALIPAY['gateway']}?{order_string}"

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })


```



#### 在配置文件中编辑支付宝的配置信息[实际的值根据自己的账号而定]

`setttins/dev.py`，代码：

```python
# 支付宝相关配置
ALIPAY = {
    # 'gateway': 'https://openapi.alipay.com/gateway.do',   # 真实网关地址
    'gateway': 'https://openapi.alipaydev.com/gateway.do',  # 沙箱网关地址
    'appid': '2016091600523592',  # 支付应用ID
    'sign_type': 'RSA2',  # 签证的加密算法
    'debug': True,  # 沙箱模式下必须设置为True
    'verbose': True,  # 是否在调试模式下输出调试数据
    'timeout': 15,  # 请求超时时间，单位：秒
    "app_private_key_path": BASE_DIR / "apps/payments/keys/app_private_key.pem",  # 应用私钥路径
    "alipay_public_key_path": BASE_DIR / "apps/payments/keys/alipay_public_key.pem",  # 支付宝公钥路径
    "return_url": "http://www.luffycity.cn:3000/alipay",  # 同步回调结果通知地址
    "notify_url": "http://api.luffycity.cn:8000/payments/alipay/notify",  # 异步回调结果通知地址
}

```

payments.urls，代码：

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
]
```

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端提供生成支付宝支付链接的api接口"
git push --set-upstream origin feature/payments
```



### 前端生成订单以后发起支付

`views/Order.vue`，代码：

```vue
<script setup>

// ... 代码省略
let store = useStore()
// ... 代码省略
const commit_order = ()=>{
    // 生成订单
    let token = sessionStorage.token || localStorage.token;
    let user_coupon_id = -1;
    if(order.select !== -1){
        user_coupon_id = order.coupon_list[order.select].user_coupon_id;
    }
    order.create_order(user_coupon_id, token).then(response=>{
        // 成功提示
        ElMessage.success("下单成功！马上跳转到支付页面，请稍候~")
        // 扣除掉被下单的商品数量，更新购物车中的商品数量
        store.commit("set_cart_total", store.state.cart_total - cart.select_course_list.length);
        // 根据订单号到服务端获取支付链接，并打开支付页面。
        order.alipay_page_pay(response.data.order_number).then(response=>{
            window.open(response.data.link,"_blank");
        })
    })
}

// ... 代码省略

</script>
```

`src/api/order.js`，代码：

```javascript
import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
    // ... 代码省略
    alipay_page_pay(order_number){
        // 获取订单的支付宝支付链接信息
        return http.get(`/payments/alipay/${order_number}`)
    }
});

export default order;
```

完成了上面的功能以后,我们就可以在沙箱环境中进行支付宝的付款了，我们会接受到支付宝界面那边通过前端js跳转回来的同步通知支付结果，跳转回到我们的客户端页面,

支付结果参数说明：https://docs.open.alipay.com/api_1/alipay.trade.page.pay

```bash
http://www.luffycity.cn:3000/alipay?charset=utf-8&out_trade_no=202207120000000100000022&method=alipay.trade.page.pay.return&total_amount=1579.00&sign=YqSmTxOPfaXV%2BTSMv8Lg1dOx71JulfaYL6Ab34LSy57Y%2BCvVAb895jPrxpqMeODxiLi65DRLLAJYK%2FQO1m6ykWuTbeQf1FpPhqTkH5LeipJ1LfPy3efj0KJFJFLVJ9pkIGs3tTD7tg%2FL9X70EVmzCxXruWtlM5pAh%2B2%2FsUVbZ4l1tMwDAt4%2FhNoPlc3jvQ07X1r7B17PPBa8Qk%2FF9PbXbIQBsoOkFa78l%2Fs5GBpLB7OTDoOCv16ijV7vTegqi9riucbJkxbk%2F%2FNR7yvLysKUkPMbkcY6uvXz9LD%2F6DQ%2BNKCz694fe0NLXgovVlhyA8l8FA9cSCYunWNELNK0MF%2FPMQ%3D%3D&trade_no=2022071222001439880503951070&auth_app_id=2016091600523592&version=1.0&app_id=2016091600523592&sign_type=RSA2&seller_id=2088102175868026&timestamp=2022-07-12+12%3A50%3A02
```



#### 支付成功的模板

提供一个接受支付结果的页面，展示支付成功的信息。

`views/AliPaySuccess.vue`,代码:

```vue
<template>
  <div class="success" v-if="order.is_show">
    <Header/>
    <div class="main">
        <div class="title">
          <i class="el-icon-chat-dot-round"></i>
          <div class="success-tips">
              <p class="tips1">您已成功购买 1 门课程！</p>
              <p class="tips2">你还可以加入QQ群 <span>747556033</span> 学习交流</p>
          </div>
        </div>
        <div class="order-info">
            <p class="info1"><b>付款时间：</b><span>2019/04/02 10:27</span></p>
            <p class="info2"><b>付款金额：</b><span >0</span></p>
            <p class="info3"><b>课程信息：</b><span><span>《Pycharm使用秘籍》</span></span></p>
        </div>
        <div class="wechat-code">
          <img src="../assets/wechat.jpg" alt="" class="er">
          <p><i class="el-icon-warning"></i>重要！微信扫码关注获得学习通知&amp;课程更新提醒！否则将严重影响学习进度和课程体验！</p>
        </div>
        <div class="study">
          <span>立即学习</span>
        </div>
    </div>
    <Footer/>
  </div>
</template>

<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {ElMessage} from "element-plus";
import order from "../api/order";

</script>
<style scoped>
.success{
  padding-top: 80px;
}
.main{
    height: 100%;
    padding-top: 25px;
    padding-bottom: 25px;
    margin: 0 auto;
    width: 1200px;
    background: #fff;
}
.main .title{
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    padding: 25px 40px;
    border-bottom: 1px solid #f2f2f2;
}
.main .title .success-tips{
    box-sizing: border-box;
}
.title img{
    vertical-align: middle;
    width: 60px;
    height: 60px;
    margin-right: 40px;
}
.title .success-tips{
    box-sizing: border-box;
}
.title .tips1{
    font-size: 22px;
    color: #000;
}
.title .tips2{
    font-size: 16px;
    color: #4a4a4a;
    letter-spacing: 0;
    text-align: center;
    margin-top: 10px;
}
.title .tips2 span{
    color: #ec6730;
}
.order-info{
    padding: 25px 48px;
    padding-bottom: 15px;
    border-bottom: 1px solid #f2f2f2;
}
.order-info p{
    display: -ms-flexbox;
    display: flex;
    margin-bottom: 10px;
    font-size: 16px;
}
.order-info p b{
  font-weight: 400;
  color: #9d9d9d;
  white-space: nowrap;
}
.wechat-code{
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    padding: 25px 40px;
    border-bottom: 1px solid #f2f2f2;
}
.wechat-code>img{
    width: 180px;
    height: 180px;
    margin-right: 15px;
}
.wechat-code p{
    font-size: 14px;
    color: #d0021b;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
}
.wechat-code p>img{
    width: 16px;
    height: 16px;
    margin-right: 10px;
}
.study{
  padding: 25px 52px;
}
.study span{
  display: block;
  width: 140px;
  height: 42px;
  text-align: center;
  line-height: 42px;
  cursor: pointer;
  background: #ffc210;
  border-radius: 6px;
  font-size: 16px;
  color: #fff;
}
.el-icon-warning{
  font-size: 22px;
  margin-right: 5px;
}
.el-icon-chat-dot-round{
  font-size: 122px;
  margin-right: 10px;
}
</style>
```

`routers/index.js`，路由代码:

```javascript
,
    {
      meta:{
        title: "支付成功",
        keepAlive: true
      },
      path: '/alipay',
      name: "PaySuccess",
      component: ()=> import("../views/AliPaySuccess.vue"),
    },
```

`src/api/order.js`，代码：

```javascript
import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
    // ... 代码省略
    // ... 代码省略
    // ... 代码省略
    course_list: [],     // 本次购买的商品课程列表
    real_price: 0,       // 付款金额
    pay_time: undefined, // 付款时间
    is_show: false,      // 是否展示支付成功的内容
    // ... 代码省略
    // ... 代码省略
    // ... 代码省略
    relay_alipay_result(query_string){
        // 把地址栏中的查询字符串(支付成功以后的同步回调通知)转发给服务端
        return http.get(`/payments/alipay/result/${query_string}`)
    }
});

export default order;
```

转发支付结果到服务端。`views/AliPaySuccess.vue`，代码：

```vue
<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {ElMessage} from "element-plus";
import order from "../api/order";

let query_string = location.search; // 获取查询字符串的支付结果参数
order.relay_alipay_result(query_string).then(response=>{
  order.is_show = true;
  order.course_list = response.data.course_list;
  order.real_price  = response.data.real_price;
  order.pay_time    = response.data.pay_time;
}).catch(error=>{
  console.log(error);
})

</script>
```

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 客户端实现发起支付并转换同步支付结果到服务端"
git push
```



### 服务端接收并处理同步通知支付结果

因为我们需要多次对支付接口进行调用，所以我们可以在缩减重复代码的情况下，对原有代码进行封装。

`luffycityapi/utils/alipaysdk.py`，代码：

```python
from django.conf import settings
from alipay import AliPay
from alipay.utils import AliPayConfig
from datetime import datetime

class AliPaySDK(AliPay):
    """支付宝接口sdk工具类"""
    def __init__(self, config=None):
        if config is None:
            self.config = settings.ALIPAY
        else:
            self.config = config

        app_private_key_string = open(self.config["app_private_key_path"]).read()
        alipay_public_key_string = open(self.config["alipay_public_key_path"]).read()
        super().__init__(
            appid=self.config["appid"],
            app_notify_url=self.config["notify_url"],  # 默认全局回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=self.config["sign_type"],  # RSA 或者 RSA2
            debug=self.config["debug"],  # 默认 False，沙箱模式下必须设置为True
            verbose=self.config["verbose"],  # 输出调试数据
            config=AliPayConfig(timeout=self.config["timeout"])  # 可选，请求超时时间，单位：秒
        )

    def page_pay(self,order_number,real_price,order_name):
        """
        生成支付链接
        @parmas order_number: 商户订单号
        @parmas real_price: 订单金额
        @parmas order_name: 订单标题
        @return 支付链接
        """
        order_string = self.client_api(
            "alipay.trade.page.pay",
            biz_content={
                "out_trade_no": order_number,  # 订单号
                "total_amount": float(real_price),  # 订单金额
                "subject": order_name,  # 订单标题
                "product_code": "FAST_INSTANT_TRADE_PAY",
            },
            return_url=self.config["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
            notify_url=self.config["notify_url"]  # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        )

        return f"{self.config['gateway']}?{order_string}"

    def check_sign(self, data):
        """
        验证返回的支付结果中的签证信息
        @params data: 支付平台返回的支付结果，字典格式
        """
        signature = data.pop("sign")
        success = self.verify(data, signature)
        return success

    def query(self,order_number):
        """
        根据订单号查询订单状态
        @params order_number: 订单号
        """
        return self.server_api(
            "alipay.trade.query",
            biz_content={
                "out_trade_no": order_number
            }
        )

    def refund(self,order_number, real_price):
        """
        原路退款
        @params order_number: 退款的订单号
        @params real_price: 退款的订单金额
        """
        self.server_api(
            "alipay.rade.refund",
            biz_content={
                "out_trade_no": order_number,
                "refund_amount": real_price
            }
        )

    def transfer(self, account,amount):
        """
        转账给个人
        @params account: 收款人的支付宝账号
        @params amount: 转账金额
        """
        return self.server_api(
            "alipay.fund.trans.toaccount.transfer",
            biz_content = {
                "out_biz_no": datetime.now().strftime("%Y%m%d%H%M%S"),
                "payee_type": "ALIPAY_LOGONID/ALIPAY_USERID",
                "payee_account": account,
                "amount": amount
            }
        )
```



`payments/views.py`，代码：

```python
from  datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from courses.serializers import CourseInfoModelSerializer
from orders.models import Order
from alipaysdk import AliPaySDK

# Create your views here.
class AlipayAPIViewSet(ViewSet):
    """支付宝接口"""

    def link(self, request, order_number):
        """生成支付宝支付链接信息"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 0:
                return Response({"message": "对不起，当前订单不能重复支付或订单已超时！"})
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在！"})

        # # 读取支付宝公钥与商户私钥
        # app_private_key_string = open(settings.ALIPAY["app_private_key_path"]).read()
        # alipay_public_key_string = open(settings.ALIPAY["alipay_public_key_path"]).read()
        #
        # # 创建alipay SDK操作对象
        # alipay = AliPay(
        #     appid=settings.ALIPAY["appid"],
        #     app_notify_url=settings.ALIPAY["notify_url"],  # 默认全局回调 url
        #     app_private_key_string=app_private_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     alipay_public_key_string=alipay_public_key_string,
        #     sign_type=settings.ALIPAY["sign_type"],  # RSA2
        #     debug=settings.ALIPAY["debug"],  # 默认 False，沙箱模式下必须设置为True
        #     verbose=settings.ALIPAY["verbose"],  # 输出调试数据
        #     config=AliPayConfig(timeout=settings.ALIPAY["timeout"])  # 可选，请求超时时间，单位：秒
        # )

        # 生成支付信息
        # order_string = alipay.client_api(
        #     "alipay.trade.page.pay",  # 接口名称
        #     biz_content={
        #         "out_trade_no": order_number,  # 订单号
        #         "total_amount": float(order.real_price),  # 订单金额 单位：元
        #         "subject": order.name,  # 订单标题
        #         "product_code": "FAST_INSTANT_TRADE_PAY",  # 产品码，目前只能支持 FAST_INSTANT_TRADE_PAY
        #     },
        #     return_url=settings.ALIPAY["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
        #     notify_url=settings.ALIPAY["notify_url"]   # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        # )
        #
        # # 拼接完整的支付链接
        # link = f"{settings.ALIPAY['gateway']}?{order_string}"

        alipay = AliPaySDK()
        link = alipay.page_pay(order_number, order.real_price, order.name)
        print(link)

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })

    def return_result(self, request):
        """支付宝支付结果的同步通知处理"""
        data = request.query_params.dict()  # QueryDict
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            return Response({"errmsg": "通知通知结果不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]

        if order.order_status == 0:
            result = alipay.query(order_number)

            print(f"result-{result}")
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                # todo 1. 修改订单状态
                order.pay_time = datetime.now()
                order.order_status = 1
                order.save()
                # todo 2. 记录扣除个人积分的流水信息，补充个人的优惠券使用记录
                # todo 3. 用户和课程的关系绑定
                # todo 4. 取消订单超时

        # 返回客户端结果
        serializer = CourseInfoModelSerializer(course_list, many=True)
        return Response({
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "real_price": float(order.real_price),
            "course_list": serializer.data
        })
```

`payments/urls.py`，代码：

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
    path("alipay/result/", views.AlipayAPIViewSet.as_view({"get":"return_result"}))
]
```

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端接收客户端转发的同步支付结果并验证修改订单状态"
git push
```



#### 服务端更新用户购买商品课程的记录

`user/models.py`，模型代码：

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from stdimage import StdImageField
from django.utils.safestring import mark_safe
from model import BaseModel
from courses.models import Course,CourseChapter,CourseLesson

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    money = models.DecimalField(max_digits=9, default=0.0, decimal_places=2, verbose_name="钱包余额")
    credit = models.IntegerField(default=0, verbose_name="积分")
    # avatar = models.ImageField(upload_to="avatar/%Y", null=True, default="", verbose_name="个人头像")
    avatar = StdImageField(variations={
        'thumb_400x400': (400, 400),  # 'medium': (400, 400),
        'thumb_50x50': (50, 50, True),  # 'small': (50, 50, True),
    }, delete_orphans=True, upload_to="avatar/%Y", blank=True, null=True, verbose_name="个人头像")


    nickname = models.CharField(max_length=50, default="", null=True, verbose_name="用户昵称")

    class Meta:
        db_table = 'lf_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


    def avatar_small(self):
        if self.avatar:
            return mark_safe(f'<img style="border-radius: 100%;" src="{self.avatar.thumb_50x50.url}">')
        return ""


    avatar_small.short_description = "个人头像(50x50)"
    avatar_small.allow_tags = True
    avatar_small.admin_order_field = "avatar"


    def avatar_medium(self):
        if self.avatar:
            return mark_safe(f'<img style="border-radius: 100%;" src="{self.avatar.thumb_400x400.url}">')
        return ""


    avatar_medium.short_description = "个人头像(400x400)"
    avatar_medium.allow_tags = True
    avatar_medium.admin_order_field = "avatar"

class Credit(BaseModel):
    """积分流水"""
    opera_choices = (
        (0, "业务增值"),
        (1, "购物消费"),
        (2, "系统赠送"),
    )
    operation = models.SmallIntegerField(choices=opera_choices, default=1, verbose_name="积分操作类型")
    number = models.IntegerField(default=0, verbose_name="积分数量", help_text="如果是扣除积分则需要设置积分为负数，如果消费10积分，则填写-10，<br>如果是添加积分则需要设置积分为正数，如果获得10积分，则填写10。")
    user = models.ForeignKey(User, related_name='user_credits', on_delete=models.CASCADE, db_constraint=False, verbose_name="用户")
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注信息")

    class Meta:
        db_table = 'ly_credit'
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.number > 0:
            oper_text = "获得"
        else:
            oper_text = "减少"
        return "[%s] %s 用户%s %s %s积分" % (self.get_operation_display(),self.created_time.strftime("%Y-%m-%d %H:%M:%S"), self.user.username, oper_text, abs(self.number))

class UserCourse(BaseModel):
    """用户的课程"""
    user   = models.ForeignKey(User, related_name='user_courses', on_delete=models.CASCADE,verbose_name="用户", db_constraint=False)
    course = models.ForeignKey(Course, related_name='course_users', on_delete=models.CASCADE, verbose_name="课程名称", db_constraint=False)
    chapter = models.ForeignKey(CourseChapter, related_name="user_chapter", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="章节信息", db_constraint=False)
    lesson = models.ForeignKey(CourseLesson, related_name="user_lesson", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="课时信息", db_constraint=False)
    study_time = models.IntegerField(default=0, verbose_name="学习时长")

    class Meta:
        db_table = 'ly_user_course'
        verbose_name = '用户课程购买记录'
        verbose_name_plural = verbose_name


```

数据迁移

```python
cd ~/Desktop/luffycity/luffycityapi
python manage.py makemigrations
python manage.py migrate
```

在订单结果处理的视图中把用户购买课程逻辑代码加上。

`payments/views.py`，代码：

```python
import logging
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from orders.models import Order
from alipaysdk import AliPaySDK
from users.models import Credit, UserCourse
from courses.serializers import CourseInfoModelSerializer
from coupon.models import CouponLog

logger = logging.getLogger("django")


# Create your views here.
class AlipayAPIViewSet(ViewSet):
    """支付宝接口"""

    def link(self, request, order_number):
        """生成支付宝支付链接信息"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 0:
                return Response({"message": "对不起，当前订单不能重复支付或订单已超时！"})
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在！"})

        # # 读取支付宝公钥与商户私钥
        # app_private_key_string = open(settings.ALIPAY["app_private_key_path"]).read()
        # alipay_public_key_string = open(settings.ALIPAY["alipay_public_key_path"]).read()
        #
        # # 创建alipay SDK操作对象
        # alipay = AliPay(
        #     appid=settings.ALIPAY["appid"],
        #     app_notify_url=settings.ALIPAY["notify_url"],  # 默认全局回调 url
        #     app_private_key_string=app_private_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     alipay_public_key_string=alipay_public_key_string,
        #     sign_type=settings.ALIPAY["sign_type"],  # RSA2
        #     debug=settings.ALIPAY["debug"],  # 默认 False，沙箱模式下必须设置为True
        #     verbose=settings.ALIPAY["verbose"],  # 输出调试数据
        #     config=AliPayConfig(timeout=settings.ALIPAY["timeout"])  # 可选，请求超时时间，单位：秒
        # )

        # 生成支付信息
        # order_string = alipay.client_api(
        #     "alipay.trade.page.pay",  # 接口名称
        #     biz_content={
        #         "out_trade_no": order_number,  # 订单号
        #         "total_amount": float(order.real_price),  # 订单金额 单位：元
        #         "subject": order.name,  # 订单标题
        #         "product_code": "FAST_INSTANT_TRADE_PAY",  # 产品码，目前只能支持 FAST_INSTANT_TRADE_PAY
        #     },
        #     return_url=settings.ALIPAY["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
        #     notify_url=settings.ALIPAY["notify_url"]   # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        # )
        #
        # # 拼接完整的支付链接
        # link = f"{settings.ALIPAY['gateway']}?{order_string}"

        alipay = AliPaySDK()
        link = alipay.page_pay(order_number, order.real_price, order.name)
        print(link)

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })

    def return_result(self, request):
        """支付宝支付结果的同步通知处理"""
        data = request.query_params.dict()  # QueryDict
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            return Response({"errmsg": "通知通知结果不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]

        if order.order_status == 0:
            # 请求支付宝，查询订单的支付结果
            result = alipay.query(order_number)
            print(f"result-{result}")
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        now_time = datetime.now()
                        # 1. 修改订单状态
                        order.pay_time = now_time
                        order.order_status = 1
                        order.save()
                        # 2.1 记录扣除个人积分的流水信息
                        if order.credit > 0:
                            Credit.objects.create(operation=1, number=order.credit, user=order.user)

                        # 2.2 补充个人的优惠券使用记录
                        coupon_log = CouponLog.objects.filter(order=order).first()
                        if coupon_log:
                            coupon_log.use_time = now_time
                            coupon_log.use_status = 1  # 1 表示已使用
                            coupon_log.save()

                        # 3. 用户和课程的关系绑定
                        user_course_list = []
                        for course in course_list:
                            user_course_list.append(UserCourse(course=course, user=order.user))
                        UserCourse.objects.bulk_create(user_course_list)

                        # todo 4. 取消订单超时

                    except Exception as e:
                        logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                        transaction.savepoint_rollback(save_id)
                        return Response({"errmsg": "当前订单支付未完成！请联系客服工作人员！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 返回客户端结果
        serializer = CourseInfoModelSerializer(course_list, many=True)
        return Response({
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "real_price": float(order.real_price),
            "course_list": serializer.data
        })

```

因为在处理同步通知结果的代码中，还进行了一次向支付宝查询订单支付结果的操作，所以有时候网络延迟的话，就会出现服务端成功，但是客户端因为超时等待而导致无法获取结果报错，此时应该设置axios的timeout为5~10秒，原来项目搭建时我们设置的是2.5秒。

`utils/http.js`，代码：

```javascript
import axios from "axios"

const http = axios.create({
    // timeout: 2500,                          // 请求超时，有大文件上传需要关闭这个配置
    baseURL: "http://api.luffycity.cn:8000",   // 设置api服务端的默认地址[如果基于服务端实现的跨域，这里可以填写api服务端的地址，如果基于nodejs客户端测试服务器实现的跨域，则这里不能填写api服务端地址]
    withCredentials: false,                    // 是否允许客户端ajax请求时携带cookie
})

// 后续代码省略....
```



客户端展示支付处理后的结果。`views/AliPaySuccess.vue`，代码：

```vue
<template>
  <div class="success" v-if="order.is_show">
    <Header/>
    <div class="main">
        <div class="title">
          <i class="el-icon-chat-dot-round"></i>
          <div class="success-tips">
             <p class="tips1">您已成功购买 {{order.course_list?.length}} 门课程！</p>
              <p class="tips2">你还可以加入QQ群 <span>747556033</span> 学习交流</p>
          </div>
        </div>
        <div class="order-info">
            <p class="info1"><b>付款时间：</b><span>{{order.pay_time}}</span></p>
            <p class="info2"><b>付款金额：</b><span >{{order.real_price?.toFixed(2)}}</span></p>
            <p class="info3"><b>课程信息：</b>
              <span v-for="course in order.course_list">《{{course.name}}》</span>
            </p>
        </div>
        <div class="wechat-code">
          <img src="../assets/wechat.jpg" alt="" class="er">
          <p><i class="el-icon-warning"></i>重要！微信扫码关注获得学习通知&amp;课程更新提醒！否则将严重影响学习进度和课程体验！</p>
        </div>
        <div class="study">
          <router-link to="/user/study"><span>立即学习</span></router-link>
        </div>
    </div>
    <Footer/>
  </div>
</template>
```

```vue

<script setup>
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import {ElMessage} from "element-plus";
import order from "../api/order";
import {useRouter} from "vue-router";
const router = useRouter()

let query_string = location.search; // 获取查询字符串的支付结果参数
order.relay_alipay_result(query_string).then(response=>{
  order.is_show = true;
  order.course_list = response.data.course_list;
  order.real_price  = response.data.real_price;
  order.pay_time    = response.data.pay_time;
}).catch(error=>{
  ElMessage.error(error.response.data.errmsg);
  router.push("/");
})

</script>
```

我们当前完成的项目具有一定特殊性，和传统卖实物商品不一样的是，我们卖的是虚拟商品，所以不存在多次购买同一款商品的，所以后续用户添加商品到购物车时， 要判断用户是否曾经购买了当前商品课程，如果在UserCourse中查询到购买记录，则不能添加商品到购物车！！`cart/views.py`，代码：

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course
from users.models import UserCourse


# Create your views here.
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 保证用户必须时登录状态才能调用当前视图

    def post(self, request):
        """添加课程商品到购物车中"""
        # 1. 接受客户端提交的商品信息：用户ID，课程ID，勾选状态
        # 用户ID 可以通过self.request.user.id 或 request.user.id 来获取
        user_id = request.user.id
        course_id = request.data.get("course_id", None)
        selected = 1  # 默认商品是勾选状态的
        print(f"user_id={user_id},course_id={course_id}")

        try:
            # 判断课程是否存在
            course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
        except:
            return Response({"errmsg": "当前课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 判断用户是否已经购买了
            UserCourse.objects.get(user_id=user_id, course_id=course_id)
            return Response({"errmsg": "对不起，您已经购买过当前课程！不需要重新购买了."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        # 3. 添加商品到购物车
        redis = get_redis_connection("cart")
        """
        cart_用户ID: {
           课程ID: 勾选状态
        }
        """
        redis.hset(f"cart_{user_id}", course_id, selected)

        # 4. 获取购物车中的商品课程数量
        cart_total = redis.hlen(f"cart_{user_id}")

        # 5. 返回结果给客户端
        return Response({"errmsg": "成功添加商品课程到购物车！", "cart_total": cart_total}, status=status.HTTP_201_CREATED)

    # ... 代码省略
```

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端更新用户购买的课程记录以及的订单支付成功后的积分流水记录与优惠券的使用状态记录，最后在购物车中防止用户重复购买商品"
git push
```



上面的支付结果处理都是基于支付平台返回的同步结果，是支付宝那边通过**js页面跳转来完成支付结果通知**的。在项目运营过程中，很容易出现跳转页面过程中无法跳转或者跳转过程中被用户手动关闭页面的情况，这些情况都会导致服务端没法完成同步通知代码的执行，也就是说，我们不能单纯等待用户付款完成以后支付宝通过页面跳转的同步通知结果，还要结合用户的行为操作和支付宝的异步通知结果处理，才能**防止订单状态的丢失**。

### 提供支付倒计时功能

客户端订单页面中添加一个倒计时的遮罩层，当用户关闭当前遮罩层则发送ajax轮询请求查询当前订单的支付结果。

`views/Order.vue`，代码

```vue
    <div class="loadding" v-if="order.loading" @click="check_order">
      <div class="box">
          <p class="time">{{fill0(parseInt(order.timeout/60))}}:{{ fill0(order.timeout%60)}}</p>
          <i class="el-icon-loading"></i><br>
          <p>支付完成！点击关闭当前页面</p>
      </div>
    </div>  <!-- 这里添加到Footer上方即可 -->
    <Footer/>
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
import {useRouter} from "vue-router";
import {fill0} from "../utils/func";

let store = useStore()
let router = useRouter()

const get_select_course = ()=>{
    // 获取购物车中的勾选商品列表
    let token = sessionStorage.token || localStorage.token;
    cart.get_select_course(token).then(response=>{
        cart.select_course_list = response.data.cart
        if(response.data.cart.length === 0){
          ElMessage.error("当前购物车中没有下单的商品！请重新重新选择购物车中要购买的商品~");
          router.back();
        }

        // 计算本次下单的总价格
        let sum = 0
        let credit_course_list= [] // 可使用积分抵扣的课程列表
        let max_use_credit = 0     // 本次下单最多可以用于抵扣的积分
        response.data.cart?.forEach((course,key)=>{
            if(course.discount.price > 0 || course.discount.price === 0){
              sum+=course.discount.price
            }else{
              sum+=course.price
            }

           if(course.credit > 0){
              max_use_credit = max_use_credit + course.credit
              credit_course_list.push(course)
            }

        })
        cart.total_price = sum;
        order.credit_course_list = credit_course_list
        order.max_use_credit = max_use_credit // 本次下单最多可以用于抵扣的积分
        console.log(`order.max_use_credit=${order.max_use_credit}`);
        // 本次订单最多可以使用的积分数量
        // 如果用户积分不足，则最多只能用完自己的积分
        if(order.max_use_credit > order.has_credit){
          order.max_use_credit = order.has_credit
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
    // 当用户选择了优惠券，则需要获取当前选择的优惠券发放记录的id
    let user_coupon_id = -1;
    if(order.select !== -1){
        user_coupon_id = order.coupon_list[order.select].user_coupon_id;
    }

    order.create_order(user_coupon_id, token).then(response=>{
      // 支付倒计时提示
      order.order_number = response.data.order_number  // 订单号
      order.loading = true                             // 显示遮罩层
      order.timeout = response.data.order_timeout      // 订单超时的时间，为15分钟
      clearInterval(order.timer)  // 先清除原有定时器，保证整个页面中timer对应的定时器是唯一的。
      order.timer = setInterval(() => {
        if(order.timeout > 1){
            order.timeout=order.timeout - 1;
        }else{
            ElMessage.error("订单超时！如果您已经支付成功！请点击关闭当前弹窗！当前页面15秒后关闭！");
            clearInterval(order.timer);
            // 发送一个订单查询
            check_order();
            // 关闭页面
            setTimeout(()=>{
                // 跳转到用户的订单用心
                router.push("/user/order");
            }, 1500);
        }
      }, 3000);

    // 成功提示
    ElMessage.success("下单成功！马上跳转到支付页面，请稍候~")
    // 扣除掉被下单的商品数量，更新购物车中的商品数量
    store.commit("cart_total", store.state.cart_total - cart.select_course_list.length);
    // 订单生成以后，先扣除临时用户积分
    order.has_credit = order.has_credit - order.credit

    // 根据订单号到服务端获取支付链接，并打开支付页面。
    console.log(order.order_number)  // 订单号
    order.alipay_page_pay().then(response=>{
        window.open(response.data.link,"_blank");
    })

  }).catch(error=>{
    if(error?.response?.status===400){
          ElMessage.success("登录超时！请重新登录后再继续操作~");
    }
  })
}


// 获取本次下单的可用优惠券
const get_enable_coupon_list = ()=>{
    let token = sessionStorage.token || localStorage.token;
    order.get_enable_coupon_list(token).then(response=>{
        order.coupon_list = response.data.coupon_list;
        // 获取积分相关信息
        order.credit_to_money = response.data.credit_to_money;
        order.has_credit      = response.data.has_credit;
    })
}
get_enable_coupon_list()


// 积分兑换抵扣
const conver_credit = ()=>{
  order.discount_price = parseFloat( (order.credit / order.credit_to_money).toFixed(2) )
}

// 本次下单的最大兑换积分
const max_conver_credit = ()=>{
  order.credit=order.max_use_credit
  conver_credit();
}

// 查询订单状态
const check_order = ()=>{
  let token = sessionStorage.token || localStorage.token;
  order.query_order(token).then(response=>{
    order.loading = false;
    router.push("/user/order");
  }).catch(error=>{
    console.log(error);
    ElMessage.error(error.response.data.errmsg);
  })
}

// 监听用户选择的支付方式
watch(
    ()=>order.pay_type,
    ()=>{
      console.log(order.pay_type)
    }
)


// 监听用户选择的优惠券
watch(
    ()=>order.select,
    ()=>{
      order.discount_price = 0;
      // 如果没有选择任何的优惠券，则select 为-1，那么不用进行计算优惠券折扣的价格了
      if (order.select === -1) {
        return // 阻止代码继续往下执行
      }

      // 根据下标select，获取当前选中的优惠券信息
      let current_coupon = order.coupon_list[order.select]
      console.log(current_coupon);

      // 针对折扣优惠券，找到最大优惠的课程
      let max_discount = -1;
      for(let course of cart.select_course_list) {  // 循环本次下单的勾选商品
        // 找到当前优惠券的可用课程
        if(current_coupon.enable_course === "__all__") { // 如果当前优惠券是通用优惠券
          if(max_discount !== -1){
            if(course.price > max_discount.price){  // 在每次循环中，那当前循环的课程的价格与之前循环中得到的最大优惠课程的价格进行比较
              max_discount = course
            }
          }else{
            max_discount = course
          }
        }else if((current_coupon.enable_course.indexOf(course.id) > -1) && (course.price >= parseFloat(current_coupon.condition))){
          // 判断 当前优惠券如果包含了当前课程， 并 课程的价格 > 当前优惠券的使用门槛
          // 只允许没有参与其他优惠券活动的课程使用优惠券，基本所有的平台都不存在折上折的。
          if( course.discount.price === undefined ) {
            if(max_discount !== -1){
              if(course.price > max_discount.price){
                max_discount = course
              }
            }else{
              max_discount = course
            }
          }
        }
      }

      if(max_discount !== -1){
        if(current_coupon.discount === '1') { // 抵扣优惠券[抵扣的价格就是当前优惠券的价格]
          order.discount_price = parseFloat( Math.abs(current_coupon.sale) )
        }else if(current_coupon.discount === '2') { // 折扣优惠券]抵扣的价格就是(1-折扣百分比) * 课程原价]
          order.discount_price = parseFloat(max_discount.price * (1-parseFloat(current_coupon.sale.replace("*",""))) )
        }
      }else{
        order.select = -1
        order.discount_price = 0
        ElMessage.error("当前课程商品已经参与了其他优惠活动，无法再次使用当前优惠券！")
      }

})


// 在切换不同的优惠类型，重置积分和优惠券信息
watch(
    ()=>order.discount_type,
    ()=>{
        order.select = -1
        order.credit = 0
        order.discount_price = 0
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

```vue
<style> <--新增样式 -->
.loadding{
  width: 100%;
  height: 100%;
  margin: auto;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
  background-color: rgba(0,0,0,.7);
}
.box{
  width: 300px;
  height: 150px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
  font-size: 40px;
  text-align: center;
  padding-top: 50px;
  color: #fff;
}
.box .time{
  font-size: 22px;
}
</style>
```

`api/order.js`，代码：

```javascript
import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
  total_price: 0,      // 勾选商品的总价格
  discount_price: 0,   // 本次下单的优惠抵扣价格
  discount_type: 0,    // 0表示优惠券，1表示积分
  use_coupon: false,   // 用户是否使用优惠
  coupon_list:[],      // 用户拥有的可用优惠券列表
  select: -1,          // 当前用户选中的优惠券下标，-1表示没有选择
  credit: 0,           // 当前用户选择抵扣的积分，0表示没有使用积分
  fixed: true,         // 底部订单总价是否固定浮动
  pay_type: 0,         // 支付方式
  credit_to_money: 0,  // 积分兑换现金的比例
  has_credit: 0,       // 用户拥有的积分
  max_use_credit: 0,   // 当前用户本次下单可用最大积分数量
  credit_course_list:[], // 可使用积分抵扣的课程列表
  course_list: [],     // 本次购买的商品课程列表
  real_price: 0,       // 付款金额
  pay_time: undefined, // 付款时间
  order_number: null,  // 订单号
  is_show: false,      // 是否展示支付成功的内容[接收到支付宝的同步处理结果以后，先把结果转发给后端验证成功以后，才把前端的页面内容展示处理]
  loading: false,      // 订单支付时的倒计时背景遮罩层
  timeout: 0,          // 订单支付超时倒计时
  timer: 0,            // 订单支付倒计时定时器的标记符
  create_order(user_coupon_id, token){
    // 生成订单
    return http.post("/orders/",{
        pay_type: this.pay_type,
        user_coupon_id,
        credit: this.credit,
    },{
        headers:{
            Authorization: "jwt " + token,
        }
    })
  },
  get_enable_coupon_list(token){
    // 获取本次下单的可用优惠券列表
    return http.get("/coupon/enable/",{
        headers:{
            Authorization: "jwt " + token,
        }
    })
  },
  alipay_page_pay(){       #修改的地方 
    // 获取订单的支付宝支付链接信息
    return http.get(`/payments/alipay/${this.order_number}`)
  },
  relay_alipay_result(query_string){
    // 把地址栏中的查询字符串(支付成功以后的同步回调通知)转发给服务端
    return http.get(`/payments/alipay/result/${query_string}`)
  },
  query_order(token){
    // 查询订单支付结果
    return http.get(`/payments/alipay/query/${this.order_number}`,{
      headers:{
        Authorization: "jwt " + token,
      }
     })
  }
})

export default order;
```

服务端下单成功返回订单号时同时返回服务端配置的订单超时时间。

`order/serializers.py`，代码：

```python
import logging
import constants

from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from django.db import transaction
from .models import Order, OrderDetail, Course
from coupon.models import CouponLog

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)
    order_timeout = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "user_coupon_id", "credit", "order_timeout"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
            "credit": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user = self.context["request"].user
        user_id = user.id

        # 判断用户如果使用了优惠券，则优惠券需要判断验证
        user_coupon_id = validated_data.get("user_coupon_id")
        # 本次下单时，用户使用的优惠券
        user_coupon = None
        if user_coupon_id != -1:
            user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user_id).first()

        # 本次下单时使用的积分数量
        use_credit = validated_data.get("credit", 0)
        if use_credit > 0 and use_credit > user.credit:
            raise serializers.ValidationError(detail="您拥有的积分不足以抵扣本次下单的积分，请重新下单！")

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

                # 用户使用优惠券或积分以后，需要在服务端计算本次使用优惠券或积分的最大优惠额度
                total_discount_price = 0    # 总优惠价格
                max_discount_course = None  # 享受最大优惠的课程

                # 本次下单最多可以抵扣的积分
                max_use_credit = 0

                for course in course_list:
                    discount_price = course.discount.get("price", None)  # 获取课程原价
                    if discount_price is not None:
                        discount_price = float(discount_price)
                    discount_name = course.discount.get("type", "")
                    detail_list.append(OrderDetail(
                        order=order,
                        course=course,
                        name=course.name,
                        price=course.price,
                        real_price=course.price if discount_price is None else discount_price,
                        discount_name=discount_name,
                    ))

                    # 统计订单的总价和实付总价
                    total_price += float(course.price)
                    real_price += float(course.price if discount_price is None else discount_price)

                    # 在用户使用了优惠券，并且当前课程没有参与其他优惠活动时，找到最佳优惠课程
                    if user_coupon and discount_price is None:
                        if max_discount_course is None:
                            max_discount_course = course
                        else:
                            if course.price >= max_discount_course.price:
                                max_discount_course = course

                    # 添加每个课程的可用积分
                    if use_credit > 0 and course.credit > 0:
                        max_use_credit += course.credit

                # 在用户使用了优惠券以后，根据循环中得到的最佳优惠课程进行计算最终抵扣金额
                if user_coupon:
                    # 优惠公式
                    sale = float(user_coupon.coupon.sale[1:])
                    if user_coupon.coupon.discount == 1:
                        """减免优惠券"""
                        total_discount_price = sale
                    elif user_coupon.coupon.discount == 2:
                        """折扣优惠券"""
                        total_discount_price = float(max_discount_course.price) * (1 - sale)

                if use_credit > 0:
                    if max_use_credit < use_credit:
                        raise serializers.ValidationError(detail="本次使用的抵扣积分数额超过了限制！")

                    # 当前订单添加积分抵扣的数量
                    order.credit = use_credit
                    total_discount_price = float(use_credit / constants.CREDIT_TO_MONEY)

                    # todo 扣除用户拥有的积分，后续在订单超时未支付，则返还订单中对应数量的积分给用户。如果订单成功支付，则添加一个积分流水记录。
                    user.credit = user.credit - use_credit
                    user.save()

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = real_price
                order.real_price =  float(real_price - total_discount_price)
                order.save()

                # 删除购物车中被勾选的商品，保留没有被勾选的商品信息
                cart = {key: value for key, value in cart_hash.items() if value == b'0'}
                pipe = redis.pipeline()
                pipe.multi()
                # 删除原来的购物车
                pipe.delete(f"cart_{user_id}")
                # 重新把未勾选的商品记录到购物车中
                if cart:
                    pipe.hmset(f"cart_{user_id}", cart)
                pipe.execute()

                # 如果有使用了优惠券，则把优惠券和当前订单进行绑定
                if user_coupon:
                    user_coupon.order = order
                    user_coupon.save()
                    # 把优惠券从redis中移除
                    redis = get_redis_connection("coupon")
                    redis.delete(f"{user_id}:{user_coupon_id}")

                # 返回订单超时时间
                order.order_timeout = constants.ORDER_TIMEOUT
                return order
            except Exception as e:
                # 1. 记录日志
                logger.error(f"订单创建失败：{e}")
                # 2. 事务回滚
                transaction.savepoint_rollback(t1)
                # 3. 抛出异常，通知视图返回错误提示
                raise serializers.ValidationError(detail="订单创建失败！")

```

utils/constants.py，代码：

```python
# 订单超时的时间(单位：秒)
ORDER_TIMEOUT = 15 * 60
```



### 服务端提供查询订单的api接口

`payments/urls.py`，代码：

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
    path("alipay/result/", views.AlipayAPIViewSet.as_view({"get":"return_result"})),
    re_path("^alipay/query/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"query"})),
]
```

`payments/views.py`，代码：

```python
import logging
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from orders.models import Order
from alipaysdk import AliPaySDK
from users.models import Credit, UserCourse
from courses.serializers import CourseInfoModelSerializer
from coupon.models import CouponLog

logger = logging.getLogger("django")


# Create your views here.
class AlipayAPIViewSet(ViewSet):
    """支付宝接口"""

    # // ... 代码省略
    # // ... 代码省略
    # // ... 代码省略


    def query(self, request, order_number):
        """主动查询订单支付的支付结果"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]
        courses_list = []
        for course in course_list:
            courses_list.append(UserCourse(course=course, user=order.user))

        if order.order_status == 0:
            # 请求支付宝，查询订单的支付结果
            alipay = AliPaySDK()
            result = alipay.query(order_number)
            print(f"result-{result}")
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        now_time = datetime.now()
                        # 1. 修改订单状态
                        order.pay_time = now_time
                        order.order_status = 1
                        order.save()
                        # 2.1 记录扣除个人积分的流水信息
                        if order.credit > 0:
                            Credit.objects.create(operation=1, number=order.credit, user=order.user)

                        # 2.2 补充个人的优惠券使用记录
                        coupon_log = CouponLog.objects.filter(order=order).first()
                        if coupon_log:
                            coupon_log.use_time = now_time
                            coupon_log.use_status = 1  # 1 表示已使用
                            coupon_log.save()

                        # 3. 用户和课程的关系绑定
                        user_course_list = []
                        for course in course_list:
                            user_course_list.append(UserCourse(course=course, user=order.user))
                        UserCourse.objects.bulk_create(user_course_list)

                        # todo 4. 取消订单超时

                    except Exception as e:
                        logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                        transaction.savepoint_rollback(save_id)
                        return Response({"errmsg": "当前订单支付未完成！请联系客服工作人员！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                """当前订单未支付"""
                return Response({"errmsg": "当前订单未支付！"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"errmsg":"当前订单已支付！"})

```

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 客户端实现支付倒计时功能"
git push
```



虽然上面提供了支付倒计时进一步确认用户是否支付了。但是还是会存在用户不点击页面而是通过页面刷新来避开了倒计时。这样的话，我们还是存存在订单状态丢失的情况。

### 接受支付宝异步发送支付结果

支付宝异步通知结果相关文档：https://opendocs.alipay.com/open/270/105902

注意：`程序执行完后必须打印输出“success”（不包含引号）。如果商家反馈给支付宝的字符不是 success 这7个字符，支付宝服务器会不断重发通知，直到超过 24 小时 22 分钟。一般情况下，25 小时以内完成 8 次通知（通知的间隔频率一般是：4m,10m,10m,1h,2h,6h,15h）。`

`payments/views.py`，代码：

```python
import logging
from datetime import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.http.response import HttpResponse

from orders.models import Order
from alipaysdk import AliPaySDK
from users.models import Credit, UserCourse
from courses.serializers import CourseInfoModelSerializer
from coupon.models import CouponLog

logger = logging.getLogger("django")


# Create your views here.
class AlipayAPIViewSet(ViewSet):
    """支付宝接口"""

    def link(self, request, order_number):
        """生成支付宝支付链接信息"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 0:
                return Response({"message": "对不起，当前订单不能重复支付或订单已超时！"})
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在！"})

        # # 读取支付宝公钥与商户私钥
        # app_private_key_string = open(settings.ALIPAY["app_private_key_path"]).read()
        # alipay_public_key_string = open(settings.ALIPAY["alipay_public_key_path"]).read()
        #
        # # 创建alipay SDK操作对象
        # alipay = AliPay(
        #     appid=settings.ALIPAY["appid"],
        #     app_notify_url=settings.ALIPAY["notify_url"],  # 默认全局回调 url
        #     app_private_key_string=app_private_key_string,
        #     # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        #     alipay_public_key_string=alipay_public_key_string,
        #     sign_type=settings.ALIPAY["sign_type"],  # RSA2
        #     debug=settings.ALIPAY["debug"],  # 默认 False，沙箱模式下必须设置为True
        #     verbose=settings.ALIPAY["verbose"],  # 输出调试数据
        #     config=AliPayConfig(timeout=settings.ALIPAY["timeout"])  # 可选，请求超时时间，单位：秒
        # )

        # 生成支付信息
        # order_string = alipay.client_api(
        #     "alipay.trade.page.pay",  # 接口名称
        #     biz_content={
        #         "out_trade_no": order_number,  # 订单号
        #         "total_amount": float(order.real_price),  # 订单金额 单位：元
        #         "subject": order.name,  # 订单标题
        #         "product_code": "FAST_INSTANT_TRADE_PAY",  # 产品码，目前只能支持 FAST_INSTANT_TRADE_PAY
        #     },
        #     return_url=settings.ALIPAY["return_url"],  # 可选，同步回调地址，必须填写客户端的路径
        #     notify_url=settings.ALIPAY["notify_url"]   # 可选，不填则使用采用全局默认notify_url，必须填写服务端的路径
        # )
        #
        # # 拼接完整的支付链接
        # link = f"{settings.ALIPAY['gateway']}?{order_string}"

        alipay = AliPaySDK()
        link = alipay.page_pay(order_number, order.real_price, order.name)
        print(link)

        return Response({
            "pay_type": 0, # 支付类型
            "get_pay_type_display": "支付宝", # 支付类型的提示
            "link": link  # 支付连接地址
        })

    def return_result(self, request):
        """支付宝支付结果的同步通知处理"""
        data = request.query_params.dict()  # QueryDict
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            return Response({"errmsg": "通知通知结果不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        order_number = data.get("out_trade_no")
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]

        if order.order_status == 0:
            # 请求支付宝，查询订单的支付结果
            result = alipay.query(order_number)
            print(f"result-{result}")
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        now_time = datetime.now()
                        # 1. 修改订单状态
                        order.pay_time = now_time
                        order.order_status = 1
                        order.save()
                        # 2.1 记录扣除个人积分的流水信息
                        if order.credit > 0:
                            Credit.objects.create(operation=1, number=order.credit, user=order.user)

                        # 2.2 补充个人的优惠券使用记录
                        coupon_log = CouponLog.objects.filter(order=order).first()
                        if coupon_log:
                            coupon_log.use_time = now_time
                            coupon_log.use_status = 1  # 1 表示已使用
                            coupon_log.save()

                        # 3. 用户和课程的关系绑定
                        user_course_list = []
                        for course in course_list:
                            user_course_list.append(UserCourse(course=course, user=order.user))
                        UserCourse.objects.bulk_create(user_course_list)

                        # todo 4. 取消订单超时

                    except Exception as e:
                        logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                        transaction.savepoint_rollback(save_id)
                        return Response({"errmsg": "当前订单支付未完成！请联系客服工作人员！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 返回客户端结果
        serializer = CourseInfoModelSerializer(course_list, many=True)
        return Response({
            "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S"),
            "real_price": float(order.real_price),
            "course_list": serializer.data
        })

    def notify_result(self, request):
        """支付宝支付结果的异步通知处理"""
        # drf中接收POST参数需要使用request.data
        data = request.data
        alipay = AliPaySDK()
        success = alipay.check_sign(data)
        if not success:
            # 因为是属于异步处理，这个过程无法通过终端调试，因此，需要把支付发送过来的结果，记录到日志中。
            logger.error(f"[支付宝]>> 异步通知结果验证失败：{data}")
            return HttpResponse("fail")

        if data.get("trade_status") not in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
            return HttpResponse("fail")

        # 基于支付包异步请求的支付结果中提取订单号
        order_number = data.get("out_trade_no")

        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return HttpResponse("fail")
        except Order.DoesNotExist:
            return HttpResponse("fail")

        # 如果已经支付完成，则不需要继续往下处理
        if order.order_status == 1:
            return HttpResponse("success")

        # 获取本次下单的商品课程列表
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]
        courses_list = []

        for course in course_list:
            courses_list.append(UserCourse(course=course, user=order.user))

        """支付成功"""
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                now_time = datetime.now()
                # 1. 修改订单状态
                order.pay_time = now_time
                order.order_status = 1
                order.save()
                # 2.1 记录扣除个人积分的流水信息
                if order.credit > 0:
                    Credit.objects.create(operation=1, number=order.credit, user=order.user)

                # 2.2 补充个人的优惠券使用记录
                coupon_log = CouponLog.objects.filter(order=order).first()
                if coupon_log:
                    coupon_log.use_time = now_time
                    coupon_log.use_status = 1  # 1 表示已使用
                    coupon_log.save()

                # 3. 用户和课程的关系绑定
                user_course_list = []
                for course in course_list:
                    user_course_list.append(UserCourse(course=course, user=order.user))
                UserCourse.objects.bulk_create(user_course_list)

                # todo 4. 取消订单超时

            except Exception as e:
                logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                transaction.savepoint_rollback(save_id)
                return HttpResponse("fail")

        return HttpResponse("success")

    def query(self, request, order_number):
        """主动查询订单支付的支付结果"""
        try:
            order = Order.objects.get(order_number=order_number)
            if order.order_status > 1:
                return Response({"errmsg": "订单超时或已取消！"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"errmsg": "订单不存在！"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取当前订单相关的课程信息，用于返回给客户端
        order_courses = order.order_courses.all()
        course_list = [item.course for item in order_courses]
        courses_list = []
        for course in course_list:
            courses_list.append(UserCourse(course=course, user=order.user))

        if order.order_status == 0:
            # 请求支付宝，查询订单的支付结果
            alipay = AliPaySDK()
            result = alipay.query(order_number)
            print(f"result-{result}")
            if result.get("trade_status", None) in ["TRADE_FINISHED", "TRADE_SUCCESS"]:
                """支付成功"""
                with transaction.atomic():
                    save_id = transaction.savepoint()
                    try:
                        now_time = datetime.now()
                        # 1. 修改订单状态
                        order.pay_time = now_time
                        order.order_status = 1
                        order.save()
                        # 2.1 记录扣除个人积分的流水信息
                        if order.credit > 0:
                            Credit.objects.create(operation=1, number=order.credit, user=order.user)

                        # 2.2 补充个人的优惠券使用记录
                        coupon_log = CouponLog.objects.filter(order=order).first()
                        if coupon_log:
                            coupon_log.use_time = now_time
                            coupon_log.use_status = 1  # 1 表示已使用
                            coupon_log.save()

                        # 3. 用户和课程的关系绑定
                        user_course_list = []
                        for course in course_list:
                            user_course_list.append(UserCourse(course=course, user=order.user))
                        UserCourse.objects.bulk_create(user_course_list)

                        # todo 4. 取消订单超时

                    except Exception as e:
                        logger.error(f"订单支付处理同步结果发生未知错误：{e}")
                        transaction.savepoint_rollback(save_id)
                        return Response({"errmsg": "当前订单支付未完成！请联系客服工作人员！"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                """当前订单未支付"""
                return Response({"errmsg": "当前订单未支付！"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"errmsg":"当前订单已支付！"})

```

路由，`payments/urls.py`，代码：

```python
from django.urls import path,re_path
from . import views
urlpatterns = [
    re_path("^alipay/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"link"})),
    path("alipay/result/", views.AlipayAPIViewSet.as_view({"get":"return_result"})),
    re_path("^alipay/query/(?P<order_number>[0-9]+)/$", views.AlipayAPIViewSet.as_view({"get":"query"})),
    path("alipay/notify", views.AlipayAPIViewSet.as_view({"post": "notify_result"})),
]
```

补充：异步支付结果的处理代码的验证，只能放在线上服务器中通过支付在日志中检验。无法在本地开发中校验。因为异步通知结果是需要支付宝能访问到我们的当前站点，但是现在属于本地开发。

提交代码版本：

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端接收并处理支付宝异步通知结果"
git push
```

