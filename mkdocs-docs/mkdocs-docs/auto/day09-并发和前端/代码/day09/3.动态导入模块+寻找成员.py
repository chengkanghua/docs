import importlib

# data_string = "commons.pager.send"
# data_string = "utils.f1"
data_string = "commons.dh.helper.xx.ms"

module_path_string, func_str = data_string.rsplit('.', maxsplit=1)
# 以字符串的形式导入模块
m = importlib.import_module(module_path_string)
func = getattr(m, func_str)
func()
