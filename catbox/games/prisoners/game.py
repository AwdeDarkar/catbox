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

import game


class Game(game.Game):
    """ Iterated prisoner's dilemma game manager """

    name = "prisoners"

    _rounds = 5

    def __init__(self):
        super().__init__()
        self.history = []
        self.current_actions = {}
        self.current_pairings = []

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
