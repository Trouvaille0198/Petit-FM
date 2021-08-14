from league_app import League
from utils.date import Date
import config
import random
from sql_app import crud


def init_leagues():
    for league in config.leagues:
        c = League(league_data=league, init_type=1)


# 初始化
config.init_current_path()
init_leagues()

# 模拟联赛
l1 = League(init_type=2, league_id=1)
l2 = League(init_type=2, league_id=2)

l1.start(start_year=2022, years=3, save_in_db=True)
l2.start(start_year=2022, years=3, save_in_db=True)

# 模拟比赛
# l1 = League(init_type=2, league_id=1)
# clubs = [l1.league_model.clubs[1], l1.league_model.clubs[2]]
# crud.delete_game_by_attri(query_str='models.Game.season=="2019"')
# for _ in range(10):
#     l1.play_game(clubs[0], clubs[1], Date(2019, 4, 6))
