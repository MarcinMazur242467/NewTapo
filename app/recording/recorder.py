import os
import cv2
import time
import numpy as np

# Correct imports for MoviePy 2.0
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip 
from moviepy.audio.AudioClip import AudioArrayClip

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
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.video_frames.append(frame_rgb)

    def add_audio(self, audio_data):
        if not self.is_recording or audio_data is None:
            return
        self.audio_chunks.append(audio_data)

    def stop_recording(self):
        if not self.is_recording:
            return

        self.is_recording = False
        
        if len(self.video_frames) > 0:
            print(f"💾 Processing {len(self.video_frames)} video frames...")
            
            # 1. Create Video Clip
            # Note: 20 FPS is an assumption. If your camera is faster/slower, 
            # this might cause video speed drift.
            video_clip = ImageSequenceClip(self.video_frames, fps=20)
            video_duration = video_clip.duration
            
            # 2. Process Audio
            if len(self.audio_chunks) > 0:
                print(f"   ...merging audio. Target duration: {video_duration}s")
                try:
                    full_audio = np.concatenate(self.audio_chunks)
                    
                    # Convert Int16 to Float
                    audio_float = full_audio / 32768.0
                    
                    # --- FIX: FORCE STEREO & DURATION ---
                    # 1. Reshape to Mono Column
                    audio_float = audio_float.reshape((-1, 1))
                    
                    # 2. Duplicate to Stereo (Left=Right)
                    # This ensures maximum compatibility with players
                    audio_stereo = np.hstack((audio_float, audio_float))
                    
                    # 3. Create Clip
                    audio_clip = AudioArrayClip(audio_stereo, fps=16000)
                    
                    # 4. Sync Duration (Cut audio to match video length)
                    # This prevents the audio from stretching or dragging on
                    audio_clip = audio_clip.with_duration(video_duration)
                    
                    # Attach
                    video_clip = video_clip.with_audio(audio_clip)
                    
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