import config
from api import init_app

# 注意，务必把模型models的内容以及 views 中的服务端接口引入当前文件，否则flask不识别。
from api import models
from api import views

app = init_app()

if __name__ == '__main__':
    app.run(host=config.API_HOST, port=config.API_PORT)
