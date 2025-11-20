from flask_socketio import emit
from app import socketio
import app.shared as shared

@socketio.on('start_recording')
def handle_start_recording():
    if shared.recorder:
        shared.recorder.start_recording()
        emit('recording_status', {'status': 'started'}, broadcast=True)

@socketio.on('stop_recording')
def handle_stop_recording():
    if shared.recorder:
        filename = shared.recorder.stop_recording()
        emit('recording_status', {'status': 'stopped', 'file': filename}, broadcast=True)

@socketio.on('move_camera')
def handle_move_camera(data):
    direction = data.get('direction')
    step = data.get('step', 5) # Default to 5 if missing
    
    if shared.camera:
        # We don't need to return a response like HTTP
        # Just do the work.
        shared.camera.move(direction, step)