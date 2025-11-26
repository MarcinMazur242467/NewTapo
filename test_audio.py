import time
import math
import struct
import threading
from flask import Flask, render_template_string
from flask_socketio import SocketIO

# Setup simple server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Audio Settings
SAMPLE_RATE = 16000
FREQUENCY = 440.0  # Hz (A4 Note)
AMPLITUDE = 10000  # Max is 32767 for Int16

def generate_sine_wave():
    """Generates a continuous beep sound."""
    print("🎵 Starting Synthetic Audio Stream (440Hz Tone)...")
    
    t = 0
    chunk_size = 1024 # Send small chunks like a real stream
    
    while True:
        # Generate raw PCM data (Signed 16-bit Integers)
        packet = bytearray()
        
        for i in range(chunk_size):
            # Math to create a sine wave
            sample = int(AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * t / SAMPLE_RATE))
            
            # Pack as 'short' (2 bytes, little endian)
            packet.extend(struct.pack('<h', sample))
            t += 1
        
        # Emit the chunk
        socketio.emit('audio_chunk', bytes(packet))
        
        # Sleep to simulate real-time (1024 samples / 16000 Hz = 0.064s)
        time.sleep(chunk_size / SAMPLE_RATE)

@app.route('/')
def index():
    # Simple HTML client embedded here for ease of testing
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Audio Test</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.3.2/socket.io.min.js"></script>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #222; color: #fff; }
        button { padding: 20px 40px; font-size: 20px; cursor: pointer; background: #e74c3c; color: white; border: none; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>🧪 Audio Isolation Test</h1>
    <p>If you hear a clear "BEEP", the browser logic is perfect.</p>
    <button id="btn" onclick="toggleAudio()">🔇 Start Test</button>
    <div id="status" style="margin-top:20px; color: #aaa;">Waiting...</div>

    <script>
        const socket = io();
        let audioCtx;
        let nextStartTime = 0;
        const btn = document.getElementById('btn');
        const status = document.getElementById('status');

        function toggleAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
                btn.innerHTML = "🔊 Stop Test";
                btn.style.background = "#27ae60";
            } else {
                audioCtx.suspend();
                btn.innerHTML = "🔇 Start Test";
                btn.style.background = "#e74c3c";
            }
        }

        socket.on('audio_chunk', (arrayBuffer) => {
            if (!audioCtx || audioCtx.state !== 'running') return;
            
            status.innerText = "Received Data: " + arrayBuffer.byteLength + " bytes";

            // --- THE LOGIC WE ARE TESTING (Int16 -> Float32) ---
            const int16Data = new Int16Array(arrayBuffer);
            const float32Data = new Float32Array(int16Data.length);
            
            for (let i = 0; i < int16Data.length; i++) {
                // Convert -32768..32767 to -1.0..1.0
                float32Data[i] = int16Data[i] / 32768.0;
            }
            // ----------------------------------------------------

            const audioBuffer = audioCtx.createBuffer(1, float32Data.length, 16000);
            audioBuffer.getChannelData(0).set(float32Data);
            
            const source = audioCtx.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioCtx.destination);

            if (nextStartTime < audioCtx.currentTime) nextStartTime = audioCtx.currentTime;
            source.start(nextStartTime);
            nextStartTime += audioBuffer.duration;
        });
    </script>
</body>
</html>
    """)

if __name__ == '__main__':
    # Start generation thread
    thread = threading.Thread(target=generate_sine_wave)
    thread.daemon = True
    thread.start()
    
    print("Server running on http://0.0.0.0:5001")
    socketio.run(app, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)