from aip import AipSpeech

APP_ID = '21212118'
API_KEY = '5RYoUwOCHcexcWfa2iRC0ftq'
SECRET_KEY = 'GQQkpl5sOZPdA90kmLPIO4oRenwmhBFG'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result = client.synthesis('你好百度', 'zh', 1, {
    'vol': 5,
})


# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('audio.mp3', 'wb') as f:
        f.write(result)
else:
    print(result)