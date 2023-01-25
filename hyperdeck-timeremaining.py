#!/usr/bin/env python

from flask import Flask, url_for, render_template, request
from flask_socketio import SocketIO, emit

debug_mode = True
secret_key = 'secret!'

uid_counter = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
socketio = SocketIO(app)

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
    socketio.run(app, host='127.0.0.1', port='1313', debug=debug_mode)

