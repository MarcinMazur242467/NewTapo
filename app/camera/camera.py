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

    def move(self, direction, step=5):
        """Moves the camera. Returns dict with success/limit status."""
        if not self.admin:
            print("❌ Camera controls not connected.")
            return {"success": False, "error": "not_connected"}

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
            
            return {"success": True}

        except Exception as e:
            error_msg = str(e).lower()
            # Check for common limit keywords in the error message
            if "range" in error_msg or "limit" in error_msg:
                print(f"⚠️ Limit Reached: {direction}")
                return {"success": False, "error": "limit_reached"}
            
            print(f"❌ Error moving camera: {e}")
            # Try to reconnect if it was a connection error
            try:
                self.admin = Tapo(self.ip, self.user, self.password)
            except:
                pass
            return {"success": False, "error": "unknown"}

    def release(self):
        if self.cap:
            self.cap.release()