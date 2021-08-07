from league_app import League
from utils.date import Date
import config
from sql_app import crud


def init_leagues():
    for league in config.leagues:
        c = League(league_data=league, init_type=1)


config.init_current_path()
# init_leagues()

# date = Date(2021, 8, 6)
l1 = League(init_type=2, league_id=1)
l1.start(start_year=2022, years=5, save_in_db=True)
