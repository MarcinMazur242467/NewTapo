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

    def _stream_loop(self):
        rtsp_url = f"rtsp://{self.camera.user}:{self.camera.password}@{self.camera.ip}/stream1"
        
        while self.is_running:
            try:
                container = av.open(rtsp_url, options={'rtsp_transport': 'tcp'})
                stream = container.streams.audio[0]
                
                # Use 's16' (Signed 16-bit)
                resampler = av.AudioResampler(format='s16', layout='mono', rate=16000)

                for packet in container.demux(stream):
                    if not self.is_running:
                        break
                        
                    for frame in packet.decode():
                        frame.pts = None
                        output_frames = resampler.resample(frame)
                        
                        for out_frame in output_frames:
                            array = out_frame.to_ndarray()
                            
                            # --- 1. HANDLE SHAPE (Fix Clicking) ---
                            # If shape is (1, 1600), we just want to flatten it to (1600,)
                            # We only slice if we see MULTIPLE channels (e.g. 2, 1600)
                            if array.ndim == 2:
                                if array.shape[0] > 1:
                                    # Planar Stereo (2, 1600) -> Mix to Mono
                                    array = np.mean(array, axis=0)
                                elif array.shape[1] > 1:
                                    # Standard Planar (1, 1600) -> Just Flatten
                                    array = array.reshape(-1)
                            
                            # --- 2. HANDLE TYPE (Fix Demon Voice) ---
                            # Explicitly convert to Int16.
                            # If this was Float32, this fixes the byte count.
                            array = array.astype(np.int16)
                            
                            # Send to Browser
                            self.socketio.emit('audio_chunk', array.tobytes())
                            
                            # Send to Recorder
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