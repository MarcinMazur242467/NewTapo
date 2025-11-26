import os
import cv2
import time
import numpy as np

# --- FIXED IMPORTS FOR MOVIEPY 2.0 ---
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip 
from moviepy.audio.AudioClip import AudioArrayClip
# -------------------------------------

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.video_frames = [] 
        self.audio_chunks = [] 
        self.filename = None
        self.save_dir = os.path.join(os.getcwd(), "recordings")
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_recording(self):
        if self.is_recording:
            return

        self.video_frames = []
        self.audio_chunks = [] 
        self.is_recording = True
        
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = os.path.join(self.save_dir, f"recording_{timestamp}.mp4")
        
        print(f"🔴 RAM Recording started: {self.filename}")
        return self.filename

    def add_frame(self, frame):
        if not self.is_recording or frame is None:
            return
        # Convert BGR (OpenCV) to RGB (MoviePy)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.video_frames.append(frame_rgb)

    def add_audio(self, audio_data):
        if not self.is_recording or audio_data is None:
            return
        # Store raw numpy array (s16)
        self.audio_chunks.append(audio_data)

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        
        if len(self.video_frames) > 0:
            print(f"💾 Processing {len(self.video_frames)} video frames...")
            
            # 1. Create Video Clip
            video_clip = ImageSequenceClip(self.video_frames, fps=20)
            
            # 2. Process Audio
            if len(self.audio_chunks) > 0:
                print(f"   ...and merging {len(self.audio_chunks)} audio chunks.")
                try:
                    # Combine chunks
                    full_audio = np.concatenate(self.audio_chunks)
                    full_audio = full_audio.reshape((-1, 1))
                    
                    # Convert Int16 to Float (-1.0 to 1.0) for MoviePy
                    audio_float = full_audio / 32768.0
                    
                    # Create Audio Clip
                    audio_clip = AudioArrayClip(audio_float, fps=16000)
                    
                    # Attach to Video
                    video_clip = video_clip.with_audio(audio_clip) 
                    # Note: In v2.0 'set_audio' is often renamed to 'with_audio'
                    # If 'with_audio' fails, try 'set_audio'
                    
                except Exception as e:
                    print(f"⚠️ Audio Merge Failed: {e}")

            # 3. Write File
            video_clip.write_videofile(
                self.filename, 
                codec='libx264', 
                audio_codec='aac', 
                preset='ultrafast', 
                ffmpeg_params=['-movflags', 'faststart'],
                logger=None
            )
            
            print(f"✅ Saved: {self.filename}")
            
            self.video_frames = []
            self.audio_chunks = []
            return self.filename
        else:
            print("⚠️ No frames recorded.")
            return None