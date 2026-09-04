
class Foo(object):
    def __enter__(self):
        print("进入了")
        return 666
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("出去了")

obj = Foo()
with obj as data:  #with 上下文管理 会自动执行， 开始 __enter___ 结束__exit__
    print(data)

