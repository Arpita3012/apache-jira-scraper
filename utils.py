import json
import datetime

def save_checkpoint(project, value, filename="checkpoint.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[project] = value
    with open(filename, "w") as f:
        json.dump(data, f)

def load_checkpoint(filename="checkpoint.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def log_message(msg, logfile="logs/scraper.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)
