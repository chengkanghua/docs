from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=32, default='')
    # 文章正文，使用的是TextField
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    content = models.TextField(null=True)

    def __str__(self):
        return self.title
