from flask import Flask
from flask_socketio import SocketIO
from app.recording.recorder import Recorder
from app.settings import load_config
from app.camera.camera import TapoCamera
from app.video.streamer import VideoStreamer
import app.shared as shared # Import the shared file

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'

    # 1. Load Config & Connect Camera
    config = load_config()
    cam = TapoCamera(config["CAMERA_IP"], config["CAMERA_USER"], config["CAMERA_PASS"], config["CAMERA_CPASS"])

    if cam.connect():
        shared.camera = cam # Store in shared file
        print("✅ Camera connected and stored in shared.")
    
    socketio.init_app(app)

    # 2. Initialize Recorder (NEW)
    shared.recorder = Recorder()

    # 3. Start Streamer
    if shared.camera:
        shared.streamer = VideoStreamer(shared.camera, socketio)
        shared.streamer.start_streaming()

    # 4. Register Routes
    from app.web.routes import web as web_blueprint
    app.register_blueprint(web_blueprint)
    
    return app

import app.web.socket_handlers