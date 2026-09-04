import xlrd, json

# 打开一个xls文件
filename = "./case_user.xls"
workbook = xlrd.open_workbook(filename, formatting_info=True)
# 获取当前excel文件中所有工作表名
names = workbook.sheet_names()
# print(names)

# 获取指定工作表对象
sheet = workbook.sheet_by_name(names[0])

# 获取当前工作表的数据量总行数和总列数
print(sheet.nrows, sheet.ncols)

# 获取第一行第一列数据
# 参数1：行
# 参数2：列
value = sheet.cell_value(0, 0)
print(value)

# 获取第一行数据
first_row_valus = [sheet.cell_value(0, col) for col in range(0, sheet.ncols)]
print(first_row_valus)

# 获取指定某一列列数据
col = 2  # 假设第3列
target_col_value = [sheet.cell_value(row, col) for row in range(sheet.nrows)]
print(target_col_value)

# 获取工作表的全部数据
data = []
for row in range(0, sheet.nrows):
    row_values = []
    for col in range(0, sheet.ncols):
        row_values.append(sheet.cell_value(row, col))
    data.append(row_values)
print(data)
