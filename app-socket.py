# flask-socketio and eventlet

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin for dev

@app.route('/')
def chat():
    return render_template('chat.html')

# Event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')
    # Broadcast to all clients (or use rooms for private chats)
    emit('message', {'username': username, 'message': message}, broadcast=True)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data.get('room', 'general')
    join_room(room)
    emit('status', f'{username} has joined the room.', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=8000)