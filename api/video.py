from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def on_connect():
    print("Client connected")

@socketio.on('offer')
def on_offer(data):
    emit('offer', data, broadcast=True)

@socketio.on('answer')
def on_answer(data):
    emit('answer', data, broadcast=True)

@socketio.on('ice')
def on_ice(data):
    emit('ice', data, broadcast=True)

def handler(environ, start_response):
    return app(environ, start_response)
