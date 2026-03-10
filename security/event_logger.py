import os
from datetime import datetime

LOG_FILE = "logs/security_log.txt"

def clear_logs():
    try:
        with open(LOG_FILE, "w") as f:
            f.write("")  # erase contents
        return True
    except Exception as e:
        return str(e)

def log_event(event_type, message):

    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{timestamp}] [{event_type}] {message}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)


def read_logs(limit=50):

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return lines[-limit:]