import json

CONFIG_FILE = "config/config.json"
DEFAULT_SPREAD_THRESHOLD = 0.005

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return float(config.get("spread_threshold", DEFAULT_SPREAD_THRESHOLD))
    except:
        return DEFAULT_SPREAD_THRESHOLD

def save_config(value):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"spread_threshold": value}, f)
