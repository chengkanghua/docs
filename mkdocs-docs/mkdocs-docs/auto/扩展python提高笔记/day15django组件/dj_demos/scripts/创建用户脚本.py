import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_demos.settings")
django.setup()

from web import models
from account.utils.encrypt import md5
models.UserInfo.objects.create(
    login_type=1,
    username="wupeiqi",
    password=md5("123123"),
)
