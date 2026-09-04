
# 封装的标题和方法对象
class Context(object):
    def __init__(self, text, method):
        self.text = text
        self.method = method

# 封装用户信息,判断登陆状态
class UserDict(object):
    def __init__(self):
        self.id = None
        self.nickname = None

    def set_info(self, user_dict):
        for k, v in user_dict.items():
            setattr(self, k, v)   # setattr(对象,成员,值)
        # self.id = user_dict['id']
        # self.nickname = user_dict['nickname']

    @property
    def is_login(self):
        if self.id:
            return True

# 封装的文章存储对象
class ArticleModel(object):
    fields = {
        "title": "标题",
        "text": "内容",
        "read_count": "阅读数",
        "comment_count": "评论数",
        "support_count": "赞数",
        "step_count": "踩数",
        "nickname": "作者",
    }

    # {"title":xxxx,"text":xxxx,read_count:"xxx"}
    def __init__(self, row_dict):
        for key in self.fields:
            setattr(self, key, row_dict.get(key)) # setattr(对象,成员,值) 新创建的成员
            # self.title = row_dict.get("title")
            # self.text = row_dict.get("title")

    @classmethod
    def db_fields(cls):  # db字段 # title,text,read_count,comment_count,support_count,step_count,nickname
        return ",".join([k for k in cls.fields])

    def show(self):
        row_display = ["title", 'text'] # 行显示字段
        for k in row_display:
            line = "{}:{}".format(self.fields[k], getattr(self, k)) # 获取当前对象的 title text内容
            print(line)

        column_display = ["nickname", "read_count", "comment_count", "support_count", "step_count"]
        section_list = []
        for k in column_display:
            section_list.append("{}:{}".format(self.fields[k], getattr(self, k)))
        others = "  ".join(section_list)
        print(others)

# 封装的踩赞对象
class UpDownModel(object):
    fields = {
        "id": "ID",
        "choice": "赞或踩",  # 1，表示是赞；0，表示是踩
    }

    def __init__(self, row_dict):
        for k in self.fields:
            setattr(self, k, row_dict.get(k))
