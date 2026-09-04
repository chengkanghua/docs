from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('verify/', verify_jwt_token),  # 这是只是校验token有效性
    path(r'refresh_jwt_token/', refresh_jwt_token),  # 校验并生成新的token
]
