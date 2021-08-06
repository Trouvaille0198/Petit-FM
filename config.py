from pathlib import Path
import enum
import os
import time
from loguru import logger

CWD_URL = 'C:/Users/Tyeah/PycharmProjects/Petit-FM'

current_path = str(Path.cwd())
# print(current_path)
current_path = current_path.replace('\\', '/')
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
                'finance': 20000
            },
            {
                'name': '皇家马德里',
                'finance': 20000
            },
            {
                'name': '曼彻斯特联',
                'finance': 20000
            },
            {
                'name': '曼彻斯特城',
                'finance': 20000
            },
            {
                'name': 'AC米兰',
                'finance': 20000
            },
            {
                'name': '国际米兰',
                'finance': 20000
            },
            {
                'name': '巴黎圣日尔曼',
                'finance': 20000
            },
            {
                'name': '阿贾克斯',
                'finance': 20000
            },
            {
                'name': '切尔西',
                'finance': 20000
            },
            {
                'name': '利物浦',
                'finance': 20000
            }
        ]
    },
    {
        'name': '世界冠军联赛',
        'clubs': [
            {
                'name': '马德里竞技',
                'finance': 20000
            },
            {
                'name': '阿森纳',
                'finance': 20000
            },
            {
                'name': '托特纳姆热刺',
                'finance': 20000
            },
            {
                'name': '尤文图斯',
                'finance': 20000
            },
            {
                'name': '多特蒙德',
                'finance': 20000
            },
            {
                'name': '里昂',
                'finance': 20000
            },
            {
                'name': '上海申花',
                'finance': 20000
            },
            {
                'name': '上海上港',
                'finance': 20000
            }]
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
logger.remove(handler_id=None)  # 禁用控制台输出
logger.add("{}\\log_{}.log".format(LOG_FOLDER, t), format="{message}",
           rotation="1 day", encoding="utf-8", retention="300 days")
