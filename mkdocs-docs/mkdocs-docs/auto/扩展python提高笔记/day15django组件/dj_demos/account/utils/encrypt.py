import hashlib
from django.conf import settings


def md5(data_string):
    md5_object = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    md5_object.update(data_string.encode('utf-8'))
    return md5_object.hexdigest()
