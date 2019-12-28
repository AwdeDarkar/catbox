"""
server
====================================================================================================

Management of an instance of the server, allows creating and managing games.

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

import sys
import logging
import string
import random

from flask import Flask, render_template, request
from flask_socketio import SocketIO

import game


class Server():
    """ Core server class """

    _room_code_length = 4
    """ Number of characters in a room code """

    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        self.client_sids = []

        self.games = {}  # associate room codes with game instances

        # self.socketio.on_event("connect", self.handle_connect)
        # self.socketio.on_event("disconnect", self.handle_disconnect)
        # self.socketio.on_event("join", self.handle_join)

        logging.info("Server initialized")

    def create_code(self):
        """ Create a short room code for joining the game """
        return "".join([random.choice(string.ascii_uppercase + string.digits) for _ in
                        range(Server._room_code_length)])

    def register_game(self, game):
        """ Register the instance of Game with the server and start hosting it """

        # search for unused code TODO find a non-evil way of doing this
        code = self.create_code()
        while code in self.games:
            logging.debug("Code %s in use, regenerating", code)
            code = self.create_code()

        self.games[code] = game
        game.server = self
        game.code = code

        logging.info("Game with code %s created", code)

    def handle_connect(self, request):
        """ Allow clients to connect to the server """
        logging.info("Client %s connected", request.sid)
        self.client_sids.append(request.sid)

    def handle_disconnect(self, request):
        """ Allow clients to disconnect from the server """
        logging.info("Client %s disconnected", request.sid)
        self.client_sids.remove(request.sid)

    def handle_join(self, data):
        """ Connect a client with a game """
        username = data["username"]
        code = data["code"]

        logging.info("User '%s' (name '%s') requesting to join room '%s'", request.sid, username,
                     code)
        if code not in self.games.keys():
            logging.error("Room %s does not exist", code)
            self.communicate(request.sid, "join error", {"msg": "Room does not exist"})
        else:
            self.games[code].add_player(username, request.sid)

    def communicate(self, sid, event, data):
        """ Sends the event and data to the client with the sid """
        logging.debug("Emitting %s to %s", event, sid)
        self.socketio.emit(event, data, room=sid)


def init_logger():
    # what loggers do we have?
    for key in logging.Logger.manager.loggerDict:
        print(key)

    # mute some things
    logging.getLogger('socketio').setLevel(logging.CRITICAL)
    logging.getLogger('socketio.client').setLevel(logging.CRITICAL)
    logging.getLogger('socketio.server').setLevel(logging.CRITICAL)
    logging.getLogger('engineio.server').setLevel(logging.CRITICAL)
    logging.getLogger('engineio.client').setLevel(logging.CRITICAL)
    logging.getLogger('engineio').setLevel(logging.CRITICAL)

    log_formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
            )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


init_logger()
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)
socketio = SocketIO(app)
server = Server(app, socketio)


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/games')
def games_launcher():
    """ List of all installed games which may be launched """
    pass


@app.route('/')
def landing():
    return render_template("page.html")


@app.route("/create-game")
def create_game():
    logging.info("Game creation requested")
    testgame = game.Game()
    testgame.server = server
    server.register_game(testgame)
    logging.info("Game created")
    return "Game created " + testgame.code


@socketio.on('connect')
def connect():
    # clients.append(request.namespace)
    logging.debug("Flask socket server received connect event")
    server.handle_connect(request)


@socketio.on('disconnect')
def disconnect():
    # clients.remove(request.namespace)
    logging.debug("Flask socket server received disconnect event")
    server.handle_disconnect(request)


@socketio.on('join')
def join(data):
    logging.debug("Flask socket server received join event %s", data)
    server.handle_join(data)


create_game() # TODO: just for debugging
if __name__ == '__main__':
    socketio.run(app, debug=False)
