import threading
import av
import time
import numpy as np
import app.shared as shared

class AudioStreamer:
    def __init__(self, camera, socketio):
        self.camera = camera
        self.socketio = socketio
        self.is_running = False
        self.thread = None

    def start_streaming(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._stream_loop)
            self.thread.daemon = True
            self.thread.start()
            print("🎤 Audio Streamer Started")

    def _stream_loop(self):
        rtsp_url = f"rtsp://{self.camera.user}:{self.camera.password}@{self.camera.ip}/stream1"
        
        while self.is_running:
            try:
                # 'tcp' is required for stable audio
                container = av.open(rtsp_url, options={'rtsp_transport': 'tcp'})
                stream = container.streams.audio[0]
                
                # USE s16 (Signed 16-bit Integer) - Matches your working test
                resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)

                for packet in container.demux(stream):
                    if not self.is_running:
                        break
                        
                    for frame in packet.decode():
                        frame.pts = None
                        output_frames = resampler.resample(frame)
                        
                        for out_frame in output_frames:
                            array = out_frame.to_ndarray()
                            
                            # 1. Send to Browser
                            self.socketio.emit('audio_chunk', array.tobytes())
                            
                            # 2. Send to Recorder (We will implement this next)
                            if shared.recorder and shared.recorder.is_recording:
                                shared.recorder.add_audio(array)

            except Exception as e:
                print(f"⚠️ Audio Error: {e}")
                time.sleep(2) 
            finally:
                try:
                    container.close()
                except:
                    pass