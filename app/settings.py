import json
import os

def load_config():
    config = {}
    
    # 1. Try to load from JSON
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    
    # 2. Override/Fill with Environment Variables (Docker Support)
    # This allows us to pass secrets via -e flags
    if os.environ.get("CAMERA_IP"):
        config["CAMERA_IP"] = os.environ.get("CAMERA_IP")
    if os.environ.get("CAMERA_USER"):
        config["CAMERA_USER"] = os.environ.get("CAMERA_USER")
    if os.environ.get("CAMERA_PASS"):
        config["CAMERA_PASS"] = os.environ.get("CAMERA_PASS")
    if os.environ.get("CAMERA_CPASS"):
        config["CAMERA_CPASS"] = os.environ.get("CAMERA_CPASS")

    return config