from config import *
from utils import utils
from player_app import PlayerGenerator
import datetime
from sql_app import schemas, crud
import random


class Coach:
    def __init__(self, init_type=1):
        self.id = 0
        self.data = dict()
        if init_type == 1:
            # 随机生成
            self.generate()
        elif init_type == 2:
            # 导入数据
            self.import_data()
        else:
            logger.error('球员初始化错误！')

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
        self.data['tactic'] = random.choice([x for x in tactic_config.keys()])
        self.data['wing_cross'] = utils.get_mean_range(50, per_range=0.9)
        self.data['under_cutting'] = utils.get_mean_range(50, per_range=0.9)
        self.data['pull_back'] = utils.get_mean_range(50, per_range=0.9)
        self.data['middle_attack'] = utils.get_mean_range(50, per_range=0.9)
        self.data['counter_attack'] = utils.get_mean_range(50, per_range=0.9)
        self.save_in_db(init=True)

    def import_data(self):
        pass

    def export_data(self) -> schemas.Coach:
        data_model = schemas.Coach(**self.data)
        return data_model

    def save_in_db(self, init: bool):
        """
        导出数据至数据库
        """
        if init:
            data = self.export_data()
            coach_model = crud.create_coach(data)
            self.id = coach_model.id
        else:
            # 更新
            pass
        print('成功导出教练数据！')

    def switch_club(self, club_id: int):
        crud.update_coach(coach_id=self.id, coach={'club_id': club_id})


if __name__ == "__main__":
    for _ in range(20):
        p = Coach()
        print(p.export_data())
