from django.db import models

# Create your models here.


'''


create table Student 

   id  int primary key
   name varchar(32) unique 
   birth_day  date 


'''

# 声明模型类


class Student(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,unique=True)
    age = models.IntegerField(default=20,null=True)
    birth_day = models.DateField()
    isMarried = models.BooleanField(default=False)

    class Meta:
        db_table = 'tb_student'


    def __str__(self):
        return self.name