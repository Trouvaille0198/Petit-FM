import config
import datetime
from sql_app import schemas, crud
from coach_app import Coach
from player_app import Player


class Club:
    def __init__(self, init_type=1, club_data: dict = None):
        self.id = 0
        self.data = dict()
        if init_type == 1:
            # 新建
            self.generate(club_data)

        elif init_type == 2:
            # 导入数据
            self.import_data()
        else:
            config.logger.error('球员初始化错误！')

    def generate(self, club_data: dict):
        self.data['created_time'] = datetime.datetime.now()
        self.data['name'] = club_data['name']
        self.data['finance'] = club_data['finance']
        self.save_in_db(init=True)
        coach = Coach(init_type=1)
        coach.switch_club(self.id)
        for _ in range(11):
            player = Player(init_type=1)
            player.switch_club(self.id)

    def import_data(self):
        pass

    def export_data(self) -> schemas.Club:
        data_model = schemas.Club(**self.data)
        return data_model

    def save_in_db(self, init: bool):
        """
        导出数据至数据库
        """
        if init:
            club_data = self.export_data()
            club_model = crud.create_club(club_data)
            self.id = club_model.id
        else:
            # 更新
            pass
        print('成功导出俱乐部数据！')
