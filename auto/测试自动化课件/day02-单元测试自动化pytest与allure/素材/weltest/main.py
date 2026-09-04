import pytest
import os
import sys
import shutil
import config

if __name__ == '__main__':
    sys.path.insert(0, str(config.BASE_DIR / "api"))
    sys.path.insert(0, str(config.BASE_DIR / "tests"))
    sys.path.insert(0, str(config.BASE_DIR / "utils"))

    try:
        # 删除之前的测试结果与测试文件目录内容
        shutil.rmtree("reports")
        shutil.rmtree("results")
    except:
        pass
    pytest.main()
    # 生成报告html文件
    os.system('allure generate ./results -o ./reports --clean')
    # 编译报告原文件并启动报告服务
    os.system('allure serve ./reports')
