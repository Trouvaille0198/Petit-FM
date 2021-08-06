import config
import random
import datetime
from utils.date import Date
from sql_app import schemas, crud, models
from club_app import Club
from game_app import Game


class League:
    def __init__(self, init_type=1, league_data: dict = None, league_id: int = 0):
        self.id = league_id
        self.league_model = None
        self.data = dict()
        if init_type == 1:
            # 新建
            self.generate(league_data)
            self.import_data()
        elif init_type == 2:
            # 导入数据
            self.import_data()
        else:
            config.logger.error('球员初始化错误！')

    def generate(self, league_data: dict):
        self.data['created_time'] = datetime.datetime.now()
        self.data['name'] = league_data['name']
        self.save_in_db(init=True)
        for club_data in league_data['clubs']:
            club = Club(init_type=1, club_data=club_data)
            club.switch_league(self.id)

    def update_league(self):
        """
        更新联赛数据，并保存至数据库
        使用时，将待修改的值送入self.data中，然后调用此函数即可
        """
        self.save_in_db(init=False)

    def import_data(self):
        self.league_model = crud.get_league_by_id(self.id)

    def export_data(self) -> schemas.League:
        """
        将初始化的联赛数据转换为schemas格式
        :return: schemas.League
        """
        data_model = schemas.League(**self.data)
        return data_model

    def save_in_db(self, init: bool):
        """
        导出数据至数据库
        """
        if init:
            data_schemas = self.export_data()
            league_model = crud.create_league(data_schemas)
            self.id = league_model.id
        else:
            # 更新
            crud.update_league(league_id=self.id, attri=self.data)
        print('成功导出联赛数据！')

    @staticmethod
    def play_game(club_model1: models.Club, club_model2: models.Club, date: Date):
        game = Game(club_model1, club_model2, date)
        scores = game.start()
        print("{} {}:{} {}".format(club_model1.name, scores[0], scores[1], club_model2.name))

    def start_season(self, date: Date):
        clubs = self.league_model.clubs
        season = dict()
        for club in clubs:
            season[club] = {rival: 2 for rival in clubs if rival != club}
        for _ in range((len(clubs) - 1) * 2):
            print('{} 的比赛'.format(str(date)))
            for club, rivals in season.items():
                rival = random.choice([x for x in list(rivals) if x != 0])
                rivals[rival] -= 1
                self.play_game(club, rival, date)
            date.plus_days(7)

    def start(self, start_year: int = 2022, years: int = 1):
        for _ in range(years):
            self.start_season(Date(start_year, 2, random.randint(1, 28)))
