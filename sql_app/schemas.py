from datetime import datetime
from typing import List
from config import Location
from pydantic import BaseModel


# region 比赛表
class GamePlayerData(BaseModel):
    # id: int
    # game_team_info_id: int
    player_id: int

    created_time: datetime
    name: str  # TODO 临时
    location: Location

    final_rating: float
    actions: int
    shots: int
    goals: int
    assists: int
    # 传球
    passes: int
    pass_success: int
    # 过人
    dribbles: int
    dribble_success: int
    # 抢断
    tackles: int
    tackle_success: int
    # 争顶
    aerials: int
    aerial_success: int
    # 扑救
    saves: int
    save_success: int
    # 体力
    original_stamina: int
    final_stamina: int


class GameTeamData(BaseModel):
    # id: int
    # game_team_info_id: int

    created_time: datetime
    attempts: int
    # 下底传中
    wing_cross: int
    wing_cross_success: int
    # 内切
    under_cutting: int
    under_cutting_success: int
    # 倒三角
    pull_back: int
    pull_back_success: int
    # 中路渗透
    middle_attack: int
    middle_attack_success: int
    # 防反
    counter_attack: int
    counter_attack_success: int


class GameTeamInfo(BaseModel):
    # id: int
    # game_id: int
    club_id: int

    created_time: datetime
    name: str  # TODO 临时
    score: int

    team_data: GameTeamData
    player_data: List[GamePlayerData]


class Game(BaseModel):
    # id: int

    created_time: datetime
    date: str
    type: str
    season: str
    script: str
    mvp: int

    teams: List[GameTeamInfo]


# endregion

# region 球员表
class Player(BaseModel):
    # id: int
    # club_id: int

    created_time: datetime
    name: str
    translated_name: str
    nationality: str
    translated_nationality: str
    age: int = 13
    height: int
    weight: int
    birth_date: str
    values: int = 0
    wages: int = 0
    # Location num
    ST_num: int = 0
    CM_num: int = 0
    LW_num: int = 0
    RW_num: int = 0
    CB_num: int = 0
    LB_num: int = 0
    RB_num: int = 0
    GK_num: int = 0
    CAM_num: int = 0
    LM_num: int = 0
    RM_num: int = 0
    CDM_num: int = 0
    # rating
    shooting: float  # 射门
    passing: float  # 传球
    dribbling: float  # 盘带
    interception: float  # 抢断
    pace: float  # 速度
    strength: float  # 力量
    aggression: float  # 侵略
    anticipation: float  # 预判
    free_kick: float  # 任意球/点球
    stamina: float  # 体能
    goalkeeping: float  # 守门
    # rating limit
    shooting_limit: int
    passing_limit: int
    dribbling_limit: int
    interception_limit: int
    pace_limit: int
    strength_limit: int
    aggression_limit: int
    anticipation_limit: int
    free_kick_limit: int
    stamina_limit: int
    goalkeeping_limit: int
    # 生涯数据
    game_data: List[GamePlayerData] = []


# endregion

# region 教练表
class Coach(BaseModel):
    # id: int
    # club_id: int
    # 基本信息
    created_time: datetime
    name: str
    translated_name: str
    nationality: str
    translated_nationality: str
    age: int = 20
    birth_date: str
    values: int = 0
    wages: int = 0
    # 战术
    tactic: str
    wing_cross: int
    under_cutting: int
    pull_back: int
    middle_attack: int
    counter_attack: int


# endregion

# region 俱乐部表
class Club(BaseModel):
    # id: int
    # league_id: int
    created_time: datetime
    name: str
    finance: float  # 单位：万

    coach: Coach = None
    players: List[Player] = []


# endregion

# region 联赛表
class League(BaseModel):
    # id: int

    created_time: datetime
    name: str

    clubs: List[Club] = []
# endregion
