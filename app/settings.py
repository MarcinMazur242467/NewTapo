import json
import os

def load_config():
    """Loads config from config.json in the root directory."""
    # Get the path to the root folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, '..', 'config.json')

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        return {}