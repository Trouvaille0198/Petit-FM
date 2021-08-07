import config
import random
import datetime
from utils.date import Date
from sql_app import schemas, crud, models
from club_app import Club
from game_app import Game
from info_app import Info


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
        crud.delete_game_by_attri(query_str='models.Game.season=="{}"'.format(date.year))

        clubs = self.league_model.clubs

        clubs_a = random.sample(clubs, len(clubs) // 2)
        clubs_b = list(set(clubs) ^ set(clubs_a))
        schedule = []  # 比赛赛程
        for _ in range((len(clubs) - 1)):
            # 前半赛季的比赛
            schedule.append([game for game in zip(clubs_a, clubs_b)])
            clubs_a.insert(1, clubs_b.pop(0))
            clubs_b.append(clubs_a.pop(-1))
        schedule_reverse = []  # 主客场对调的后半赛季赛程
        for games in schedule:
            schedule_reverse.append([tuple(list(x)[::-1]) for x in games])
        schedule.extend(schedule_reverse)

        for games in schedule:
            # 进行每一轮比赛
            print('{} 的比赛'.format(str(date)))
            for game in games:
                self.play_game(game[0], game[1], date)
            date.plus_days(7)

    def start(self, start_year: int = 2022, years: int = 1, save_in_db: bool = False):
        info = Info()
        for _ in range(years):
            self.start_season(Date(start_year, 2, random.randint(1, 28)))
            info.save(info.get_season_player_chart(
                str(start_year)), filename='output_data/{}{}赛季球员数据榜.csv'.format(
                self.league_model.name, str(start_year)), file_format='csv')
            info.save(info.get_points_table(
                str(start_year)), filename='output_data/{}{}赛季积分榜.csv'.format(
                self.league_model.name, str(start_year)), file_format='csv')
            if save_in_db:
                info.save_in_db(info.get_season_player_chart(str(start_year)),
                                '{}{}赛季球员数据榜'.format(
                                    self.league_model.name, str(start_year)))
                info.save_in_db(info.get_points_table(str(start_year)),
                                '{}{}赛季积分榜'.format(
                                    self.league_model.name, str(start_year)))
            start_year += 1
