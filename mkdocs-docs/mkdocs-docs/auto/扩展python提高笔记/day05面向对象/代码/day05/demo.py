class LocalProxy(object):

    def __init__(self, func):
        object.__setattr__(self, 'func', func)  # self.func = get_top

    def get_current_object(self):
        return self.func()  # get_top()


def get_top():
    return "alex"


req = LocalProxy(get_top)

v1 = req.get_current_object()
print(v1)  # alex
