import time
from utils.context import Context, UserDict
from utils import validator
from src import account, article


class Handler(object):
    LOGIN_USER_DICT = UserDict()  # {"id":None,"nickname":xxx} 记录登录状态

    NAV = []  # 标题导航

    def wrapper(self, method):  # 闭包函数
        def inner(*args, **kwargs):
            print(" > ".join(self.NAV).center(50, "*"))  # 打印导航位置
            res = method(*args, **kwargs)
            self.NAV.pop(-1)
            return res

        return inner

    def login(self):
        """ 登录 """
        while True:
            user = input("用户名(Q/q退出)：")
            if user.upper() == 'Q':
                return
            pwd = input("密码：")

            user_dict = account.login(user, pwd)
            if not user_dict:
                print("用户名或密码错误，请重新输入。")
                continue

            print("登录成功")
            self.LOGIN_USER_DICT.set_info(user_dict)

            self.NAV.insert(0, self.LOGIN_USER_DICT.nickname)  # 导航0的位置插入用户昵称
            return

    def register(self):
        """ 注册 """
        while True:
            nickname = validator.while_input("昵称(Q/q退出)：")
            if nickname.upper() == 'Q':
                return
            user = validator.while_input("用户名：")
            pwd = validator.while_input("密码：")
            email = validator.while_input("邮箱：", validator.email)
            cellphone = validator.while_input("手机号：", validator.cellphone)

            if not account.register(user, pwd, nickname, cellphone, email):
                print("注册失败，请重新注册。")
                continue
            print("注册成功，请使用新账户去登录。")
            return

    def publish_blog(self):
        """ 发布博客"""
        if not self.LOGIN_USER_DICT.is_login:
            print("未登录用户不允许发布博客，请登录后再访问。")
            time.sleep(2)
            return

        while True:
            title = validator.while_input("标题：")
            text = validator.while_input("正文：")

            if not article.publish(title, text, self.LOGIN_USER_DICT.id):
                print("发布失败，请重新发布")
                time.sleep(1)
                continue
            print("发布成功，可进入博客列表查看")
            return

    def blog_list(self):
        """ 查看博客列表 """
        # 数据库的现在总共有多少条数据 100条 10   10页
        total_count = article.total_count()
        # 每页显示10条数据
        per_page_count = 10
        # 总共需要多少页来展示数据（用户输入的页码）
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1  # 总页数

        # 当前想查看的页码
        current_page_num = 1

        if not max_page_num:
            print("无数据")
            return

        counter = 0
        while True:
            if counter:  # 翻页的时候走这里
                print(" > ".join(self.NAV).center(50, "*"))
            counter += 1
            # 10, 0   第1页
            # 10, 10  第2页
            # 10, 20  第3页
            # 10, 30  第4页
            # select x from xxxx limit 10 offset 30
            data_list = article.page_list(per_page_count, (current_page_num - 1) * per_page_count)  # 博客列表数据
            print("文章列表：")
            for row in data_list:
                line = "    {id}. {title}".format(**row)
                print(line)

            print("\n注意：输入p数字格式，表示翻页； 仅数字表示文章ID，可查看文章详细。\n")
            text = input("请输入(Q/q退出)：").strip()
            if text.upper() == "Q":
                return

            # 1. 翻页
            if text.startswith("p"):
                page_num = int(text[1:])  # 可以再进行校验
                if 0 < page_num <= max_page_num:
                    current_page_num = page_num  # current_page_num=4
                continue

            # 2. 查看文章详细
            if not text.isdecimal():  # 是否可以转换成十进制数
                print("格式错误，请重新输入")
                continue
            article_id = int(text)
            # 根据文章ID去数据获取文章信息(对象)
            article_object = article.get_article(article_id)
            if not article_object:
                print("文章不存在，请重新输入。")
                continue

            # 查看文章详细
            # self.article_detail(article_id, article_object)
            self.NAV.append("文章详细")
            self.wrapper(self.article_detail)(article_id, article_object)  # 文章信息(文章id,文章信息对象)

    def article_detail(self, article_id, article_object):
        # 展示文章信息，article_object封装了这一行的所有的数据。
        article_object.show()

        # 2.2 阅读数+1
        article.update_read_count(article_id)

        def up():
            # 先去数据库中获取 当前用户、对这篇文章的 赞踩记录
            up_down_object = article.fetch_up_down(self.LOGIN_USER_DICT.id, article_id)
            if not up_down_object:  # 表里没数据
                if article.up(self.LOGIN_USER_DICT.id, article_id):
                    print("点赞成功")
                else:
                    print("点赞失败")
                return

            if up_down_object.choice == 1:  # 表里有数据 并且 choice=1 表示已赞过
                print("已赞过，不能重复操作")
                return

            if article.update_down_to_up(article_id, up_down_object.id):  # 之前是踩的改点赞
                print("点赞成功")
            else:
                print("点赞失败")

        def down():
            up_down_object = article.fetch_up_down(self.LOGIN_USER_DICT.id, article_id)  # 获取up_down表里的信息.
            if not up_down_object:  # 表里没信息 更新
                if article.down(self.LOGIN_USER_DICT.id, article_id):
                    print("踩成功")
                else:
                    print("踩失败")
                return
            if up_down_object.choice == 0:  # 如果有信息 choice 并且等于0
                print("已踩过，不能重复操作")
                return

            if article.update_up_to_down(article_id, up_down_object.id):  # 之前是赞的选择改踩了
                print("踩成功")
            else:
                print("踩失败")

        def comment():
            comment_text = input("请输入评论内容：")
            if article.comment(self.LOGIN_USER_DICT.id, article_id, comment_text):
                print("评论成功")
            else:
                print("评论失败")

        mapping = {
            "1": Context("赞", up),
            "2": Context("踩", down),
            "3": Context("评论", comment),
        }
        message = ";".join(["{}.{}".format(k, v.text) for k, v in mapping.items()])
        message = "\n提示：{}".format(message)
        while True:
            print(message)
            choice = input("请输入(Q/q退出)：").strip()
            if choice.upper() == 'Q':
                break
            if not self.LOGIN_USER_DICT.is_login:
                print("用户未登录，无法进行赞、踩、评论操作。")
                time.sleep(2)
                return
            if not choice:
                continue
            ctx = mapping.get(choice)
            if not ctx:
                print("输入错误，请重新输入。")
                continue
            ctx.method()

    def run(self):
        """ 主程序 """
        self.NAV.append("系统首页")  # 标题导航

        mapping = {
            "1": Context("登录", self.wrapper(self.login)),  # Context 对象存储 text method
            "2": Context("注册", self.wrapper(self.register)),
            "3": Context("发布博客", self.wrapper(self.publish_blog)),
            "4": Context("查看博客列表", self.wrapper(self.blog_list)),
        }

        message = "\n".join(["{}.{}".format(k, v.text) for k, v in mapping.items()])
        while True:
            # ["系统首页",""注册",]
            print(" > ".join(self.NAV).center(50, "*"))  # 打印导航位置
            print(message)  # 打印功能选项列表
            choice = input("请输入序号：").strip()
            if not choice:
                continue

            if choice.upper() == "Q":
                return

            context = mapping.get(choice)
            if not context:
                print("序号输入错误，请重新输入。\n")
                continue

            self.NAV.append(context.text)  # 选择的位置 增加到导航列表
            context.method()  # 运行所选择的对应方法


handler = Handler()
handler.run()