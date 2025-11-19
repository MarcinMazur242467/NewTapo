import cv2
import time
import os
import threading

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.writer = None
        self.filename = None
        # Where to save videos?
        self.save_dir = os.path.join(os.getcwd(), "recordings")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_recording(self):
        if self.is_recording:
            return

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = os.path.join(self.save_dir, f"recording_{timestamp}.mp4")
        
        # Define codec (mp4v is widely supported)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # We initialize the writer later, inside the first frame write
        # to ensure we get the exact dimensions of the video stream
        self.writer = None
        
        self.is_recording = True
        print(f"🔴 Recording started: {self.filename}")
        return self.filename

    def add_frame(self, frame):
        if not self.is_recording or frame is None:
            return

        # Initialize writer on the first frame to match dimensions exactly
        if self.writer is None:
            height, width = frame.shape[:2]
            # 20 FPS is a safe guess for RTSP streams
            self.writer = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (width, height))

        self.writer.write(frame)

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        if self.writer:
            self.writer.release()
            self.writer = None
        
        print(f"⏹ Recording saved: {self.filename}")
        return self.filename