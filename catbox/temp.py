from flask import Flask, render_template
from flask_socketio import SocketIO

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


# TODO: this should be in some class if possible?


class Server():

    def __init__(self, socketio):
        self.socketio = socketio
        self.client_sids = []
            
    def handle_connect(self, request):
        self.client_sids.append(request.sid)
    
    def handle_disconnect(self, request):
        self.client_sids.remove(request.sid)
        
    def communicate(sid, event, data):
        self.socketio.emit(event, data, room=sid)
