import pytest
import os
import sys

import config

if __name__ == '__main__':
    os.system(f"rd /s /q results")
    os.system(f"rd /s /q reports")

    # 让python解释器，追加3个项目中的核心目录为导包路径
    sys.path.insert(0, str(config.BASE_DIR / "api"))
    sys.path.insert(0, str(config.BASE_DIR / "tests"))
    sys.path.insert(0, str(config.BASE_DIR / "utils"))

    # 启动pytest框架
    pytest.main()

    # 生成报告html文件
    os.system('allure generate ./results -o ./reports')

    # 基于http协议打开HTML测试报告
    os.system(f'allure open ./reports -h {config.HOST} -p {config.PORT}')
