from django.shortcuts import render, HttpResponse

# Create your views here.
from django.views import View

from rest_framework.views import APIView
from drfdemo.models import Student, Publish, Book, Author

from rest_framework import serializers
from rest_framework.response import Response


class StudentSerializer(serializers.Serializer):
    names = serializers.CharField(source="name", max_length=5)
    sex = serializers.BooleanField()

    # age = serializers.IntegerField()
    # class_null = serializers.CharField()

    def create(self, validated_data):
        # 插入记录
        print("validated_data", self.validated_data)
        instance = Student.objects.create(**self.validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance


class StudentView(APIView):

    def get(self, request):
        # 查看所有资源
        # print(request.GET)
        # print(request.query_params)

        students = Student.objects.all()

        # [Student,Student,Student,....]
        # [{},{},{}]

        serializer = StudentSerializer(instance=students, many=True)

        return Response(serializer.data)

    def post(self, request):
        # post请求
        print(request.data, type(request.data))

        serializer = StudentSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

            serializer.save()  # serializer.create

            return Response(serializer.data)


        except Exception as e:
            print("e", e)
            print("serializer.errors", serializer.errors)
            return Response(serializer.errors)


class StudentDetailView(APIView):

    def get(self, reqeust, id):
        student = Student.objects.get(pk=id)
        serializer = StudentSerializer(instance=student, many=False)
        return Response(serializer.data)

    def delete(self, reqeust, id):
        Student.objects.get(pk=id).delete()
        return Response()

    def put(self, request, id):

        # post请求

        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # # 插入记录
            # print("validated_data", serializer.validated_data)
            # n = Student.objects.filter(pk=id).update(**serializer.validated_data)
            # print("n", n)
            #
            # stu = Student.objects.get(id=id)
            # ser = StudentSerializer(instance=stu, many=False)

            serializer.save()  # instance.update(serializer.validated_data)

            return Response(serializer.data)

        else:
            print("serializer.errors", serializer.errors)
            return Response(serializer.errors)


###################################################################################


class PublishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        # fiedls = "__all__"
        fields = ["name", "email"]


class PublishView(APIView):
    def get(self, reqeust):
        publishes = Publish.objects.all()
        ps = PublishSerializer(instance=publishes, many=True)
        return Response(ps.data)

    def post(self, request):
        print(request.data, type(request.data))

        serializer = PublishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # create方法 将符合条件的数据插入到数据库
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublishDetailView(APIView):

    def get(self, reqeust, id):
        publish = Publish.objects.get(pk=id)
        ps = PublishSerializer(instance=publish, many=False)
        return Response(ps.data)

    def delete(self, request, id):
        Publish.objects.get(pk=id).delete()
        return Response()

    def put(self, request, id):
        # post请求
        instance = Publish.objects.get(pk=id)
        serializer = PublishSerializer(data=request.data, instance=instance)

        if serializer.is_valid():
            serializer.save()  # instance的 update
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


#############################################################################

# from rest_framework.generics import GenericAPIView
#
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ["name", "age"]
#
#
# class AuthorView(GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self, reqeust):
#         # serializer = self.serializer_class(instance=self.queryset,many=True)
#         serializer = self.get_serializer(instance=self.get_queryset(), many=True)
#
#         return Response(serializer.data)
#
#     def post(self, request):
#
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()  # create方法 将符合条件的数据插入到数据库
#             return Response(serializer.data)
#         else:
#
#             return Response(serializer.errors)
#
#
# class AuthorDetailView(GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self, request, pk):  # url的pk名
#         serializer = self.get_serializer(instance=self.get_object(), many=False)
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         self.get_object().delete()
#         return Response()
#
#     def put(self, request, id):
#         # post请求
#         instance = self.get_object()
#         serializer = self.get_serializer(data=request.data, instance=instance)
#
#         if serializer.is_valid():
#             serializer.save()  # instance的 update
#             return Response(serializer.data)
#
#         else:
#             return Response(serializer.errors)


############################################################################


# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, \
#     UpdateModelMixin
#
# from rest_framework.generics import GenericAPIView
#
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ["name", "age"]
#
#
# class AuthorView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self, reqeust):
#         return self.list(reqeust)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class AuthorDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#
#     def get(self, request, pk):  # url的pk名
#         return self.retrieve(request)
#
#     def delete(self, request, pk):
#         return self.destroy(request)
#
#     def put(self, request, pk):
#         return self.update(request)


############################################################################

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id","name", "age"]


class AuthorView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
