from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from sql_app.database import Base
from config import Location


# region 比赛输出数据
class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, index=True)

    created_time = Column(DateTime)
    date = Column(String)
    script = Column(String)
    teams = relationship("GameTeamInfo", backref="game")


class GameTeamInfo(Base):
    __tablename__ = 'game_team_info'
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'))  # 外键
    # club_id = Column(Integer, Foreign('club.id')) # 与俱乐部类连接的外键

    created_time = Column(DateTime)
    name = Column(String)  # TODO 临时
    score = Column(Integer)
    team_data = relationship("GameTeamData", uselist=False, backref="game_team_info")
    player_data = relationship("GamePlayerData", backref="game_team_info")


class GameTeamData(Base):
    __tablename__ = 'game_team_data'
    id = Column(Integer, primary_key=True, index=True)
    game_team_info_id = Column(Integer, ForeignKey('game_team_info.id'))

    created_time = Column(DateTime)
    attempts = Column(Integer)
    # 下底传中
    wing_cross = Column(Integer)
    wing_cross_success = Column(Integer)
    # 内切
    under_cutting = Column(Integer)
    under_cutting_success = Column(Integer)
    # 倒三角
    pull_back = Column(Integer)
    pull_back_success = Column(Integer)
    # 中路渗透
    middle_attack = Column(Integer)
    middle_attack_success = Column(Integer)
    # 防反
    counter_attack = Column(Integer)
    counter_attack_success = Column(Integer)


class GamePlayerData(Base):
    __tablename__ = 'game_player_data'
    id = Column(Integer, primary_key=True, index=True)
    game_team_info_id = Column(Integer, ForeignKey('game_team_info.id'))
    player_id = Column(Integer, ForeignKey('player.id'))

    created_time = Column(DateTime)
    name = Column(String)  # TODO 临时
    location = Column(Enum(Location))
    actions = Column(Integer)
    shots = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    # 传球
    passes = Column(Integer)
    pass_success = Column(Integer)
    # 过人
    dribbles = Column(Integer)
    dribble_success = Column(Integer)
    # 抢断
    tackles = Column(Integer)
    tackle_success = Column(Integer)
    # 争顶
    aerials = Column(Integer)
    aerial_success = Column(Integer)
    # 扑救
    saves = Column(Integer)
    save_success = Column(Integer)
    # 体力
    original_stamina = Column(Integer)
    final_stamina = Column(Integer)


# endregion

# region 球员数据

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey('club.id'))

    created_time = Column(DateTime)
    name = Column(String)
    translated_name = Column(String)
    nationality = Column(String)
    translated_nationality = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    birth_date = Column(String)

    values = Column(Integer)
    wages = Column(Integer)
    # Location
    ST_num = Column(Integer)
    CM_num = Column(Integer)
    LW_num = Column(Integer)
    RW_num = Column(Integer)
    CB_num = Column(Integer)
    LB_num = Column(Integer)
    RB_num = Column(Integer)
    GK_num = Column(Integer)
    CAM_num = Column(Integer)
    LM_num = Column(Integer)
    RM_num = Column(Integer)
    CDM_num = Column(Integer)
    # rating
    shooting = Column(Integer)
    passing = Column(Integer)
    dribbling = Column(Integer)
    interception = Column(Integer)
    pace = Column(Integer)
    strength = Column(Integer)
    aggression = Column(Integer)
    anticipation = Column(Integer)
    free_kick = Column(Integer)
    stamina = Column(Integer)
    goalkeeping = Column(Integer)
    # rating limit
    shooting_limit = Column(Integer)
    passing_limit = Column(Integer)
    dribbling_limit = Column(Integer)
    interception_limit = Column(Integer)
    pace_limit = Column(Integer)
    strength_limit = Column(Integer)
    aggression_limit = Column(Integer)
    anticipation_limit = Column(Integer)
    free_kick_limit = Column(Integer)
    stamina_limit = Column(Integer)
    goalkeeping_limit = Column(Integer)
    # 生涯数据
    game_data = relationship('GamePlayerData', backref='player')


# endregion

# region 教练数据
class Coach(Base):
    __tablename__ = 'coach'
    id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey('club.id'))

    created_time = Column(DateTime)
    name = Column(String)
    translated_name = Column(String)
    nationality = Column(String)
    translated_nationality = Column(String)
    age = Column(Integer)
    birth_date = Column(String)
    values = Column(Integer)
    wages = Column(Integer)
    # 战术
    tactic = Column(String)
    wing_cross = Column(Integer)
    under_cutting = Column(Integer)
    pull_back = Column(Integer)
    middle_attack = Column(Integer)
    counter_attack = Column(Integer)


# endregion

# region 俱乐部数据
class Club(Base):
    __tablename__ = 'club'
    id = Column(Integer, primary_key=True, index=True)

    created_time = Column(DateTime)
    name = Column(String)
    finance = Column(Float)

    coach = relationship("Coach", uselist=False, backref="club")
    players = relationship("Player", backref="club")

# endregion
