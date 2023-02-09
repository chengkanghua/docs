from django.shortcuts import render, HttpResponse

# Create your views here.
from .models import Book, Publish, Author

from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response

from rest_framework.mixins import UpdateModelMixin


# 一 ---------------------------   基于APIView的接口实现  ---------------------------


# 针对模型设计序列化器
# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()  # required=False
#     date = serializers.DateField(source="pub_date")
#
#     def create(self, validated_data):
#         # 添加数据逻辑
#         new_book = Book.objects.create(**self.validated_data)
#
#         return new_book
#
#     def update(self, instance, validated_data):
#         # 更新逻辑
#         # serializer.validated_data
#         Book.objects.filter(pk=instance.pk).update(**validated_data)
#         updated_book = Book.objects.get(pk=id)
#         return updated_book


class BookSerializers(serializers.ModelSerializer):
    date = serializers.DateField(source="pub_date")

    class Meta:
        model = Book
        # fields = "__all__"
        # fields = ["title", "price"]
        exclude = ["pub_date"]


from rest_framework.authentication import SessionAuthentication

# class MyAuthentication(object):
#     def authenticate(self, request):
#         return ("yuan", None)

from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated, IsAuthenticated


# class MyPermission(BasePermission):
#     def has_permission(self, request, view):
#
#         return False


class BookView(APIView):
    authentication_classes = [SessionAuthentication, ]

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        查看所有书籍

        序列化的过程
        temp = []

        for obj in book_list:
            d = {}
            d["title"] = obj.title
            d["price"] = obj.price
            # d["date"] = obj.pub_date

            temp.append(d)

        :param request:
        :return:
        '''
        print("request.user:::", request.user)
        # 获取所有的书籍
        book_list = Book.objects.all()  # queryset[book01,book02,...]
        # 构建序列化器对象:
        serializer = BookSerializers(instance=book_list, many=True)
        return Response(serializer.data)  # 针对serializer.instance

    def post(self, request):
        # 获取请求数据
        print("data", request.data)
        # 构建序列化器对象
        serializer = BookSerializers(data=request.data)
        # 校验数据
        if serializer.is_valid():  # 返回一个布尔值，所有字段皆通过才返回True，serializer.validated_data   serializer.errors
            # 数据校验通过,将数据插入到数据库中
            # new_book = Book.objects.create(**serializer.validated_data)
            serializer.save()
            return Response(serializer.data)  # 针对serializer.instance序列化

        else:
            # 校验失败
            return Response(serializer.errors)


class BookDetailView(APIView):

    def get(self, request, id):
        '''
        序列化的过程

        d = {}
        d["title"] = obj.title
        d["price"] = obj.price
        # d["date"] = obj.pub_date

        :param request:
        :param id:
        :return:
        '''
        book = Book.objects.get(pk=id)

        # 序列化传参instance，反序列化传参data
        serializer = BookSerializers(instance=book, many=False)

        return Response(serializer.data)  # 针对serializer.instance序列化

    def put(self, request, id):
        # 获取提交的更新数据
        print("data:", request.data)
        update_book = Book.objects.get(pk=id)
        # 构建序列化器对象
        serializer = BookSerializers(instance=update_book, data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)  # 针对serializer.instance序列化
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        Book.objects.get(pk=id).delete()
        return Response()


# 二 ---------------------------   基于GenericAPIView的接口实现  ---------------------------


# from rest_framework.generics import GenericAPIView
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(GenericAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self, request):
#
#         serializer = self.get_serializer(instance=self.get_queryset(), many=True)
#
#         return Response(serializer.data)  # 针对serializer.instance
#
#     def post(self, request):
#         # 获取请求数据
#         print("data", request.data)
#         # 构建序列化器对象
#         serializer = self.get_serializer(data=request.data)
#         # 校验数据
#         if serializer.is_valid():  # 返回一个布尔值，所有字段皆通过才返回True，serializer.validated_data   serializer.errors
#             # 数据校验通过,将数据插入到数据库中
#             # new_book = Book.objects.create(**serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data)  # 针对serializer.instance序列化
#
#         else:
#             # 校验失败
#             return Response(serializer.errors)
#
#
# class PublishDetailView(GenericAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self, request, pk):
#
#         # 序列化传参instance，反序列化传参data
#         serializer = self.get_serializer(instance=self.get_object(), many=False)
#
#         return Response(serializer.data)  # 针对serializer.instance序列化
#
#     def put(self, request, pk):
#         # 获取提交的更新数据
#         print("data:", request.data)
#
#         # 构建序列化器对象
#         serializer = self.get_serializer(instance=self.get_object(), data=request.data)
#
#         if serializer.is_valid():
#
#             serializer.save()
#
#             return Response(serializer.data)  # 针对serializer.instance序列化
#         else:
#             return Response(serializer.errors)
#
#     def delete(self, request, pk):
#         self.get_object().delete()
#
#         return Response()
#
# class AuthorSerializers(serializers.ModelSerializer):
#         class Meta:
#             model = Author
#             fields = "__all__"
#
#
#
#
# class AuthorView(GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request):
#
#         serializer = self.get_serializer(instance=self.get_queryset(), many=True)
#
#         return Response(serializer.data)  # 针对serializer.instance
#
#     def post(self, request):
#         # 获取请求数据
#         print("data", request.data)
#         # 构建序列化器对象
#         serializer = self.get_serializer(data=request.data)
#         # 校验数据
#         if serializer.is_valid():  # 返回一个布尔值，所有字段皆通过才返回True，serializer.validated_data   serializer.errors
#             # 数据校验通过,将数据插入到数据库中
#             # new_book = Book.objects.create(**serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data)  # 针对serializer.instance序列化
#
#         else:
#             # 校验失败
#             return Response(serializer.errors)
#
# class AuthorDetailView(GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request, pk):
#
#         # 序列化传参instance，反序列化传参data
#         serializer = self.get_serializer(instance=self.get_object(), many=False)
#
#         return Response(serializer.data)  # 针对serializer.instance序列化
#
#     def put(self, request, pk):
#         # 获取提交的更新数据
#         print("data:", request.data)
#
#         # 构建序列化器对象
#         serializer = self.get_serializer(instance=self.get_object(), data=request.data)
#
#         if serializer.is_valid():
#
#             serializer.save()
#
#             return Response(serializer.data)  # 针对serializer.instance序列化
#         else:
#             return Response(serializer.errors)
#
#     def delete(self, request, pk):
#         self.get_object().delete()
#
#         return Response()
#

# 三 ---------------------------   基于MinIN混合类的接口实现  ---------------------------
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin

# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class PublishDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
#
#     def put(self, request, pk):
#         return self.update(request, pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk)
#
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = "__all__"
#
#
# class AuthorView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class AuthorDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
#
#     def put(self, request, pk):
#         return self.update(request, pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk)

# 四 --------------------------- 再封装  ---------------------------

# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(ListCreateAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#
# class PublishDetailView(RetrieveUpdateAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers
#
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = "__all__"
#
#
# class AuthorView(ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#
# class AuthorDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers


# 五 --------------------------- ViewSet类:重新构建了分发机制  ---------------------------


from rest_framework.viewsets import ViewSet
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(ViewSet):
#
#     def get_all(self,request):
#         return Response("查看所有资源")
#
#     def add_object(self,request):
#         return Response("添加资源")
#
#     def get_object(self,request,pk):
#         return Response("查看单一资源")
#
#     def update_object(self,request,pk):
#         return Response("更新单一资源")
#
#     def delete_object(self,request,pk):
#         return Response("删除单一资源")

# 六 ---------------------------   ---------------------------

from rest_framework.viewsets import GenericViewSet

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import ModelViewSet


class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


#
# class PublishView(GenericViewSet, ListModelMixin, CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSerializers


class PublishView(ModelViewSet):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers


class AuthorView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
