from app.camera.camera import TapoCamera
from app.settings import load_config

# 1. Load Config
config = load_config()
cam = TapoCamera(
    config["CAMERA_IP"], 
    config["CAMERA_USER"], 
    config["CAMERA_PASS"],
    config["CAMERA_CPASS"]
)

# 2. Connect
if cam.connect():
    print("Controls connected.")
    
    # 3. Test a command
    try:
        # info = cam.admin.getBasicInfo()
        cam.admin.moveMotor(0, 5)
        # print(f"✅ Camera Name: {info['device_info']['basic_info']['device_name']}")
    except Exception as e:
        print(f"❌ Could not read info: {e}")

    cam.release()