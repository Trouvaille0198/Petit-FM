import random
from pathlib import Path
from decimal import *


def get_mean_range(*value, per_range: float = 0.1) -> float:
    """
    返回几个数均值的随机范围
    :param value: 值关键字
    :param per_range: 百分比范围
    :return: 均值在一定范围内的偏移随机数
    """
    return sum(value) / len(value) * (1 + random.uniform(-per_range, per_range))


def get_offset(value, offset) -> float:
    return float(retain_decimal(value * (1 + offset)))


def normalvariate(mu, sigma=2):
    """
    正态分布
    :param mu: 平均值
    :param sigma: 方差
    :return: 正态分布下的随机值
    """
    return random.normalvariate(mu, sigma)


def retain_decimal(value, n=3):
    """
    保留n位小数
    :param value: 数
    :param n: 保留小数位数
    :return: 保留n位小数后的数
    """
    return Decimal("%.{}f".format(n) % value)


def is_happened_by_pro(pro):
    """
    根据概率判断是否发生
    :param pro: 概率，范围0-1
    :return: 发生为True，不发生为False
    """
    pro = pro if pro <= 1 else 1
    pro = int(pro * 1000)
    pool = [1 for i in range(pro)] + [0 for i in range(1000 - pro)]
    flag = random.choice(pool)
    return flag


def act_by_pro(pro, func, *args, **kwargs):
    """
    根据概率判断函数是否执行
    :param pro: 概率，范围0-1
    :param func: 待判断的函数
    """
    flag = is_happened_by_pro(pro)
    if flag:
        func(*args, **kwargs)


def select_by_pro(pro_dict: dict):
    """
    按概率选取选项
    :param pro_dict: 概率字典，形如{'A':60,'B':40}
    :return: 字典键值（即选项）
    """
    num_sum = 0
    for value in pro_dict.values():
        num_sum += value
    ran = random.random() * num_sum
    sum_ = 0
    for key, value in pro_dict.items():
        sum_ += value
        if ran <= sum_:
            return key


def plus_dict(a: dict, b: dict) -> dict:
    """
    将两个字典相加
    :param a: 字典a
    :param b: 字典b
    :return: 相加后的字典
    """
    for key, value in b.items():
        if key in a:
            a[key] += value
        else:
            a[key] = value
    return a
