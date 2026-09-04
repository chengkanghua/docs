from django.shortcuts import render

# Create your views here.


from rest_framework.viewsets import ModelViewSet
from .models import Student
from app01.sers import StudentModelSerializer


# Create your views here.
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer



