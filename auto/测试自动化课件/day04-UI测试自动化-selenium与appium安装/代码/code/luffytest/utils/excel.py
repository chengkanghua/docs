import xlrd, json

class Excel(object):
    """Excel文件操作工具类"""
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename, formatting_info=True)

    def get_sheet_names(self):
        """
        获取当前excel文件所有的工作表的表名
        :return:
        """
        return self.workbook.sheet_names()

    def __get_sheet(self, sheet_index_or_name):
        """
        根据sheet的索引或名称，获取sheet对象
        :param sheet_index_or_name: sheet的索引或名称
        :return:sheet对象
        """
        if isinstance(sheet_index_or_name, int):
            if len(self.workbook.sheet_names()) > sheet_index_or_name:
                return self.workbook.sheet_by_index(sheet_index_or_name)
            else:
                raise Exception("Invalid Sheet Index!")
        elif isinstance(sheet_index_or_name, str):
            if sheet_index_or_name in self.workbook.sheet_names():
                return self.workbook.sheet_by_name(sheet_index_or_name)
            else:
                raise Exception("Invalid Sheet Name!")

    def get_rows_num(self,sheet_index_or_name):
        """
        获取指定工作表的数据总行数
        :param sheet_index_or_name: 工作表名或索引
        :return:
        """
        return self.__get_sheet(sheet_index_or_name).nrows

    def get_cols_num(self,sheet_index_or_name):
        """
        获取指定工作表的数据总列数
        :param sheet_index_or_name: 工作表名或索引
        :return:
        """
        return self.__get_sheet(sheet_index_or_name).ncols

    def get_cell_value(self, sheet_index_or_name, row_index, col_index):
        """
        获取指定工作表的指定位置的数据值
        :param sheet_index_or_name: 工作表名或索引
        :param row_index: 行下标，从0开始
        :param col_index: 列下标，从0开始
        :return:
        """
        sheet = self.__get_sheet(sheet_index_or_name)
        if sheet.nrows and sheet.ncols:
            return sheet.cell_value(row_index, col_index)
        else:
            raise Exception("Index out of range!")

    def get_data(self, sheet_index_or_name, fields, first_line_is_header=True):
        """
        获取工作表的所有数据
        :param sheet_index_or_name: 工作表名或索引
        :param fields: 返回数据的字段名
        :param first_line_is_header: 工作表是否是否表头，也就是非数据
        :return:
        """
        rows = self.get_rows_num(sheet_index_or_name)
        cols = self.get_cols_num(sheet_index_or_name)
        data = []
        for row in range(int(first_line_is_header), rows):
            row_data = {}
            for col in range(cols):
                cell_data = self.get_cell_value(sheet_index_or_name, row, col)
                if type(cell_data) is str and ("{" in cell_data and "}" in cell_data or "[" in cell_data and "]" in cell_data):
                    """判断如果表格中填写的数据是json格式键值对，则采用json模块转换成字典"""
                    cell_data = json.loads(cell_data)
                row_data[fields[col]] = cell_data
            data.append(row_data)

        return data

if __name__ == '__main__':
    xls = Excel("../data/case_user.xls")
    fields = [
        "case_id",
        "module_name",
        "case_name",
        "method",
        "url",
        "headers",
        "params_desc",
        "params",
        "assert_result",
        "real_result",
        "remark",
    ]

    print(xls.get_data(0, fields))

"""
[
    
    {'case_id': 1.0, 'module_name': '用户模块', 'case_name': '用户登录-测试用户名为空的情况', 'method': 'post', 'url': 'http://127.0.0.1:8000/user/login', 'headers': '', 'params_desc': 'username: 用户名\npassword: 密码', 'params': {'username': '', 'password': '123456'}, 'assert_result': 'code==400', 'real_result': '', 'remark': ''}, 
    {'case_id': 2.0, 'module_name': '用户模块', 'case_name': '用户登录-测试密码为空的情况', 'method': 'post', 'url': 'http://127.0.0.1:8000/user/login', 'headers': '', 'params_desc': 'username: 用户名\npassword: 密码', 'params': {'username': 'xiaoming', 'password': ''}, 'assert_result': 'code==400', 'real_result': '', 'remark': ''}, 
    {'case_id': 3.0, 'module_name': '用户模块', 'case_name': '用户登录-测试账号密码正确的情况', 'method': 'post', 'url': 'http://127.0.0.1:8000/user/login', 'headers': '', 'params_desc': 'username: 用户名\npassword: 密码', 'params': {'username': 'xiaoming', 'password': '123456'}, 'assert_result': ['code==200', "'data' in json"], 'real_result': '', 'remark': ''}, 
    {'case_id': 4.0, 'module_name': '用户模块', 'case_name': '用户登录-测试使用手机号码登录', 'method': 'post', 'url': 'http://127.0.0.1:8000/user/login', 'headers': '', 'params_desc': 'username: 手机号\npassword: 密码', 'params': {'username': '13312345678', 'password': '123456'}, 'assert_result': 'code==200', 'real_result': '', 'remark': ''}
]
"""
