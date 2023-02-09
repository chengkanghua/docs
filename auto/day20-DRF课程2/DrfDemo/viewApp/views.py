from django.shortcuts import render

# Create your views here.
from rest_framework import serializers

from rest_framework.views import APIView
from viewApp.models import Author, Book, Publish
from rest_framework.response import Response


class AuthorSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=32)
    age = serializers.IntegerField()

    def create(self, validated_data):
        # 向数据库Author添加记录
        author_obj = Author.objects.create(**validated_data)
        return author_obj

    def update(self, instance, validated_data):
        Author.objects.filter(pk=instance.pk).update(**validated_data)

        return instance


class AuthorView(APIView):

    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializers(instance=authors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializers(data=request.data)
        # 数据校验:  验证通过的数据：serializer.validated_data   验证失败的数据serializer.errors
        if serializer.is_valid():  # 所有的字段通过验证
            print("serializer.validated_data", serializer.validated_data)
            serializer.save()  # if instance:serializer.update()   else:serializer.create()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AuthorDetailView(APIView):
    def get(self, request, id):
        author = Author.objects.get(pk=id)
        serializer = AuthorSerializers(instance=author, many=False)

        return Response(serializer.data)

    def put(self, request, id):
        author = Author.objects.get(pk=id)
        serializer = AuthorSerializers(instance=author, data=request.data)
        if serializer.is_valid():
            # 更新 # if instance:serializer.update()   else:serializer.create()
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        Author.objects.get(pk=id).delete()
        return Response()


#########################################################################################

# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(APIView):
#
#     def get(self, request):
#         publish_list = Publish.objects.all()
#         serializer = PublishSerializers(instance=publish_list, many=True)
#
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PublishSerializers(data=request.data)
#         # 数据校验:  验证通过的数据：serializer.validated_data   验证失败的数据serializer.errors
#         if serializer.is_valid():  # 所有的字段通过验证
#             print("serializer.validated_data", serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class PublishDetailView(APIView):
#
#     def get(self, request, id):
#         publish = Publish.objects.get(pk=id)
#         serializer = PublishSerializers(instance=publish, many=False)
#         print("serializer.data", serializer.data)
#
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         publish = Publish.objects.get(pk=id)
#         serializer = PublishSerializers(instance=publish, data=request.data)
#         if serializer.is_valid():
#             # 更新 # if instance:serializer.update()   else:serializer.create()
#             serializer.save()
#             return Response(serializer.data)
#
#         else:
#             return Response(serializer.errors)
#
#     def delete(self, request, id):
#         Publish.objects.get(pk=id).delete()
#         return Response()


# #########################################################################################
#
# from rest_framework.views import APIView
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
#     queryset = Publish.objects
#     serializer_class = PublishSerializers
#
#     def get(self, request):
#
#         # serializer = self.serializer_class(instance=self.queryset, many=True)
#         # serializer = self.get_serializer_class()(instance=self.queryset, many=True)
#         serializer = self.get_serializer(instance=self.get_queryset(), many=True)
#
#         return Response(serializer.data)
#
#     def post(self, request):
#
#         serializer = self.get_serializer(data=request.data)
#
#         # 数据校验:  验证通过的数据：serializer.validated_data   验证失败的数据serializer.errors
#         if serializer.is_valid():  # 所有的字段通过验证
#             print("serializer.validated_data", serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class PublishDetailView(GenericAPIView):
#
#     queryset = Publish.objects
#     serializer_class = PublishSerializers
#
#     def get(self, request, pk):
#
#         serializer = self.get_serializer(instance=self.get_object(), many=False)
#         print("serializer.data", serializer.data)
#
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#
#         serializer = self.get_serializer(instance=self.get_object(), data=request.data)
#         if serializer.is_valid():
#             # 更新 # if instance:serializer.update()   else:serializer.create()
#             serializer.save()
#             return Response(serializer.data)
#
#         else:
#             return Response(serializer.errors)
#
#     def delete(self, request, pk):
#         self.get_object().delete()
#         return Response()


# #########################################################################################
#
# from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, \
#     DestroyModelMixin
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = Publish.objects
#     serializer_class = PublishSerializers
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class PublishDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Publish.objects
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


#########################################################################################


# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(ListCreateAPIView):
#     queryset = Publish.objects
#     serializer_class = PublishSerializers
#
#
# class PublishDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Publish.objects
#     serializer_class = PublishSerializers


# #########################################################################################
#
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.viewsets import ViewSetMixin
#
#
# class PublishSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = "__all__"
#
#
# class PublishView(ViewSetMixin, APIView):
#     def list(self, request):
#         return Response("list...")
#
#     def create(self, request):
#         return Response("create...")
#
#     def single(self, request, pk):
#         return Response("single...")
#
#     def edit(self, request, pk):
#         return Response("edit...")


#########################################################################################

# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.viewsets import ViewSetMixin
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,ListModelMixin,CreateModelMixin

class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"

    def validate_name(self, value):

        if value.endswith("出版社"):
            return value
        else:
            #  验证失败
            raise serializers.ValidationError(" 出版社名称没有以出版社结尾！")


# class PublishView(ViewSetMixin,GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,ListModelMixin,CreateModelMixin):
#
#     queryset = Publish.objects
#     serializer_class = PublishSerializers

from rest_framework.viewsets import ModelViewSet


class PublishView(ModelViewSet):
    queryset = Publish.objects
    serializer_class = PublishSerializers

    def list(self, request, *args, **kwargs):
        pass


#########################################################################################


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32)
    price = serializers.IntegerField()
    pub_date = serializers.DateField()

    publish = serializers.PrimaryKeyRelatedField(queryset=Publish.objects)
    # publish = serializers.SlugRelatedField(queryset=Publish.objects,slug_field="email")

    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects, many=True)

    def create(self, validated_data):
        print("validated_data",validated_data)

        authors = validated_data.pop("authors")
        book = Book.objects.create(**validated_data)
        book.authors.add(*authors)
        return book


class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



