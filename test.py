from league_app import League
from utils.date import Date
import config


def init_leagues():
    for league in config.leagues:
        c = League(league_data=league, init_type=1)


# init_leagues()
date = Date(2021, 8, 6)
l1 = League(init_type=2, league_id=1)
l1.start_season(date)
