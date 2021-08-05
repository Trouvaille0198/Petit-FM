from pathlib import Path
import enum
import os
import time
from loguru import logger

current_path = str(Path.cwd())
# print(current_path)
current_path = current_path.replace('\\', '/')
# SQLALCHEMY_DATABASE_URL = "sqlite:///" + current_path + "/db_file/sql_app.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///" + "C:/Users/Tyeah/PycharmProjects/Petit-FM" + "/db_file/sql_app.db"  # TODO 路径会变

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
clubs = [
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
    }, {
        'name': '拜仁慕尼黑',
        'finance': 20000
    }

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
t = time.strftime("%m_%d_%H")

logger = logger
logger.remove(handler_id=None)  # 禁用控制台输出
logger.add("{}\\log_{}.log".format(LOG_FOLDER, t), format="{message}",
           rotation="1 day", encoding="utf-8", retention="300 days")
