from pathlib import Path
import enum
import os
import time
from loguru import logger

CWD_URL = 'C:/Users/Tyeah/PycharmProjects/Petit-FM'


def init_current_path():
    """
    确定根目录，在整个游戏开始前调用
    """
    global CWD_URL
    CWD_URL = str(Path.cwd())
    logger.info("根目录为：{}".format(CWD_URL))


# current_path = str(Path.cwd())
# print(current_path)
# current_path = current_path.replace('\\', '/')
# SQLALCHEMY_DATABASE_URL = "sqlite:///" + current_path + "/db_file/sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///" + CWD_URL + "/db_file/sql_app.db"  # TODO 路径会变

# country
country_potential = {
    '西班牙': 12,
    '葡萄牙': 11,
    '比利时': 8,
    '荷兰': 12,
    '英国': 11,
    '法国': 11,
    '意大利': 10,
    '德国': 9,
    '巴西': 11,
    '阿根廷': 11,
    '乌拉圭': 6,
    '哥伦比亚': 7,
    '克罗地亚': 5,
    '丹麦': 6,
    '瑞士': 4,
    '墨西哥': 3,
    '中国': 9,
    '日本': 8,
    '韩国': 7
}

# tactics
tactic_config = {
    '4-4-2': {
        "ST": 2,
        "CM": 2,
        "LW": 0,
        "RW": 0,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1,
        "CAM": 0,
        "LM": 1,
        "RM": 1,
        "CDM": 0
    },
    '4-1-4-1': {
        "ST": 1,
        "CM": 2,
        "LW": 0,
        "RW": 0,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1,
        "CAM": 0,
        "LM": 1,
        "RM": 1,
        "CDM": 1
    },
    '4-1-2-3': {
        "ST": 1,
        "CM": 0,
        "LW": 1,
        "RW": 1,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1,
        "CAM": 2,
        "LM": 0,
        "RM": 0,
        "CDM": 1
    },
    '3-5-2': {
        "ST": 2,
        "CM": 1,
        "LW": 0,
        "RW": 0,
        "CB": 3,
        "LB": 0,
        "RB": 0,
        "GK": 1,
        "CAM": 0,
        "LM": 1,
        "RM": 1,
        "CDM": 2
    },
    '4-3-1-2': {
        "ST": 2,
        "CM": 0,
        "LW": 0,
        "RW": 0,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1,
        "CAM": 1,
        "LM": 0,
        "RM": 0,
        "CDM": 3
    },
    '4-3-3': {
        "ST": 1,
        "CM": 1,
        "LW": 1,
        "RW": 1,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1,
        "CAM": 0,
        "LM": 1,
        "RM": 1,
        "CDM": 0
    }
}

# clubs
leagues = [
    {
        'name': '世界超级联赛',
        'clubs': [
            {
                'name': '巴塞罗那',
                'finance': 50000
            },
            {
                'name': '皇家马德里',
                'finance': 43000
            },
            {
                'name': '曼彻斯特联',
                'finance': 45000
            },
            {
                'name': '曼彻斯特城',
                'finance': 45000
            },
            {
                'name': 'AC米兰',
                'finance': 38000
            },
            {
                'name': '国际米兰',
                'finance': 38000
            },
            {
                'name': '巴黎圣日尔曼',
                'finance': 42000
            },
            {
                'name': '阿贾克斯',
                'finance': 34000
            },
            {
                'name': '切尔西',
                'finance': 41000
            },
            {
                'name': '利物浦',
                'finance': 38000
            },
            {
                'name': '马德里竞技',
                'finance': 32000
            },
            {
                'name': '阿森纳',
                'finance': 30000
            },
            {
                'name': '托特纳姆热刺',
                'finance': 28000
            },
            {
                'name': '尤文图斯',
                'finance': 32000
            },
            {
                'name': '多特蒙德',
                'finance': 31000
            },
            {
                'name': '拜仁慕尼黑',
                'finance': 37000
            },
            {
                'name': '上海申花',
                'finance': 20000
            },
            {
                'name': '上海上港',
                'finance': 20000
            },
            {
                'name': '莱斯特城',
                'finance': 16000
            },
            {
                'name': '塞维利亚',
                'finance': 16000
            }
        ]
    },
    {
        'name': '世界冠军联赛',
        'clubs': [
            {
                'name': '里昂',
                'finance': 14000
            },
            {
                'name': '里斯本竞技',
                'finance': 14000
            },
            {
                'name': '莱比锡',
                'finance': 16000
            },
            {
                'name': '浙江绿城',
                'finance': 25000
            },
            {
                'name': '勒沃库森',
                'finance': 15000
            },
            {
                'name': '西汉姆联',
                'finance': 18000
            },
            {
                'name': '狼队',
                'finance': 13000
            },
            {
                'name': '罗马',
                'finance': 13000
            },
            {
                'name': '摩纳哥',
                'finance': 14000
            },
            {
                'name': '广州恒大',
                'finance': 21000
            },
            {
                'name': '马赛',
                'finance': 15000
            },
            {
                'name': '波尔图',
                'finance': 14000
            },
            {
                'name': '本菲卡',
                'finance': 15000
            },
            {
                'name': '博卡',
                'finance': 19000
            },
            {
                'name': '河床',
                'finance': 19000
            },
            {
                'name': '川崎前锋',
                'finance': 14000
            },
            {
                'name': '北京国安',
                'finance': 14000
            },
            {
                'name': '江苏苏宁',
                'finance': 14000
            },
            {
                'name': '埃因霍温',
                'finance': 14000
            },
            {
                'name': '桑托斯',
                'finance': 14000
            }
        ]
    }
]

# location_potential
rating_potential = [
    {'name': 'ST',
     'offset': {'shooting': 0.6, 'anticipation': 0.2, 'strength': 0.2}},
    {'name': 'LW',
     'offset': {'dribbling': 0.4, 'pace': 0.4, 'passing': 0.1, 'shooting': 0.1}},
    {'name': 'RW',
     'offset': {'dribbling': 0.4, 'pace': 0.4, 'passing': 0.1, 'shooting': 0.1}},
    {'name': 'CM',
     'offset': {'passing': 0.6, 'stamina': 0.3, 'shooting': 0.1}},
    {'name': 'CB',
     'offset': {'interception': 0.5, 'anticipation': 0.2, 'strength': 0.2, 'passing': 0.1}},
    {'name': 'LB',
     'offset': {'interception': 0.3, 'shooting': 0.4, 'dribbling': 0.1, 'passing': 0.2}},
    {'name': 'RB',
     'offset': {'interception': 0.3, 'shooting': 0.4, 'dribbling': 0.1, 'passing': 0.2}},
    {'name': 'GK',
     'offset': {'goalkeeping': 1.5}},
    {'name': 'CAM',
     'offset': {'passing': 0.3, 'shooting': 0.3, 'anticipation': 0.2, 'strength': 0.2}},
    {'name': 'LM',
     'offset': {'passing': 0.5, 'shooting': 0.2, 'dribbling': 0.1, 'pace': 0.1, 'stamina': 0.1}},
    {'name': 'RM',
     'offset': {'passing': 0.5, 'shooting': 0.2, 'dribbling': 0.1, 'pace': 0.1, 'stamina': 0.1}},
    {'name': 'CDM',
     'offset': {'passing': 0.4, 'interception': 0.4, 'anticipation': 0.1, 'strength': 0.1}},
]

# select_player
select_location = [
    {'name': 'ST',
     'weight': {'shooting': 0.5, 'passing': 0, 'dribbling': 0.05, 'interception': 0, 'pace': 0.05, 'strength': 0.15,
                'aggression': 0, 'anticipation': 0.15, 'free_kick': 0, 'stamina': 0.1, 'goalkeeping': 0}},
    {'name': 'LW',
     'weight': {'shooting': 0.2, 'passing': 0.2, 'dribbling': 0.4, 'interception': 0, 'pace': 0.2, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'RW',
     'weight': {'shooting': 0.2, 'passing': 0.2, 'dribbling': 0.4, 'interception': 0, 'pace': 0.2, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'CM',
     'weight': {'shooting': 0.2, 'passing': 0.7, 'dribbling': 0, 'interception': 0, 'pace': 0, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0.1, 'goalkeeping': 0}},
    {'name': 'CB',
     'weight': {'shooting': 0, 'passing': 0, 'dribbling': 0, 'interception': 0.5, 'pace': 0, 'strength': 0.25,
                'aggression': 0, 'anticipation': 0.25, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'LB',
     'weight': {'shooting': 0, 'passing': 0.1, 'dribbling': 0.1, 'interception': 0.4, 'pace': 0.4, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'RB',
     'weight': {'shooting': 0, 'passing': 0.1, 'dribbling': 0.1, 'interception': 0.4, 'pace': 0.4, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'GK',
     'weight': {'shooting': 0, 'passing': 0.05, 'dribbling': 0, 'interception': 0, 'pace': 0, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0.95}},
    {'name': 'CAM',
     'weight': {'shooting': 0.4, 'passing': 0.5, 'dribbling': 0, 'interception': 0, 'pace': 0, 'strength': 0.05,
                'aggression': 0, 'anticipation': 0.05, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'LM',
     'weight': {'shooting': 0.1, 'passing': 0.5, 'dribbling': 0.2, 'interception': 0, 'pace': 0.2, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'RM',
     'weight': {'shooting': 0.1, 'passing': 0.5, 'dribbling': 0.2, 'interception': 0, 'pace': 0.2, 'strength': 0,
                'aggression': 0, 'anticipation': 0, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
    {'name': 'CDM',
     'weight': {'shooting': 0, 'passing': 0.5, 'dribbling': 0, 'interception': 0.3, 'pace': 0, 'strength': 0.1,
                'aggression': 0, 'anticipation': 0.1, 'free_kick': 0, 'stamina': 0, 'goalkeeping': 0}},
]


# Enum


class Location(str, enum.Enum):
    ST = 'ST'
    LW = 'LW'
    RW = 'RW'
    CM = 'CM'
    CB = 'CB'
    LB = 'LB'
    RB = 'RB'
    GK = 'GK'

    CAM = 'CAM'
    LM = 'LM'
    RM = 'RM'
    CDM = 'CDM'


# 日志收集器
# LOG_FOLDER = os.getcwd() + '\\logs'
LOG_FOLDER = "C:/Users/Tyeah/PycharmProjects/Petit-FM/logs"
if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)
t = time.strftime("%m_%d")

logger = logger
# logger.remove(handler_id=None)  # 禁用控制台输出
logger.add("{}\\log_{}.log".format(LOG_FOLDER, t), format="{message}",
           rotation="1 day", encoding="utf-8", retention="300 days")
