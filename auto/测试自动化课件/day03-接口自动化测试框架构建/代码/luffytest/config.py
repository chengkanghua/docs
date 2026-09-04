import pathlib  # 路径操作模块，替代 os.path模块，os.path采用字符串来操作路径，pathlib采用面向对象来操作路径

# 项目目录的主目录路径[字符串路徑]
BASE_DIR_STR = pathlib.Path(__file__).parent.resolve().as_posix()  # 基本操作系统转换路径的分隔符 as_posix
# 項目目录的主目录路径[路径对象]
BASE_DIR = pathlib.Path(BASE_DIR_STR)

# 项目名
WEB_NAME = "路飞自动化接口测试框架-master"

# 测试自动化项目的运行端口与IP地址
HOST = "127.0.0.1"
PORT = 8088

"""日志配置"""
LOGGING = {
    "name": "luffytest",  # 日志处理器的名称，一般使用当前项目名作为名称
    "filename": (BASE_DIR / "logs/luffytest.log").as_posix(),  # 日志文件存储路径，注意，一定要在项目根目录下手动创建logs目录
    "charset": "utf-8",  # 日志内容的编码格式
    "backup_count": 31,  # 日志文件的备份数量
    "when": "d",   # 日志文件的创建间隔事件,m 表示每分钟创建1个，h表示每小时创建1个，d表示每天创建1个，m0~m6表示每周星期日~星期六创建1个，midnight表示每日凌晨
}


# excel测试用例字段格式
FIELD_LIST = [
    "case_id",        # 用例编号
    "module_name",    # 模块名称
    "case_name",      # 用例名称
    "method",         # 请求方式
    "url",            # 接口地址
    "headers",        # 请求头
    "params_desc",    # 参数说明
    "params",         # 请求参数
    "assert_result",  # 预期结果
    "real_result",    # 实际结果
    "remark",         # 备注
]


"""mock server 的服务端配置"""
# 数据库连接
# SQLALCHEMY_DATABASE_URI: str = "数据库类型://账户:密码@IP地址:端口/数据库名称?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI: str = "mysql+pymysql://root:123@127.0.0.1:3306/pytest?charset=utf8mb4"
# 查询时会显示原始SQL语句
SQLALCHEMY_ECHO: bool = True

# 调试模式
DEBUG = True
# 监听端口
API_PORT = 8000
# 监听地址
API_HOST = "127.0.0.1"

# 秘钥，不管是使用session还是jwt认证，都需要对认证的信息鉴权加密
SECRET_KEY = "9b882670b5313f4a4a47a726618bf62f66c1bd9be36a0e40bb98c792d66c449a"
