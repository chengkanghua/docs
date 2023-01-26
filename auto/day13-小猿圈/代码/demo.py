def func(v1, **context):
    print(v1, context)


func("xx.html", v1=123, v2=456)
func("xx.html", **{"v1": 123, "v2": 456})
