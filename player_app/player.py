from config import *
from player_app import PlayerGenerator
import datetime
from sql_app import schemas, crud


class Player:
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
        generator = PlayerGenerator()
        self.data['created_time'] = datetime.datetime.now()
        self.data['name'] = generator.get_name()
        self.data['translated_name'] = generator.translate(self.data['name'])
        self.data['nationality'] = generator.get_nationality() \
            if self.data['name'] != self.data['translated_name'] else 'China'
        self.data['translated_nationality'] = generator.translate(self.data['nationality'])
        self.data['height'] = generator.get_height()
        self.data['weight'] = generator.get_weight()
        self.data['birth_date'] = generator.get_birthday()
        # rating generation
        self.data['shooting'] = generator.get_rating(self.data['translated_nationality'])
        self.data['passing'] = generator.get_rating(self.data['translated_nationality'])
        self.data['dribbling'] = generator.get_rating(self.data['translated_nationality'])
        self.data['interception'] = generator.get_rating(self.data['translated_nationality'])
        self.data['pace'] = generator.get_rating(self.data['translated_nationality'])
        self.data['strength'] = generator.get_rating(self.data['translated_nationality'])
        self.data['aggression'] = generator.get_rating(self.data['translated_nationality'])
        self.data['anticipation'] = generator.get_rating(self.data['translated_nationality'])
        self.data['free_kick'] = generator.get_rating(self.data['translated_nationality'])
        self.data['stamina'] = generator.get_rating(self.data['translated_nationality'])
        self.data['goalkeeping'] = generator.get_rating(self.data['translated_nationality'])
        # rating limit generation
        self.data['shooting_limit'] = generator.get_rating_potential()
        self.data['passing_limit'] = generator.get_rating_potential()
        self.data['dribbling_limit'] = generator.get_rating_potential()
        self.data['interception_limit'] = generator.get_rating_potential()
        self.data['pace_limit'] = generator.get_rating_potential()
        self.data['strength_limit'] = generator.get_rating_potential()
        self.data['aggression_limit'] = generator.get_rating_potential()
        self.data['anticipation_limit'] = generator.get_rating_potential()
        self.data['free_kick_limit'] = generator.get_rating_potential()
        self.data['stamina_limit'] = generator.get_rating_potential()
        self.data['goalkeeping_limit'] = generator.get_rating_potential()
        self.save_in_db(init=True)

    def import_data(self):
        pass

    def export_data(self) -> schemas.Player:
        data_model = schemas.Player(**self.data)
        return data_model

    def save_in_db(self, init: bool):
        """
        导出数据至数据库
        """
        if init:
            data = self.export_data()
            player_model = crud.create_player(data)
            self.id = player_model.id

        else:
            # 更新
            pass
        print('成功导出球员数据！')

    def switch_club(self, club_id: int):
        crud.update_player(player_id=self.id, player={'club_id': club_id})


if __name__ == "__main__":
    for _ in range(200):
        p = Player()
        print(p.export_data())
