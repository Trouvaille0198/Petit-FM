from sqlalchemy.orm import Session
from sql_app import models, schemas, database
from sql_app.database import db_openish
import config


# region 比赛操作
@db_openish
def create_game(game: schemas.Game, db: Session):
    db_game = models.Game(created_time=game.created_time, date=game.date, script=game.script, season=game.season,
                          mvp=game.mvp)
    # 提交数据库，生成id
    db.add(db_game)
    db.commit()

    for team_info in game.teams:
        create_game_team_info(db_game.id, team_info)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@db_openish
def create_game_team_info(game_id: int, game_team_info: schemas.GameTeamInfo, db: Session):
    db_game_team_info = models.GameTeamInfo(
        game_id=game_id,
        club_id=game_team_info.club_id,
        created_time=game_team_info.created_time,
        name=game_team_info.name,
        score=game_team_info.score)
    # 提交数据库，生成id
    db.add(db_game_team_info)
    db.commit()

    create_game_team_data(db_game_team_info.id, game_team_info.team_data)
    for player_datum in game_team_info.player_data:
        create_game_player_data(db_game_team_info.id, player_datum)

    db.add(db_game_team_info)
    db.commit()
    db.refresh(db_game_team_info)
    return db_game_team_info


@db_openish
def create_game_team_data(game_team_info_id: int, game_team_data: schemas.GameTeamData, db: Session):
    db_game_team_data = models.GameTeamData(game_team_info_id=game_team_info_id, **game_team_data.dict())
    db.add(db_game_team_data)
    db.commit()
    db.refresh(db_game_team_data)
    return db_game_team_data


@db_openish
def create_game_player_data(game_team_info_id: int, game_player_data: schemas.GamePlayerData, db: Session):
    db_game_player_data = models.GamePlayerData(game_team_info_id=game_team_info_id, **game_player_data.dict())
    db.add(db_game_player_data)
    db.commit()
    db.refresh(db_game_player_data)
    return db_game_player_data


@db_openish
def get_games_by_attri(query_str: str, db: Session, only_one: bool = False):
    if only_one:
        db_game = db.query(models.Game).filter(eval(query_str)).first()
        return db_game
    else:
        db_games = db.query(models.Game).filter(eval(query_str)).all()
        return db_games


@db_openish
def delete_game_by_attri(query_str: str, db: Session):
    db_games = db.query(models.Game).filter(eval(query_str)).all()
    if not db_games:
        config.logger.info('无比赛表可删！')
    for db_game in db_games:
        db_game_teams_info = db.query(models.GameTeamInfo).filter(
            models.GameTeamInfo.game_id == db_game.id).all()
        for db_game_team_info in db_game_teams_info:
            db_game_team_data = db.query(models.GameTeamData).filter(
                models.GameTeamData.game_team_info_id == db_game_team_info.id).first()
            db.delete(db_game_team_data)
            db_game_players_data = db.query(models.GamePlayerData).filter(
                models.GamePlayerData.game_team_info_id == db_game_team_info.id).all()
            for db_game_player_data in db_game_players_data:
                db.delete(db_game_player_data)
            db.delete(db_game_team_info)
        db.delete(db_game)
        db.commit()


# endregion


# region 球员操作
@db_openish
def create_player(player: schemas.Player, db: Session):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


@db_openish
def update_player(player_id: int, attri: dict, db: Session):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    for key, value in attri.items():
        setattr(db_player, key, value)
    db.commit()
    return db_player


@db_openish
def get_player_by_id(player_id: int, db: Session):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    return db_player


def get_players_by_attri(attri: str, db: Session, only_one: bool = False):
    if only_one:
        db_player = db.query(models.Player).filter(eval(attri)).first()
        return db_player
    else:
        db_players = db.query(models.Player).filter(eval(attri)).all()
        return db_players


@db_openish
def delete_player(player_id: int, db: Session):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    db.delete(db_player)


# endregion

# region 教练操作
@db_openish
def create_coach(coach: schemas.Coach, db: Session):
    db_coach = models.Coach(**coach.dict())
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach


@db_openish
def update_coach(coach_id: int, attri: dict, db: Session):
    db_coach = db.query(models.Coach).filter(models.Coach.id == coach_id).first()
    for key, value in attri.items():
        setattr(db_coach, key, value)
    db.commit()
    return db_coach


@db_openish
def get_coach_by_id(coach_id: int, db: Session):
    db_coach = db.query(models.Coach).filter(models.Coach.id == coach_id).first()
    return db_coach


# endregion

# region 俱乐部操作
@db_openish
def create_club(club: schemas.Club, db: Session):
    db_club = models.Club(**club.dict())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club


@db_openish
def update_club(club_id: int, attri: dict, db: Session):
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    for key, value in attri.items():
        setattr(db_club, key, value)
    db.commit()
    return db_club


@db_openish
def get_club_by_id(club_id: int, db: Session):
    db_club = db.query(models.Club).filter(models.Club.id == club_id).first()
    return db_club


# endregion

# region 联赛操作
@db_openish
def create_league(league: schemas.League, db: Session):
    db_league = models.League(**league.dict())
    db.add(db_league)
    db.commit()
    db.refresh(db_league)
    return db_league


@db_openish
def get_league_by_id(league_id: int, db: Session):
    db_league = db.query(models.League).filter(models.League.id == league_id).first()
    return db_league


@db_openish
def update_league(league_id: int, attri: dict, db: Session):
    db_league = db.query(models.League).filter(models.League.id == league_id).first()
    for key, value in attri.items():
        setattr(db_league, key, value)
    db.commit()
    return db_league

# endregion
