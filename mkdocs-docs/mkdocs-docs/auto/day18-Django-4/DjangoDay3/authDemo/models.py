from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class NewUserInfo(User):
    tel = models.CharField(max_length=12)