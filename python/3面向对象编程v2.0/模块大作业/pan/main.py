from src.handlers.pan import PanHandler
from src.server import Server
from src.select_server import SelectServer
# server = Server()
server = SelectServer()

if __name__ == '__main__':
    server.run(PanHandler)


'''
- config  配置文件夹
- db      数据目录
- files   登陆之后用户家目录
- src     源文件 业务处理代码
- utils   工具箱 公共功能
main.py   主运行程序

'''