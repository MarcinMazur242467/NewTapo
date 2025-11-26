from abc import ABC, abstractmethod

class BaseDetector(ABC):
    @abstractmethod
    def detect(self, frame):
        """
        Input: A raw video frame (numpy array).
        Output: A tuple (is_detected, info)
                - is_detected: Boolean (True if motion/incident found)
                - info: Dictionary with metadata (e.g., bounding boxes, count)
        """
        pass