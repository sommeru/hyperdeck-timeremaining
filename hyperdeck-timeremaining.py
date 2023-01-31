#!/usr/bin/env python

from flask import Flask, url_for, render_template, request
from flask_socketio import SocketIO, emit
import logging

debug_mode = False
secret_key = 'secret!'

uid_counter = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
socketio = SocketIO(app)

if (debug_mode == True):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

print('server start')

@socketio.on('connect')
def socket_connect():
    print('somebody connected')

    global uid_counter
    uid_counter += 1
    json = {}
    json['name'] = 'User {}'.format(uid_counter)
    emit('join', json, json=True, broadcast=True)

@socketio.on('send_update')
def on_send_update(json):
    emit('update', json, json=True, broadcast=True)

@app.route('/')
def render_index():
    global secret_key
    return render_template('index.j2', secret_key=secret_key)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port='1313', allow_unsafe_werkzeug=True, debug=debug_mode)

