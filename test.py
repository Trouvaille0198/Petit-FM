from club_app import Club
import config


def init_clubs():
    for club in config.clubs:
        c = Club(club_data=club, init_type=1)


init_clubs()
