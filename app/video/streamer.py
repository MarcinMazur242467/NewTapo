import threading
import cv2
import base64
import time
import app.shared as shared
from app.detection.motion import MotionDetector 

class VideoStreamer:
    def __init__(self, camera, socketio):
        self.camera = camera
        self.socketio = socketio
        self.is_running = False
        self.thread = None
        self.fps_counter = 0 
        self.last_fps_time = time.time()
        
        self.detector = MotionDetector(min_area=1000)
        self.motion_active = False 

    def start_streaming(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop)
            self.thread.daemon = True
            self.thread.start()

    def _capture_loop(self):
        while self.is_running:
            # 1. Get RAW Frame
            raw_frame = self.camera.read_frame()
            
            if raw_frame is not None:
                # 2. Send to Recorder (if active)
                if shared.recorder and shared.recorder.is_recording:
                    shared.recorder.add_frame(raw_frame)

                # --- NEW: Run Detection ---
                # We detect on the raw frame.
                is_motion, _ = self.detector.detect(raw_frame)
                
                # State Change Logic (Only emit if state changes)
                if is_motion != self.motion_active:
                    self.motion_active = is_motion
                    self.socketio.emit('motion_status', {'motion': self.motion_active})
                # --------------------------

                # --- POMIAR FPS ---
                self.fps_counter += 1
                if time.time() - self.last_fps_time >= 1.0:
                    print(f"[DATA_POINT] Metric=FPS Value={self.fps_counter} Timestamp={time.time()}")
                    self.fps_counter = 0
                    self.last_fps_time = time.time()


                # 3. Resize for Web
                web_frame = cv2.resize(raw_frame, (1000, 562))

                # 4. Encode & Emit
                success, buffer = cv2.imencode('.jpg', web_frame)
                if success:
                    b64_frame = base64.b64encode(buffer).decode('utf-8')
                    self.socketio.emit('video_frame', {'frame': b64_frame}) 

            self.socketio.sleep(0.033)