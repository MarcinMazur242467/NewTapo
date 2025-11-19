import threading
import cv2
import time
import base64

import app.shared as shared

class VideoStreamer:
    def __init__(self, camera, socketio):
        self.camera = camera
        self.socketio = socketio
        self.is_running = False
        self.thread = None

    def start_streaming(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop)
            self.thread.daemon = True
            self.thread.start()

    def _capture_loop(self):
        while self.is_running:
            # 1. Get the RAW (High Quality) frame
            raw_frame = self.camera.read_frame()
            
            if raw_frame is not None:
                # 2. Send RAW frame to recorder (Best quality for saved files)
                if shared.recorder and shared.recorder.is_recording:
                    shared.recorder.add_frame(raw_frame)

                # 3. Resize for Web (Lower bandwidth/Speed)
                web_frame = cv2.resize(raw_frame, (1000, 562))

                # 4. Encode the resized frame for the browser
                success, buffer = cv2.imencode('.jpg', web_frame)
                
                if success:
                    b64_frame = base64.b64encode(buffer).decode('utf-8')
                    self.socketio.emit('video_frame', {'frame': b64_frame}) 

            self.socketio.sleep(0.04) # ~25 FPS