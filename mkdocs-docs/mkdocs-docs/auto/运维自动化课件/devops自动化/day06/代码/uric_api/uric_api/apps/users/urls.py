from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [

    path('login/', obtain_jwt_token),
]
