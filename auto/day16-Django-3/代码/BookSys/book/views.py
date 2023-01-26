from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from book.models import Book, Publish, Author, AuthorDetail


def add(request):
    # 一对多
    # publish_object = Publish.objects.get(pk=1)
    # book = Book.objects.create(title="西游记",price=199,publishDate="2012-12-12",publish=publish_object)

    # book = Book.objects.create(title="飘", price=399, publishDate="2011-12-12", publish_id=2)
    # book.authors.add(1, 2)
    # print(book.title)
    # print(book.publish_id)
    # print(book.publish)  # Publish object (2) book关联的出版社对象
    # print(book.publish.name)  # book关联的出版社对象,西瓜出版社

    # 一对一的添加
    # author = Author.objects.create(name="rain", age=26, ad_id=2)

    # 多对多的增删改查
    # book = Book.objects.get(title="西游记")
    # 添加关系表记录
    # yuan = Author.objects.get(name="yuan")
    # rain = Author.objects.get(name="rain")
    #
    # book.authors.add(yuan, rain)
    # book.authors.add(2)
    # l = [1, 2]
    # book.authors.add(*l)
    # 删除和更新关系表记录
    # book.authors.remove(2)
    # book.authors.clear()
    # book.authors.set([1,2])
    # 关系表记录查询
    # 查询飘的所有作者的名字
    # book = Book.objects.get(title="飘")
    # ret = book.authors.all() # queryset:[author1,author2]
    # ret = book.authors.all().values("name", "age")  # queryset:[author1,author2]
    # print(ret)

    # 反向查询
    # 查询yuan作者出版了的书籍名称
    author = Author.objects.get(name="yuan")
    ret = author.books.all()  # queryset:[book1,book2]
    print(ret)

    # 查询苹果出版社出版的书籍名称
    publish = Publish.objects.get(name="苹果出版社")
    ret = publish.book_list.all()
    print(ret)


    return HttpResponse("添加成功")


def index(request):
    import time
    time.sleep(10)
    book_list = Book.objects.all()

    return render(request, "index.html", {"book_list": book_list})


def addbook(request):
    if request.method == "GET":
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()

        return render(request, "addbook.html", {"publish_list": publish_list, "author_list": author_list})
    else:

        # print(request.POST)
        # print(request.POST.getlist("authors"))
        authors = request.POST.getlist("authors")
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        data.pop("authors")

        book = Book.objects.create(**data)
        # 绑定多对多的关系
        book.authors.add(*authors)

        return redirect("/")


def deletebook(request, del_id):
    if request.method == "GET":

        return render(request, "deletebook.html")
    else:

        Book.objects.get(id=del_id).delete()

        return redirect("/")
