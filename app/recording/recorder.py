import os
import cv2
import time
import numpy as np
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip 
from moviepy.audio.AudioClip import AudioArrayClip

class Recorder:
    def __init__(self):
        self.is_recording = False
        self.video_frames = [] 
        self.audio_chunks = [] 
        self.filename = None
        self.start_time = 0 # Track exact time for FPS calculation
        self.save_dir = os.path.join(os.getcwd(), "recordings")
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_recording(self):
        if self.is_recording:
            return

        self.video_frames = []
        self.audio_chunks = [] 
        self.is_recording = True
        self.start_time = time.time() # Start the clock
        
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
        elapsed_time = time.time() - self.start_time # Calculate actual duration
        
        if len(self.video_frames) > 0:
            print(f"💾 Processing {len(self.video_frames)} frames over {elapsed_time:.2f}s...")
            
            # 1. Calculate REAL FPS
            # If we guess 20 but camera sent 15, audio desyncs. This fixes it.
            real_fps = len(self.video_frames) / elapsed_time
            if real_fps <= 0: real_fps = 20 # Safety fallback
            
            print(f"   (Calculated FPS: {real_fps:.2f})")

            # 2. Create Video Clip with Real FPS
            video_clip = ImageSequenceClip(self.video_frames, fps=real_fps)
            
            # 3. Process Audio
            if len(self.audio_chunks) > 0:
                try:
                    full_audio = np.concatenate(self.audio_chunks)
                    
                    # Int16 -> Float
                    audio_float = full_audio / 32768.0
                    
                    # Force Stereo (Fixes compatibility)
                    audio_float = audio_float.reshape((-1, 1))
                    audio_stereo = np.hstack((audio_float, audio_float))
                    
                    # Create Audio Clip (Source is still 16k)
                    audio_clip = AudioArrayClip(audio_stereo, fps=16000)
                    
                    # Attach
                    video_clip = video_clip.with_audio(audio_clip)
                    
                except Exception as e:
                    print(f"⚠️ Audio Merge Failed: {e}")

            # 4. Write File with UPSAMPLING
            video_clip.write_videofile(
                self.filename, 
                codec='libx264', 
                audio_codec='aac', 
                preset='ultrafast', 
                audio_fps=44100,  # <--- CRITICAL FIX: Upsample to Standard
                audio_bitrate='192k', # <--- CRITICAL FIX: Higher Quality
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