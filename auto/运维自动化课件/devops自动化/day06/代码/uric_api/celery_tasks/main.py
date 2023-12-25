import os

# 为celery设置django相关的环境变量，方便将来在celery中调用django的代码
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uric_api.settings.dev')

from celery import Celery
from . import config

# 创建celery实例对象[可以以项目名作为名称，或者以项目根目录名也可以]
app = Celery('uric_api')

# 从配置文件中加载celery的相关配置
app.config_from_object(config)

# 设置app自动加载任务
app.autodiscover_tasks([
    'celery_tasks', # celery会自动得根据列表中对应的目录下的tasks.py 进行搜索注册
])