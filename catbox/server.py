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
import yaml
import logging
import string
import random
import threading
import time
import importlib
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO


def game_tick(newgame, rest_time):
    while True:
        time.sleep(rest_time)
        newgame.game_loop()


class Server():
    """ Core server class """

    _room_code_length = 4
    """ Number of characters in a room code """

    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        self.client_sids = []
        self.installed = {}

        self.games = {}  # associate room codes with game instances

        self.ip = "http://127.0.0.1"
        self.port = 5000

        logging.info("Server initialized")

    def create_code(self):
        """ Create a short room code for joining the game """
        return "".join([random.choice(string.ascii_uppercase + string.digits) for _ in
                        range(Server._room_code_length)])

    def register_game(self, newgame):
        """ Register the instance of Game with the server and start hosting it """

        # search for unused code TODO find a non-evil way of doing this
        code = self.create_code()
        while code in self.games:
            logging.debug("Code %s in use, regenerating", code)
            code = self.create_code()

        self.games[code] = newgame
        newgame.server = self
        newgame.code = code

        logging.info("Creating game timer for game loop...")
        game_timer_thread = threading.Thread(target=game_tick, args=(newgame, 1))
        game_timer_thread.start()

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

    def load_games(self):
        """ Load all locally installed games """
        path = Path("games")
        for gmod in path.iterdir():
            if gmod.is_file() or "__pycache__" in gmod.name:
                continue
            name = ""
            config = {}
            with gmod.joinpath("config.yml").open("r") as f:
                config = yaml.load(f.read())
                name = config["name"]
            self.installed[name] = (config, importlib.import_module("games.%s.game" % gmod.name))


def init_logger():
    # what loggers do we have?
    """
    for key in logging.Logger.manager.loggerDict:
        print(key)
    """

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


@app.route('/games/<name>')
def create_game(name):
    logging.info("Game creation requested")
    config, gmod = server.installed[name]
    newgame = gmod.game.Game()
    newgame.server = server
    newgame.config = config
    server.register_game(newgame)
    logging.info("Game %s created with code %s", name, newgame.code)
    return render_template("table_join.html", code=newgame.code)


@app.route('/games')
def games_launcher():
    """ List of all installed games which may be launched """
    if not server.installed:
        server.load_games()
    print(server.installed)
    return render_template("games.html", games=list(server.installed.keys()))


@app.route('/')
def landing():
    return render_template("page.html")


@app.route('/<room>/resource/<resource_name>')
def serve_resource(room, resource_name):
    path = server.games[room].config["resources"][resource_name]
    return send_from_directory("/games", path)


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


@socketio.on('game msg')
def game_msg(data):
    logging.debug("Flask socket server received game message", data)
    room = data["room"]

    # check room exists
    if room not in server.games:
        logging.error("Room %s does not exist", room)
        # TODO: send error back
        return

    # check username exists
    username = server.games[room].find_username(request.sid)
    if username is None:
        # TODO: send error back
        return

    server.games[room].handle_message(username, data["data"])


if __name__ == '__main__':
    socketio.run(app, debug=False)
