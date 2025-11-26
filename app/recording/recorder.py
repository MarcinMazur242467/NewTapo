import os
import cv2
import time
# Import for MoviePy 2.0+
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip 

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.frames = [] 
        self.filename = None
        self.save_dir = os.path.join(os.getcwd(), "recordings")
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_recording(self):
        if self.is_recording:
            return

        self.frames = [] 
        self.is_recording = True
        
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = os.path.join(self.save_dir, f"recording_{timestamp}.mp4")
        
        print(f"🔴 RAM Recording started for: {self.filename}")
        return self.filename

    def add_frame(self, frame):
        if not self.is_recording or frame is None:
            return

        # Convert BGR (OpenCV) to RGB (MoviePy)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frames.append(frame_rgb)

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        
        if len(self.frames) > 0:
            print(f"💾 Processing {len(self.frames)} frames with MoviePy...")
            
            # Create video clip
            clip = ImageSequenceClip(self.frames, fps=20)
            
            # Write file (REMOVED verbose=False for MoviePy 2.0 compatibility)
            clip.write_videofile(
                self.filename, 
                codec='libx264', 
                audio=False, 
                preset='ultrafast', 
                ffmpeg_params=['-movflags', 'faststart'],
                logger=None  # This still works to keep it silent
            )


            
            self.frames = [] 
            return self.filename
        else:
            print("⚠️ No frames recorded.")
            return None