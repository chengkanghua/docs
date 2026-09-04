class F1(object):
    def __init__(self):
        print('init')

    def __call__(self, *args, **kwargs):
        print(1)


obj = F1()

obj()
