import numpy as np
from const import *
from player import Player
from ball import Ball
import bisect


class Field():
    __length = FIELD_LENGTH
    __width = FIELD_WIDTH

    def __init__(self):
        self.coors = [[None for i in range(self.__length)] for j in range(self.__width)]

    # 辅助函数
    def init_field(self):
        """
        初始化球场
        """
        self.coors = [[None for i in range(self.__length)] for j in range(self.__width)]

    def get_coor_content(self, coor: tuple):
        """
        获取坐标内容
        :param coor: 坐标值
        :return: 坐标内容
        """
        return self.coors[coor[0]][coor[1]]

    def update_coor_content(self, coor: tuple, sth):
        """
        更新坐标内容
        :param coor: 坐标值
        :param sth: 待更新的内容
        """
        self.coors[coor[0]][coor[1]] = sth

    def exchange_coor_content(self, coor1: tuple, coor2: tuple):
        """
        交换两个坐标的内容
        :param coor1: 坐标1
        :param coor2: 坐标2
        """
        temp = self.get_coor_content(coor1)
        self.update_coor_content(coor1, self.get_coor_content(coor2))
        self.update_coor_content(coor2, temp)

    def is_out_of_border(self, coor: tuple):
        """
        是否出界
        :param coor: 目标坐标
        :return: 是否出界
        """
        if 0 <= coor[0] <= FIELD_LENGTH and 0 <= coor[1] <= FIELD_WIDTH:
            return False
        else:
            return True

    def adjust_out_of_border(self, coor: tuple):
        """
        若出界，选取边界坐标，不考虑修改后的坐标上是否有其他实例
        :param coor: 目标坐标
        :return: 原坐标或修改后的边界坐标
        """
        if self.is_out_of_border(coor):
            coor = list(coor)
            if coor[0] < 0:
                coor[0] = 0
            if coor[0] > FIELD_WIDTH:
                coor[0] = FIELD_WIDTH
            if coor[1] < 0:
                coor[1] = 0
            if coor[1] > FIELD_LENGTH:
                coor[1] = FIELD_LENGTH
            return tuple(coor)
        else:
            return tuple(coor)

    def get_range_coors(self, start_row=0, end_row=FIELD_WIDTH-1, start_col=0, end_col=FIELD_LENGTH-1) -> list:
        """
        获取指定长宽范围内的二维坐标
        :param start_row: 起始行
        :param r_len: 终止行
        :param start_col: 起始列
        :param  c_len: 终止列
        :return: 范围内的二维坐标
        """
        return list(
            map(lambda x: x[start_col:end_col+1],
                self.coors[start_row:end_row+1]))

    def coor_content_generator(self, start_row=0, end_row=FIELD_WIDTH-1, start_col=0, end_col=FIELD_LENGTH-1):
        """
        指定长宽范围内二维坐标实例生成器
        :param start_row: 起始行
        :param r_len: 终止行
        :param start_col: 起始列
        :param  c_len: 终止列
        :yield: 实例
        """
        range_coors = self.get_range_coors(start_row, end_row, start_col, end_col)
        for a in range_coors:
            for b in a:
                yield b

    def get_all_players(self) -> list:
        """
        获取场上所有球员实例
        :return: 球员实例列表
        """
        players = []
        for a in self.coor_content_generator():
            if isinstance(a, Player):
                players.append(a)
        return players

    def get_ball_held_player(self):
        if self.ball_is_held():
            for player in self.get_all_players():
                if player.ball_state == True:
                    return player
        return None

    def get_square_range_coors(self, coor: tuple, width=2) -> list:
        """
        获取方形范围内的二维坐标
        :param coor: 中心坐标
        :param width: 从中心扩展的长度
        :return: 范围内的二维坐标
        """
        return list(
            map(lambda x: x[(coor[1] - width):(coor[1] + width + 1)],
                self.coors[(coor[0] - width):(coor[0] + width + 1)]))

    def get_square_range_player(self, coor: tuple, side=1, width=2) -> list:
        """
        获取方形范围内单方球员实例
        :param coor: 中心坐标
        :param side: 球员选边
        :param width: 从中心扩展的长度
        :return: 球员实例列表
        """
        range_player = []
        range_coor = self.get_range_coors(coor=coor, width=width)
        for a in range_coor:
            for b in a:
                if isinstance(b, Player) and b.side == side:
                    range_player.append(b)
        return range_player

    def get_square_range_player_num(self, coor: tuple, side: int = 1, width: int = 2) -> int:
        """
        获取方形范围内某一方球员数量
        :param coor: 中心坐标
        :param side: 球员选边
        :param width: 从中心扩展的长度
        :return: 数量
        """
        return len(self.get_range_player(coor, side, width))

    def update_ball_location(self, ball, ball_coor: tuple):
        """
        更新足球位置
        :param ball: 球实例，来自player_group
        :param ball_coor: 球坐标
        """
        # 正常情况下，更新球位置时，球原本是被持有的，所以不用判断是否有未持有球的情况
        ball_coor = self.adjust_out_of_border(ball_coor)  # TODO暂时不考虑球出界
        coor_content = self.get_coor_content(ball_coor)
        if self.is_out_of_border(ball_coor):
            pass
        elif coor_content == None:
            # 空地改为球落点
            self.update_coor_content(ball_coor, ball)
            ball.coor = ball_coor
            ball.is_held = False
        elif isinstance(coor_content, Player):
            # 若更新的位置有球员
            coor_content.ball_state = True  # 修改球员持球情况
            ball.coor = ball_coor

    def update_player_location(self, player, target_coor: tuple):
        """
        更新球员位置
        :param player: 球员实例
        :param target_coor: 目标坐标
        """
        target_coor = self.adjust_out_of_border(target_coor)
        target_coor_content = self.get_coor_content(target_coor)
        if isinstance(target_coor_content, Ball):
            # 恰好移动到足球处
            player.ball_state = True
            target_coor_content.is_held = True
            self.update_coor_content(target_coor_content, None)
        elif isinstance(target_coor_content, Player):
            # 如果目标坐标是球员实例
            if target_coor_content.side == player.side:
                # TODO与对友重叠
                while isinstance(self.get_coor_content(target_coor)):
                    # 随机增减最终坐标，直到不与球员重叠
                    target_coor = list(target_coor)
                    x = random.choice((-1, 1, 0, -2, 2))
                    y = random.choice((-1, 1, 0, -2, 2))
                    target_coor[0] += y
                    target_coor[1] += x
                    target_coor = self.adjust_out_of_border(tuple(target_coor))
            elif target_coor_content.side == -player.side:
                # 与对手重叠，若无球球员移动到有球球员上，则应该在时间帧开始时进行逼抢判定，这里不修改
                if target_coor_content.ball_state == False:
                    # 若被重叠的球员没有持球，则主动移动球员不论是否持球，都应该闪避
                    while isinstance(self.get_coor_content(target_coor)):
                        # 随机增减最终坐标，直到不与球员重叠
                        target_coor = list(target_coor)
                        x = random.choice((-1, 1, 0, -2, 2))
                        y = random.choice((-1, 1, 0, -2, 2))
                        target_coor[0] += y
                        target_coor[1] += x
                        target_coor = self.adjust_out_of_border(tuple(target_coor))
                else:
                    # 若无球球员移动到有球球员上，则允许重叠，在下一个时间帧进行抢断与过人判定
                    player.overlap = True  # 此时不变动坐标，仅仅修改重叠状态
        else:
            # 可能还有其他情况
            pass
        self.exchange_coor_content(player.coor, target_coor)  # 完成移动
        player.coor = target_coor

    def get_distance(self, coor1, coor2) -> int:
        """
        获取两个坐标之间的距离
        :param coor1: 坐标1
        :param coor2: 坐标2
        :return: 距离的整数值
        """
        return int(((coor1[0]-coor2[0])**2 + (coor1[1]-coor2[1])**2) ** 0.5)

    def ball_is_held(self) -> bool:
        """
        足球是否有人持有
        :return: 持有情况
        """
        for a in self.coor_content_generator():
            if isinstance(a, Ball):
                return False
        return True

    def get_ball_location(self) -> tuple:
        """
        获取球坐标
        :return: 球坐标
        """
        for a in self.coor_content_generator():
            if isinstance(a, Ball):
                return a.coor
            if isinstance(a, Player) and a.ball_state:
                return a.coor

    def get_nearest_player(self, coor: tuple = None, n=3) -> list:
        """
        获取离指定坐标最近的n个球员
        :param coor: 指定坐标
        :param n: 返回个数
        :return: 球员实例列表
        """
        if not coor:
            # coor默认为无人持有的足球坐标
            if self.ball_is_held():
                raise ValueError('没有有效的coor值，且场上足球被人持有')
            else:
                coor = self.get_ball_location()
        player_list = []
        for a in self.coor_content_generator():
            if isinstance(a, Player):
                bisect.insort(
                    player_list, (self.get_distance(a.coor, coor), a)
                )
        return [x[1] for x in player_list[:n]]
