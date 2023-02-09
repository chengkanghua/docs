from django.db import models

# Create your models here.
from django.db import models
from uric_api.utils.models import BaseModel

class CmdTemplateCategory(BaseModel):
    class Meta:
        db_table = "cmd_template_category"
        verbose_name = "模板分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CmdTemplate(BaseModel):
    category = models.ForeignKey('CmdTemplateCategory', on_delete=models.CASCADE,verbose_name='模板类别')
    cmd = models.TextField(verbose_name='模板内容')

    class Meta:
        db_table = "cmd_template"
        verbose_name = "指令模板"
        verbose_name_plural = verbose_name