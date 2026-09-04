import time

from utils import validator
from utils import context
from src import account
from src.article import art


class Handler(object):
    LOCAL_USER_DICT = context.UserDict()
    Navigation = []

    # 导航闭包函数
    def wrapper(self, method):
        def inner(*args, **kwargs):
            print(' > '.join(self.Navigation).center(50, "*"))
            res = method(*args, **kwargs)
            self.Navigation.pop(-1)
            print(' > '.join(self.Navigation).center(50, "*"))
            return res

        return inner

    # 登陆
    def login(self):
        if self.LOCAL_USER_DICT.is_login:
            print('登陆过了, 请不要重复登陆')
            return
        while True:
            user = input('请输入用户名 (q/Q退出): ')
            if user.upper() == 'Q':
                return
            pwd = input('请输入密码: ')
            user_dict = account.login(user, pwd)
            if not user_dict:
                print('用户或密码错误,请重试')
                continue
            print('登陆成功')
            self.LOCAL_USER_DICT.set_info(user_dict)
            self.Navigation.insert(0, self.LOCAL_USER_DICT.nickname)
            return

    # 注册
    def registry(self):
        while True:
            nickname = validator.while_input('昵称 q退出: ')
            if nickname.upper() == 'Q':
                return
            username = validator.while_input('用户名: ')
            password = validator.while_input('密码: ')
            email = validator.while_input('邮箱: ', validator.email)
            cellphone = validator.while_input('手机号: ', validator.cellphone)



            if not account.registry(username, nickname, password, cellphone, email):
                print('注册失败, 请重试')
                continue
            print('注册成功')
            return

    # 发表文章
    def publish(self):
        if not self.LOCAL_USER_DICT.id:
            print('请登录后再发布文章')
            time.sleep(2)
            return
        while True:
            title = validator.while_input('标题: ')
            if not title:
                return
            text = validator.while_input('内容: ')
            if not art.publish(title, text, self.LOCAL_USER_DICT.id):
                print('发布失败,请重试')
                continue
            print('发布成功,请到博客列表查看')
            return

    # 博客列表
    def article_list(self):
        page_count = art.article_count
        if not page_count:
            print('无数据')
            return
        # print(list_count)  /4
        page_num_count = 2  # 每页显示数量
        current_page = 1  # 当前页码

        max_num, div = divmod(page_count, page_num_count)
        if div:
            max_num += 1
        while True:
            data_list = art.page_list(page_num_count, (current_page - 1) * page_num_count)
            # data_list = art.page_list(10,0)
            # id,title,read_count,comment_count,support_count,step_count
            print('文章列表: ')
            for line in data_list:
                print(' {id}.{title} ---阅读数:{read_count},评论数:{comment_count},点赞数:{support_count},点踩数{step_count}'.format(**line))

            print('\n 请输入p数字 表示翻页,仅数字表示文章id 查看文章详情: ')
            cmd = input('请输入 (q退出): ')
            if cmd.upper() == 'Q':
                return

            # 翻页
            if cmd.startswith('p'):
                page_num = int(cmd[1:])
                if 0 < page_num <= max_num:
                    current_page = page_num
                continue

            # 查看文章详细
            if not cmd.isdecimal():
                print('输入格式错误, 请重试')
                continue
            article_id = int(cmd)
            # print(article_id)
            article_object = art.get_article(article_id)
            if not article_object:
                print('文章不存在, 请重试')
                continue
            self.Navigation.append('文章详情')
            self.wrapper(self.article_detail)(article_id,article_object)
    # 文章详情
    def article_detail(self,article_id,article_object):
        def support():
            # 先去数据库中获取 当前用户、对这篇文章的 赞踩记录
            up_down_object = art.get_up_down(self.LOCAL_USER_DICT.id, article_id)
            if not up_down_object:  # 表里没数据
                if art.support(self.LOCAL_USER_DICT.id, article_id):
                    print("点赞成功")
                else:
                    print("点赞失败")
                return

            if up_down_object.choice == 1:  # 表里有数据 并且 choice=1 表示已赞过
                print("已赞过，不能重复操作")
                return

            if art.update_step(self.LOCAL_USER_DICT.id, article_id):  # 之前是踩的改点赞
                print("点赞成功")
            else:
                print("点赞失败")
        def step():
            # 先去数据库中获取 当前用户、对这篇文章的 赞踩记录
            up_down_object = art.get_up_down(self.LOCAL_USER_DICT.id, article_id)
            print(up_down_object.choice,self.LOCAL_USER_DICT.id,article_id)
            if not up_down_object:  # 表里没数据
                if art.step(self.LOCAL_USER_DICT.id, article_id):
                    print("踩成功")
                else:
                    print("踩失败")
                return

            if up_down_object.choice == 0:  # 表里有数据 并且 choice=0 表示已踩过
                print("已踩过，不能重复操作")
                return

            if art.update_support(self.LOCAL_USER_DICT.id, article_id):  # 之前是赞 改踩
                print("踩成功")
            else:
                print("踩失败")
        def comment():
            while True:
                comment_text = input("请输入评论内容：")
                if not comment_text:
                    continue
                if art.comment(self.LOCAL_USER_DICT.id, article_id, comment_text):
                    print("评论成功")
                else:
                    print("评论失败")
                return
        article_object.show()
        art.update_read(article_id)

        print("-------评论区------------")
        comment_dict = art.get_comment(article_id)
        # print(comment_dict)
        for item in comment_dict:
            for k,v in item.items():
                print(k,v, end=' ')
            print()
        mapping = {
            '1': context.Context('赞',support),
            '2': context.Context('踩',step),
            '3': context.Context('评论',comment)
        }
        message = ' '.join(['{}.{} '.format(k,v.title) for k,v in mapping.items()])
        message = '提示: {}'.format(message)
        while True:
            print(message)
            cmd = input('请输入: (q退出)')
            if cmd.upper() == 'Q':
                return
            if not self.LOCAL_USER_DICT.is_login:
                print('用户未登陆 不可以踩赞,评论')
                return
            data = mapping.get(cmd)
            if not data:
                print('输入错误, 请重试')
                continue
            data.method()




    # run
    def run(self):
        '''主入口'''
        self.Navigation.append('系统首页')
        mapping = {
            '1': context.Context('登陆', self.wrapper(self.login)),
            '2': context.Context('注册', self.wrapper(self.registry)),
            '3': context.Context('发布博客', self.wrapper(self.publish)),
            '4': context.Context('查看博客列表', self.wrapper(self.article_list))
        }
        print(' > '.join(self.Navigation).center(50, "*"))
        message = '\n'.join(['{} {}'.format(k, v.title) for k, v in mapping.items()])
        while True:
            print(message)
            cmd = input('请输入序号, Q退出: ')
            if cmd.upper() == 'Q':
                break
            data = mapping.get(cmd)
            if not data:
                print('输入错误, 请重试')
                continue
            self.Navigation.append(data.title)
            data.method()



