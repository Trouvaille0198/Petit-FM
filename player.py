import random
from const import *
from logger import logger


class Player():
    def __init__(self, coor=(0, 0), side=-1, position='DEFAULT'):
        self.id = random.randint(0, 65536)
        self.coor = coor
        self.side = side
        self.ball_state = False
        self.done = False
        self.position = position
        self.overlap = False

    # 辅助函数
    def init_player(self, game, coor):
        """
        初始化球员状态
        :param game: 上级game实例
        :param coor: 初始坐标
        """
        self.coor = coor
        self.ball_state = False
        self.done = False
        game.field.update_coor_content(coor, self)

    def is_same_side(self, another_player):
        return self.side == another_player.side

    def random_select_coor(self, coor: tuple, width: int = 2) -> tuple:
        """
        随机选择附近的坐标
        :param coor: 中心坐标
        :param width: 范围
        :return: 随机坐标
        """
        row = random.randint(coor[0]-width, coor[0]+width)
        col = random.randint(coor[1]-width, coor[1]+width)
        return (row, col)

    # 球员操作
    def move_to(self, game, coor: tuple):
        """
        移动到指定坐标处
        :param game: 比赛类实例
        :param coor: 目标坐标
        """
        if coor != self.coor:
            game.field.update_player_location(self, coor)

    def pass_ball(self, game, next_player):
        """
        传球
        :param game: 比赛类实例
        :param next_player: 传给的球员
        """
        if ball_state:
            self.ball_state = False
            target_coor = next_player.coor
            # TODO 拦截判定
            distance = int(game.field.get_distance(self.coor, next_player.coor)/10)  # 12级
            # TODO 补充落地范围判定逻辑
            final_coor = self.random_select_coor(target_coor, distance)  # 暂时先随机选择
            game.field.update_ball_location(game.players.ball, (x, y))

    def scramble(self, another_player):
        """
        当球无人持有时，争抢球权
        :param another_player: 另一个球员
        :return: 争抢成功的球员实例
        """
        # TODO 补充争抢逻辑，决出胜者
        win_player = random.choice((self, another_player))  # 暂时随机选
        return win_player

    def challenge(self, another_player):
        """
        过人或抢断
        :param another_player: 另一个球员
        """
        # TODO 补充过人和抢断逻辑，决出胜者
        win_player = random.choice((self, another_player))  # 暂时随机选
        return win_player

    def overlap_judge(self):
        """
        可能不需要
        持球球员遇到重合时的动作
        """

    def act(self, game):
        """
        球员进行相应位置的动作
        :param game: 比赛实例
        """
        if not self.done:
            for position in POSITION_LIST:
                if position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                elif position == 'DEFALUT':
                    pass
                else:
                    pass
        self.done = True
