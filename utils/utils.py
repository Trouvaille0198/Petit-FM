import random
from pathlib import Path
from logger import logger


def get_random_name() -> str:
    word_list = [chr(i) for i in range(97, 123)]
    name = ''.join([random.choice(word_list) for i in range(random.randint(3, 10))])
    return name


def get_random_land_name() -> str:
    return random.choice(list(map(lambda x: str(x), range(10000, 99999))))


def get_mean_range(*value, per_range: float = 0.1) -> float:
    """
    返回几个数均值的随机范围
    :param value: 值关键字
    :param per_range: 范围
    :return: 均值在一定范围内的偏移随机数
    """
    return sum(value) / len(value) * (1 + random.uniform(-per_range, per_range))


def get_offset(value, offset) -> float:
    return value * (1 + offset)


def normalvariate(mu, sigma=2):
    return random.normalvariate(mu, sigma)


def retain_demical(value, n=3):
    x = 10 ** n
    return int(value * x) / x


def is_happened_by_pro(pro):
    pro = pro if pro <= 1 else 1
    pro = int(pro * 1000)
    pool = [1 for i in range(pro)] + [0 for i in range(1000 - pro)]
    flag = random.choice(pool)
    return flag


def act_by_pro(pro, func, *args):
    flag = is_happened_by_pro(pro)
    if flag:
        func(*args)


def select_by_pro(pro_dict: dict):
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
