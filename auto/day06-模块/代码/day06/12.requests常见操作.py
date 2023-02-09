import requests

# requests.post(
#     url="https://api.luffycity.com/api/v1/auth/password/login/",
#     params={
#         'loginWay': "password"
#     },
#     data={
#         "username": "alex",
#         "password": "123123",
#     },
#     headers={
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
#     }
# )
#
# res = requests.get(
#     url="https://api.luffycity.com/api/v1/course/category/actual/?courseType=actual",
#     headers={
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
#     }
# )

#
# res = requests.get(
#     url="https://www.zhihu.com/api/v4/answers/2251390935/root_comments?order=normal&limit=20&offset=0&status=open",
#     headers={
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
#     }
# )
#
# print(res.text)

# import requests
# res = requests.post(
#     url="https://api.luffycity.com/api/v1/auth/password/login/?loginWay=password",
#     json={"username": "alex", "password": "alex4608!!asdfasdf"},
# )
# print(res.text)


import requests

print(requests.__version__)
