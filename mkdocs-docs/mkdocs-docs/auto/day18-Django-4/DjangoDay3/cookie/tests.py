from django.test import TestCase

# Create your tests here.


import hashlib

md5 = hashlib.md5(b"xxx")

md5.update(b"yuan is a teacher!")
print(md5.hexdigest())
print(len(md5.hexdigest()))
