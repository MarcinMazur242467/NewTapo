import sys
import os
import numpy as np
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.recording.recorder import Recorder

def test_recording_memory_growth():
    print("=== TEST ZUZYCIA PAMIECI (In-Memory Buffering) ===")
    recorder = Recorder()
    recorder.start_recording()
    
    # Parametry symulacji
    fps = 25
    duration_seconds = 10
    total_frames = fps * duration_seconds
    
    # Rozmiar klatki 1080p w formacie surowym (H * W * Channels)
    # 1080 * 1920 * 3 bajty = ~6.22 MB na klatke
    frame_shape = (1080, 1920, 3)
    frame_size_mb = (1080 * 1920 * 3) / (1024 * 1024)
    
    print(f"Symulacja nagrania: {duration_seconds}s @ {fps} FPS")
    print(f"Rozmiar pojedynczej klatki: {frame_size_mb:.2f} MB")
    
    current_frames_memory = 0
    
    for i in range(total_frames):
        # Tworzymy nowa macierz dla kazdej klatki
        frame = np.zeros(frame_shape, dtype=np.uint8)
        recorder.add_frame(frame)
        
        # Co sekunde (25 klatek) raportujemy zuzycie
        if (i + 1) % fps == 0:
            # Estymacja zajetoscy bufora
            estimated_size = len(recorder.video_frames) * frame_size_mb
            print(f"Czas nagrania: {(i+1)//fps}s | Zbuforowane klatki: {len(recorder.video_frames)} | Estymowane zuzycie RAM: {estimated_size:.2f} MB")

    print("\nWniosek: Widoczny liniowy wzrost zuzycia pamieci potwierdza koniecznosc limitowania dlugosci nagran w tym modelu architektonicznym.")
    
    # Czyszczenie
    recorder.video_frames = []

if __name__ == "__main__":
    test_recording_memory_growth()