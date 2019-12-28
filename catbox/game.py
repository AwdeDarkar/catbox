"""
game
====================================================================================================

Parent class for catbox games, manages things

----------------------------------------------------------------------------------------------------

**Created**
    2019-12-28
**Updated**
    2019-12-28 by Darkar
**Author**
    WildfireXIII
**Copyright**
    This software is Free and Open Source for any purpose
"""

import logging

# NOTE: if a player has not disconnected, do not allow someone else to take
# (on a player disconnect, remove sid from dictionary [set to none?])

# TODO: have extendable player class that extended game classes can add things to?


class Game():
    """ Core game class """

    def __init__(self):
        self.server = None
        self.code = None
        self.players = {}

        self.table_sid = None

    def add_player(self, username, sid):
        """
        When a new person joins a game, this is called to create their player,
        also handles connection dropping and re-connecting

        TODO: if someone disconnects set their sid to None
        """
        logging.info("Player add requested with username '%s' and sid '%s'", username, sid)

        if username in self.players.keys():
            if self.players[username] is not None:
                logging.error("Username is already taken and player still connected")
                # TODO: error message
                pass
            else:
                logging.info("User is a reconnect, resetting sid")
                self.players[username] = sid
        else:
            logging.info("New player added")
            self.players[username] = sid
            # TODO: send event to clients?

    def broadcast(self, event, data, include_table=True):
        """ Send an event and possibly a table to all players """
        logging.info("Broadcasting %s", event)
        logging.debug("Broadcast data - %s", data)

        if include_table:
            self.send_table(event, data)
        for player in self.players:
            self.send(player, event, data)

    def send(self, username, event, data):
        """ Send an event and data to a player """
        logging.info("Sending to '%s': %s", username, event)
        logging.debug("Send data - %s", data)

        if username not in self.players.keys():
            logging.error("User %s not found", username)
            # TODO: error
            pass
        else:
            if self.players[username] is None:
                logging.error("User %s is not connected", username)
                # TODO: add to queue
                pass
            else:
                self.server.communicate(self.players[username], event, data)

    def send_table(self, event, data):
        """ Send an HTML table to a player """
        logging.info("Sending to TABLE: %s", event)
        logging.debug("Send data - %s", data)

        if self.table_sid is not None:
            self.server.communicate(self.table_sid, event, data)
        else:
            logging.error("No table connected!")
            # TODO: add to queue?
            pass
