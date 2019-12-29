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
from enum import Enum

import game
import logging


class Game(game.Game):
    """ Iterated prisoner's dilemma game manager """

    name = "prisoners"

    _rounds = 5
    _round_length = 20

    class state(Enum):
        """ Game state """

        not_started = 0
        """ The game has not begun yet """

        in_round = 1
        """ The game is in the middle of the round """

        inter_round = 2
        """ The game is in between rounds """

        completed = 3
        """ The game is over """

    class result(Enum):
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
        self.state = Game.state.not_started
        logging.debug("Inside prisoners game")

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
            self.state = Game.state.completed
            pass
            return
        if self.state == Game.state.inter_round:
            # Inter round is complete, start round
            self.current_pairings = []
            players = list(self.players.keys())
            while len(players) > 1:
                player1 = pop_random(players)
                player2 = pop_random(players)
                self.current_pairings.append((player1, player2))
            self.timer = Game._round_length
            return
        # We are starting a new round and may need to wrap up a previous one
        self.state = Game.state.inter_round
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

    def on_table_join(self):
        super().on_table_join()
        music = self.get_resource_url("song")
        self.send_table_html("<audio src='" + music + "' autoplay loop></audio>", "#audio")

    def on_join(self, username):
        super().on_join(username)
        if username == self.gm:
            logging.info("Sending special join to GM")
            start_button = "<button onclick='startGame()'>Start Game</button>"
            self.send_html(username, start_button, "#content")
        self.send_js(username, "primary_js")

    def render_dilemma(self, username1, username2):
        defect_icon_url = self.get_resource_url("defect_icon")
        cooperate_icon_url = self.get_resource_url("cooperate_icon")
        
        defect_button = "<button onclick='dilemmaInput(\"defect\")'><img src='" + defect_icon_url + "' /> Defect</button>"
        cooperate_button = "<button onclick='dilemmaInput(\"cooperate\")'><img src='" + cooperate_icon_url + "' /> Cooperate</button>"

        html1 = "<h1>You vs " + username2 + "</h1>"
        html2 = "<h1>You vs " + username1 + "</h1>"
        
        html1 += defect_button + cooperate_button
        html2 += defect_button + cooperate_button

        self.send_html(username1, html1, "#content")
        self.send_html(username2, html2, "#content")
        
    #def display_lobby(self, additional_html=""):
    #    music = self.get_resource_url("song")
    #    super().display_lobby("<audio src='" + music + "' autoplay loop></audio>")

def pop_random(lst):
    """ Pop a random item off the list """
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)
