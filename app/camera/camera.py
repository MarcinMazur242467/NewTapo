import cv2
from pytapo import Tapo

class TapoCamera:
    def __init__(self, ip, user, password, cloudPassword):
        self.ip = ip
        self.user = user
        self.password = password
        self.cloudPassword = cloudPassword
        self.cap = None
        self.admin = None 

    def connect(self):
        # 1. Setup Video (RTSP)
        url = f"rtsp://{self.user}:{self.password}@{self.ip}/stream1"
        self.cap = cv2.VideoCapture(url)
        video_success = self.cap.isOpened()

        # 2. Setup Controls (Pytapo)
        try:
            self.admin = Tapo(self.ip, self.user, self.cloudPassword)
            # Try a simple command to verify connection
            self.admin.getBasicInfo() 
            control_success = True
        except Exception as e:
            print(f"⚠️ Control Error: {e}")
            control_success = False

        if video_success and control_success:
            print(f"✅ Fully Connected to {self.ip}")
            return True
        else:
            print(f"❌ Connection Issues: Video={video_success}, Controls={control_success}")
            return False

    def read_frame(self):
        if self.cap and self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                return frame
        return None

    def move(self, direction, step=10):
        """Moves the camera. Step is the degrees to move."""
        if not self.admin:
            print("❌ Camera controls not connected.")
            return

        # Ensure step is an integer
        step = int(step)

        try:
            if direction == "up":
                self.admin.moveMotor(0, step)
            elif direction == "down":
                self.admin.moveMotor(0, -step)
            elif direction == "left":
                self.admin.moveMotor(-step, 0)
            elif direction == "right":
                self.admin.moveMotor(step, 0)
            
        except Exception as e:
            print(f"❌ Error moving camera: {e}")
            try:
                self.admin = Tapo(self.ip, self.user, self.password)
            except:
                pass


    def release(self):
        if self.cap:
            self.cap.release()