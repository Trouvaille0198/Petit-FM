from pydantic import BaseModel
from typing import Dict, List, Sequence, Set, Tuple, Optional
from enum import Enum


class Location(str, Enum):
    ST = 'ST'
    LW = 'LW'
    RW = 'RW'
    CM = 'CM'
    CB = 'CB'
    LB = 'LB'
    RB = 'RB'
    GK = 'GK'


class TacticsPro(BaseModel):
    wing_cross: float
    under_cutting: float
    pull_back: float
    middle_attack: float
    counter_attack: float


class Rating(BaseModel):
    shooting: int  # 射门
    passing: int  # 传球
    dribbling: int  # 盘带
    interception: int  # 抢断
    pace: int  # 速度
    strength: int  # 力量
    aggression: int  # 侵略
    anticipation: int  # 预判
    free_kick: int  # 任意球/点球
    stamina: int  # 体能
    goalkeeping: int  # 守门


class BasicInfo(BaseModel):
    first_name: str  # 名
    last_name: str  # 姓
    age: int  # 年龄


class PlayerBase(BaseModel):
    base_info: BasicInfo
    rating: Rating
