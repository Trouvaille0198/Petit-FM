from model import *
import random
from utils.utils import *
from typing import Dict, List, Sequence, Set, Tuple, Optional
import json
import os
from logger import logger

DEFAULT_RATING = {
    "shooting": 50,  # 射门
    "passing": 50,  # 传球
    "dribbling": 50,  # 盘带
    "interception": 50,  # 抢断
    "pace": 50,  # 速度
    "strength": 50,  # 力量
    "aggression": 50,  # 侵略
    "anticipation": 50,  # 预判
    "free_kick": 50,  # 任意球/点球
    "stamina": 50,  # 体能
    "goalkeeping": 50  # 守门
}

DEFAULT_TACTIC = {
    "name": "4-4-2",
    "location": {
        "ST": 2,
        "CM": 2,
        "LW": 1,
        "RW": 1,
        "CB": 2,
        "LB": 1,
        "RB": 1,
        "GK": 1
    },
    "probability": {
        "wing_cross": 40,
        "under_cutting": 40,
        "pull_back": 40,
        "middle_attack": 40,
        "counter_attack": 40
    }
}


class Player:
    def __init__(self, player_info: dict):
        self.name = player_info["name"]
        self.location = player_info["location"]
        self.real_location = player_info["location"]
        self.rating = player_info["rating"]
        self.stamina = 100
        self.data = {
            "actions": 0,
            "goals": 0,
            "assists": 0,
            "shots": 0,
            "dribbles": 0,
            "dribble_success": 0,
            "passes": 0,
            "pass_success": 0,
            "tackles": 0,
            "tackle_success": 0,
            "saves": 0,
            "save_success": 0,
            "aerials": 0,
            "aerial_success": 0
        }

    def get_rating(self, rating_name: str) -> float:
        """
        获取能力属性
        """
        if rating_name == 'stamina':
            return self.rating[rating_name]
        return self.rating[rating_name] * (self.stamina / 100)

    def get_data(self, data_name: str):
        return self.data[data_name]

    def plus_data(self, data_name: str, average_stamina: Optional[float] = None):
        if data_name == 'shots' or data_name == 'dribbles' \
                or data_name == 'tackles' \
                or data_name == 'saves' or data_name == 'aerials':
            self.data['actions'] += 1
            if select_by_pro(
                    {False: self.get_rating('stamina'), True: average_stamina}
            ) and average_stamina:
                self.stamina -= 2.5
                if self.stamina < 0:
                    self.stamina = 0
        elif data_name == 'passes':
            self.data['actions'] += 1
            if select_by_pro(
                    {False: self.get_rating('stamina'), True: average_stamina}
            ) and average_stamina:
                self.stamina -= 1
                if self.stamina < 0:
                    self.stamina = 0
        self.data[data_name] += 1

    def shift_location(self):
        """
        确定每次战术的场上位置
        """
        if self.location == Location.CAM:
            self.real_location = select_by_pro(
                {Location.ST: 40, Location.CM: 60}
            )
        elif self.location == Location.LM:
            self.real_location = select_by_pro(
                {Location.LW: 40, Location.CM: 60}
            )
        elif self.location == Location.RM:
            self.real_location = select_by_pro(
                {Location.RW: 40, Location.CM: 60}
            )
        elif self.location == Location.CDM:
            self.real_location = select_by_pro(
                {Location.CB: 40, Location.CM: 60}
            )
        elif self.location == Location.CM:
            # 中场有概率前压或后撤
            self.real_location = select_by_pro(
                {Location.ST: 20, Location.CB: 15, Location.CM: 75}
            )
        elif self.location == Location.LB:
            self.real_location = select_by_pro(
                {Location.LW: 20, Location.LB: 80}
            )
        elif self.location == Location.RB:
            self.real_location = select_by_pro(
                {Location.RW: 20, Location.RB: 80}
            )
        else:
            self.real_location = self.location

    def get_location(self):
        return self.real_location


class Team:
    def __init__(self, game: 'Game', team_info: dict):
        self.game = game
        self.name = team_info['name']
        self.players: list = []
        self.score: int = 0
        self.tactic = team_info['tactic']
        self.data = {
            'attempts': 0,
            "wing_cross": 0,
            "wing_cross_success": 0,
            "under_cutting": 0,
            "under_cutting_success": 0,
            "pull_back": 0,
            "pull_back_success": 0,
            "middle_attack": 0,
            "middle_attack_success": 0,
            "counter_attack": 0,
            "counter_attack_success": 0
        }

        self.init_players(team_info['players'])

    def set_capa(self, capa_name: str, num):
        for player in self.players:
            player.rating[capa_name] = num

    def init_players(self, players_list: list):
        for player_info in players_list:
            self.players.append(Player(player_info))

    def get_rival_team(self):
        if self.game.lteam == self:
            return self.game.rteam
        else:
            return self.game.lteam

    def plus_data(self, data_name: str):
        if data_name == "wing_cross" or data_name == "under_cutting" or data_name == "pull_back" \
                or data_name == "middle_attack" or data_name == "counter_attack":
            self.data['attempts'] += 1
        self.data[data_name] += 1

    def select_tactic(self, counter_attack_permitted):
        """
        选择进攻战术
        :param counter_attack_permitted: 是否允许使用防反
        :return: 战术名
        """
        tactic_pro_total = self.tactic['probability'].copy()
        tactic_pro = self.tactic['probability'].copy()
        tactic_pro.pop("counter_attack")
        while True:
            tactic_name = select_by_pro(tactic_pro_total) if counter_attack_permitted else select_by_pro(tactic_pro)
            if tactic_name == 'wing_cross' and not self.get_location_players(
                    (Location.LW, Location.RW, Location.LB, Location.RB)):
                continue
            if tactic_name == 'under_cutting' and not self.get_location_players((Location.LW, Location.RW)):
                continue
            if tactic_name == 'pull_back' and not self.get_location_players((Location.LW, Location.RW)):
                continue
            if tactic_name == 'middle_attack' and not self.get_location_players((Location.CM,)):
                self.shift_location()
            else:
                break

        return tactic_name

    def get_average_capability(self, capa_name: str):
        """
        计算某能力的队内平均值
        :param capa_name: 能力名
        :return: 队内均值
        """
        average_capa = sum([player.get_rating(capa_name) for player in self.players]) / len(self.players)
        return average_capa

    def shift_location(self):
        for player in self.players:
            player.shift_location()

    def get_location_players(self, location_tuple: tuple) -> list:
        """
        获取指定位置上的球员
        :param location_tuple: 位置名
        :return: 球员实例列表
        """
        player_list = []
        for player in self.players:
            if player.get_location() in location_tuple:
                player_list.append(player)
        return player_list

    def attack(self, rival_team: 'Team', counter_attack_permitted=False) -> bool:
        """
        执行战术
        :param rival_team: 防守队伍实例
        :param counter_attack_permitted: 是否允许使用防反战术
        :return: 是否交换球权
        """
        tactic_name = self.select_tactic(counter_attack_permitted)
        exchange_ball = False
        if tactic_name == 'wing_cross':
            exchange_ball = self.wing_cross(rival_team)
        elif tactic_name == 'under_cutting':
            exchange_ball = self.under_cutting(rival_team)
        elif tactic_name == 'pull_back':
            exchange_ball = self.pull_back(rival_team)
        elif tactic_name == 'middle_attack':
            exchange_ball = self.middle_attack(rival_team)
        elif tactic_name == 'counter_attack':
            exchange_ball = self.counter_attack(rival_team)
        else:
            logger.warning('战术名称{}错误！'.format(tactic_name))
        return exchange_ball

    def shot_and_save(self, attacker: Player, defender: Player,
                      assister: Optional[Player] = None) -> bool:
        """
        射门与扑救，一对一
        :param attacker: 进攻球员实例
        :param defender: 防守球员（门将）实例
        :param assister: 助攻球员实例
        :return: 进攻是否成功
        """
        logger.info('{}起脚打门！'.format(attacker.name))
        average_stamina = self.get_rival_team().get_average_capability('stamina')
        attacker.plus_data('shots', average_stamina)
        defender.plus_data('saves', average_stamina)
        win_player = select_by_pro(
            {attacker: attacker.get_rating('shooting'), defender: defender.get_rating('goalkeeping')})
        if win_player == attacker:
            self.score += 1
            attacker.plus_data('goals')
            if assister:
                assister.plus_data('assists')
            logger.info('球进啦！{} {}:{} {}'.format(
                self.game.lteam.name, self.game.lteam.score, self.game.rteam.score, self.game.rteam.name))
            if attacker.get_data('goals') == 2:
                logger.info('{}梅开二度！'.format(attacker.name))
            if attacker.get_data('goals') == 3:
                logger.info('{}有如神助，完成了帽子戏法！'.format(attacker.name))
            return True
        else:
            defender.plus_data('save_success')
            logger.info('{}发挥神勇，扑出这脚劲射'.format(defender.name))
            return False

    def dribble_and_block(self, attacker: Player, defender: Player) -> bool:
        """
        过人与抢断，一对一，发生在内切时
        :param attacker: 进攻球员（边锋）实例
        :param defender: 防守球员（中卫）实例
        :return: 进攻是否成功
        """
        average_stamina = self.get_rival_team().get_average_capability('stamina')
        attacker.plus_data('dribbles', average_stamina)
        defender.plus_data('tackles', average_stamina)

        win_player = select_by_pro(
            {attacker: attacker.get_rating('dribbling'),
             defender: defender.get_rating('interception')})
        if win_player == attacker:
            attacker.plus_data('dribble_success')
            logger.info('{}过掉了{}'.format(attacker.name, defender.name))
            return True
        else:
            defender.plus_data('tackle_success')
            logger.info('{}阻截了{}的进攻'.format(defender.name, attacker.name))
            return False

    def sprint_dribble_and_block(self, attackers: List[Player], defenders: List[Player]) -> \
            Tuple[bool, Player]:
        """
        冲刺、过人与抢断，多对多
        :param attackers: 进攻球员组
        :param defenders: 防守球员组
        :return: 进攻是否成功
        """
        average_stamina = self.get_rival_team().get_average_capability('stamina')
        if not defenders:
            return True, random.choice(attackers)
        if not attackers:
            return False, random.choice(defenders)
        while True:
            attacker = random.choice(attackers)
            defender = random.choice(defenders)
            attacker.plus_data('dribbles', average_stamina)
            defender.plus_data('tackles', average_stamina)
            win_player = select_by_pro(
                {attacker: attacker.get_rating('dribbling') + attacker.get_rating('pace'),
                 defender: defender.get_rating('interception') + defender.get_rating('pace')})
            if win_player == attacker:
                attacker.plus_data('dribble_success')
                defenders.remove(defender)
            else:
                defender.plus_data('tackle_success')
                attackers.remove(attacker)
            if not attackers:
                logger.info('{}抢到皮球'.format(win_player.name))
                return False, win_player
            elif not defenders:
                logger.info('{}过掉了{}'.format(win_player.name, defender.name))
                return True, win_player
            else:
                pass

    def drop_ball(self, attackers: List[Player], defenders: List[Player]) -> Tuple[bool, Player]:
        """
        争顶
        :param attackers: 进攻球员组
        :param defenders: 防守球员组
        :return: 进攻是否成功、争顶成功的球员
        """
        logger.info('球员们尝试争顶')
        average_stamina = self.get_rival_team().get_average_capability('stamina')
        while True:
            attacker = random.choice(attackers)
            defender = random.choice(defenders)
            attacker.plus_data('aerials', average_stamina)
            defender.plus_data('aerials', average_stamina)
            win_player = select_by_pro(
                {attacker: attacker.get_rating('anticipation') + attacker.get_rating('strength'),
                 defender: defender.get_rating('anticipation') + defender.get_rating('strength')})
            win_player.plus_data('aerial_success')
            if win_player == attacker:
                defenders.remove(defender)
            else:
                attackers.remove(attacker)
            if not attackers:
                return False, win_player
            elif not defenders:
                logger.info('{}抢到球权'.format(win_player.name))
                return True, win_player
            else:
                pass

    def pass_ball(self, attacker, defender_average: float, is_long_pass: bool = False) -> bool:
        """
        传球
        :param attacker: 传球球员实例
        :param defender_average: 防守方传球均值
        :param is_long_pass: 是否为长传
        :return: 进攻是否成功
        """
        average_stamina = self.get_rival_team().get_average_capability('stamina')
        attacker.plus_data('passes', average_stamina)
        if is_long_pass:
            win_player = select_by_pro(
                {attacker: attacker.get_rating('passing') / 2,
                 defender_average: defender_average / 2})
        else:
            win_player = select_by_pro(
                {attacker: attacker.get_rating('passing'),
                 defender_average: defender_average / 2})
        if win_player == attacker:
            attacker.plus_data('pass_success')
            return True
        else:
            return False

    def corner_kick(self, attacker: list, defender: list):
        """
        角球
        """
        pass

    def wing_cross(self, rival_team: 'Team'):
        """
        下底传中
        :param rival_team: 防守队伍
        :return: 是否交换球权
        """
        self.plus_data('wing_cross')
        logger.info('\n{}尝试下底传中'.format(self.name))
        # 边锋或边卫过边卫
        while True:
            flag = is_happened_by_pro(0.5)
            if flag:
                wings = self.get_location_players((Location.LW, Location.LB))
                wing_backs = rival_team.get_location_players((Location.LB,))
                if wings:
                    break
            else:
                wings = self.get_location_players((Location.RW, Location.RB))
                wing_backs = rival_team.get_location_players((Location.RB,))
                if wings:
                    break

        state, win_player = self.sprint_dribble_and_block(wings, wing_backs)  # 一对一或一对多
        if state:
            # 边锋传中
            logger.info('{}一脚起球传中'.format(win_player.name))
            state = self.pass_ball(win_player, rival_team.get_average_capability('passing'), is_long_pass=True)
            if state:
                # 争顶
                assister = win_player
                strikers = self.get_location_players((Location.ST,))
                centre_backs = rival_team.get_location_players((Location.CB,))
                state, win_player = self.drop_ball(strikers, centre_backs)
                if state:
                    # 射门
                    goal_keeper = rival_team.get_location_players((Location.GK,))[0]
                    state = self.shot_and_save(win_player, goal_keeper, assister)
                    if state:
                        self.plus_data('wing_cross_success')
                else:
                    # 防守球员解围
                    logger.info('{}将球解围'.format(win_player.name))
                    state = rival_team.pass_ball(win_player, self.get_average_capability('passing'),
                                                 is_long_pass=True)
                    if not state:
                        logger.info('进攻方仍然持球')
                        return False
                    else:
                        logger.info('{}拿到球权'.format(rival_team.name))
            else:
                logger.info('{}抢到球权'.format(rival_team.name))
        return True

    def under_cutting(self, rival_team: 'Team'):
        """
        边路内切
        :param rival_team: 防守队伍
        :return: 是否交换球权
        """
        self.plus_data('under_cutting')
        logger.info('\n{}尝试边路内切'.format(self.name))
        # 边锋过边卫
        wing = random.choice(self.get_location_players((Location.LW, Location.RW)))
        if wing.get_location() == Location.LW:
            wing_backs = rival_team.get_location_players((Location.RB,))
        elif wing.get_location() == Location.RW:
            wing_backs = rival_team.get_location_players((Location.LB,))
        else:
            raise ValueError('边锋不存在！')
        logger.info('{}拿球，尝试过掉{}'.format(wing.name, ' '.join([back.name for back in wing_backs])))
        state, win_player = self.sprint_dribble_and_block([wing], wing_backs)  # 一对一或一对多
        if state:
            # 边锋内切
            logger.info('{}尝试内切'.format(win_player.name))
            centre_backs = rival_team.get_location_players((Location.CB,))
            # centre_back = random.choice(rival_team.get_location_players((Location.CB,)))
            # state = self.dribble_and_block(win_player, centre_back)
            for centre_back in centre_backs:
                state = self.dribble_and_block(win_player, centre_back)
                if not state:
                    return True
            if state:
                # 射门
                goal_keeper = rival_team.get_location_players((Location.GK,))[0]
                state = self.shot_and_save(win_player, goal_keeper, None)
                if state:
                    self.plus_data('under_cutting_success')
        return True

    def pull_back(self, rival_team: 'Team'):
        """
        倒三角
        :param rival_team: 防守队伍
        :return: 是否交换球权
        """
        self.plus_data('pull_back')
        logger.info('\n{}尝试倒三角传球'.format(self.name))
        # 边锋过边卫
        wing = random.choice(self.get_location_players((Location.LW, Location.RW)))
        if wing.get_location() == Location.LW:
            wing_backs = rival_team.get_location_players((Location.RB,))
        elif wing.get_location() == Location.RW:
            wing_backs = rival_team.get_location_players((Location.LB,))
        else:
            raise ValueError('边锋不存在！')
        logger.info('{}拿球，尝试过掉{}'.format(wing.name, ' '.join([back.name for back in wing_backs])))
        state, win_player = self.sprint_dribble_and_block([wing], wing_backs)  # 一对一或一对多
        if state:
            # 边锋内切
            assister = win_player
            logger.info('{}尝试内切'.format(win_player.name))
            centre_back = random.choice(rival_team.get_location_players((Location.CB,)))
            state = self.dribble_and_block(win_player, centre_back)
            # for centre_back in centre_backs:
            #     state = self.dribble_and_block(win_player, centre_back)
            #     if not state:
            #         return True
            if state:
                # 倒三角传球
                logger.info('{}倒三角传中'.format(win_player.name))
                state = self.pass_ball(win_player, rival_team.get_average_capability('passing'))
                if state:
                    shooter = random.choice(self.get_location_players((Location.ST, Location.CM)))
                    goal_keeper = rival_team.get_location_players((Location.GK,))[0]
                    state = self.shot_and_save(shooter, goal_keeper, assister)
                    if state:
                        self.plus_data('pull_back_success')
        return True

    def middle_attack(self, rival_team: 'Team'):
        """
        中路渗透
        :param rival_team: 防守队伍
        :return: 是否交换球权
        """
        self.plus_data('middle_attack')
        logger.info('\n{}尝试中路渗透'.format(self.name))
        count_dict = {}
        for _ in range(10):
            midfielders = self.get_location_players((Location.CM,))
            while True:
                player = random.choice(midfielders)
                flag = self.pass_ball(player, rival_team.get_average_capability('passing'))
                if flag:
                    count_dict[player] = count_dict.get(player, 0) + 1
                    break
                midfielders.remove(player)
                if not midfielders:
                    logger.info('{}丢失了球权'.format(self.name))
                    return True
        assister = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[0][0]
        # 争顶
        strikers = self.get_location_players((Location.ST,))
        centre_backs = rival_team.get_location_players((Location.CB,))
        state, win_player = self.drop_ball(strikers, centre_backs)
        if state:
            # 射门
            goal_keeper = rival_team.get_location_players((Location.GK,))[0]
            state = self.shot_and_save(win_player, goal_keeper, assister)
            if state:
                self.plus_data('middle_attack_success')
        else:
            # 防守球员解围
            logger.info('{}将球解围'.format(win_player.name))
            state = rival_team.pass_ball(win_player, self.get_average_capability('passing'), is_long_pass=True)
            if state:
                # 外围争顶
                centre_backs = self.get_location_players((Location.CB,))
                strikers = rival_team.get_location_players((Location.ST,))
                state, win_player = rival_team.drop_ball(strikers, centre_backs)
                if state:
                    return True
            logger.info('进攻方仍然持球')
            return False
        return True

    def counter_attack(self, rival_team: 'Team'):
        """
        防守反击
        :param rival_team: 防守队伍
        :return: 是否交换球权
        """
        self.plus_data('counter_attack')
        logger.info('\n{}尝试防守反击'.format(self.name))
        passing_player = random.choice(
            self.get_location_players((Location.GK, Location.CB, Location.LB, Location.RB,
                                       Location.CM, Location.LW, Location.RW)))
        state = self.pass_ball(passing_player, rival_team.get_average_capability('passing'))
        logger.info('{}一脚长传，直击腹地'.format(passing_player.name))
        if state:
            # 过人
            assister = passing_player
            strikers = self.get_location_players((Location.ST,))
            centre_backs = rival_team.get_location_players((Location.CB,))
            if not strikers:
                logger.info("很可惜，无锋阵容没有中锋进行接应，球权被{}夺去".format(rival_team.name))
                return True
            state, win_player = self.sprint_dribble_and_block(strikers, centre_backs)
            if state:
                # 射门
                goal_keeper = rival_team.get_location_players((Location.GK,))[0]
                state = self.shot_and_save(win_player, goal_keeper, assister)
                if state:
                    self.plus_data('counter_attack_success')
        logger.info('{}持球'.format(rival_team.name))
        return True


class Game:
    def __init__(self, team1_info: dict, team2_info: dict):
        self.lteam = Team(self, team1_info)
        self.rteam = Team(self, team2_info)

    def start(self):
        logger.info('比赛开始！')
        hold_ball_team, no_ball_team = self.init_hold_ball_team()
        counter_attack_permitted = False
        for _ in range(50):
            # 确定本次战术组织每个球员的场上位置
            self.lteam.shift_location()
            self.rteam.shift_location()
            original_score = (self.lteam.score, self.rteam.score)
            # 执行进攻战术
            exchange_ball = hold_ball_team.attack(no_ball_team, counter_attack_permitted)
            if exchange_ball:
                hold_ball_team, no_ball_team = self.exchange_hold_ball_team(hold_ball_team)
            if exchange_ball and original_score == (self.lteam.score, self.rteam.score):
                counter_attack_permitted = True
            else:
                counter_attack_permitted = False
        logger.info('比赛结束！ {} {}:{} {}'.format(
            self.lteam.name, self.lteam.score, self.rteam.score, self.rteam.name))
        # print('比赛结束！ {} {}:{} {}'.format(
        #     self.lteam.name, self.lteam.score, self.rteam.score, self.rteam.name))
        self.show_data()
        logger.info('---------------------------------------------------------------------------')
        return self.lteam.score, self.rteam.score

    def init_hold_ball_team(self):
        hold_ball_team = random.choice([self.lteam, self.rteam])
        no_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        return hold_ball_team, no_ball_team

    def exchange_hold_ball_team(self, hold_ball_team: Team):
        hold_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        no_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        return hold_ball_team, no_ball_team

    def show_data(self):
        logger.info('\n赛后统计')
        logger.info('控球：{}，{}'.format(self.lteam.data['attempts'], self.rteam.data['attempts']))
        logger.info('{}队'.format(self.lteam.name))
        logger.info(self.lteam.data)
        anal = {
            '下底传中成功率': self.lteam.data['wing_cross_success'] / self.lteam.data['wing_cross'] if self.lteam.data[
                'wing_cross'] else 0,
            '边路内切成功率': self.lteam.data['under_cutting_success'] / self.lteam.data['under_cutting'] if
            self.lteam.data[
                'under_cutting'] else 0,
            '倒三角成功率': self.lteam.data['pull_back_success'] / self.lteam.data['pull_back'] if self.lteam.data[
                'pull_back'] else 0,
            '中路渗透成功率': self.lteam.data['middle_attack_success'] / self.lteam.data['middle_attack'] if
            self.lteam.data[
                'middle_attack'] else 0,
            '防守反击成功率': self.lteam.data['counter_attack_success'] / self.lteam.data['counter_attack'] if
            self.lteam.data[
                'counter_attack'] else 0
        }
        logger.info(anal)
        for player in self.lteam.players:
            logger.info('{}'.format(player.name))
            logger.info(player.data)
            anal = {
                '射门转化率': player.data['goals'] / player.data['shots'] if player.data['shots'] else 0,
                '传球成功率': player.data['pass_success'] / player.data['passes'] if player.data['passes'] else 0,
                '过人成功率': player.data['dribble_success'] / player.data['dribbles'] if player.data[
                    'dribbles'] else 0,
                '抢断成功率': player.data['tackle_success'] / player.data['tackles'] if player.data['tackles'] else 0,
                '争顶成功率': player.data['aerial_success'] / player.data['aerials'] if player.data['aerials'] else 0,
                '扑救率': player.data['save_success'] / player.data['saves'] if player.data['saves'] else 0,
                '终场体能': player.stamina
            }
            logger.info(anal)

        logger.info('\n{}队'.format(self.rteam.name))
        logger.info(self.rteam.data)
        anal = {
            '下底传中成功率': self.rteam.data['wing_cross_success'] / self.rteam.data['wing_cross'] if self.rteam.data[
                'wing_cross'] else 0,
            '边路内切成功率': self.rteam.data['under_cutting_success'] / self.rteam.data['under_cutting'] if
            self.rteam.data[
                'under_cutting'] else 0,
            '倒三角成功率': self.rteam.data['pull_back_success'] / self.rteam.data['pull_back'] if self.rteam.data[
                'pull_back'] else 0,
            '中路渗透成功率': self.rteam.data['middle_attack_success'] / self.rteam.data['middle_attack'] if
            self.rteam.data[
                'middle_attack'] else 0,
            '防守反击成功率': self.rteam.data['counter_attack_success'] / self.rteam.data['counter_attack'] if
            self.rteam.data[
                'counter_attack'] else 0
        }
        logger.info(anal)
        for player in self.rteam.players:
            logger.info('{}'.format(player.name))
            logger.info(player.data)
            anal = {
                '射门转化率': player.data['goals'] / player.data['shots'] if player.data['shots'] else 0,
                '传球成功率': player.data['pass_success'] / player.data['passes'] if player.data['passes'] else 0,
                '过人成功率': player.data['dribble_success'] / player.data['dribbles'] if player.data[
                    'dribbles'] else 0,
                '抢断成功率': player.data['tackle_success'] / player.data['tackles'] if player.data['tackles'] else 0,
                '争顶成功率': player.data['aerial_success'] / player.data['aerials'] if player.data['aerials'] else 0,
                '扑救率': player.data['save_success'] / player.data['saves'] if player.data['saves'] else 0,
                '终场体能': player.stamina
            }
            logger.info(anal)

    def get_data(self):
        lanal = {
            '下底传中成功率': self.lteam.data['wing_cross_success'] / self.lteam.data['wing_cross'] if self.lteam.data[
                'wing_cross'] else 0,
            '边路内切成功率': self.lteam.data['under_cutting_success'] / self.lteam.data['under_cutting'] if
            self.lteam.data[
                'under_cutting'] else 0,
            '倒三角成功率': self.lteam.data['pull_back_success'] / self.lteam.data['pull_back'] if self.lteam.data[
                'pull_back'] else 0,
            '中路渗透成功率': self.lteam.data['middle_attack_success'] / self.lteam.data['middle_attack'] if
            self.lteam.data[
                'middle_attack'] else 0,
            '防守反击成功率': self.lteam.data['counter_attack_success'] / self.lteam.data['counter_attack'] if
            self.lteam.data[
                'counter_attack'] else 0
        }
        ranal = {
            '下底传中成功率': self.rteam.data['wing_cross_success'] / self.rteam.data['wing_cross'] if self.rteam.data[
                'wing_cross'] else 0,
            '边路内切成功率': self.rteam.data['under_cutting_success'] / self.rteam.data['under_cutting'] if
            self.rteam.data[
                'under_cutting'] else 0,
            '倒三角成功率': self.rteam.data['pull_back_success'] / self.rteam.data['pull_back'] if self.rteam.data[
                'pull_back'] else 0,
            '中路渗透成功率': self.rteam.data['middle_attack_success'] / self.rteam.data['middle_attack'] if
            self.rteam.data[
                'middle_attack'] else 0,
            '防守反击成功率': self.rteam.data['counter_attack_success'] / self.rteam.data['counter_attack'] if
            self.rteam.data[
                'counter_attack'] else 0
        }
        return self.lteam.data, self.rteam.data, lanal, ranal


def simulate_games(team1: dict, team2: dict, num: int = 1000):
    """
    模拟比赛
    :param team1: 队1
    :param team2: 队2
    :param num: 比赛场数
    """
    l_win = 0
    r_win = 0
    draw = 0

    ldata_sum = {}
    rdata_sum = {}
    for _ in range(num):
        game = Game(team1, team2)
        # game.lteam.set_capa('stamina', 100)
        l, r = game.start()
        ldata, rdata, lanal, ranal = game.get_data()
        ldata_sum = plus_dict(ldata_sum, ldata)
        rdata_sum = plus_dict(rdata_sum, rdata)
        if l > r:
            l_win += 1
        elif l < r:
            r_win += 1
        else:
            draw += 1

    lanal = {
        '下底传中成功率': ldata_sum['wing_cross_success'] / ldata_sum['wing_cross'] * 100 if ldata_sum[
            'wing_cross'] else 0,
        '边路内切成功率': ldata_sum['under_cutting_success'] / ldata_sum['under_cutting'] * 100 if
        ldata_sum[
            'under_cutting'] else 0,
        '倒三角成功率': ldata_sum['pull_back_success'] / ldata_sum['pull_back'] * 100 if ldata_sum[
            'pull_back'] else 0,
        '中路渗透成功率': ldata_sum['middle_attack_success'] / ldata_sum['middle_attack'] * 100 if
        ldata_sum[
            'middle_attack'] else 0,
        '防守反击成功率': ldata_sum['counter_attack_success'] / ldata_sum['counter_attack'] * 100 if
        ldata_sum[
            'counter_attack'] else 0
    }
    ranal = {
        '下底传中成功率': rdata_sum['wing_cross_success'] / rdata_sum['wing_cross'] * 100 if rdata_sum[
            'wing_cross'] else 0,
        '边路内切成功率': rdata_sum['under_cutting_success'] / rdata_sum['under_cutting'] * 100 if
        rdata_sum[
            'under_cutting'] else 0,
        '倒三角成功率': rdata_sum['pull_back_success'] / rdata_sum['pull_back'] * 100 if rdata_sum[
            'pull_back'] else 0,
        '中路渗透成功率': rdata_sum['middle_attack_success'] / rdata_sum['middle_attack'] * 100 if
        rdata_sum[
            'middle_attack'] else 0,
        '防守反击成功率': rdata_sum['counter_attack_success'] / rdata_sum['counter_attack'] * 100 if
        rdata_sum[
            'counter_attack'] else 0
    }
    logger.info('{} vs {}---左胜{}，右胜：{}，平局：{}'.format(team1["name"], team2["name"], l_win, r_win, draw))
    print('{} vs {}---左胜{}，右胜：{}，平局：{}'.format(team1["name"], team2["name"], l_win, r_win, draw))
    print('{}: {}'.format(team1["name"], ldata_sum))
    print(lanal)
    print('{}: {}'.format(team2["name"], rdata_sum))
    print(ranal)
    print('\n')


def tactics_test(team_info):
    t4141 = team_info['4-1-4-1']
    t433 = team_info['4-3-3']
    t442 = team_info['4-4-2']
    t352 = team_info['3-5-2']
    t4312 = team_info['4-3-1-2']
    print('4141')
    simulate_games(t4141, t433, 500)
    simulate_games(t4141, t442, 500)
    simulate_games(t4141, t352, 500)
    simulate_games(t4141, t4312, 500)
    print('433')
    simulate_games(t433, t4141, 500)
    simulate_games(t433, t442, 500)
    simulate_games(t433, t352, 500)
    simulate_games(t433, t4312, 500)
    print('442')
    simulate_games(t442, t4141, 500)
    simulate_games(t442, t433, 500)
    simulate_games(t442, t352, 500)
    simulate_games(t442, t4312, 500)
    print('352')
    simulate_games(t352, t4141, 500)
    simulate_games(t352, t433, 500)
    simulate_games(t352, t442, 500)
    simulate_games(t352, t4312, 500)
    print('4312')
    simulate_games(t4312, t4141, 500)
    simulate_games(t4312, t433, 500)
    simulate_games(t4312, t442, 500)
    simulate_games(t4312, t352, 500)


if __name__ == '__main__':
    path = os.getcwd()
    file_name = path + r'/test.json'
    with open(file_name) as file_obj:
        team = json.load(file_obj)

    bar = team['巴塞罗那']
    manu = team['曼联']
    paris = team['巴黎圣日耳曼']
    simulate_games(bar, manu, 3)
    simulate_games(bar, paris, 3)
    simulate_games(manu, paris, 3)

    # tactics_test(team)
