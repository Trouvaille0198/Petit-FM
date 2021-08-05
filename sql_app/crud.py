from sqlalchemy.orm import Session
from sql_app import models, schemas, database
from sql_app.database import db_openish


@db_openish
def create_game(game: schemas.Game, db: Session):
    db_game = models.Game(created_time=game.created_time, date=game.date, script=game.script)
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
def test(db: Session):
    players = db.query(models.GamePlayerData).filter(models.GamePlayerData.name == '梅西',
                                                     models.GamePlayerData.game_team_info.has(
                                                         models.GameTeamInfo.name == '巴塞罗那')).all()
    print([player.final_stamina for player in players])


if __name__ == '__main__':
    test()
