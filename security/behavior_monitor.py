import psutil
import time
import os

from security.event_logger import log_event

# thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 500 * 1024 * 1024  # 500 MB

# Safe executable paths
SAFE_PATHS = (
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users"
)

# Whitelisted processes
SAFE_PROCESSES = [
    "Code.exe",
    "ollama app.exe",
    "python.exe",
    "MsMpEng.exe",
    "explorer.exe"
]


def monitor_process_behavior():

    behavior_alerts = []

    for proc in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_info", "exe"]
    ):

        try:

            pid = proc.info["pid"]
            name = proc.info["name"]
            exe = proc.info["exe"]

            if name in SAFE_PROCESSES:
                continue

            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.info["memory_info"].rss

            # ---------- HIGH CPU ----------
            if cpu > CPU_THRESHOLD:

                message = f"High CPU usage: {name} (PID {pid}) {cpu}%"

                behavior_alerts.append(message)
                log_event("BEHAVIOR", message)

            # ---------- HIGH MEMORY ----------
            if mem > MEMORY_THRESHOLD:

                mb = mem // (1024 * 1024)

                message = f"High memory usage: {name} (PID {pid}) {mb}MB"

                behavior_alerts.append(message)
                log_event("BEHAVIOR", message)

            # ---------- UNKNOWN EXECUTABLE ----------
            if exe and not exe.startswith(SAFE_PATHS):

                filename = os.path.basename(exe)

                if filename.endswith((".exe", ".bat", ".ps1")):

                    message = f"Suspicious executable location: {exe}"

                    behavior_alerts.append(message)
                    log_event("BEHAVIOR", message)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return behavior_alerts


def continuous_monitor():

    print("🛡 Luna Behavior Monitor Started")

    while True:

        alerts = monitor_process_behavior()

        for alert in alerts:
            print("[BEHAVIOR ALERT]", alert)

        time.sleep(10)