import pandas as pd
from typing import List
import config
from sql_app import crud, models, database
from utils import utils


class Info:
    def __init__(self):
        pass

    @staticmethod
    def switch2df(data: List[dict]):
        return pd.DataFrame(data)

    def get_season_player_chart(self, year: str) -> pd.DataFrame:
        """
        获取赛季球员数据
        :param year: 赛季年份
        :return: df
        """
        query_str = 'models.Game.season=="{}"'.format(year)
        games = crud.get_games_by_attri(query_str=query_str)
        player_data_list = [player_data for game in games for game_team_info in game.teams for player_data in
                            game_team_info.player_data]
        filtered_list = []
        for player_data in player_data_list:
            one_piece = {
                'id': player_data.player_id,
                '名字': player_data.name,
                '进球数': player_data.goals,
                '助攻数': player_data.assists,
                '传球数': player_data.passes,
                '传球成功数': player_data.pass_success,
                '过人数': player_data.dribbles,
                '过人成功数': player_data.dribble_success,
                '抢断数': player_data.tackles,
                '抢断成功数': player_data.tackle_success,
                '争顶数': player_data.aerials,
                '争顶成功数': player_data.aerial_success,
                '扑救数': player_data.saves,
                '扑救成功数': player_data.save_success
            }
            filtered_list.append(one_piece)
        df = self.switch2df(filtered_list)
        df = df.groupby(by=['id', '名字']).agg(
            {
                '进球数': 'sum', '助攻数': 'sum',
                '传球数': 'sum', '传球成功数': 'sum',
                '过人数': 'sum', '过人成功数': 'sum',
                '抢断数': 'sum', '抢断成功数': 'sum',
                '争顶数': 'sum', '争顶成功数': 'sum',
                '扑救数': 'sum', '扑救成功数': 'sum', })
        s = df.apply(
            lambda row: float(utils.retain_decimal(row['传球成功数'] / row['传球数']) * 100) if row['传球数'] != 0 else 0, axis=1)
        df.insert(2, '传球成功率', s)

        s = df.apply(
            lambda row: float(utils.retain_decimal(row['过人成功数'] / row['过人数']) * 100) if row['过人数'] != 0 else 0, axis=1)
        df.insert(3, '过人成功率', s)

        s = df.apply(
            lambda row: float(utils.retain_decimal(row['抢断成功数'] / row['抢断数']) * 100) if row['抢断数'] != 0 else 0, axis=1)
        df.insert(4, '抢断成功率', s)

        s = df.apply(
            lambda row: float(utils.retain_decimal(row['争顶成功数'] / row['争顶数']) * 100) if row['争顶数'] != 0 else 0, axis=1)
        df.insert(5, '争顶成功率', s)

        s = df.apply(
            lambda row: float(utils.retain_decimal(row['扑救成功数'] / row['扑救数']) * 100) if row['扑救数'] != 0 else 0, axis=1)
        df.insert(6, '扑救成功率', s)
        return df

    @staticmethod
    def save_in_db(df, filename: str):
        # df.to_csv(path + '/' + filename)
        df.to_sql(filename, database.engine)


if __name__ == '__main__':
    info = Info()
    print(info.get_season_player_chart('2021'))
    info.save_in_db(info.get_season_player_chart('2021'), 'season_2021_chart')
