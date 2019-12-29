"""
game
====================================================================================================

Implementation of an iterated prisoner's dilemma for catbox

----------------------------------------------------------------------------------------------------

**Created**
    2019-12-29
**Updated**
    2019-12-29 by Darkar
**Author**
    Darkar
**Copyright**
    This software is Free and Open Source for any purpose
"""

import logging
import random
import enum

import game


class Game(game.Game):
    """ Iterated prisoner's dilemma game manager """

    name = "prisoners"

    _rounds = 5
    _round_length = 20

    class result(enum):
        """ There are three possible results of a prisoner's dilemma """

        cooperate_cooperate = "cc"
        """ Both players cooperate """

        cooperate_defect = "cd"
        """ One player cooperates, one player defects """

        defect_defect = "dd"
        """ Both players defect """

    _payoffs = {
        result.cooperate_cooperate: (2, 2),
        result.cooperate_defect: (3, 0),
        result.defect_defect: (1, 1),
    }

    def __init__(self):
        super().__init__()
        self.history = []
        self.current_actions = {}
        self.current_pairings = []
        self.points = {}
        self.timer = 0

    def handle_message(self, username, data):
        """ Recieve message data and process it """
        if "type" not in data:
            logging.debug("Untyped message receieved from %s : $s", username, data)
            return
        if data["type"] == "action":
            if data["cooperate"]:
                self.current_actions[username] = "cooperate"
            else:
                self.current_actions[username] = "defect"

    def game_loop(self):
        if self.timer:
            # We are in a round, count down the timer
            self.timer -= 1
            return
        if len(self.history) >= Game._rounds:
            # We've completed all rounds, show the results
            pass
            return
        # We are starting a new round and may need to wrap up a previous one
        round_results = []  # (player1, player2, result[cc|cd|dd])
        if self.current_actions:  # debt notice: what happens if everyone times out?
            for player1, player2 in self.current_pairings:
                outcome = None
                if player1 in self.current_actions and self.current_actions[player1] == "defect":
                    if player2 in self.current_actions and self.current_actions[player2] == \
                            "defect":
                        outcome = Game.result.defect_defect
                        points1, points2 = Game._payoffs[outcome]
                        self.points[player1] += points1
                        self.points[player2] += points2
                    else:
                        outcome = Game.result.defect_defect
                        points1, points2 = Game._payoffs[outcome]
                        self.points[player1] += points1
                        self.points[player2] += points2
                else:
                    if player2 in self.current_actions and self.current_actions[player2] == \
                            "defect":
                        outcome = Game.result.defect_defect
                        points2, points1 = Game._payoffs[outcome]
                        self.points[player1] += points1
                        self.points[player2] += points2
                    else:
                        outcome = Game.result.cooperate_cooperate
                        points1, points2 = Game._payoffs[outcome]
                        self.points[player1] += points1
                        self.points[player2] += points2
                round_results.append((player1, player2, outcome))
            self.history.append(round_results)
        self.timer = Game._round_length
        self.current_pairings = []
        players = list(self.players.keys())
        while len(players) > 1:
            player1 = pop_random(players)
            player2 = pop_random(players)
            self.current_pairings.append((player1, player2))


def pop_random(lst):
    """ Pop a random item off the list """
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)
