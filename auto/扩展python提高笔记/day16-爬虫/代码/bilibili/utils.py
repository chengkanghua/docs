import json
data_string = "aid=803139487&cid=340411234&bvid=BV1Wy4y1W7bM&part=1&mid=0&lv=0&ftime=1625967900&stime=1625968662&jsonp=jsonp&type=3&sub_type=0"

info = {item.split("=")[0]: item.split("=")[1] for item in data_string.split("&")}

print(json.dumps(info,indent=4))
