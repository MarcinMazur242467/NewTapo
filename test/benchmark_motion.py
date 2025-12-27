import time
import cv2
import numpy as np
import sys
import os

# Dodanie katalogu glownego do sciezki, aby zaimportowac moduly aplikacji
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.detection.motion import MotionDetector

def benchmark_motion_detection():
    print("=== ROZPOCZECIE TESTU WYDAJNOSCI DETEKCJI RUCHU ===")
    
    # Inicjalizacja detektora
    detector = MotionDetector(min_area=1000)
    
    # Generowanie sztucznej klatki Full HD (1920x1080) - czarny obraz
    # Symulujemy najgorszy przypadek rozmiaru klatki
    frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    # Rozgrzewka (warm-up) - pierwsze wywolania moga byc wolniejsze
    for _ in range(10):
        detector.detect(frame)
        
    iterations = 500
    start_time = time.time()
    
    for _ in range(iterations):
        # Symulacja zmiany w obrazie (szum)
        noise = np.random.randint(0, 50, (1080, 1920, 3), dtype=np.uint8)
        test_frame = cv2.add(frame, noise)
        detector.detect(test_frame)
        
    end_time = time.time()
    total_time = end_time - start_time
    avg_time_per_frame = total_time / iterations
    fps_theoretical = 1.0 / avg_time_per_frame

    print(f"Liczba iteracji: {iterations}")
    print(f"Sredni czas przetwarzania klatki (1080p): {avg_time_per_frame:.4f} s")
    print(f"Teoretyczna maksymalna wydajnosc: {fps_theoretical:.2f} FPS")

if __name__ == "__main__":
    benchmark_motion_detection()