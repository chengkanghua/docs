## 优惠券

### 创建优惠券子应用

创建coupon子应用

```bash
git checkout master
git merge feature/order
git push --set-upstream origin master


git checkout -b feature/coupon
cd luffycityapi/apps
python ../../manage.py startapp coupon
```

注册子应用，`settings/dev.py`，代码：

```python
INSTALLED_APPS = [
 
    # 子应用
	。。。
    'coupon',
]
```

子路由，`coupon/urls.py`，代码：

```python
from django.urls import path
from . import views
urlpatterns = [
    
]
```

总路由，`luffycityapi/urls.py`，代码：

```python
path("coupon/", include("coupon.urls")),
```



### 优惠券模型

模型分析：

![image-20211129085657537](assets/image-20211129085657537.png)

`coupon/models.py`，模型创建，代码：

```python
from model import BaseModel, models
from courses.models import CourseDirection, CourseCategory, Course
from users.models import User
from orders.models import Order


# Create your models here.
class Coupon(BaseModel):
    discount_choices = (
        (1, '减免'),
        (2, '折扣'),
    )
    type_choices = (
        (0, '通用类型'),
        (1, '指定方向'),
        (2, '指定分类'),
        (3, '指定课程'),
    )
    get_choices = (
        (0, "系统赠送"),
        (1, "自行领取"),
    )
    discount = models.SmallIntegerField(choices=discount_choices, default=1, verbose_name="优惠方式")
    coupon_type = models.SmallIntegerField(choices=type_choices, default=0, verbose_name="优惠券类型")
    total = models.IntegerField(blank=True, default=100, verbose_name="发放数量")
    has_total = models.IntegerField(blank=True, default=100, verbose_name="剩余数量")
    start_time = models.DateTimeField(verbose_name="启用时间")
    end_time = models.DateTimeField(verbose_name="过期时间")
    get_type = models.SmallIntegerField(choices=get_choices, default=0, verbose_name="领取方式")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足使用优惠券的价格条件")
    per_limit = models.SmallIntegerField(default=1, verbose_name="每人限制领取数量")
    sale = models.TextField(verbose_name="优惠公式", help_text="""
            *号开头表示折扣价，例如*0.82表示八二折；<br>
            -号开头表示减免价,例如-10表示在总价基础上减免10元<br>   
            """)

    class Meta:
        db_table = "ly_coupon"
        verbose_name = "优惠券"
        verbose_name_plural = verbose_name


class CouponDirection(models.Model):
    direction = models.ForeignKey(CourseDirection, on_delete=models.CASCADE, related_name="to_coupon", verbose_name="学习方向", db_constraint=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="to_direction", verbose_name="优惠券", db_constraint=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "ly_coupon_course_direction"
        verbose_name = "优惠券与学习方向"
        verbose_name_plural = verbose_name


class CouponCourseCat(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="to_coupon", verbose_name="课程分类", db_constraint=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="to_category", verbose_name="优惠券", db_constraint=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "ly_coupon_course_category"
        verbose_name = "优惠券与课程分类"
        verbose_name_plural = verbose_name


class CouponCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="to_coupon", verbose_name="课程", db_constraint=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="to_course", verbose_name="优惠券", db_constraint=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "ly_coupon_course"
        verbose_name = "优惠券与课程信息"
        verbose_name_plural = verbose_name


class CouponLog(BaseModel):
    use_choices = (
        (0, "未使用"),
        (1, "已使用"),
        (2, "已过期"),
    )
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name="名称/标题")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_coupon", verbose_name="用户",
                             db_constraint=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="to_user", verbose_name="优惠券",
                               db_constraint=False)
    order = models.ForeignKey(Order, null=True, blank=True, default=None, on_delete=models.CASCADE,
                              related_name="to_coupon", verbose_name="订单", db_constraint=False)
    use_time = models.DateTimeField(null=True, blank=True, verbose_name="使用时间")
    use_status = models.SmallIntegerField(choices=use_choices, null=True, blank=True, default=0, verbose_name="使用状态")

    class Meta:
        db_table = "ly_coupon_log"
        verbose_name = "优惠券发放和使用日志"
        verbose_name_plural = verbose_name

```

数据迁移，终端下执行：

```bash
cd ../..
python manage.py makemigrations
python manage.py migrate 
```



### 把当前子应用注册到Admin管理站点

`coupon/apps.py`，代码：

```python
from django.apps import AppConfig

class CouponConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupon'
    verbose_name = "优惠券管理"
    verbose_name_plural = verbose_name
```

`coupon/admin.py`，代码：

```python
from django.contrib import admin
from .models import Coupon, CouponDirection, CouponCourseCat, CouponCourse, CouponLog


# Register your models here.
class CouponDirectionInLine(admin.TabularInline):  # admin.StackedInline
    """学习方向的内嵌类"""
    model = CouponDirection
    fields = ["id", "direction"]


class CouponCourseCatInLine(admin.TabularInline):  # admin.StackedInline
    """课程分类的内嵌类"""
    model = CouponCourseCat
    fields = ["id", "category"]


class CouponCourseInLine(admin.TabularInline):  # admin.StackedInline
    """课程信息的内嵌类"""
    model = CouponCourse
    fields = ["id", "course"]


class CouponModelAdmin(admin.ModelAdmin):
    """优惠券的模型管理器"""
    list_display = ["id", "name", "start_time", "end_time", "total", "has_total", "coupon_type", "get_type", ]
    inlines = [CouponDirectionInLine, CouponCourseCatInLine, CouponCourseInLine]


admin.site.register(Coupon, CouponModelAdmin)


class CouponLogModelAdmin(admin.ModelAdmin):
    """优惠券发放和使用日志"""
    list_display = ["id", "user", "coupon", "order", "use_time", "use_status"]


admin.site.register(CouponLog, CouponLogModelAdmin)
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 创建优惠券子应用并设计优惠券的存储数据模型"
git push --set-upstream origin feature/coupon
```



实现后台管理员给用户分发优惠券时自动记录到redis中。

`settings/dev.py`，代码：

```python
# 设置redis缓存
CACHES = {
    # 。。。
    # 提供存储优惠券
    "coupon": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

```

`coupon/admin.py`，代码：

```python
from django.contrib import admin
from django_redis import get_redis_connection
from .models import Coupon,CouponDirection,CouponCourseCat,CouponCourse,CouponLog
from django.utils.timezone import datetime
import json
class CouponDirectionInLine(admin.TabularInline): # admin.StackedInline
    """学习方向的内嵌类"""
    model = CouponDirection
    fields = ["id","direction"]

class CouponCourseCatInLine(admin.TabularInline): # admin.StackedInline
    """课程分类的内嵌类"""
    model = CouponCourseCat
    fields = ["id","category"]

class CouponCourseInLine(admin.TabularInline): # admin.StackedInline
    """课程信息的内嵌类"""
    model = CouponCourse
    fields = ["id","course"]

class CouponModelAdmin(admin.ModelAdmin):
    """优惠券的模型管理器"""
    list_display = ["id","name","start_time","end_time","total","has_total","coupon_type","get_type",]
    inlines = [CouponDirectionInLine, CouponCourseCatInLine, CouponCourseInLine]

admin.site.register(Coupon, CouponModelAdmin)

class CouponLogModelAdmin(admin.ModelAdmin):
    """优惠券发放和使用记录"""
    list_display = ["id","user","coupon","order","use_time","use_status"]
    def save_model(self,  request, obj, form, change):
        """
        保存或更新记录时自动执行的钩子
        request: 本次客户端提交的请求对象
        obj: 本次操作的模型实例对象
        form: 本次客户端提交的表单数据
        change: 值为True，表示更新数据，值为False，表示添加数据
        """
        obj.save()
        # 同步记录到redis中
        redis = get_redis_connection("coupon")
        # print(obj.use_status , obj.use_time)
        if obj.use_status == 0 and obj.use_time == None:
            # 记录优惠券信息到redis中
            pipe = redis.pipeline()
            pipe.multi()
            pipe.hset(f"{obj.user.id}:{obj.id}","coupon_id", obj.coupon.id)
            pipe.hset(f"{obj.user.id}:{obj.id}","name", obj.coupon.name)
            pipe.hset(f"{obj.user.id}:{obj.id}","discount", obj.coupon.discount)
            pipe.hset(f"{obj.user.id}:{obj.id}","get_discount_display", obj.coupon.get_discount_display())
            pipe.hset(f"{obj.user.id}:{obj.id}","coupon_type", obj.coupon.coupon_type)
            pipe.hset(f"{obj.user.id}:{obj.id}","get_coupon_type_display", obj.coupon.get_coupon_type_display())
            pipe.hset(f"{obj.user.id}:{obj.id}","start_time", obj.coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(f"{obj.user.id}:{obj.id}","end_time", obj.coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(f"{obj.user.id}:{obj.id}","get_type", obj.coupon.get_type)
            pipe.hset(f"{obj.user.id}:{obj.id}","get_get_type_display", obj.coupon.get_get_type_display())
            pipe.hset(f"{obj.user.id}:{obj.id}","condition", obj.coupon.condition)
            pipe.hset(f"{obj.user.id}:{obj.id}","sale", obj.coupon.sale)
            pipe.hset(f"{obj.user.id}:{obj.id}","to_direction", json.dumps(list(obj.coupon.to_direction.values("direction__id","direction__name"))))
            pipe.hset(f"{obj.user.id}:{obj.id}","to_category", json.dumps(list(obj.coupon.to_category.values("category__id","category__name"))))
            pipe.hset(f"{obj.user.id}:{obj.id}","to_course", json.dumps(list(obj.coupon.to_course.values("course__id","course__name"))))
            # 设置当前优惠券的有效期
            pipe.expire(f"{obj.user.id}:{obj.id}", int(obj.coupon.end_time.timestamp() - datetime.now().timestamp()))
            pipe.execute()
        else:
            redis.delete(f"{obj.user.id}:{obj.id}")

    def delete_model(self, request, obj):
        """删除记录时自动执行的钩子"""
        # 如果系统后台管理员删除当前优惠券记录，则redis中的对应记录也被删除
        print(obj, "详情页中删除一个记录")
        redis = get_redis_connection("coupon")
        redis.delete(f"{obj.user.id}:{obj.id}")
        obj.delete()

    def delete_queryset(self, request, queryset):
        """在列表页中进行删除优惠券记录时，也要同步删除容redis中的记录"""
        print(queryset, "列表页中删除多个记录")
        redis = get_redis_connection("coupon")
        for obj in queryset:
            redis.delete(f"{obj.user.id}:{obj.id}")
        queryset.delete()

admin.site.register(CouponLog, CouponLogModelAdmin)
```

添加测试数据，代码：

```sql
-- 优惠券测试数据
truncate table ly_coupon;
INSERT INTO ly_coupon (id, name, is_deleted, orders, is_show, created_time, updated_time, discount, coupon_type, total, has_total, start_time, end_time, get_type, `condition`, per_limit, sale) VALUES (1, '30元通用优惠券', 0, 1, 1, '2022-05-04 10:35:40.569417', '2022-06-30 10:25:00.353212', 1, 0, 10000, 10000, '2022-05-04 10:35:00', '2023-01-02 10:35:00', 0, 100, 1, '-30'),(2, '前端学习通用优惠券', 0, 1, 1, '2022-05-04 10:36:58.401527', '2022-05-04 10:36:58.401556', 1, 1, 100, 100, '2022-05-04 10:36:00', '2022-08-04 10:36:00', 0, 0, 1, '-50'),(3, 'Typescript课程专用券', 0, 1, 1, '2022-05-04 10:38:36.134581', '2022-05-04 10:38:36.134624', 2, 3, 1000, 1000, '2022-05-04 10:38:00', '2022-08-04 10:38:00', 0, 0, 1, '*0.88'),(4, 'python七夕专用券', 0, 1, 1, '2022-05-04 10:40:08.022904', '2022-06-30 10:25:46.949197', 1, 2, 200, 200, '2022-05-04 10:39:00', '2022-11-15 10:39:00', 1, 0, 1, '-99'),(5, '算法学习优惠券', 0, 1, 1, '2021-08-05 10:05:07.837008', '2022-06-30 10:26:12.133812', 2, 2, 1000, 1000, '2022-08-05 10:04:00', '2022-12-25 10:04:00', 0, 200, 1, '*0.85');

-- 优惠券与学习方向的关系测试数据
truncate table ly_coupon_course_direction;
INSERT INTO ly_coupon_course_direction (id, created_time, coupon_id, direction_id) VALUES (1, '2022-05-04 10:36:58.414461', 2, 1);

-- 优惠券与课程分类的关系测试数据
truncate table ly_coupon_course_category;
INSERT INTO .ly_coupon_course_category (id, created_time, category_id, coupon_id) VALUES (1, '2022-05-04 10:40:08.029505', 20, 4),(2, '2022-05-04 10:40:08.042891', 21, 4),(3, '2021-08-05 10:05:07.966221', 33, 5);

-- 优惠券与课程信息的关系测试数据
truncate table ly_coupon_course;
INSERT INTO ly_coupon_course (id, created_time, coupon_id, course_id) VALUES (1, '2022-05-04 10:38:36.140929', 3, 1),(2, '2022-05-04 10:38:36.143166', 3, 2);

-- 优惠券的发放和使用日志的测试数据
truncate table ly_coupon_log;
INSERT INTO luffycity.ly_coupon_log (id, is_deleted, orders, is_show, created_time, updated_time, name, use_time, use_status, coupon_id, order_id, user_id) VALUES (5, 0, 1, 1, '2022-05-04 12:00:25.051976', '2022-06-30 10:25:17.681298', '30元通用优惠券222', null, 0, 1, null, 1),(8, 0, 1, 1, '2022-05-04 12:03:24.331024', '2022-06-30 10:22:45.834401', '前端学习通用优惠券', null, 0, 2, null, 1),(9, 0, 1, 1, '2022-05-04 12:03:31.692397', '2022-06-30 10:23:41.492205', 'Typescript课程专用券', null, 0, 3, null, 1),(10, 0, 1, 1, '2022-05-04 12:03:38.225438', '2022-06-30 10:25:49.797318', 'python七夕专用券', null, 0, 4, null, 1),(11, 0, 1, 1, '2022-05-04 12:09:25.406437', '2022-06-30 10:23:55.832262', '前端学习通用优惠券', null, 0, 2, null, 1),(12, 0, 1, 1, '2021-08-05 10:06:06.036230', '2022-06-30 10:26:20.723668', '算法学习优惠券', null, 0, 5, null, 1);
```

> 注意：添加测试数据完成以后，因为是通过SQL语句来添加的。务必在Admin站点中对优惠券的发放和使用日志这功能中每一条数据进行一次的更新操作，打开数据详情页不需要修改任何数据，保存即可，这样才能让用户的优惠券信息同步到redis中！！！注意：如果是已经过期的优惠券，则不会被同步到redis中。

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 实现后台管理员给用户分发优惠券时自动记录到redis中"
git push --set-upstream origin feature/coupon
```

 

### 获取用户本次下单的可用优惠券

封装工具函数，获取当前用户拥有的所有优惠券以及本次下单的可用优惠券列表，`coupon/services.py`，代码：

```python
import json
from django_redis import get_redis_connection
from courses.models import Course


def get_user_coupon_list(user_id):
    """获取指定用户拥有的所有优惠券列表"""
    redis = get_redis_connection("coupon")
    coupon_list = redis.keys(f"{user_id}:*")
    
    try:
        coupon_id_list = [item.decode() for item in coupon_list]
    except:
        coupon_id_list = []
    coupon_data = []
    # 遍历redis中所有的优惠券数据并转换数据格式
    for coupon_key in coupon_id_list:
        coupon_item = {"user_coupon_id": int(coupon_key.split(":")[-1])}
        coupon_hash = redis.hgetall(coupon_key)
        for key, value in coupon_hash.items():
            key = key.decode()
            value = value.decode()
            if key in ["to_course", "to_category", "to_direction"]:
                value = json.loads(value)
            coupon_item[key] = value
        coupon_data.append(coupon_item)

    return coupon_data


def get_user_enable_coupon_list(user_id):
    """
    获取指定用户本次下单的可用优惠券列表
    # 根据当前本次客户端购买商品课程进行比较，获取用户的当前可用优惠券。
    """
    redis = get_redis_connection("cart")

    # 先获取所有的优惠券列表
    coupon_data = get_user_coupon_list(user_id)

    # 获取指定用户的购物车中的勾选商品[与优惠券的适用范围进行比对，找出能用的优惠券]
    cart_hash = redis.hgetall(f"cart_{user_id}")

    # 获取被勾选的商品课程的ID列表
    course_id_list = {int(key.decode()) for key, value in cart_hash.items() if value == b'1'}

    # 获取被勾选的商品课程的模型对象列表
    course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()

    category_id_list = set()
    direction_id_list = set()
    for course in course_list:
        # 获取被勾选的商品课程的父类课程分类id列表，并保证去重
        category_id_list.add(int(course.category.id))
        # # 获取被勾选的商品课程的父类学习方向id列表，并保证去重
        direction_id_list.add(int(course.direction.id))

    # 创建一个列表用于保存所有的可用优惠券
    enable_coupon_list = []
    for item in coupon_data:
        coupon_type = int(item.get("coupon_type"))

        if coupon_type == 0:
            # 通用类型优惠券
            item["enable_course"] = "__all__"
            enable_coupon_list.append(item)

        elif coupon_type == 3:
            # 指定课程优惠券
            coupon_course = {int(course_item["course__id"]) for course_item in item.get("to_course")}
            # 并集处理
            ret = course_id_list & coupon_course
            if len(ret) > 0:
                item["enable_course"] = {int(course.id) for course in course_list if course.id in ret}
                enable_coupon_list.append(item)

        elif coupon_type == 2:
            # 指定课程分配优惠券
            coupon_category = {int(category_item["category__id"]) for category_item in item.get("to_category")}
            # 并集处理
            ret = category_id_list & coupon_category

            if len(ret) > 0:
                item["enable_course"] = {int(course.id) for course in course_list if course.category.id in ret}
                enable_coupon_list.append(item)

        elif coupon_type == 1:
            # 指定学习方向的优惠券
            coupon_direction = {int(direction_item["direction__id"]) for direction_item in item.get("to_direction")}
            # 并集处理
            ret = direction_id_list & coupon_direction

            if len(ret) > 0:
                item["enable_course"] = {int(course.id) for course in course_list if course.direction.id in ret}
                enable_coupon_list.append(item)

    return enable_coupon_list

```

`coupon/views.py`，代码：

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import get_user_coupon_list, get_user_enable_coupon_list


class CouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户拥有的所有优惠券"""
        user_id = request.user.id
        coupon_data = get_user_coupon_list(user_id)
        return Response(coupon_data)


class EnableCouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户本次拥有的本次下单可用所有优惠券"""
        user_id = request.user.id
        coupon_data = get_user_enable_coupon_list(user_id)
        return Response(coupon_data)
```



`coupon/urls.py`，代码：

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.CouponListAPIView.as_view()),
    path("enable/", views.EnableCouponListAPIView.as_view()),
]
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端实现获取用户所有优惠券与本次下单的可用优惠券列表"
git push 
```



### 客户端展示用户拥有的可用优惠券

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
  create_order(token){
    // 生成订单
    return http.post("/orders/",{
        pay_type: this.pay_type
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
  }
})

export default order;
```



`views/Order.vue`，代码：

```vue
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
                 <li class="l" :class="{select: order.select === key}" @click="order.select = (order.select === key?-1:key)" v-for="(coupon,key) in order.coupon_list" :key="key">
                  <div class="detail-box more-del-box">
                   <div class="price-box">
                    <p class="coupon-price l" v-if="coupon.discount === '1'"> ￥{{Math.abs(coupon.sale)}} </p>
                    <p class="coupon-price l" v-if="coupon.discount === '2'"> {{coupon.sale.replace("*0.","")}}折 </p>
                    <p class="use-inst l" v-if="coupon.condition>0">满{{coupon.condition}}元可用</p>
                    <p class="use-inst l" v-else>任意使用</p>
                   </div>
                   <div class="use-detail-box">
                    <div class="use-ajust-box">适用于：{{coupon.name}}</div>
                    <div class="use-ajust-box">有效期：{{coupon.start_time.split(" ")[0].replaceAll("-",".")}}-{{coupon.end_time.split(" ")[0].replaceAll("-",".")}}</div>
                   </div>
                  </div>
                 </li>
                </ul>
<!--                <ul class="use-box">-->
<!--                 <li class="l useing">-->
<!--                  <div class="detail-box more-del-box">-->
<!--                   <div class="price-box">-->
<!--                    <p class="coupon-price l"> ￥100 </p>-->
<!--                    <p class="use-inst l">满499可用</p>-->
<!--                   </div>-->
<!--                   <div class="use-detail-box">-->
<!--                    <div class="use-ajust-box">适用于：全部实战课程</div>-->
<!--                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>-->
<!--                   </div>-->
<!--                  </div>-->
<!--                 </li>-->
<!--                 <li class="l">-->
<!--                  <div class="detail-box more-del-box">-->
<!--                   <div class="price-box">-->
<!--                    <p class="coupon-price l"> ￥248 </p>-->
<!--                    <p class="use-inst l">满999可用</p>-->
<!--                   </div>-->
<!--                   <div class="use-detail-box">-->
<!--                    <div class="use-ajust-box">适用于：全部实战课程</div>-->
<!--                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>-->
<!--                   </div>-->
<!--                  </div>-->
<!--                 </li>-->
<!--                </ul>-->
<!--                <ul class="overdue-box">-->
<!--                 <li class="l useing">-->
<!--                  <div class="detail-box more-del-box">-->
<!--                   <div class="price-box">-->
<!--                    <p class="coupon-price l"> ￥100 </p>-->
<!--                    <p class="use-inst l">满499可用</p>-->
<!--                   </div>-->
<!--                   <div class="use-detail-box">-->
<!--                    <div class="use-ajust-box">适用于：全部实战课程</div>-->
<!--                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>-->
<!--                   </div>-->
<!--                  </div>-->
<!--                 </li>-->
<!--                 <li class="l">-->
<!--                  <div class="detail-box more-del-box">-->
<!--                   <div class="price-box">-->
<!--                    <p class="coupon-price l"> ￥248 </p>-->
<!--                    <p class="use-inst l">满999可用</p>-->
<!--                   </div>-->
<!--                   <div class="use-detail-box">-->
<!--                    <div class="use-ajust-box">适用于：全部实战课程</div>-->
<!--                    <div class="use-ajust-box">有效期：2021.06.01-2021.06.18</div>-->
<!--                   </div>-->
<!--                  </div>-->
<!--                 </li>-->
<!--                </ul>-->
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


// 获取本次下单的可用优惠券
const get_enable_coupon_list = ()=>{
    let token = sessionStorage.token || localStorage.token;
    order.get_enable_coupon_list(token).then(response=>{
        order.coupon_list = response.data
    })
}
get_enable_coupon_list()

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



### 用户勾选优惠券后调整订单实付价格

```vue
<div class="pay-box" :class="{fixed:order.fixed}">
				  <div class="row-bottom">
            <div class="row">
              <div class="goods-total-price-box">
                <p class="r rw price-num"><em>￥</em><span>{{cart.total_price.toFixed(2)}}</span></p>
                <p class="r price-text"><span>共<span>{{cart.select_course_list?.length}}</span>件商品，</span>商品总金额：</p>
              </div>
            </div>
            <div class="coupons-discount-box">
              <p class="r rw price-num">-<em>￥</em><span>{{order.discount_price.toFixed(2)}}</span></p>
              <p class="r price-text">优惠券/积分抵扣：</p>
            </div>
            <div class="pay-price-box clearfix">
              <p class="r rw price"><em>￥</em><span id="js-pay-price">{{ (cart.total_price-order.discount_price).toFixed(2)}}</span></p>
              <p class="r price-text">应付：</p>
            </div>
            <span class="r btn btn-red submit-btn" @click="commit_order">提交订单</span>
					</div>
          <div class="pay-add-sign">
            <ul class="clearfix">
              <li>支持花呗</li>
              <li>可开发票</li>
              <li class="drawback">7天可退款</li>
            </ul>
          </div>
	      </div>
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

        // 计算本次下单的总价格
        let sum = 0
        response.data.cart?.forEach((course,key)=>{
            if(course.discount.price > 0 || course.discount.price === 0){
              sum+=course.discount.price
            }else{
              sum+=course.price
            }
        })
        cart.total_price = sum;

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


// 获取本次下单的可用优惠券
const get_enable_coupon_list = ()=>{
    let token = sessionStorage.token || localStorage.token;
    order.get_enable_coupon_list(token).then(response=>{
        order.coupon_list = response.data
    })
}
get_enable_coupon_list()

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
git commit -m "feature: 客户端展示用户本次下单的可用优惠券并重新调整价格"
git push
```



### 客户端发送请求附带优惠券记录ID

客户端下单以后，本次请求附带使用的 **用户优惠券记录ID**到服务端，服务端进行验证计算，得到正确的实付价格，并从redis中删除用户使用的优惠券。

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
  create_order(user_coupon_id, token){
    // 生成订单
    return http.post("/orders/",{
        pay_type: this.pay_type,
        user_coupon_id,
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
  }
})

export default order;
```

`views/Order.vue`，代码：

```vue
<script setup>

 // 中间代码省略....

const commit_order = ()=>{
    // 生成订单
    let token = sessionStorage.token || localStorage.token;
    
    // 当用户选择了优惠券，则需要获取当前选择的优惠券发放记录的id
    let user_coupon_id = -1;
    if(order.select !== -1){
        user_coupon_id = order.coupon_list[order.select].user_coupon_id;
    }

    order.create_order(user_coupon_id, token).then(response=>{
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

 // 中间代码省略....

</script>
```



### 服务端接收并验证优惠券发送记录ID再重新计算本次下单的实付价格

`order/serializers.py`，代码：

```python
from datetime import datetime
from rest_framework import serializers
from django_redis import get_redis_connection
from django.db import transaction
from .models import Order, OrderDetail, Course
from coupon.models import CouponLog
import logging

logger = logging.getLogger("django")


class OrderModelSerializer(serializers.ModelSerializer):
    pay_link = serializers.CharField(read_only=True)
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link", "user_coupon_id"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
        }

    def create(self, validated_data):
        """创建订单"""
        redis = get_redis_connection("cart")
        user_id = self.context["request"].user.id  # 1

        # 判断用户如果使用了优惠券，则优惠券需要判断验证
        user_coupon_id = validated_data.get("user_coupon_id")
        # 本次下单时，用户使用的优惠券
        user_coupon = None
        if user_coupon_id != -1:
            user_coupon = CouponLog.objects.filter(pk=user_coupon_id, user_id=user_id).first()

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

                # 一次性批量添加本次下单的商品记录
                OrderDetail.objects.bulk_create(detail_list)

                # 保存订单的总价格和实付价格
                order.total_price = real_price
                order.real_price =  float(real_price - total_discount_price)
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
                if cart:  # 判断如果是空购物，则不需要再次添加cart购物车数据了。
                    pipe.hmset(f"cart_{user_id}", cart)
                pipe.execute()

                # 如果有使用了优惠券，则把优惠券和当前订单进行绑定
                if user_coupon:
                    user_coupon.order = order
                    user_coupon.save()
                    # 把优惠券从redis中移除
                    print(f"{user_id}:{user_coupon_id}")
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

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 服务端在用户选择优惠券以后重新计算订单实付价格"
git push
```



## 积分

```
实现积分功能，必须具备以下条件：
1. 用户模型中必须有积分字段credit[积分不会过期]
2. 在服务端必须有一个常量配置，表示积分与现金的换算比例
3. 订单模型中新增一个积分字段, 用于记录积分的消费和积分折算的价格
4. 新增一个积分流水模型, 用于记录积分的收支记录
   operation  操作类型
   number     积分数量
	 user     用户ID
```

我们之前在自定义用户模型的时候，已经声明了积分字段，所以此处为了方便后面开发积分功能的时候，能够在admin管理站点中进行积分的调整使用，所以我们此处在users/admin.py后台站点配置文件中，配置user用户模型的模型管理器。

先新增积分流水模型

`users/models.py`，代码：

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from stdimage import StdImageField
from django.utils.safestring import mark_safe
from model import BaseModel


# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号')
    money = models.DecimalField(max_digits=9, default=0.0, decimal_places=2, verbose_name="钱包余额")
    credit = models.IntegerField(default=0, verbose_name="积分")
    # avatar = models.ImageField(upload_to="avatar/%Y", null=True, default="", verbose_name="个人头像")
    avatar = StdImageField(variations={
            'thumb_400x400': (400, 400),   # 'medium': (400, 400),
            'thumb_50x50': (50, 50, True), # 'small': (50, 50, True),
    }, delete_orphans=True, upload_to="avatar/%Y", blank=True, null=True, verbose_name="个人头像")

    nickname = models.CharField(max_length=50, default="", null=True, verbose_name="用户昵称")

    class Meta:
        db_table = 'lf_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def avatar_small(self):
        if self.avatar:
            return mark_safe( f'<img style="border-radius: 100%;" src="{self.avatar.thumb_50x50.url}">' )
        return ""

    avatar_small.short_description = "个人头像(50x50)"
    avatar_small.allow_tags = True
    avatar_small.admin_order_field = "avatar"

    def avatar_medium(self):
        if self.avatar:
            return mark_safe( f'<img style="border-radius: 100%;" src="{self.avatar.thumb_400x400.url}">' )
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


```

订单模型新增积分字段，`orders/models.py`，代码：

```python
class Order(BaseModel):
    """订单基本信息模型"""
    status_choices = (
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
    user = models.ForeignKey(User, related_name='user_orders', on_delete=models.DO_NOTHING,verbose_name="下单用户")
    credit = models.IntegerField(default=0, null=True, blank=True, verbose_name="积分")   #新增积分

    class Meta:
        db_table = "fg_order"
        verbose_name = "订单记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s,总价: %s,实付: %s" % (self.name, self.total_price, self.real_price)
```

数据迁移

```bash
cd ~/Desktop/luffycity/luffycityapi
python manage.py makemigrations
python manage.py migrate
```

当管理员在admin运营后台中, 给用户新增积分时，需要自动生成对应的流水记录。

`users/admin.py`，代码：

```python
from django.contrib import admin
from .models import User,Credit
# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    """用户的模型管理器"""
    list_display = ["id","username","avatar_image","money","credit"]
    list_editable = ["credit"]  

    def save_model(self, request, obj, form, change):
        if change:
            """更新数据"""
            user = User.objects.get(pk=obj.id)
            has_credit = user.credit # 原来用户的积分数据
            new_credit = obj.credit  # 更新后用户的积分数据

            Credit.objects.create(
                user=user,
                number=int(new_credit - has_credit),
                operation=2,
            )

        obj.save()

        if not change:
            """新增数据"""
            Credit.objects.create(
                user=obj.id,
                number=obj.credit,
                operation=2,
            )


admin.site.register(User, UserModelAdmin)

class CreditModelAdmin(admin.ModelAdmin):
    """积分流水的模型管理器"""
    list_display = ["id","user","number","__str__"]

admin.site.register(Credit,CreditModelAdmin)
```

课程模型新增积分字段，`courses/models.py`，代码：

```python
class Course(BaseModel):
    # ....省略
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, default=0, verbose_name="课程原价")
    credit= models.IntegerField(blank=True, null=True, default=0, verbose_name="积分")
```

数据迁移

```bash
cd ~/Desktop/luffycity/luffycityapi/
python manage.py makemigrations
python manage.py migrate
```

接下来，在课程详情展示页面中新增显示当前课程可以抵扣的积分数量。`courses/serializers.py`，代码：

```python
class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """课程详情的序列化器"""
    diretion_name = serializers.CharField(source="diretion.name")
    # diretion = serializers.SlugRelatedField(read_only=True, slug_field='name')
    category_name = serializers.CharField(source="category.name")
    # 序列化器嵌套
    teacher = CourseTearchModelSerializer()

    class Meta:
        model = Course
        fields = [
            "name", "course_cover", "course_video", "level", "get_level_display",
            "description", "pub_date", "status", "get_status_display", "students","discount", "credit",
            "lessons", "pub_lessons", "price", "diretion", "diretion_name", "category", "category_name", "teacher","can_free_study"
        ]
```

因为课程模型新增了credit字段在elasticsearch搜索引擎中是没有对应的。所以我们需要在es索引模型文件新增credit字段，并在终端下手动重建索引。

`apps/courses/search_indexes.py`，代码：

```python
from haystack import indexes
from .models import Course


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
   # 中间字段声明省略
    price = indexes.DecimalField(model_attr="price")
    credit = indexes.IntegerField(model_attr="credit")  # 新增积分字段
   # 中间字段声明省略
```

重建es索引

```bash
python manage.py rebuild_index
```

接下来，我们就可以直接在admin管理站点中对课程的抵扣积分进行设置了。

客户端中展示积分相关信息，`views/Info.vue`，代码：

```vue
            <p class="course-price" v-if="course.info.discount.price >= 0">
              <span>活动价</span>
              <span class="discount">¥{{parseFloat(course.info.discount.price).toFixed(2)}}</span>
              <span class="original">¥{{parseFloat(course.info.price).toFixed(2)}}</span>
            </p>
            <p class="course-price" v-if="course.info.credit>0">
              <span>抵扣积分</span>
              <span class="discount">{{course.info.credit}}</span>
            </p>
```

效果：

![image-20220630205437762](assets/image-20220630205437762.png)

在购物车和确定订单页面中，服务端返回的购物车商品列表的数据以及勾选商品列表数据中增加返回credit积分字段。

`cart/views.py`，代码：

```python
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
from courses.models import Course


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
            # todo 同时，判断用户是否已经购买了
            course = Course.objects.get(is_show=True, is_deleted=False, pk=course_id)
        except:
            return Response({"errmsg": "当前课程不存在！"}, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self,request):
        """获取购物车中的商品列表"""
        user_id = request.user.id
        redis = get_redis_connection("cart")
        cart_hash = redis.hgetall(f"cart_{user_id}")
        """
        cart_hash = {
            // b'商品课程ID': b'勾选状态', 
            b'2': b'1', 
            b'4': b'1', 
            b'5': b'1'
        }
        """
        if len(cart_hash) < 1:
            return Response({"errmsg":"购物车没有任何商品。"})

        cart = [(int(key.decode()), bool(value.decode())) for key, value in cart_hash.items()]
        # cart = [ (2,True) (4,True) (5,True) ]
        course_id_list = [item[0] for item in cart]
        course_list = Course.objects.filter(pk__in=course_id_list, is_deleted=False, is_show=True).all()
        print(course_list)
        data = []
        for course in course_list:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_cover": course.course_cover.url,
                "price": float(course.price),
                "credit": course.credit,
                "discount": course.discount,
                "course_type": course.get_course_type_display(),
                # 勾选状态：把课程ID转换成bytes类型，判断当前ID是否在购物车字典中作为key存在，如果存在，判断当前课程ID对应的值是否是字符串"1"，是则返回True
                "selected": (str(course.id).encode() in cart_hash) and cart_hash[ str(course.id).encode()].decode() == "1"
            })
        return Response({"errmsg": "ok!", "cart": data})

    def patch(self, request):
        """切换购物车中商品勾选状态"""
        # 谁的购物车？user_id
        user_id = request.user.id
        # 获取购物车的课程ID与勾选状态
        course_id = int(request.data.get("course_id", 0))
        selected = int(bool(request.data.get("selected", True)))

        redis = get_redis_connection("cart")

        try:
            Course.objects.get(pk=course_id, is_show=True, is_deleted=False)
        except Course.DoesNotExist:
            redis.hdel(f"cart_{user_id}", course_id)
            return Response({"errmsg": "当前商品不存在或已经被下架！！"})

        redis.hset(f"cart_{user_id}", course_id, selected)
        return Response({"errmsg": "ok"})

    def put(self,request):
        """"全选 / 全不选"""
        user_id = request.user.id
        selected = int(bool(request.data.get("selected", True)))
        redis = get_redis_connection("cart")

        # 获取购物车中所有商品课程信息
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

        # 把redis中的购物车课程ID信息转换成普通列表
        cart_list = [int(course_id.decode()) for course_id in cart_hash]

        # 批量修改购物车中素有商品课程的勾选状态
        pipe = redis.pipeline()
        pipe.multi()
        for course_id in cart_list:
            pipe.hset(f"cart_{user_id}", course_id, selected)
        pipe.execute()

        return Response({"errmsg": "ok"})

    def delete(self, request):
        """从购物车中删除指定商品"""
        user_id = request.user.id
        # 因为delete方法没有请求体，所以改成地址栏传递课程ID，Django restframework中通过request.query_params来获取
        course_id = int(request.query_params.get("course_id", 0))
        redis = get_redis_connection("cart")
        redis.hdel(f"cart_{user_id}", course_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                "credit": course.credit,
                "discount": course.discount,
                "course_type": course.get_course_type_display(),
            })

        # 返回客户端
        return Response({"errmsg": "ok！", "cart": data})

```

客户端购物车与确认订单页面中的商品列表展示当前可以使用的积分数量.

`views/Cart.vue`，和 `views/Order.vue`，代码：

```vue
              <div class="item-2">
                  <router-link :to="`/project/${course_info.id}`" class="img-box l">
                    <img :src="course_info.course_cover">
                  </router-link>
                  <dl class="l has-package">
                    <dt>【{{course_info.course_type}}】 {{course_info.name}}</dt>
                    <p class="package-item" v-if="course_info.discount.type">{{ course_info.discount.type }}</p>
                    <p class="package-item" v-if="course_info.credit>0">{{course_info.credit}}积分抵扣</p>
                  </dl>
              </div>
```



客户端返回积分抵扣现金的数据。

`utils/constants.py`，代码：

```python
# 积分抵扣现金的比例，n积分:1元
CREDIT_TO_MONEY = 10
```

`coupon/views.py`，代码：

```python
import constants
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import get_user_coupon_list, get_user_enable_coupon_list


class CouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户拥有的所有优惠券"""
        user_id = request.user.id
        coupon_data = get_user_coupon_list(user_id)
        return Response(coupon_data)


class EnableCouponListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取用户本次拥有的本次下单可用所有优惠券"""
        user_id = request.user.id
        coupon_data = get_user_enable_coupon_list(user_id)
        return Response({
            "errmsg":"ok",
            'has_credit': request.user.credit,
            'credit_to_money': constants.CREDIT_TO_MONEY,
            "coupon_list": coupon_data
        })

```



### 客户端获取当前用户本地下单时可用优惠券列表并获取当前用户拥有的积分。

`api/order.js`，新增属性，`credit_to_money`与`has_credit`，代码：

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
  create_order(user_coupon_id, token){
    // 生成订单
    return http.post("/orders/",{
        pay_type: this.pay_type,
        user_coupon_id,
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
  }
})

export default order;
```

`views/Order.vue`，代码：

```vue

<script setup>
// ... 代码省略
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

// ... 代码省略 
</script>
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 积分功能实现-上"
git push
```



### 在确认订单页面中，查询当前本次购买可使用积分抵扣的商品列表以及最大抵扣积分数量。

获取用户本次下单能使用的最大抵扣积分，需要考虑当前用户拥有的积分数量。

```text
1. 当用户积分 > 本次下单可使用积分抵扣总数量:
   用户最高可使用积分=本次下单的可使用积分数量

2. 当用户积分 < 本次购课可使用积分抵扣总数量:
  用户最高可使用积分=用户拥有的所有积分
```

客户端切换不同的优惠类型时，重置积分和优惠券的选择信息，同时当用户选择了积分抵扣时，发送积分数量到服务端。

`views/Order.vue`，代码：

```vue
<div class="coupon-content code" v-else>
                <div class="input-box">
                  <el-input-number v-model="order.credit" :step="1" :min="0" :max="order.max_use_credit"></el-input-number>
                  <a class="convert-btn" @click="conver_credit">兑换</a>
                  <a class="convert-btn" @click="max_conver_credit">最大积分兑换</a>
                </div>
                <div class="converted-box">
                  <p class="course-title" v-for="course in order.credit_course_list">
                    课程:<span class="c_name">{{course.name}}</span>
                    <span class="discount-cash">{{course.credit}}积分抵扣：<em>{{ (course.credit/order.credit_to_money).toFixed(2) }}</em>元</span>
                  </p>
                </div>
                <p class="error-msg">本次订单最多可以使用{{order.max_use_credit}}积分，您当前拥有{{order.has_credit}}积分。({{order.credit_to_money}}积分=1元)</p>
                <p class="tip">说明：每笔订单只能使用一次积分，并只有在部分允许使用积分兑换的课程中才能使用。</p>
              </div>
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

`src/api/order.js`，代码：

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
  }
})

export default order;
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 积分功能实现-中"
git push
```



### 服务端在下单时 如果用户使用积分，则重新计算最终实付价格

序列化器，`orders/serializers.py`，代码:

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
    pay_link = serializers.CharField(read_only=True)
    user_coupon_id = serializers.IntegerField(write_only=True, default=-1)

    class Meta:
        model = Order
        fields = ["pay_type", "id", "order_number", "pay_link", "user_coupon_id", "credit"]
        read_only_fields = ["id", "order_number"]
        extra_kwargs = {
            "pay_type": {"write_only": True},
             "credit": {"write_only":True},
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

```python
关于积分扣除和优惠券的使用问题！
我们下单的时候就要扣除积分或者记录优惠券和订单的关系，在用户如果取消订单或者订单超时以后，我们则返还扣除的积分或清除优惠券使用记录的订单号，如果结算支付成功，则记录积分的流水或者优惠券使用记录的状态。
```

提交代码版本

```bash
cd ~/Desktop/luffycity
git add .
git commit -m "feature: 积分功能实现-下"
git push
```



