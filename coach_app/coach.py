import config
from utils import utils
from player_app import PlayerGenerator
import datetime
from sql_app import schemas, crud, models
from typing import List
import random


class Coach:
    def __init__(self, init_type: int = 1, coach_id: int = 0):
        self.id = coach_id
        self.coach_model = None
        self.data = dict()
        if init_type == 1:
            # 随机生成
            self.generate()
            self.import_data()
        elif init_type == 2:
            # 导入数据
            self.import_data()
        else:
            config.logger.error('球员初始化错误！')

    def generate(self):
        generator = PlayerGenerator()  # 球员的生成器，暂且给教练用用
        self.data['created_time'] = datetime.datetime.now()
        self.data['name'] = generator.get_name()
        self.data['translated_name'] = generator.translate(self.data['name'])
        self.data['nationality'] = generator.get_nationality() \
            if self.data['name'] != self.data['translated_name'] else 'China'
        self.data['translated_nationality'] = generator.translate(self.data['nationality'])
        self.data['birth_date'] = generator.get_birthday()
        # tactic
        self.data['tactic'] = random.choice([x for x in config.tactic_config.keys()])
        self.data['wing_cross'] = utils.get_mean_range(50, per_range=0.9)
        self.data['under_cutting'] = utils.get_mean_range(50, per_range=0.9)
        self.data['pull_back'] = utils.get_mean_range(50, per_range=0.9)
        self.data['middle_attack'] = utils.get_mean_range(50, per_range=0.9)
        self.data['counter_attack'] = utils.get_mean_range(50, per_range=0.9)
        self.save_in_db(init=True)

    def import_data(self):
        self.coach_model = crud.get_coach_by_id(self.id)

    def update_coach(self):
        """
        更新教练数据，并保存至数据库
        使用时，将待修改的值送入self.data中，然后调用此函数即可
        """
        self.save_in_db(init=False)

    def export_data(self) -> schemas.Coach:
        data_model = schemas.Coach(**self.data)
        return data_model

    def save_in_db(self, init: bool):
        """
        导出数据至数据库
        """
        if init:
            data_schemas = self.export_data()
            coach_model = crud.create_coach(data_schemas)
            self.id = coach_model.id
        else:
            # 更新
            crud.update_coach(coach_id=self.id, attri=self.data)
        print('成功导出教练数据！')

    def switch_club(self, club_id: int):
        crud.update_coach(coach_id=self.id, attri={'club_id': club_id})

    def select_players(self, players: List[models.Player]):
        final_players = []
        final_locations = []
        players_copy = players.copy()
        location_list = config.tactic_config[self.coach_model.tactic]
        for name, num in location_list.items():
            if num != 0:
                # TODO 选人机制
                final_players.append(random.choice(players_copy))
                final_locations.append(name)
        return final_players, final_locations


if __name__ == "__main__":
    for _ in range(20):
        p = Coach()
        print(p.export_data())
