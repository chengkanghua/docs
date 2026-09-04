# 封装的标题和方法
class Context(object):
    def __init__(self, title, method):
        self.title = title
        self.method = method


# 封装的用户信息
class UserDict(object):
    def __init__(self):
        self.id = None
        self.nickname = None

    def set_info(self, userdict: dict):
        for k, v in userdict.items():
            setattr(self, k, v)

    @property
    def is_login(self):
        if self.id:
            return True


# 封装的文章存储对象
class ArticleModel(object):
    fields = {
        'title': '标题',
        'text': '内容',
        'read_count': '阅读数',
        'comment_count': '评论数',
        'support_count': '点赞数',
        'step_count': '踩数',
        'nickname': '作者'
    }

    def __init__(self, article_dict: dict):
        for k, v in article_dict.items():
            setattr(self, k, v)

    @classmethod
    def db_fields(cls):
        fields = ','.join([k for k in cls.fields.keys()])
        # print(fields)
        return fields

    def show(self):
        row_list = ['title', 'text']
        for k in row_list:
            line = '{}:{}'.format(k, getattr(self, k))
            print(line)

        # column_list = ['read_count', 'comment_count', 'support_count', 'step_count', 'nickname']
        # session_list = []
        # for k in column_list:
        #     session_list.append('{}:{}'.format(k, getattr(self, k)))
        #
        # info = ' '.join(session_list)
        # print('提示:', info)


# 封装文章踩赞对象
class UpDownModel(object):
    fields = {
        'id': 'ID',
        'choice': '赞或踩'
    }

    def __init__(self, a_dict: dict):
        for k in self.fields:
            setattr(self, k, a_dict.get(k))
