from flask import Flask, render_template
from flask_socketio import SocketIO

client_sids = []

# NOTE: unclear where below should go
socketio = SocketIO(app)

@socketio.on('connect')
def connect():
    client_sids.append(request.sid)


@socketio.on('disconnect')
def disconnect():
    client_sids.remove(request.sid)


def communicate(sid, event, data):
    socketio.emit(event, data, room=sid)
