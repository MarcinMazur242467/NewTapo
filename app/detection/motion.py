import cv2
from .base import BaseDetector

class MotionDetector(BaseDetector):
    def __init__(self, min_area=500):
        self.avg_frame = None
        self.min_area = min_area # Ignore movement smaller than this (dust, bugs)

    def detect(self, frame):
        # 1. Resize and convert to Grayscale (Faster processing)
        # We work on a copy to not mess up the original frame
        small_frame = cv2.resize(frame, (500, 300))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 2. Initialize average frame if first run
        if self.avg_frame is None:
            self.avg_frame = gray.copy().astype("float")
            return False, {}

        # 3. Accumulate weighted average (Background model)
        # 0.5 is the weight. Higher = background updates faster.
        cv2.accumulateWeighted(gray, self.avg_frame, 0.5)
        
        # 4. Compute difference
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg_frame))
        
        # 5. Threshold (Turn differences into white blobs)
        thresh = cv2.threshold(frame_delta, 5, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 6. Find Contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_found = False
        
        # Check if any contour is big enough
        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue
            motion_found = True
            break # We found at least one big movement
            
        return motion_found, {}