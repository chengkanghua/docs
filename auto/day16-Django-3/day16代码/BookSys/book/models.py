from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # 999999.99
    publishDate = models.DateField()

    # 一对多的关联属性,创建关联字段
    publish = models.ForeignKey("Publish",related_name="book_list", on_delete=models.CASCADE)

    # 多对多的关联属性，创建关系表
    authors = models.ManyToManyField("Author",related_name="books", db_table="book2author")  # book_authors

    def __str__(self):
        return self.title

class Publish(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)
    email = models.CharField(max_length=32)


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    ad = models.OneToOneField("AuthorDetail", on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    tel = models.IntegerField()
    addr = models.CharField(max_length=32)

# class Auhtor2Book(models.Model):
#     book = models.ForeignKey("Book", on_delete=models.CASCADE)
#     author = models.ForeignKey("Author", on_delete=models.CASCADE)
