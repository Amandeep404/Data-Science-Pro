from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

tasks = {'default': []}

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks['default'])

@socketio.on('add_task')
def handle_add_task(data):
    tasks[data['user']].append(data['task'])
    emit('update_tasks', tasks[data['user']], broadcast=True)

@socketio.on('edit_task')
def handle_edit_task(data):
    tasks[data['user']][data['index']] = data['task']
    emit('update_tasks', tasks[data['user']], broadcast=True)

@socketio.on('delete_task')
def handle_delete_task(data):
    del tasks[data['user']][data['index']]
    emit('update_tasks', tasks[data['user']], broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
