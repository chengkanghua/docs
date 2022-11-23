"""
MySQL数据库：博客系统案例
功能包含：
    - 登录
    - 注册
    - 发布博客
    - 查看博客列表，显示博客标题、创建时间、阅读数量、评论数量、赞数量等。（支持分页查看）
    - 博客详细，显示博文详细、评论 等。
        - 发表评论
        - 赞 or 踩
        - 阅读数量 + 1
"""
from src.handler import handler

if __name__ == '__main__':
    handler.run()

