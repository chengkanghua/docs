"""
大家：
    根据业务需求开始写代码（错误）。
正确：
    整体设计（逻辑能力）
     - 1. xxx
     - 2. xxx
     - 3. xxx
    写代码（某个代码不会写，网上找）
"""

"""
主要设计思路：
    豹子：  6 xx 00 00
    同花顺：5 xx 00 00
    同花：  4 xx xx xx
    顺子：  3 xx 00 00    QKA > A23 > JQK
    对子：  2 xx xx 00
    单点：  1 xx xx xx
"""
import random
import functools


# 检查是否是豹子，如果是则生成分值
def calculate_same_num_rule(poke_list):
    """判断是否是豹子"""
    card_num_set = set([item[1] for item in poke_list])
    if len(card_num_set) == 1:
        value = str(card_num_set.pop())
        return "6{}0000".format(value.rjust(2, "0"))


# 同花顺 & 同花
def calculate_same_color_rule(poke_list):
    """检查同花"""
    card_color_set = set([i[0] for i in poke_list])
    if len(card_color_set) != 1:  # 不是花色
        return

    # 是否顺子
    straight = calculate_straight_rule(poke_list, "5{}0000")
    if straight:
        return straight

    # 普通大小
    single = calculate_single_card_rule(poke_list, "4{}")
    return single


# 顺子
def calculate_straight_rule(poke_list, tpl):
    """检测顺子"""
    p1 = poke_list[0][1]
    p2 = poke_list[1][1]
    p3 = poke_list[2][1]
    # 12 13 14   # 最大 15
    # 2  3  14  # 次之 14
    if p1 == 2 and p2 == 3 and p3 == 14:
        return tpl.format("15".rjust(2, "0"))
    elif p3 - p2 == 1 and p2 - p1 == 1:
        if p3 == 14:
            return tpl.format("14".rjust(2, "0"))
        else:
            return tpl.format(str(p3).rjust(2, "0"))


# 单点
def calculate_single_card_rule(poke_list, tpl):
    num_list = []
    for index in range(len(poke_list) - 1, -1, -1):
        num = poke_list[index][1]
        num_list.append(str(num).rjust(2, "0"))
    return tpl.format("".join(num_list))


# 对子
def calculate_double_card_rule(poke_list):
    """计算有没有对 2 01 01 00 """
    num_dict = {}
    for _, num in poke_list:
        num = str(num)
        if num in num_dict:
            num_dict[num] += 1
        else:
            num_dict[num] = 1
    if len(num_dict) != 2:
        return
    p1, p2 = sorted(num_dict.items(), key=lambda x: x[1], reverse=True)
    return "2{}{}00".format(p1[0].rjust(2, "0"), p2[0].rjust(2, "0"))


def run():
    check_func_list = [
        calculate_same_num_rule,  # 6xx0000
        calculate_same_color_rule,  # 5xx0000  4xxxxxx
        functools.partial(calculate_straight_rule, tpl="3{}0000"),
        calculate_double_card_rule,
        functools.partial(calculate_single_card_rule, tpl="1{}"),
    ]

    # 生成一副扑克牌
    card_color_list = ["红桃", "黑桃", "方片", "梅花"]
    card_nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # A
    all_card_list = [[color, num] for color in card_color_list for num in card_nums]

    # 洗牌（好用功能）
    random.shuffle(all_card_list)

    # 给5个玩家发牌
    players = {}
    for i in range(5):

        # 随机抽取三张牌，并对牌面值从小到大排序
        # [ ["黑桃",5], ["红桃",3], ["方片",9] ]
        user_poke = random.sample(all_card_list, 3)

        # 根据牌面大小排序
        # [ ["红桃",3], ["黑桃",5],  ["方片",9] ]
        user_poke.sort(key=lambda x: x[1])

        # 删除抽取的牌，防止重复
        for card in user_poke:
            all_card_list.remove(card)

        # 计算牌的分值
        # 根据牌去计算 [ ["红桃",3], ["黑桃",5],  ["方片",9] ] 他的分值
        for func in check_func_list:
            weight = func(user_poke)
            if weight:
                break

        # 将牌和权重赋值给玩家
        players[weight] = user_poke

    for weight, item in players.items():
        print(weight, item)


if __name__ == '__main__':
    run()
