from xml.etree import ElementTree

content = """<xml>
    <ToUserName>程聪</ToUserName>
    <FromUserName>小魏</FromUserName>
    <CreateTime>1395658920</CreateTime>
    <MsgType>even</MsgType>
    <Event>123</Event>
    <MsgID>200163836</MsgID>
    <Status>success</Status>
</xml>"""

root = ElementTree.XML(content)

info = {}
for node in root:
    # print(node.tag,node.text)
    info[node.tag] = node.text
print(info)

from openpyxl import load_workbook

wb = load_workbook("files/p1.xlsx")
sheet = wb.worksheets[0]
for row in sheet.rows:
    print(row[0].value, row[1].value)
