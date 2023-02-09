import hashlib
import uuid

# 哈希算法是基于计算机的二进制来进行哈希计算的
# 生成随机的统一标记符
print(uuid.uuid4())
# 使用uuid生成一个随机字符串，进行哈希加密
sha = hashlib.sha256()
# 指定加密的数据
sha.update(str(uuid.uuid4()).encode())

# 获取加密的十六进制结果
print(sha.hexdigest())

import base64
header = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
print(base64.b64decode(header.encode()))  # b'{"typ":"JWT","alg":"HS256"}'
payload = "eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1NDk0Mzg3MSwianRpIjoiNDg3NTk3YmEtMTJjZC00YjNlLTg0N2ItYmJiMjJkZmEyMTgyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MSwidXNlcm5hbWUiOiJ4aWFvbWluZyJ9LCJuYmYiOjE2NTQ5NDM4NzEsImV4cCI6MTY1NDk0NDc3MX0"
print(base64.b64decode(payload.encode())) # b'{"fresh":false,"iat":1654943871,"jti":"487597ba-12cd-4b3e-847b-bbb22dfa2182","type":"access","sub":{"id":1,"username":"xiaoming"},"nbf":1654943871,"exp":1654944771}'