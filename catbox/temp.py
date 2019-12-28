from flask import Flask, render_template
from flask_socketio import SocketIO

client_sids = []

@socketio.on('connect')
def connect():
    client_sids.append(request.sid)

@socketio.on('disconnect')
def disconnect():
    client_sids.remove(request.sid)
