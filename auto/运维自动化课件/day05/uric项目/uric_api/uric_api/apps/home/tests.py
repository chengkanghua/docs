from django.test import TestCase

# Create your tests here.


import base64, json

data = {
    'typ': 'JWT',
    'alg': 'HS256'
}

header = base64.b64encode(json.dumps(data).encode()).decode()
print(header)

import base64, json

data = {
    "sub": "1234567890",
    "exp": "3422335555",
    "name": "yuan",
    "admin": True,
}

preload = base64.b64encode(json.dumps(data).encode()).decode()
print(preload)



