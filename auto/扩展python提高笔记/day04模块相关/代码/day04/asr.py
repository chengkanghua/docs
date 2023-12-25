from aip import AipSpeech


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


APP_ID = '21212118'
API_KEY = '5RYoUwOCHcexcWfa2iRC0ftq'
SECRET_KEY = 'GQQkpl5sOZPdA90kmLPIO4oRenwmhBFG'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 识别本地文件
result = client.asr(get_file_content('sample-files/16k.pcm'), 'wav', 16000, {'dev_pid': 1537})
print(result)
