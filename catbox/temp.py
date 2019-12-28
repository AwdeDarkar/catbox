import logging
import string
import random

from flask import Flask, render_template
from flask_socketio import SocketIO

from game import Game

client_sids = []

# NOTE: unclear where below should go
socketio = SocketIO(app)
server = Server(socketio)

@socketio.on('connect')
def connect():
    # client_sids.append(request.sid)
    server.handle_connect(request)


@socketio.on('disconnect')
def disconnect():
    # client_sids.remove(request.sid)
    # TODO: remove sid from game connected to
    server.handle_disconnect(request)


class Server():

    def __init__(self, socketio):
        self.socketio = socketio
        self.client_sids = []

        self.games = {} # associate room codes with game instances (also namepace should be the code?)

        logging.info("Server initialized")

    def create_code(self):
        for i in range(0, 4):
            code += random.choice(string.ascii_letters)
        
    def create_game(self, game): # game would be instance of a game child class
        # search for unused code
        code = create_code()
        while code in self.games.keys():
            logging.debug("Code %s in use, regenerating", code)
            code = create_code()
        
        self.games[code] = game
        game.server = self
        game.code = code

        logging.info("Game with code %s created", code)
        
    def handle_connect(self, request):
        logging.info("Client %s connected", request.sid)
        self.client_sids.append(request.sid)
        
    def handle_disconnect(self, request):
        logging.info("Client %s disconnected", request.sid)
        self.client_sids.remove(request.sid)
        
    def communicate(sid, event, data):
        logging.debug("Emitting %s to %s", event, sid)
        self.socketio.emit(event, data, room=sid)
