
import psutil

# -------- TRUSTED PROGRAMS --------

TRUSTED_PROGRAMS = {
    "python.exe",
    "streamlit.exe",
    "code.exe",
    "ollama.exe",
    "ollama app.exe",
    "explorer.exe",
    "svchost.exe",
    "winlogon.exe",
    "lsass.exe",
    "services.exe",
    "dwm.exe",
    "taskhostw.exe"
}

# -------- TRUSTED INSTALL PATHS --------

TRUSTED_PATHS = [
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "AppData\\Local\\Programs"
]

# -------- SUSPICIOUS LOCATIONS --------

SUSPICIOUS_PATHS = [
    "\\Temp\\",
    "\\Downloads\\",
    "\\AppData\\Roaming\\"
]


def is_trusted_path(path):

    for trusted in TRUSTED_PATHS:
        if trusted.lower() in path.lower():
            return True

    return False


def is_suspicious_path(path):

    for folder in SUSPICIOUS_PATHS:
        if folder.lower() in path.lower():
            return True

    return False


def check_running_processes():

    alerts = []
    seen = set()  # prevents duplicate alerts

    for process in psutil.process_iter(["name", "exe"]):

        try:

            name = process.info["name"]
            path = process.info["exe"]

            if not name or not path:
                continue

            name = name.lower()

            # ignore trusted software
            if name in TRUSTED_PROGRAMS:
                continue

            # ignore trusted install locations
            if is_trusted_path(path):
                continue

            # detect suspicious locations
            if is_suspicious_path(path):

                alert = f"Suspicious process location: {name} running from {path}"

                if alert not in seen:
                    alerts.append(alert)
                    seen.add(alert)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return alerts

