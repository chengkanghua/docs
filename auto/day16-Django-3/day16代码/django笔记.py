ORM

python模型类映射sql的table表
python模型类对象映射sql的table表记录
python模型类成员变量映射sql的table表的字段（包含类型和约束）


# models.py
class Stu(models.Model):
   name = models.CharField(max_length=32)
   ...

python manage.py  makemigrations
python manage.py  migrate


# 增
# 方式1
stu = Stu(name="yuan",...)
stu.save()

# 方式2
stu = Stu.objects.create(name="yuan",...)

# 查询API（重点：queryset对象和模型类对象）


class queryset():
	 def order_by():
	 	pass

	 def count():
	 	pass

	 def value():
	 	pass

ret = Stu.objects.all()   # queryset([stu1,stu2,....])

ret = Stu.objects.filter(查询条件) # queryset([stu1,stu2,....])

ret = Stu.objects.filter(name__contains="张",age=22) 
ret = Stu.objects.filter(name__contains="张").filter(age=22) 


ret = Stu.objects.exclude(查询条件) # queryset([stu1,stu2,....])

ret = Stu.objects.get(查询条件) # 模型类对象（有且只有一条记录）

ret = Stu.objects.all().order_by("-age") #  # queryset([stu1,stu2,....])
ret = Stu.objects.all().order_by("-age").count() #  # queryset([stu1,stu2,....])

ret = Stu.objects.filter(查询条件).values("name","age") # queryset[{"name":"yuan"},{"name":"rain"}]
ret = Stu.objects.filter(查询条件).values_list("name","age") # queryset[("yuan",22),("rain",22)]
ret = Stu.objects.filter(查询条件).values_list("name","age").distinct()

# 修改update
queryset.update(字段=值)

# 删除 delete
queryset.delete()
模型类对象.delete()




book

id title price  publish_id   
                    1
                    1 
publish

name mail addr


author

id name   ad_id(unique)
1  rain     1
2  alvin    1


authorDetail
gender tel   gf 
male   110   xxx
male   911   yyy

book_author

id book_id author_id
 1    1        1
 2    1        2
 3    2        2   



局部刷新
异步请求

















__