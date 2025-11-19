import os
from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect, url_for
import app.shared as shared 

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

# ===========================
# 1. MAIN CAMERA ROUTES
# ===========================

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/move', methods=['POST'])
def move_camera():
    data = request.json
    direction = data.get('direction')
    if shared.camera:
        shared.camera.move(direction)
        return jsonify({"status": "success", "direction": direction})
    return jsonify({"error": "Camera not connected"}), 500


# ===========================
# 2. RECORDING ROUTES
# ===========================

@web.route('/recordings')
def list_recordings():
    """Lists all .mp4 files in the recordings folder."""
    recordings_dir = os.path.join(os.getcwd(), 'recordings')
    
    if not os.path.exists(recordings_dir):
        os.makedirs(recordings_dir)

    # List files, newest first
    files = [f for f in os.listdir(recordings_dir) if f.endswith('.mp4')]
    files.sort(reverse=True) 

    return render_template('recordings.html', files=files)

# --- FIX 1: Specific route for PLAYING (Streaming) ---
@web.route('/recordings/play/<path:filename>')
def play_recording(filename):
    recordings_dir = os.path.join(os.getcwd(), 'recordings')
    return send_from_directory(recordings_dir, filename)

# --- FIX 2: Specific route for DOWNLOADING ---
@web.route('/recordings/download/<path:filename>')
def download_recording(filename):
    recordings_dir = os.path.join(os.getcwd(), 'recordings')
    # as_attachment=True forces the browser to download instead of play
    return send_from_directory(recordings_dir, filename, as_attachment=True)

# --- FIX 3: Specific route for DELETING (Allows POST) ---
@web.route('/recordings/delete/<path:filename>', methods=['POST'])
def delete_recording(filename):
    recordings_dir = os.path.join(os.getcwd(), 'recordings')
    file_path = os.path.join(recordings_dir, filename)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {filename}")
        else:
            print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error deleting file: {e}")

    # Reload the list after deleting
    return redirect(url_for('web.list_recordings'))