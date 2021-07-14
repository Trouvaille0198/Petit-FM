from model import *
import random
from utils.utils import *
from typing import Dict, List, Sequence, Set, Tuple, Optional
import json
import os

path = os.getcwd()
file_name = path+r'/PETIT-FM/test.json'
with open(file_name) as file_obj:
    team_list = json.load(file_obj)
# print(team_list)

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


class Team:
    pass


class Player:
    pass


class Game:
    pass


class Player:
    def __init__(self, player_info: dict):
        self.name = player_info["name"]
        self.location = player_info["location"]
        self.rating = player_info["rating"]
        self.data = {
            "goal": 0,
            "assist": 0
        }

    def get_rating(self, rating_name: str):
        """
        获取能力属性
        """
        return self.rating[rating_name]


class Team:
    def __init__(self, team_info: dict):
        self.name = team_info['name']

        self.players: list = []
        self.init_players(team_info['players'])
        self.score: int = 0
        self.tactic = team_info['tactic']

    def init_players(self, players_list: list):
        for player_info in players_list:
            self.players.append(Player(player_info))

    def select_tactic(self, counter_attack_permitted):
        tactic_pro_total = self.tactic['probability'].copy()
        tactic_pro = self.tactic['probability'].copy()
        tactic_pro.pop("counter_attack")

        tactic_name = select_by_pro(tactic_pro_total) if counter_attack_permitted else select_by_pro(tactic_pro)
        return tactic_name

    def get_average_capability(self, capa_name: str):
        """
        计算指定能力的队内平均值
        """
        average_capa = sum([player.rating[capa_name] for player in self.players])/len(self.players)
        return average_capa

    def get_location_players(self, location_tuple: tuple) -> list:
        """
        获取指定位置上的球员
        """
        player_list = []
        for player in self.players:
            if player.location in location_tuple:
                player_list.append(player)
        return player_list

    def attack(self, another_team: Team, counter_attack_permitted=False) -> bool:
        """
        执行战术
        :return: 是否交换球权
        """
        tactic_name = self.select_tactic(counter_attack_permitted)
        if tactic_name == 'wing_cross':
            exchange_ball = self.wing_cross(another_team)
            # print('下底传中！')
        elif tactic_name == 'under_cutting':
            exchange_ball = self.under_cutting(another_team)
            # print('边路内切！')
        elif tactic_name == 'pull_back':
            exchange_ball = self.pull_back(another_team)
            # print('倒三角！')
        elif tactic_name == 'middle_attack':
            exchange_ball = self.middle_attack(another_team)
            # print('中路渗透！')
        elif tactic_name == 'counter_attack':
            exchange_ball = self.counter_attack(another_team)
            # print('防守反击！')
        else:
            print('?')
        return exchange_ball

    def shot_and_save(self, attacker: Player, defender: Player) -> bool:
        """
        射门与扑救，一对一
        """
        win_player = select_by_pro(
            {attacker: attacker.rating['shooting'], defender: defender.rating['goalkeeping']})
        if win_player == attacker:
            self.score += 1
            return True
        else:
            return False

    def dribble_and_block(self, attacker: Player, defender: Player):
        """
        过人与抢断，一对一，发生在内切时
        """
        win_player = select_by_pro(
            {attacker: attacker.rating['dribbling'],
             defender: defender.rating['interception']})
        if win_player == attacker:
            return True
        else:
            return False

    def sprint_dribble_and_block(self, attackers: List[Player], defenders: List[Player]) -> Tuple[bool, Player]:
        """
        冲刺、过人与抢断，多对多
        """
        while True:
            attacker = random.choice(attackers)
            defender = random.choice(defenders)
            win_player = select_by_pro(
                {attacker: attacker.rating['dribbling']+attacker.rating['pace'],
                 defender: defender.rating['interception']+defender.rating['pace']})
            if win_player == attacker:
                defenders.remove(defender)
            else:
                attackers.remove(attacker)
            if not attackers:
                return (False, win_player)
            elif not defenders:
                return (True, win_player)
            else:
                pass

    def drop_ball(self, attackers: List[Player], defenders: List[Player]) -> Tuple[bool, Player]:
        """
        争顶
        :return: 争顶成功的球员
        """
        while True:
            attacker = random.choice(attackers)
            defender = random.choice(defenders)
            win_player = select_by_pro(
                {attacker: attacker.rating['anticipation']+attacker.rating['strength'],
                 defender: defender.rating['anticipation']+defender.rating['strength']})
            if win_player == attacker:
                defenders.remove(defender)
            else:
                attackers.remove(attacker)
            if not attackers:
                return (False, win_player)
            elif not defenders:
                return (True, win_player)
            else:
                pass

    def pass_ball(self, attacker, defender_average: float):
        """
        传球
        """
        win_player = select_by_pro(
            {attacker: attacker.rating['passing'],
             defender_average: defender_average})
        if win_player == attacker:
            return True
        else:
            return False

    def corner_kick(self, attacker: list, defender: list):
        """
        角球
        """
        pass

    def wing_cross(self, another_team: Team):
        """
        边路传中
        """
        # 边锋过边卫
        wing = random.choice(self.get_location_players((Location.LW, Location.RW)))
        if wing.location == Location.LW:
            backs = another_team.get_location_players((Location.LB))
        elif wing.location == Location.RW:
            backs = another_team.get_location_players((Location.RB))
        else:
            raise ValueError('边锋不存在！')
        state, win_player = self.sprint_dribble_and_block([wing], backs)  # 一对一或一对多
        if state:
            # 边锋传中
            state = self.pass_ball(win_player, another_team.get_average_capability('passing'))
            if state:
                # 争顶
                strikers = self.get_location_players((Location.ST))
                centre_backs = another_team.get_location_players((Location.CB))
                state, win_player = self.drop_ball(strikers, centre_backs)
                if state:
                    goal_keeper = another_team.get_location_players((Location.GK))[0]
                    state = self.shot_and_save(win_player, goal_keeper)
                else:
                    # 防守球员解围
                    state = another_team.pass_ball(win_player, self.get_average_capability('passing'))
                    if not state:
                        return False
        return True

    def under_cutting(self, another_team: Team):
        """
        边路内切
        """
        # 边锋过边卫
        wing = random.choice(self.get_location_players((Location.LW, Location.RW)))
        if wing.location == Location.LW:
            backs = another_team.get_location_players((Location.LB))
        elif wing.location == Location.RW:
            backs = another_team.get_location_players((Location.RB))
        else:
            raise ValueError('边锋不存在！')
        state, win_player = self.sprint_dribble_and_block([wing], backs)  # 一对一或一对多
        if state:
            # 边锋内切
            centre_back = random.choice(another_team.get_location_players((Location.CB)))
            state = self.dribble_and_block(win_player, centre_back)
            if state:
                # 射门
                goal_keeper = another_team.get_location_players((Location.GK))[0]
                state = self.shot_and_save(win_player, goal_keeper)
        return True

    def pull_back(self, another_team: Team):
        """
        倒三角
        """
        # 边锋过边卫
        wing = random.choice(self.get_location_players((Location.LW, Location.RW)))
        if wing.location == Location.LW:
            wing_backs = another_team.get_location_players((Location.LB))
        elif wing.location == Location.RW:
            wing_backs = another_team.get_location_players((Location.RB))
        else:
            raise ValueError('边锋不存在！')
        state, win_player = self.sprint_dribble_and_block([wing], wing_backs)  # 一对一或一对多
        if state:
            # 边锋内切
            centre_back = random.choice(another_team.get_location_players((Location.CB)))
            state = self.dribble_and_block(win_player, centre_back)
            if state:
                # 倒三角传球
                state = self.pass_ball(win_player, another_team.get_average_capability('passing'))
                if state:
                    shooter = random.choice(self.get_location_players((Location.ST, Location.CM)))
                    goal_keeper = another_team.get_location_players((Location.GK))[0]
                    state = self.shot_and_save(shooter, goal_keeper)
        return True

    def middle_attack(self, another_team: Team):
        midfielders = self.get_location_players((Location.CM))
        state = True
        for _ in range(5):
            judge_list = []
            for player in midfielders:
                judge_list.append(self.pass_ball(player, another_team.get_average_capability('passing')))
            if True not in judge_list:
                state = False
                break
        if state:
            # 争顶
            strikers = self.get_location_players((Location.ST))
            centre_backs = another_team.get_location_players((Location.CB))
            state, win_player = self.drop_ball(strikers, centre_backs)
            if state:
                # 射门
                goal_keeper = another_team.get_location_players((Location.GK))[0]
                state = self.shot_and_save(win_player, goal_keeper)
            else:
                # 防守球员解围
                state = another_team.pass_ball(win_player, self.get_average_capability('passing'))
                if state:
                    # 外围争顶
                    centre_backs = self.get_location_players((Location.CB))
                    strikers = another_team.get_location_players((Location.ST))
                    state, win_player = another_team.drop_ball(strikers, centre_backs)
                    if state:
                        return True
                return False
        return True

    def counter_attack(self, another_team: Team):
        passing_player = random.choice(
            self.get_location_players((Location.GK, Location.CB, Location.LB, Location.RB,
                                       Location.CM, Location.LW, Location.RW)))
        state = self.pass_ball(passing_player, another_team.get_average_capability('passing'))
        if state:
            # 过人
            strikers = self.get_location_players((Location.ST))
            centre_backs = another_team.get_location_players((Location.CB))
            if not strikers:
                print("很可惜，无锋阵容没有中锋进行接应，球权被{}夺去".format(another_team.name))
                return True
            state, win_player = self.sprint_dribble_and_block(strikers, centre_backs)
            if state:
                # 射门
                goal_keeper = another_team.get_location_players((Location.GK))[0]
                state = self.shot_and_save(win_player, goal_keeper)
        return True


class Game:
    def __init__(self, team1_info: dict, team2_info: dict):
        self.lteam = Team(team1_info)
        self.rteam = Team(team2_info)

    def start(self):
        hold_ball_team, no_ball_team = self.init_hold_ball_team()
        original_score = (self.lteam.score, self.rteam.score)
        counter_attack_permitted = False
        for _ in range(100):
            exchange_ball = hold_ball_team.attack(no_ball_team, counter_attack_permitted)
            if exchange_ball:
                hold_ball_team, no_ball_team = self.exchange_hold_ball_team(hold_ball_team)
            if exchange_ball and original_score == (self.lteam.score, self.rteam.score):
                counter_attack_permitted = not counter_attack_permitted
        # print((self.lteam.score, self.rteam.score))
        return (self.lteam.score, self.rteam.score)

    def init_hold_ball_team(self):
        hold_ball_team = random.choice([self.lteam, self.rteam])
        no_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        return hold_ball_team, no_ball_team

    def exchange_hold_ball_team(self, hold_ball_team: Team):
        hold_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        no_ball_team = self.lteam if hold_ball_team == self.rteam else self.rteam
        return hold_ball_team, no_ball_team


if __name__ == '__main__':
    l_win = 0
    r_win = 0
    draw = 0
    for _ in range(1000):

        game = Game(*team_list)
        l, r = game.start()
        if l > r:
            l_win += 1
        elif l < r:
            r_win += 1
        else:
            draw += 1
    print('左胜：{}，右胜：{}，平局：{}'.format(l_win, r_win, draw))
