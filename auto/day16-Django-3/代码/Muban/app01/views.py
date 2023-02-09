from django.shortcuts import render, HttpResponse
import datetime
import json


# Create your views here.
class Stu(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


def index(request):
    name = "yuan"
    books = ["西游记", "三国演义", "金瓶梅", "红楼梦"]
    # books = []
    info = {"name": "yuan", "age": 22}

    s1 = Stu("rain", 23)
    s2 = Stu("alvin", 24)
    s3 = Stu("yuan", 25)
    s4 = Stu("eric", 26)

    stu_list = [s1, s2, s3, s4]

    now = datetime.datetime.now()

    age = 10
    fileSize = 20343423131231

    link = '<a href="http://www.baidu.com">click</a>'
    # link = '<script>alert(123)</script>'

    user = "yuan"
    score = 56

    book_list1 = [
        {"id": 11, "name": "python基础入门", "price": 130.00},
        {"id": 17, "name": "Go基础入门", "price": 230.00},
        {"id": 23, "name": "PHP基础入门", "price": 330.00},
        {"id": 44, "name": "Java基础入门", "price": 730.00},
        {"id": 51, "name": "C++基础入门", "price": 300.00},
        {"id": 56, "name": "C#基础入门", "price": 100.00},
        {"id": 57, "name": "前端基础入门", "price": 380.00},
    ]

    # return render(request, "index_back.html", {"name": name, "books": books,"info":info})
    return render(request, "index.html", locals())


def order(request):
    return render(request, "order.html")


#############################################################################################


from app01.models import Student


def add_stu(request):
    # 方式1
    # s1 = Student(name="alvin",age=23,birth_day="1987-12-12")
    # print(s1.id)
    # s1.save()
    # print(s1.id)

    # 方式2
    s2 = Student.objects.create(name="eric", age=24, birth_day="1999-12-12")
    print(s2.id)
    print(s2.name)

    return HttpResponse("添加成功")


def select_stu(request):
    # （1）all() 返回值queryset对象
    # student_list = Student.objects.all()
    '''
    
  select * from tb_student; 
+----+-------+------------+------+-----------+
| id | name  | birth_day  | age  | isMarried |
+----+-------+------------+------+-----------+
|  1 | yuan  | 1998-12-12 |   23 |         0 |
|  2 | alvin | 1987-12-12 |   23 |         0 |
|  3 | rain  | 1999-12-12 |   24 |         0 |
|  7 | eric  | 1999-12-12 |   24 |         0 |
+----+-------+------------+------+-----------+
    
    class Queryset():
         pass
         
     s1 = Student(1,yuan,1998-12-12 ,23,0)    
     s2 = Student(2,alvin,1998-12-12 ,23,0)    
     s3 = Student(3,rain,1998-12-12 ,23,0)    
     s4 = Student(4,eric,1998-12-12 ,23,0) 
     
     q = Queryset([s1,s2,s3,s4]) 
     

    
    '''
    # print("student_list",student_list,type(student_list))
    #
    # for stu in student_list:
    #     print(stu.name,stu.age)

    # （2）filter() 返回值queryset对象

    # q2 = Student.objects.filter(age=24)
    # print(q2)

    # （3）get() 返回值一个模型类对象（有且只有一条记录）
    # s = Student.objects.get(name="yuan")
    # print(s.name)

    # (4) exclude:排除符合条件的记录， 返回值queryset对象
    # Student.objects.exclude()

    # （5）first() last():返回值一个模型类对象

    # Student.objects.all().first()

    # （6）sort: 返回值queryset对象
    q3 = Student.objects.all().order_by("-age", "-id").reverse()
    print(q3)

    # (7) count()
    # n = Student.objects.all().count()
    # print(n)

    # 链式操作
    # Student.objects.all().filter(age=24).order_by("-id").count()

    # (8) values方法
    ret = Student.objects.all().values("name", "age")
    '''

      select name,age from tb_student; 
    +----+-------+-----------
    |    | name  | | age  | 
    +----+-------+-----------
    |    | yuan  |    23 |     
    |    | alvin |    23 |     
    |    | rain  |    24 |    
    |    | eric  |    24 |   
    +----+-------+----------

        class Queryset():
             pass

         s1 = {"name":"yuan","age":23}
         s2 = {"name":"alvin","age":23}
         s3 = {"name":"rain","age":24}
         s4 = {"name":"eric","age":24}
       

         q = Queryset([s1,s2,s3,s4]) 



        '''
    print(ret)

    # (9) values_ list方法
    ret = Student.objects.all().values_list("name", "age")
    print(ret)

    # (10)   distinct()
    ret = Student.objects.all().values("age").distinct()
    print(ret)

    return HttpResponse("查询成功")


def delete_stu(request, del_id):
    # Student.objects.filter(id=del_id).delete()
    try:
        Student.objects.get(id=del_id).delete()
    except:
        pass

    return HttpResponse("删除成功")


def update_stu(request, update_id):
    # 方式1
    # s1 = Student.objects.get(id=update_id)
    # s1.name = "RAIN"
    # s1.save()

    # 方式2
    Student.objects.filter(id=update_id).update(name="RAIN123")

    return HttpResponse("更新成功")


def select_stu2(request):
    from django.db.models import F, Q
    # 模糊查询
    # ret = Student.objects.filter(age__gt=20).values("name", "age")
    # ret = Student.objects.filter(birth_day__=1999).values("name", "age")

    # F与Q查询
    ret = Student.objects.filter(height__gt=F("weight")).values("name", "age")
    ret = Student.objects.filter(~Q(height__gt=170) | Q(age=23)).values("name", "age")

    # 聚合查询
    from django.db.models import Sum, Count, Avg, Max, Min

    ret = Student.objects.all().aggregate(avg_a=Avg("age"))  # {"avg_a":22}
    print(ret)

    # 分组查询 group by
    #  查询每个班级最高的的学生
    ret = Student.objects.all().values("class_name").annotate(c= Max("height")) # 返回字典的queryset
    print(ret)

    return HttpResponse(json.dumps(list(ret)))
