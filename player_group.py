from player import Player
from ball import Ball
import random
from const import *
from logger import logger


class PlayerGroup():
    def __init__(self, game):
        self.ball = Ball()
        self.init_player_info()
        self.init_player_location(game)

    # 构造函数
    def init_player_info(self):
        self.left_players = [Player(side=-1)]
        self.right_players = [Player(side=1)]

    def init_player_location(self, game):
        game.field.init_field()
        for player in self.left_players:
            if player.position == 'DEFAULT':
                player.init_player(game, (24, 30))
        for player in self.right_players:
            if player.position == 'DEFAULT':
                player.init_player(game, (24, 38))

        self.ball.coor = self.left_players[0].coor
        self.left_players[0].ball_state = True

    # 辅助函数
    def get_player_by_coor(self, coor: tuple):
        """
        根据坐标返回球员实例
        :param coor: 坐标
        :return: 球员实例
        """
        for player in self.left_players:
            if player.coor == coor:
                return player
        for player in self.right_players:
            if player.coor == coor:
                return player
        return None

    def scramble(self, p1, p2):
        """
        争抢，返回胜负者
        :param p1: 球员1
        :param p2: 球员2
        :return: 胜者，败者
        """
        win_player = p1.scramble(p2)
        if win_player == p1:
            return p1, p2
        else:
            return p2, p1

    # 判定函数
    def scramble_judge(self, game):
        """
        争抢判定
        :param game: 比赛实例
        """
        if not game.field.ball_is_held():
            # 判定是否无人持球
            logger.debug('争抢判定')
            ball_location = game.field.get_ball_location()
            players = game.field.get_nearest_player()
            lplayers = []
            rplayers = []
            for player in players:
                if player in self.left_players:
                    logger.debug('添加一名球员到左方')
                    lplayers.append(player)
                else:
                    rplayers.append(player)
            if not lplayers:
                # 没有左队球员
                rplayers[0].move_to(game, ball_location)  # 右队最近的球员移动到球位置
            elif not rplayers:
                # 没有右队球员
                lplayers[0].move_to(game, ball_location)  # 左队最近的球员移动到球位置
            else:
                while True:
                    lplayer = random.choice(lplayers)
                    rplayer = random.choice(rplayers)
                    win_player, lose_player = self.scramble(lplayer, rplayer)
                    lose_player.done = True
                    if lose_player in lplayers:
                        lplayers.remove(lose_player)
                    else:
                        rplayers.remove(lose_player)
                    if not lplayers or not rplayers:
                        win_player.move_to(game, ball_location)  # 争抢成功者可以继续完成动作帧

    def overlap_judge(self, game):
        """
        异队球员重合判定
        :param game: 比赛实例
        """
        challenge_player = [player for player in game.field.get_all_players() if player.overlap == True]
        if challenge_player:
            ball_held_player = game.field.get_ball_held_player()
            for player in challenge_player:
                player.overlap = False
                player.done = True  # 抢断者结束本帧动作
                win_player = ball_held_player.challenge(player)
                if win_player != ball_held_player:
                    # 若被抢断
                    ball_held_player.done = True  # 持球者结束本帧动作
                    game.field.update_ball_location(self.ball, win_player.coor)
                    break

    def frame_act(self, game):
        self.scramble_judge(game)
        self.overlap_judge(game)
        for player in self.left_players:
            player.act(game)
            game.check_state()
        for player in self.left_players:
            player.act(game)
            game.check_state()
