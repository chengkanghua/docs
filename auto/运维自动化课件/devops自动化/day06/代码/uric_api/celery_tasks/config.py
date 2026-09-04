# 为celery设置django相关的环境变量，方便将来在celery中调用django的代码
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uric_api.settings.dev')
from django.conf import settings

# 设置celery接受任务的队列
broker_url = 'redis://:@127.0.0.1:6379/14'
# 设置celery保存任务执行结果的队列
result_backend = 'redis://:@127.0.0.1:6379/15'

# celery 的启动工作数量设置[进程数量]
CELERY_WORKER_CONCURRENCY = 20

# 任务预取功能，就是每个工作的进程／线程在获取任务的时候，会尽量多拿 n 个，以保证获取的通讯成本可以压缩。
WORKER_PREFETCH_MULTIPLIER = 20

# 非常重要,有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 100

# 禁用所有速度限制，如果网络资源有限，不建议开足马力。
worker_disable_rate_limits = True

# celery beat配置
CELERY_ENABLE_UTC = False
settings.USE_TZ = True
timezone = settings.TIME_ZONE
# 保存定时任务记录的驱动类，使用mysql数据库来进行定时任务
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'