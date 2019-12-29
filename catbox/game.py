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

    name = ""

    def __init__(self):
        self.server = None
        self.code = None
        self.players = {}
        self.config = {}

        self.table_sid = None

        logging.info("Game initialized")

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
        elif username == "table":
            self.table_sid = sid
            self.display_lobby()
        else:
            logging.info("New player added")
            self.players[username] = sid

            self.on_join(username)

    def find_username(self, sid):
        """ Get the user with the passed SID """

        for key, value in self.players.items():
            if value == sid:
                return key
            else:
                logging.error("Username for SID %s not found", sid)
                return None

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
        """ Send message to table display """
        logging.info("Sending to TABLE: %s", event)
        logging.debug("Send data - %s", data)

        if self.table_sid is not None:
            self.server.communicate(self.table_sid, event, data)
        else:
            logging.error("No table connected!")
            # TODO: add to queue?
            pass

    def send_html(self, username, html):
        """ Sends raw html to display to the specified user """
        self.send(username, "display", {"html": html})
        
    def send_table_html(self, html):
        """ Sends raw html to display on table """
        self.send_table("display", {"html": html})
        
    def broadcast_html(self, html):
        """ Sends raw html to display on every client """
        self.broadcast("display", {"html": html})

    def handle_message(self, username, data):
        """ Receive message from connected client (from username) """
        logging.debug("Message receieved from %s : $s", username, data)

    def game_loop(self):
        """ The main game loop function called by an external timer thread """
        # logging.debug("Game tick")
        # print(self.players)
        # print(self.table_sid)
        pass

    def on_join(self, username):
        """ Handler that is called when a player joins the game """
        self.send(username, "clear page", {})
        self.send_html(username, "<h1>Welcome to " + self.code + " " + username + "</h1>")

        self.display_lobby()

    def display_lobby(self):
        """ Send a lobby of connected players to the table """
        html = """
            <h1>Lobby for room """ + self.code + """</h1>

            <p>Players:</p>
            <ul>"""

        for username in self.players:
            html += "<li>" + username + "</li>"
            
        html += "</ul>"
        
        self.send_table_html(html)
        # self.broadcast_html(html) # TODO debug
