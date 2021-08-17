from league_app import League
from utils.date import Date
import config
import random
from sql_app import crud
from league_system_app import LeagueSystem
from info_app import Info

# 初始化
config.init_current_path()

world = LeagueSystem(init_leagues=False)
world.start_season(2030, 1)

# 模拟比赛
# l1 = League(init_type=2, league_id=1)
# clubs = [l1.league_model.clubs[1], l1.league_model.clubs[2]]
# crud.delete_game_by_attri(query_str='models.Game.season=="2019"')
# for _ in range(10):
#     l1.play_game(clubs[0], clubs[1], Date(2019, 4, 6))
